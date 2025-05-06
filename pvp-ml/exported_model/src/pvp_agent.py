import os
import json
import torch
import numpy as np
import time
from microbot.api.plugin import Plugin
from microbot.api.definitions import Coordinate, Equipment, Prayer, Magic, Item, Spellbook, Style
from microbot.api.script import Script
from microbot.api.plugin.framework import LoopState
from microbot.api.plugin.observer import Observer, ObserverState
from microbot.api.handlers import Handlers
from microbot.api.common import Rect
from typing import List, Dict, Optional, Tuple

class PvpAgent(Plugin):
    def __init__(self, script: Script):
        super().__init__(script)
        self.script = script
        self.model = None
        self.meta = None
        self.is_initialized = False
        self.observation_mean = None
        self.observation_var = None
        
        # Combat state tracking
        self.last_action_time = 0
        self.action_cooldown = 0.6  # seconds
        self.target_entity = None
        self.current_style = None
        self.last_style_switch_time = 0
        self.style_switch_cooldown = 1.2  # seconds
        self.last_food_time = 0
        self.food_cooldown = 1.8  # seconds
        self.last_prayer_change_time = 0
        self.prayer_cooldown = 0.3  # seconds
        
        # Track when we last executed specific action types
        self.last_action_times = {
            "attack": 0,
            "food": 0,
            "potion": 0,
            "prayer": 0,
            "movement": 0,
            "special": 0,
            "gear": 0
        }
        
        # Combat tracking
        self.player_health = 100
        self.player_prayer = 100
        self.target_health = 100
        self.target_prayer = 100
        self.player_frozen = False
        self.target_frozen = False
        self.player_moving = False
        self.target_moving = False
        self.player_distance = 1
        
        # Weapon/gear tracking
        self.using_melee = False
        self.using_ranged = False
        self.using_mage = False
        self.spec_enabled = False
        self.spec_energy = 100
        
        # Prayer tracking
        self.melee_prayer = False
        self.ranged_prayer = False
        self.magic_prayer = False
        self.smite_prayer = False
        self.redemption_prayer = False
        
        # Inventory tracking
        self.food_count = 0
        self.karambwan_count = 0
        self.brew_count = 0
        self.restore_count = 0
        self.range_pot_count = 0
        self.combat_pot_count = 0
        
    def initialize(self):
        """Initialize the PVP agent with the trained model."""
        self.script.log_msg("Initializing PVP Agent...")
        
        # Load model info
        model_dir = os.path.dirname(os.path.realpath(__file__))
        model_dir = os.path.join(os.path.dirname(model_dir), "resources")
        
        # Load metadata
        meta_path = os.path.join(model_dir, "model_meta.json")
        with open(meta_path, 'r') as f:
            self.meta = json.load(f)
        
        # Set normalization parameters
        if self.meta.get("normalized_observations", False):
            self.observation_mean = torch.tensor(self.meta["observation_mean"], dtype=torch.float32)
            self.observation_var = torch.tensor(self.meta["observation_var"], dtype=torch.float32)
        
        # Load the model
        model_path = os.path.join(model_dir, "policy.pt")
        try:
            self.model = torch.jit.load(model_path)
            self.model.eval()  # Set to evaluation mode
            self.script.log_msg("PVP Agent model loaded successfully")
            self.script.log_msg(f"Model trained for {self.meta['trained_steps']} steps")
            self.is_initialized = True
        except Exception as e:
            self.script.log_msg(f"Failed to load model: {str(e)}")
            return LoopState.STOP
        
        return LoopState.CONTINUE
        
    def update_combat_state(self):
        """Update the internal combat state based on game state."""
        # Get player state
        self.player_health = self.script.get_stat_level_percent("hitpoints")
        self.player_prayer = self.script.get_stat_level_percent("prayer")
        
        # Get target state
        self.target_entity = self.script.get_target_entity()
        if self.target_entity:
            self.target_health = self.target_entity.get_health_percent()
            self.player_distance = self.script.get_distance_to(self.target_entity.get_position())
            self.target_moving = self.target_entity.is_moving()
        else:
            # Find a potential target if none is selected
            potential_targets = self.script.get_surrounding_players(max_distance=10)
            if potential_targets:
                self.target_entity = potential_targets[0]
                self.script.select_entity(self.target_entity)
        
        # Get player equipment and style
        equipped_weapon = self.script.get_equipped_item(Equipment.WEAPON)
        
        # Determine combat style based on weapon
        if equipped_weapon:
            weapon_name = equipped_weapon.get_name().lower()
            
            # Check weapon type to determine style
            if any(melee_weapon in weapon_name for melee_weapon in ["whip", "scimitar", "godsword", "claws", "dagger", "maul"]):
                self.using_melee = True
                self.using_ranged = False
                self.using_mage = False
            elif any(ranged_weapon in weapon_name for ranged_weapon in ["bow", "crossbow", "blowpipe", "knife", "javelin", "ballista"]):
                self.using_melee = False
                self.using_ranged = True
                self.using_mage = False
            elif any(mage_weapon in weapon_name for mage_weapon in ["staff", "wand", "trident"]):
                self.using_melee = False
                self.using_ranged = False
                self.using_mage = True
        
        # Get spec weapon energy
        self.spec_energy = self.script.get_special_energy()
        self.spec_enabled = self.script.is_special_enabled()
        
        # Check prayers
        self.melee_prayer = self.script.is_prayer_active(Prayer.PROTECT_FROM_MELEE)
        self.ranged_prayer = self.script.is_prayer_active(Prayer.PROTECT_FROM_MISSILES)
        self.magic_prayer = self.script.is_prayer_active(Prayer.PROTECT_FROM_MAGIC)
        self.smite_prayer = self.script.is_prayer_active(Prayer.SMITE)
        self.redemption_prayer = self.script.is_prayer_active(Prayer.REDEMPTION)
        
        # Count inventory items
        inventory_items = self.script.get_inventory_items()
        self.food_count = sum(1 for item in inventory_items if "shark" in item.get_name().lower() or "tuna" in item.get_name().lower() or "swordfish" in item.get_name().lower() or "anglerfish" in item.get_name().lower())
        self.karambwan_count = sum(1 for item in inventory_items if "karambwan" in item.get_name().lower())
        self.brew_count = sum(1 for item in inventory_items if "saradomin brew" in item.get_name().lower())
        self.restore_count = sum(1 for item in inventory_items if "super restore" in item.get_name().lower())
        self.range_pot_count = sum(1 for item in inventory_items if "ranging" in item.get_name().lower())
        self.combat_pot_count = sum(1 for item in inventory_items if "super combat" in item.get_name().lower() or "super strength" in item.get_name().lower() or "super attack" in item.get_name().lower())
        
        # Movement detection
        self.player_moving = self.script.is_player_moving()
        
    def get_observation(self) -> torch.Tensor:
        """Get the current game state as observations for the model."""
        # Create observation array with the same shape as training data
        observation = np.zeros(len(self.meta["observations"]), dtype=np.float32)
        
        # Basic combat observations
        observation[0] = float(self.using_melee)  # player_using_melee
        observation[1] = float(self.using_ranged)  # player_using_ranged
        observation[2] = float(self.using_mage)  # player_using_mage
        observation[3] = float(self.spec_enabled)  # player_spec_equipped
        observation[4] = self.spec_energy / 100.0  # special_energy_percent
        observation[5] = float(self.melee_prayer)  # player_melee_prayer
        observation[6] = float(self.ranged_prayer)  # player_ranged_prayer
        observation[7] = float(self.magic_prayer)  # player_magic_prayer
        observation[8] = float(self.smite_prayer)  # player_smite_prayer
        observation[9] = float(self.redemption_prayer)  # player_redemption_prayer
        observation[10] = self.player_health / 100.0  # player_health_percent
        observation[11] = self.target_health / 100.0 if self.target_entity else 1.0  # target_health_percent
        
        # Target combat style observations (using defaults because we can't directly observe this in game)
        observation[12] = 0.33  # target_using_melee (default assumption)
        observation[13] = 0.33  # target_using_ranged (default assumption)
        observation[14] = 0.33  # target_using_mage (default assumption)
        observation[15] = 0.0   # target_spec_equipped (default assumption)
        observation[16] = 0.0  # target_melee_prayer (default assumption) 
        observation[17] = 0.0  # target_ranged_prayer (default assumption)
        observation[18] = 0.0  # target_magic_prayer (default assumption)
        observation[19] = 0.0  # target_smite_prayer (default assumption)
        observation[20] = 0.0  # target_redemption_prayer (default assumption)
        observation[21] = self.spec_energy / 100.0  # target_special_percent (default assumption)
        
        # Inventory observations
        observation[22] = self.range_pot_count  # range_potion_doses
        observation[23] = self.combat_pot_count  # combat_potion_doses
        observation[24] = self.restore_count  # super_restore_doses
        observation[25] = self.brew_count  # brew_doses
        observation[26] = self.food_count  # food_count
        observation[27] = self.karambwan_count  # karambwan_count
        observation[28] = self.player_prayer / 100.0  # prayer_points
        
        # Fill remaining observations with default values
        # We can't observe everything the model was trained on, 
        # so we provide sensible defaults and track what we can
        for i in range(29, len(observation)):
            observation[i] = 0.0  # Default value
        
        # Distance-based observations
        if self.target_entity:
            observation[62] = min(self.player_distance / 10.0, 1.0)  # player_to_target_distance scaled
        
        # Action cooldown observations
        current_time = time.time()
        observation[39] = min((current_time - self.last_action_times.get("attack", 0)) / 3.0, 1.0)  # attack_cycle_ticks approximation
        observation[40] = min((current_time - self.last_action_times.get("food", 0)) / 3.0, 1.0)  # food_cycle_ticks approximation
        observation[41] = min((current_time - self.last_action_times.get("potion", 0)) / 3.0, 1.0)  # potion_cycle_ticks approximation
        observation[42] = min((current_time - self.last_action_times.get("food", 0)) / 3.0, 1.0)  # karambwan_cycle_ticks approximation (same as food)
        
        # Fill in some player stats
        observation[96] = self.script.get_stat_level("attack") / 99.0  # absolute_attack_level
        observation[97] = self.script.get_stat_level("strength") / 99.0  # absolute_strength_level
        observation[98] = self.script.get_stat_level("defence") / 99.0  # absolute_defense_level
        observation[99] = self.script.get_stat_level("ranged") / 99.0  # absolute_ranged_level
        observation[100] = self.script.get_stat_level("magic") / 99.0  # absolute_magic_level
        observation[101] = self.script.get_stat_level("prayer") / 99.0  # absolute_prayer_level
        observation[102] = self.script.get_stat_level("hitpoints") / 99.0  # absolute_hitpoints_level
        
        # Movement observations
        observation[55] = float(self.player_moving)  # player_is_moving
        observation[56] = float(self.target_moving) if self.target_entity else 0.0  # target_is_moving
        
        # Convert to PyTorch tensor and add batch dimension
        return torch.tensor(observation, dtype=torch.float32).unsqueeze(0)
    
    def normalize_observation(self, observation: torch.Tensor) -> torch.Tensor:
        """Normalize the observation according to training statistics."""
        if self.meta.get("normalized_observations", False):
            epsilon = 1e-8
            return (observation - self.observation_mean) / torch.sqrt(self.observation_var + epsilon)
        return observation
    
    def predict_action(self, observation: torch.Tensor) -> int:
        """Get the next action from the model based on current observation."""
        # Normalize observation if needed
        normalized_obs = self.normalize_observation(observation)
        
        # Stack observation for the model (model expects a sequence)
        stacked_obs = normalized_obs.unsqueeze(1)  # Add sequence dimension
        
        # Get action masks (all actions available in this case)
        action_mask = torch.ones((1, len(self.meta["actions"])), dtype=torch.bool)
        
        # Apply basic restrictions based on cooldowns
        current_time = time.time()
        if current_time - self.last_action_times.get("attack", 0) < 1.2:
            # Block attack actions when on cooldown
            for action_idx in [1, 2, 3, 5, 6, 8, 9, 11, 12, 13]:
                action_mask[0, action_idx] = False
        
        if current_time - self.last_action_times.get("food", 0) < 1.8:
            # Block food actions when on cooldown
            action_mask[0, 20] = False
            action_mask[0, 22] = False
            
        if current_time - self.last_action_times.get("potion", 0) < 1.8:
            # Block potion actions when on cooldown
            for action_idx in [15, 16, 17, 18]:
                action_mask[0, action_idx] = False
        
        # Run inference
        try:
            with torch.no_grad():
                action_logits = self.model(stacked_obs, action_mask)
                action_probs = torch.softmax(action_logits, dim=-1)
                
                # Get action with highest probability that's valid
                valid_probs = action_probs * action_mask.float()
                action = torch.argmax(valid_probs, dim=1).item()
                
                return action
        except Exception as e:
            self.script.log_msg(f"Error predicting action: {str(e)}")
            return 0  # No-op action
        
    def execute_action(self, action_idx: int):
        """Execute the chosen action in the game."""
        current_time = time.time()
        action_name = self.meta["actions"][action_idx]["id"]
        action_desc = self.meta["actions"][action_idx]["description"]
        
        self.script.log_msg(f"Action: {action_desc}")
        
        # Handle the action based on its type
        if action_idx == 0:  # no_op_attack
            pass  # Do nothing for no-op
            
        elif action_idx == 1:  # mage_attack
            if self.target_entity and current_time - self.last_action_times.get("attack", 0) > 1.2:
                self.script.cast_spell_on(Magic.FIRE_SURGE, self.target_entity)
                self.last_action_times["attack"] = current_time
                
        elif action_idx == 2:  # ranged_attack
            if self.target_entity and current_time - self.last_action_times.get("attack", 0) > 1.2:
                self.script.attack_entity(self.target_entity)
                self.last_action_times["attack"] = current_time
                
        elif action_idx == 3:  # melee_attack
            if self.target_entity and current_time - self.last_action_times.get("attack", 0) > 1.2:
                self.script.attack_entity(self.target_entity)
                self.last_action_times["attack"] = current_time
                
        elif action_idx in [11, 12]:  # use_ice_spell or use_blood_spell
            if self.target_entity and current_time - self.last_action_times.get("attack", 0) > 1.2:
                spell = Magic.ICE_BARRAGE if action_idx == 11 else Magic.BLOOD_BARRAGE
                self.script.cast_spell_on(spell, self.target_entity)
                self.last_action_times["attack"] = current_time
                
        elif action_idx == 15:  # use_brew
            if current_time - self.last_action_times.get("potion", 0) > 1.8:
                if self.script.click_inventory_item_by_name("Saradomin brew"):
                    self.last_action_times["potion"] = current_time
                    
        elif action_idx == 16:  # use_restore_potion
            if current_time - self.last_action_times.get("potion", 0) > 1.8:
                if self.script.click_inventory_item_by_name("Super restore"):
                    self.last_action_times["potion"] = current_time
                    
        elif action_idx == 17:  # use_combat_potion
            if current_time - self.last_action_times.get("potion", 0) > 1.8:
                if self.script.click_inventory_item_by_name("Super combat"):
                    self.last_action_times["potion"] = current_time
                    
        elif action_idx == 18:  # use_ranged_potion
            if current_time - self.last_action_times.get("potion", 0) > 1.8:
                if self.script.click_inventory_item_by_name("Ranging potion"):
                    self.last_action_times["potion"] = current_time
                    
        elif action_idx == 20:  # eat_primary_food
            if current_time - self.last_action_times.get("food", 0) > 1.8:
                # Try various food types
                if (self.script.click_inventory_item_by_name("Shark") or 
                    self.script.click_inventory_item_by_name("Anglerfish") or
                    self.script.click_inventory_item_by_name("Manta ray")):
                    self.last_action_times["food"] = current_time
                    
        elif action_idx == 22:  # eat_karambwan
            if current_time - self.last_action_times.get("food", 0) > 1.8:
                if self.script.click_inventory_item_by_name("Karambwan"):
                    self.last_action_times["food"] = current_time
                    
        elif action_idx in [40, 41, 42]:  # prayer actions
            if current_time - self.last_action_times.get("prayer", 0) > 0.3:
                if action_idx == 40:  # mage_prayer
                    self.script.toggle_prayer(Prayer.PROTECT_FROM_MAGIC)
                elif action_idx == 41:  # ranged_prayer
                    self.script.toggle_prayer(Prayer.PROTECT_FROM_MISSILES)
                elif action_idx == 42:  # melee_prayer
                    self.script.toggle_prayer(Prayer.PROTECT_FROM_MELEE)
                self.last_action_times["prayer"] = current_time
                
        elif action_idx == 43:  # smite_prayer
            if current_time - self.last_action_times.get("prayer", 0) > 0.3:
                self.script.toggle_prayer(Prayer.SMITE)
                self.last_action_times["prayer"] = current_time
                
        elif action_idx in [28, 29, 30, 31]:  # movement actions
            if self.target_entity and current_time - self.last_action_times.get("movement", 0) > 0.6:
                if action_idx == 28:  # move_next_to_target
                    target_pos = self.target_entity.get_position()
                    self.script.click_on_world_map(target_pos.x, target_pos.y)
                elif action_idx == 29:  # move_under_target
                    target_pos = self.target_entity.get_position()
                    self.script.click_on_world_map(target_pos.x, target_pos.y)
                elif action_idx == 30:  # move_to_farcast_tile
                    # Move 7 tiles away in a random direction
                    if self.target_entity:
                        target_pos = self.target_entity.get_position()
                        angle = np.random.random() * 2 * np.pi
                        distance = 7
                        new_x = target_pos.x + int(np.cos(angle) * distance)
                        new_y = target_pos.y + int(np.sin(angle) * distance)
                        self.script.click_on_world_map(new_x, new_y)
                self.last_action_times["movement"] = current_time
        
    def loop(self):
        """Main loop for the PVP agent."""
        if not self.is_initialized:
            return self.initialize()
        
        # Update our knowledge of the game state
        self.update_combat_state()
        
        # Find a target if we don't have one
        if not self.target_entity:
            nearby_players = self.script.get_surrounding_players(max_distance=15)
            if nearby_players:
                self.target_entity = nearby_players[0]
                self.script.log_msg(f"Found target: {self.target_entity.get_name()}")
                self.script.select_entity(self.target_entity)
            else:
                self.script.log_msg("No targets found nearby.")
                return LoopState.CONTINUE
        
        # Get current game state observation
        observation = self.get_observation()
        
        # Get action from model
        action_idx = self.predict_action(observation)
        
        # Execute the action in game
        self.execute_action(action_idx)
        
        # Sleep to prevent too rapid execution
        time.sleep(0.1)
        
        return LoopState.CONTINUE
