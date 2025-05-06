import asyncio
import argparse
import logging
import os
import sys
import random
from functools import partial
from typing import Any, Callable

from pvp_ml.env.pvp_env import PvpEnv
from pvp_ml.env.simulation import Simulation
from pvp_ml.util.async_evaluator import AsyncEvaluator
from pvp_ml.ppo.ppo import PPO
from pvp_ml.util.elo_tracker import EloTracker, Outcome
from pvp_ml.util.match_outcome_tracker import MatchOutcomeTracker
from pvp_ml.util.remote_processor.remote_processor import create_remote_processor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)-8s] [%(name)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class ModelComparer:
    def __init__(self, model1_path: str, model2_path: str):
        self.model1_path = model1_path
        self.model2_path = model2_path
        self.model1_name = os.path.basename(model1_path).replace('.zip', '')
        self.model2_name = os.path.basename(model2_path).replace('.zip', '')
        self.elo_tracker = EloTracker()
        self.match_outcome_tracker = MatchOutcomeTracker()
        
    async def run_battles(self, num_fights: int, concurrent_fights: int, processor_pool_size: int):
        logger.info(f"Setting up battles: {self.model1_name} vs {self.model2_name} - {num_fights} fights")
        
        # Start the simulation
        with Simulation() as simulation:
            simulation.wait_until_loaded()
            
            # Create remote processor
            async with await create_remote_processor(
                pool_size=processor_pool_size, 
                processor_type="thread", 
                device="cpu"
            ) as remote_processor:
                # Run concurrent fights
                await asyncio.gather(
                    *[
                        self.run_single_battle(
                            fight_index=i,
                            simulation=simulation,
                            remote_processor=remote_processor
                        )
                        for i in range(num_fights)
                    ]
                )
                
        # Print results
        self.print_results()
                
    async def run_single_battle(self, fight_index: int, simulation: Simulation, remote_processor: Any):
        # Load models and their metadata
        model1_meta = PPO.load_meta(self.model1_path)
        model2_meta = PPO.load_meta(self.model2_path)
        
        # Set up environment kwargs
        env1_kwargs = model1_meta.custom_data["env_kwargs"].copy()
        env2_kwargs = model2_meta.custom_data["env_kwargs"].copy()
        
        # Update with simulation info
        env1_kwargs[PvpEnv.REMOTE_ENV_PORT_KEY] = simulation.remote_env_port
        env1_kwargs[PvpEnv.REMOTE_ENV_HOST_KEY] = "localhost"
        env2_kwargs[PvpEnv.REMOTE_ENV_PORT_KEY] = simulation.remote_env_port
        env2_kwargs[PvpEnv.REMOTE_ENV_HOST_KEY] = "localhost"
        
        # Random placement value to make each fight unique
        placement_value = random.randint(0, 1000)
        
        # Set up environment IDs
        player1_id = f"{fight_index}-1-{placement_value}"
        player2_id = f"{fight_index}-2-{placement_value}"
        
        # Create environments
        env1 = PvpEnv(**env1_kwargs, env_id=player1_id, target=player2_id)
        env2 = PvpEnv(**env2_kwargs, env_id=player2_id, target=player1_id)
        
        logger.info(f"Starting battle #{fight_index}: {player1_id} vs {player2_id}")
        
        # Track match completion
        match_done = False
        
        def _handle_done(
            model: str,
            reward: float,
            info: dict[str, Any],
            player_a: str,
            player_b: str,
        ) -> bool:
            nonlocal match_done
            if not match_done:
                match_done = True
                # Get outcome from terminal state
                outcome = Outcome[info.get("terminal_state", "TIED")]
                player_a_name = os.path.basename(player_a).replace('.zip', '')
                player_b_name = os.path.basename(player_b).replace('.zip', '')
                
                # Update ELO tracker
                self.elo_tracker.add_outcome(
                    player_a_name,
                    player_b_name,
                    outcome,
                )
                
                # Update match outcome tracker
                if outcome == Outcome.WON:
                    self.match_outcome_tracker.add_win(player_a_name)
                    self.match_outcome_tracker.add_loss(player_b_name)
                elif outcome == Outcome.LOST:
                    self.match_outcome_tracker.add_loss(player_a_name)
                    self.match_outcome_tracker.add_win(player_b_name)
                elif outcome == Outcome.TIED:
                    self.match_outcome_tracker.add_tie(player_a_name)
                    self.match_outcome_tracker.add_tie(player_b_name)
                
                logger.info(
                    f"Match finished - {info['id']} ({player_a_name}) {reward:.1f} vs. {info['target']} ({player_b_name}) - Outcome: {outcome.name}"
                )
            return True
        
        # Run the agents
        await asyncio.gather(
            AsyncEvaluator.evaluate(
                env1,
                lambda: self.model1_path,
                fight_index % remote_processor.get_pool_size(),
                remote_processor,
                deterministic=False,
                on_episode_complete=partial(
                    _handle_done, player_a=self.model1_path, player_b=self.model2_path
                ),
            ),
            AsyncEvaluator.evaluate(
                env2,
                lambda: self.model2_path,
                fight_index % remote_processor.get_pool_size(),
                remote_processor,
                deterministic=False,
                on_episode_complete=partial(
                    _handle_done, player_a=self.model2_path, player_b=self.model1_path
                ),
            )
        )
    
    def print_results(self):
        # Print ELO ratings
        ratings = [
            f"{player} \t- {rating}" for player, rating in self.elo_tracker.list_ratings()
        ]
        rating_lines = "\n".join(ratings)
        logger.info(f"\n---- ELO Ratings ----\n{rating_lines}")
        
        # Print match outcomes
        outcomes = [
            f"{player} \t- {outcomes.wins} wins\t {outcomes.losses} losses\t {outcomes.ties} ties\t {outcomes.total_matches()} total"
            for player, outcomes in self.match_outcome_tracker.list_outcomes()
        ]
        outcome_lines = "\n".join(outcomes)
        logger.info(f"\n---- Match Outcomes ----\n{outcome_lines}")
        
        # Print win rate
        for player, outcome in self.match_outcome_tracker.list_outcomes():
            total = outcome.total_matches()
            if total > 0:
                win_rate = outcome.wins / total * 100
                logger.info(f"{player} win rate: {win_rate:.1f}%")

def parse_args():
    parser = argparse.ArgumentParser(description="Compare two models in a series of battles")
    parser.add_argument(
        "--model1",
        type=str,
        default="experiments/ThreadParallel/models/main-15667200-steps.zip",
        help="Path to first model",
    )
    parser.add_argument(
        "--model2",
        type=str,
        default="models/FineTunedNh.zip",
        help="Path to second model",
    )
    parser.add_argument(
        "--num-fights",
        type=int,
        default=5,
        help="Number of fights to run",
    )
    parser.add_argument(
        "--concurrent-fights",
        type=int,
        default=2,
        help="Number of fights to run concurrently",
    )
    parser.add_argument(
        "--processor-pool-size",
        type=int,
        default=4,
        help="Size of the remote processor pool",
    )
    return parser.parse_args()

async def main():
    args = parse_args()
    
    # Initialize model comparer
    comparer = ModelComparer(args.model1, args.model2)
    
    # Run battles
    await comparer.run_battles(
        num_fights=args.num_fights,
        concurrent_fights=args.concurrent_fights,
        processor_pool_size=args.processor_pool_size,
    )

if __name__ == "__main__":
    asyncio.run(main())