#!/usr/bin/env python3
"""
Convert a non-trainable model to a trainable one.
This script loads a model in non-trainable mode and saves it again with the trainable flag.
"""

import argparse
import os
import sys
import torch as th
import torch.optim as optim

sys.path.append(os.path.join(os.path.dirname(__file__), 'pvp-ml'))
from pvp_ml.ppo.ppo import PPO
from pvp_ml.util.files import get_experiment_dir

def parse_args():
    parser = argparse.ArgumentParser(description="Convert a non-trainable model to a trainable one")
    parser.add_argument("--input-model", type=str, required=True, help="Path to input model file")
    parser.add_argument("--output-model", type=str, help="Path to output model file (default: same as input with _trainable suffix)")
    parser.add_argument("--device", type=str, default="cpu", help="Device to use for model loading")
    return parser.parse_args()

def main():
    args = parse_args()
    
    input_path = args.input_model
    if not os.path.exists(input_path):
        print(f"Error: Input model '{input_path}' does not exist.")
        return 1
    
    # Default output path adds _trainable suffix before the extension
    if args.output_model:
        output_path = args.output_model
    else:
        name, ext = os.path.splitext(input_path)
        output_path = f"{name}_trainable{ext}"
    
    # Make sure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    print(f"Loading model from {input_path}...")
    # First load the checkpoint directly to extract all data
    checkpoint = th.load(input_path, map_location=args.device)
    
    # Load in non-trainable mode to avoid the error
    model = PPO.load(input_path, device=args.device, trainable=False)
    
    print("Creating policy for trainable model...")
    # Create a new trainable model with the same parameters
    trainable_model = PPO(
        policy_params=checkpoint["policy_params"],
        meta=checkpoint["meta"],
        device=args.device,
        trainable=True,
        policy_state=checkpoint["policy"],
        extensions={
            saved_extension["name"]: saved_extension["type"](
                **saved_extension["params"]
            )
            for saved_extension in checkpoint.get(
                "extensions", []
            )
        },
    )
    
    print(f"Saving trainable model to {output_path}...")
    trainable_model.save(output_path)
    print("Conversion complete!")
    
    # Verify the model is now trainable
    verify = PPO.load(output_path, device=args.device, trainable=True)
    print(f"Verification successful: Model is now trainable")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 