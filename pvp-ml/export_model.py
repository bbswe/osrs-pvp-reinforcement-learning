#!/usr/bin/env python
"""
Export a trained PPO model to a format that can be loaded by Microbot.
This script converts the PyTorch model to TorchScript and saves policy weights.

Usage:
    ./env/bin/python export_model.py [input_model_path] [output_directory]

Example:
    ./env/bin/python export_model.py experiments/ThreadParallel/models/main-8192000-steps.zip ~/Project/Client/Microbot/plugins/pvp_agent/
"""
import os
import sys
import json
import torch
import logging
import numpy as np
import shutil
from typing import Dict, Any, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-8s | %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("model_exporter")

def load_model(model_path: str) -> Tuple[Any, Dict[str, Any]]:
    """Load a model from the given path."""
    from pvp_ml.ppo.ppo import PPO
    
    logger.info(f"Loading model from {model_path}")
    model = PPO.load(model_path, trainable=False)
    
    # Extract metadata
    meta = {
        "trained_steps": model.meta.trained_steps,
        "trained_rollouts": model.meta.trained_rollouts,
        "normalized_observations": model.meta.normalized_observations,
        "observation_mean": model.meta.running_observation_stats.mean.cpu().numpy().tolist() if model.meta.normalized_observations else None,
        "observation_var": model.meta.running_observation_stats.var.cpu().numpy().tolist() if model.meta.normalized_observations else None,
    }
    
    # Add environment metadata
    if "env_meta" in model.meta.custom_data:
        env_meta = model.meta.custom_data["env_meta"]
        meta["observations"] = [
            {"id": obs.id, "description": obs.description} 
            for obs in env_meta.observations
        ]
        
        # Handle actions correctly
        actions_list = []
        for action_head in env_meta.actions:
            # Extract actions from each action head
            for action in action_head.actions:
                actions_list.append({
                    "id": action.id, 
                    "description": action.description,
                    "size": 1  # Default size if not available
                })
        
        meta["actions"] = actions_list
    
    return model, meta

def export_model(model, output_dir: str, meta: Dict[str, Any]) -> None:
    """Export the model to the specified directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save policy as TorchScript
    logger.info("Converting model to TorchScript format")
    
    # Check if policy exists
    if not hasattr(model, '_eval_policy') or model._eval_policy is None:
        logger.error("Model doesn't have a valid eval_policy attribute")
        raise ValueError("Model doesn't have a valid policy")
        
    # Get the policy (already in eval mode from load)
    scripted_model = model._eval_policy
    
    # Save the model
    script_path = os.path.join(output_dir, "policy.pt")
    logger.info(f"Saving TorchScript model to {script_path}")
    scripted_model.save(script_path)
    
    # Save metadata
    meta_path = os.path.join(output_dir, "model_meta.json")
    logger.info(f"Saving metadata to {meta_path}")
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    
    # Create a simple readme
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, 'w') as f:
        f.write(f"# Exported PVP Agent Model\n\n")
        f.write(f"Model exported from: {os.path.basename(model_path)}\n")
        f.write(f"Training steps: {meta['trained_steps']}\n")
        f.write(f"Training rollouts: {meta['trained_rollouts']}\n\n")
        f.write("## Files\n\n")
        f.write("- `policy.pt`: TorchScript model containing the policy network\n")
        f.write("- `model_meta.json`: Model metadata including observation normalization stats\n")
    
    logger.info(f"Model export complete. Files saved to {output_dir}")

def create_microbot_plugin(output_dir: str, meta: Dict[str, Any]) -> None:
    """Create a basic Microbot plugin structure."""
    plugin_dir = output_dir
    src_dir = os.path.join(plugin_dir, "src")
    resources_dir = os.path.join(plugin_dir, "resources")
    
    # Create directories
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(resources_dir, exist_ok=True)
    
    # Create plugin.properties
    with open(os.path.join(plugin_dir, "plugin.properties"), 'w') as f:
        f.write("name=PVP-AI-Agent\n")
        f.write("version=1.0.0\n")
        f.write("description=OSRS PVP Agent using trained RL model\n")
        f.write("entrypoint=src/pvp_agent:PvpAgent\n")
        f.write("type=active\n")
    
    # Create sample implementation file
    with open(os.path.join(src_dir, "pvp_agent.py"), 'w') as f:
        f.write("""import os
import json
import torch
import numpy as np
from microbot.api.plugin import Plugin
from microbot.api.definitions import Coordinate
from microbot.api.script import Script
from microbot.api.plugin.framework import LoopState
from microbot.api.plugin.observer import Observer, ObserverState
from microbot.api.handlers import Handlers
from microbot.api.common import Rect

