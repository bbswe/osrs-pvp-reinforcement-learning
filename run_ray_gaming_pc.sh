#!/bin/bash
# Optimized Ray training script for Gaming PC with Ryzen 9 7950X3D CPU (32 threads) and RTX 4090 GPU
# This script configures Ray as a head node and optimizes for high core count CPU and powerful GPU

# Get timestamp for changelog
TIMESTAMP=$(date "+%Y-%b-%d %H:%M:%S")
echo "Running Ray-optimized training on Gaming PC (Ryzen 9 7950X3D + RTX 4090) at $TIMESTAMP"

# Parse command line options
DEBUG_MODE=false
HEAD_ONLY=false
GAMING_PC_IP="192.168.1.100"  # REPLACE WITH YOUR ACTUAL GAMING PC IP ADDRESS
RAY_PORT=6379

while getopts "dhip:" opt; do
  case $opt in
    d) DEBUG_MODE=true ;;
    h) HEAD_ONLY=true ;;
    i) GAMING_PC_IP=$OPTARG ;;
    p) RAY_PORT=$OPTARG ;;
    *) echo "Unknown option: -$OPTARG" >&2; exit 1 ;;
  esac
done
shift $((OPTIND - 1))

# Training configuration optimized for high-end gaming PC
EXPERIMENT_NAME="RayDistributed"
NUM_ENVS=160  # Increased environment count for powerful CPU
POOL_SIZE=16  # Increased worker pool size for 32-thread CPU
PRESET=PastSelfPlay

# Ray-specific configuration parameters
# - Uses 1.5 CPU per actor (appropriate for 32-thread CPU)
# - Configures concurrency to maximize CPU utilization
# - Extended model caching to reduce overhead (4 hours)
# - Uses GPU for model inference
RAY_CONFIG='{
  "cpus_per_actor": 1.5, 
  "max_concurrency": 4,
  "shared": true,
  "expiration_check_interval_seconds": 300,
  "expiry_time_seconds": 14400,
  "use_gpu": true
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
      "expiry_time_seconds": 14400,
      "use_gpu": true
    }'
    RAY_CONFIG_ESCAPED=$(echo $RAY_CONFIG | sed 's/"/\\"/g')
    
    # Verify Ray installation and parameters
    echo "Checking Ray installation..."
    python3 -c "import ray; print(f'Ray version: {ray.__version__}')"
    echo "Available Ray workers configuration:"
    python3 -c "import ray; ray.init(); print(ray.cluster_resources()); ray.shutdown()"
fi

# Start Ray head node
echo "Starting Ray head node on $GAMING_PC_IP:$RAY_PORT"
ray stop
ray start --head --port=$RAY_PORT --num-cpus=32 --num-gpus=1

# If head-only mode, just start the ray node and exit
if [ "$HEAD_ONLY" = true ]; then
    echo "Ray head node is running. Other machines can connect using:"
    echo "ray start --address=$GAMING_PC_IP:$RAY_PORT"
    exit 0
fi

# Set RAY_ADDRESS for the training script
export RAY_ADDRESS=$GAMING_PC_IP:$RAY_PORT

# Echo actual command to be run
echo "Running command with RAY_ADDRESS=$RAY_ADDRESS"
echo "train --preset $PRESET --name $EXPERIMENT_NAME --override \"--num-envs\" \"$NUM_ENVS\" \"--remote-processor-type\" \"ray\" \"--remote-processor-pool-size\" \"$POOL_SIZE\" \"--remote-processor-kwargs\" \"$RAY_CONFIG_ESCAPED\" \"--remote-processor-device\" \"cuda\" \"--continue-training\" \"true\" \"--allow-cleanup\" \"true\""

# Ask for confirmation before running
read -p "Run this command? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Execute the training command
    if [ "$DEBUG_MODE" = true ]; then
        # Run with verbose logging in debug mode
        train --preset $PRESET --name $EXPERIMENT_NAME --override "--num-envs" "$NUM_ENVS" "--remote-processor-type" "ray" "--remote-processor-pool-size" "$POOL_SIZE" "--remote-processor-kwargs" "$RAY_CONFIG" "--remote-processor-device" "cuda" "--continue-training" "true" "--allow-cleanup" "true" "--debug" "true" "--log-level" "debug"
    else
        train --preset $PRESET --name $EXPERIMENT_NAME --override "--num-envs" "$NUM_ENVS" "--remote-processor-type" "ray" "--remote-processor-pool-size" "$POOL_SIZE" "--remote-processor-kwargs" "$RAY_CONFIG" "--remote-processor-device" "cuda" "--continue-training" "true" "--allow-cleanup" "true"
    fi
    
    # Update changelog
    if [ $? -eq 0 ]; then
        echo "Updating CHANGELOG.md with this Ray training run..."
        
        # Check if we should add to the changelog
        read -p "Add this run to CHANGELOG.md? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]
        then
            # Prepend to CHANGELOG.md
            TMP_FILE=$(mktemp)
            cat > $TMP_FILE << EOF
## $TIMESTAMP

### Ray Distributed Training on Gaming PC
- Started Ray head node on Ryzen 9 7950X3D (32 threads) with RTX 4090 GPU
- Configured with $NUM_ENVS environments and $POOL_SIZE dedicated worker processors
- Allocated 1.5 CPU cores per actor with max concurrency of 4
- Leveraged RTX 4090 GPU for model inference with "--remote-processor-device cuda"
- Extended model caching to 4 hours to reduce serialization overhead
- Enabled Ray address sharing for multi-machine distributed training
- Optimized for high-performance gaming hardware with increased environment count

$(cat CHANGELOG.md)
EOF
            mv $TMP_FILE CHANGELOG.md
            echo "CHANGELOG.md updated!"
        fi
    fi
else
    echo "Command not executed."
fi 