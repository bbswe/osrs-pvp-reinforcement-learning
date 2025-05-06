#!/bin/bash
# Script for connecting Dell PowerEdge R620 server to a Ray cluster as a worker node
# This script optimizes for server hardware with many cores but no GPU

# Get timestamp for changelog
TIMESTAMP=$(date "+%Y-%b-%d %H:%M:%S")
echo "Connecting Dell PowerEdge R620 to Ray cluster at $TIMESTAMP"

# Parse command line options
DEBUG_MODE=false
GAMING_PC_IP="192.168.1.100"  # REPLACE WITH YOUR ACTUAL GAMING PC IP ADDRESS
RAY_PORT=6379
SERVER_CPUS=24  # Adjust based on your R620 configuration (typically 16-24 cores)

while getopts "di:p:c:" opt; do
  case $opt in
    d) DEBUG_MODE=true ;;
    i) GAMING_PC_IP=$OPTARG ;;
    p) RAY_PORT=$OPTARG ;;
    c) SERVER_CPUS=$OPTARG ;;
    *) echo "Unknown option: -$OPTARG" >&2; exit 1 ;;
  esac
done
shift $((OPTIND - 1))

# Training configuration for server (these are only used if we decide to also run training here)
EXPERIMENT_NAME="RayDistributed"
NUM_ENVS=120  # High environment count for server with many cores
POOL_SIZE=8   # Worker pool size appropriate for server
PRESET=PastSelfPlay

# Ray-specific configuration optimized for server hardware
# - Uses 2.0 CPU per actor (server-grade CPU can handle more work per actor)
# - Configures appropriate concurrency for server workloads
# - Extended model caching to match gaming PC
RAY_CONFIG='{
  "cpus_per_actor": 2.0, 
  "max_concurrency": 3,
  "shared": true,
  "expiration_check_interval_seconds": 300,
  "expiry_time_seconds": 14400
}'

# Resolve escaped quotes issue with different shells
RAY_CONFIG_ESCAPED=$(echo $RAY_CONFIG | sed 's/"/\\"/g')

# Debug mode configuration
if [ "$DEBUG_MODE" = true ]; then
    echo "Running in DEBUG mode"
    # Use fewer environments and workers in debug mode
    NUM_ENVS=40
    POOL_SIZE=4
    
    # Add debugging parameters to config
    RAY_CONFIG='{
      "cpus_per_actor": 1.0,
      "max_concurrency": 2,
      "shared": true,
      "expiration_check_interval_seconds": 300,
      "expiry_time_seconds": 14400
    }'
    RAY_CONFIG_ESCAPED=$(echo $RAY_CONFIG | sed 's/"/\\"/g')
    
    # Verify Ray installation
    echo "Checking Ray installation..."
    python3 -c "import ray; print(f'Ray version: {ray.__version__}')"
fi

# Stop any existing Ray processes
ray stop

# Connect to the Ray head node on the gaming PC
echo "Connecting to Ray head node at $GAMING_PC_IP:$RAY_PORT with $SERVER_CPUS CPUs"
ray start --address=$GAMING_PC_IP:$RAY_PORT --num-cpus=$SERVER_CPUS

# Set RAY_ADDRESS environment variable
export RAY_ADDRESS=$GAMING_PC_IP:$RAY_PORT

echo "Successfully connected to Ray cluster at $RAY_ADDRESS"
echo "This server is now contributing $SERVER_CPUS CPUs to the distributed training"
echo
echo "To run training from this server (optional), use:"
echo "train --preset $PRESET --name $EXPERIMENT_NAME --override \"--num-envs\" \"$NUM_ENVS\" \"--remote-processor-type\" \"ray\" \"--remote-processor-pool-size\" \"$POOL_SIZE\" \"--remote-processor-kwargs\" \"$RAY_CONFIG_ESCAPED\" \"--continue-training\" \"true\" \"--allow-cleanup\" \"true\""
echo
echo "For optimal results, run the training on the gaming PC with GPU support"
echo "The server is now available as a compute resource for the Ray cluster" 