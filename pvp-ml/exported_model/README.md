# Exported PVP Agent Model

Model exported from: main-13312000-steps.zip
Training steps: 13312000
Training rollouts: 130

## Overview

This Microbot plugin implements an AI PVP agent for Last Man Standing (LMS) in Old School RuneScape. The agent uses a deep reinforcement learning model trained with Proximal Policy Optimization (PPO) through self-play and environment simulation.

## Files

- `policy.pt`: TorchScript model containing the policy network
- `model_meta.json`: Model metadata including observation normalization stats
- `src/pvp_agent.py`: Main plugin implementation file
- `plugin.properties`: Plugin configuration

## Installation

1. Copy the entire `exported_model` directory to your Microbot plugins folder
2. Rename the directory to `pvp_ai_agent`
3. Ensure the model files are in the `resources` directory
4. Restart Microbot if it's already running

## Usage

1. Start Microbot
2. Select the PVP-AI-Agent-LMS plugin
3. Start the plugin within Last Man Standing
4. The AI will automatically:
   - Find and select targets
   - Switch prayers based on opponent's style
   - Perform proper weapon and gear switches
   - Eat food when health is low
   - Use potions when beneficial
   - Perform special attacks when appropriate
   - Move strategically around the arena

## Limitations

- The agent works best in Last Man Standing where equipment is standardized
- Performance may vary depending on lag and ping
- The agent needs to observe the opponent's actions to respond effectively

## Customization

You can modify `src/pvp_agent.py` to customize the agent's behavior. The main components you might want to tweak are:

- Combat style preferences in the `execute_action` method
- Food eating thresholds
- Prayer switching behavior
- Movement patterns
