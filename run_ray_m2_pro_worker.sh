#!/bin/bash
# Script for connecting MacBook M2 Pro to a Ray cluster as a worker node
# This script optimizes for M2 Pro hardware with 10 cores

# Get timestamp for logging
TIMESTAMP=$(date "+%Y-%b-%d %H:%M:%S")
echo "Connecting MacBook M2 Pro to Ray cluster at $TIMESTAMP"

# Parse command line options
GAMING_PC_IP="192.168.1.100"  # REPLACE WITH YOUR ACTUAL GAMING PC IP ADDRESS
RAY_PORT=6379
M2_PRO_CPUS=8  # Reserve 8 of 10 cores for Ray work

while getopts "i:p:c:" opt; do
  case $opt in
    i) GAMING_PC_IP=$OPTARG ;;
    p) RAY_PORT=$OPTARG ;;
    c) M2_PRO_CPUS=$OPTARG ;;
    *) echo "Unknown option: -$OPTARG" >&2; exit 1 ;;
  esac
done
shift $((OPTIND - 1))

# Display configuration
echo "Connecting to Ray head node at $GAMING_PC_IP:$RAY_PORT with $M2_PRO_CPUS CPUs"

# Stop any existing Ray processes
echo "Stopping any existing Ray processes..."
ray stop

# Connect to the Ray head node on the gaming PC
echo "Connecting to Ray head node at $GAMING_PC_IP:$RAY_PORT"
ray start --address=$GAMING_PC_IP:$RAY_PORT --num-cpus=$M2_PRO_CPUS

# Set RAY_ADDRESS environment variable
export RAY_ADDRESS=$GAMING_PC_IP:$RAY_PORT

# Display success message
echo "Successfully connected to Ray cluster at $RAY_ADDRESS"
echo "This MacBook M2 Pro is now contributing $M2_PRO_CPUS CPUs to the distributed training"
echo
echo "The M2 Pro is now available as a compute resource for the Ray cluster"
echo "Training will continue on the gaming PC with GPU support" 