class PvpAgent(Plugin):
    def __init__(self, script: Script):
        super().__init__(script)
        self.script = script
        self.model = None
        self.meta = None
        self.is_initialized = False
        self.observation_mean = None
        self.observation_var = None
        
    def initialize(self):
        # Load model info
        model_dir = os.path.dirname(os.path.realpath(__file__))
        model_dir = os.path.join(os.path.dirname(model_dir), "resources")
        
        # Load metadata
        meta_path = os.path.join(model_dir, "model_meta.json")
        with open(meta_path, 'r') as f:
            self.meta = json.load(f)
        
        # Set normalization parameters
        if self.meta["normalized_observations"]:
            self.observation_mean = torch.tensor(self.meta["observation_mean"], dtype=torch.float32)
            self.observation_var = torch.tensor(self.meta["observation_var"], dtype=torch.float32)
        
        # Load the model
        model_path = os.path.join(model_dir, "policy.pt")
        self.model = torch.jit.load(model_path)
        self.model.eval()  # Set to evaluation mode
        
        self.script.log_msg("PVP Agent model loaded successfully")
        self.script.log_msg(f"Model trained for {self.meta['trained_steps']} steps")
        self.is_initialized = True
        return LoopState.CONTINUE
        
    def get_observation(self):
        # TO IMPLEMENT: Get the game state information
        # This is just a placeholder - you'll need to implement this based on Microbot's API
        # to gather the same observations your model was trained on
        observation = np.zeros(len(self.meta["observations"]), dtype=np.float32)
        
        # Example observation gathering
        # observation[0] = self.script.get_stat_level("hitpoints") / 99.0  # Health
        # observation[1] = self.script.get_stat_level("prayer") / 99.0  # Prayer
        # ... etc for other observations
        
        return torch.tensor(observation, dtype=torch.float32).unsqueeze(0)
    
    def normalize_observation(self, observation):
        if self.meta["normalized_observations"]:
            epsilon = 1e-8
            return (observation - self.observation_mean) / torch.sqrt(self.observation_var + epsilon)
        return observation
    
    def predict_action(self, observation):
        # Normalize observation if needed
        normalized_obs = self.normalize_observation(observation)
        
        # Get action masks (all actions available in this case)
        action_mask = torch.ones((1, len(self.meta["actions"])), dtype=torch.bool)
        
        # Run inference
        with torch.no_grad():
            action_logits = self.model(normalized_obs, action_mask)
            action_probs = torch.softmax(action_logits, dim=-1)
            action = torch.argmax(action_probs, dim=-1).item()
        
        return action
        
    def execute_action(self, action_idx):
        # TO IMPLEMENT: Convert action index to game action
        # This is a placeholder - you'll need to map the action index to actual game controls
        self.script.log_msg(f"Executing action {action_idx}")
        
        # Example action execution
        # if action_idx == 0:
        #     self.script.click_item("Shark")
        # elif action_idx == 1:
        #     self.script.click_prayer("Protect from Melee")
        # ... etc for other actions
        
        pass
        
    def loop(self):
        if not self.is_initialized:
            return self.initialize()
        
        # Get current game state observation
        observation = self.get_observation()
        
        # Get action from model
        action_idx = self.predict_action(observation)
        
        # Execute the action in game
        self.execute_action(action_idx)
        
        return LoopState.CONTINUE
""")
    
    # Create resources directory and copy model files
    model_resources_dir = os.path.join(resources_dir)
    
    # Create directory structure explanation
    with open(os.path.join(plugin_dir, "SETUP.md"), 'w') as f:
        f.write("# PVP Agent Plugin Setup\n\n")
        f.write("This plugin uses a trained reinforcement learning model to play PVP in Last Man Standing.\n\n")
        f.write("## Integration Steps\n\n")
        f.write("1. The model files (`policy.pt` and `model_meta.json`) should be in the `resources/` directory\n")
        f.write("2. The implementation is in `src/pvp_agent.py`\n\n")
        f.write("## Required Customization\n\n")
        f.write("You will need to customize the following functions in the `pvp_agent.py` file:\n\n")
        f.write("- `get_observation()`: Extract game state from Microbot API to match the observations used in training\n")
        f.write("- `execute_action()`: Convert the model's action decisions to Microbot API calls\n\n")
        f.write("## Observation Mapping\n\n")
        f.write("The model expects these observations:\n\n")
        for i, obs in enumerate(meta.get("observations", [])):
            f.write(f"{i}. {obs['id']}: {obs['description']}\n")
        
        f.write("\n## Action Mapping\n\n")
        f.write("The model can take these actions:\n\n")
        for i, action in enumerate(meta.get("actions", [])):
            f.write(f"{i}. {action['id']}: {action['description']}\n")

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} [input_model_path] [output_directory]")
        sys.exit(1)
    
    model_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.getcwd(), "exported_model")
    
    # Check if model file exists
    if not os.path.exists(model_path):
        logger.error(f"Model file not found: {model_path}")
        sys.exit(1)
    
    try:
        # Load the model
        model, meta = load_model(model_path)
        
        # Export the model
        export_model(model, output_dir, meta)
        
        # Create Microbot plugin structure
        create_microbot_plugin(output_dir, meta)
        
    except Exception as e:
        logger.error(f"Error exporting model: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1) 