#!/bin/bash
# Optimized Ray training script for MacBook M2 Pro (10 cores)
# This script configures Ray for optimal performance on M2 Pro hardware

# Get timestamp for changelog
TIMESTAMP=$(date "+%b %d, %Y - %H:%M %Z")
echo "Running Ray-optimized training on MacBook M2 Pro at $TIMESTAMP"

# Parse command line options
DEBUG_MODE=false
while getopts "d" opt; do
  case $opt in
    d) DEBUG_MODE=true ;;
    *) echo "Unknown option: -$OPTARG" >&2; exit 1 ;;
  esac
done
shift $((OPTIND - 1))

# Training configuration optimized for M2 Pro
EXPERIMENT_NAME="RayM2Pro"
NUM_ENVS=40
POOL_SIZE=4
PRESET=PastSelfPlay

# Ray-specific configuration parameters
# - Uses 0.75 CPU per actor (allowing efficient use of 10 cores)
# - Limits concurrency to 2 tasks per actor
# - Extended model caching to reduce overhead (2 hours)
# - Less frequent cache cleanup (5 minutes)
RAY_CONFIG='{
  "cpus_per_actor": 0.75, 
  "max_concurrency": 2,
  "shared": true,
  "expiration_check_interval_seconds": 300,
  "expiry_time_seconds": 7200
}'

# Resolve escaped quotes issue with different shells
RAY_CONFIG_ESCAPED=$(echo $RAY_CONFIG | sed 's/"/\\"/g')

# Debug mode configuration
if [ "$DEBUG_MODE" = true ]; then
    echo "Running in DEBUG mode"
    # Use fewer environments and workers in debug mode
    NUM_ENVS=20
    POOL_SIZE=2
    # Add debugging parameters to config
    RAY_CONFIG='{
      "cpus_per_actor": 0.5,
      "max_concurrency": 1,
      "shared": true,
      "expiration_check_interval_seconds": 300,
      "expiry_time_seconds": 7200
    }'
    RAY_CONFIG_ESCAPED=$(echo $RAY_CONFIG | sed 's/"/\\"/g')
    # Verify Ray installation and parameters first
    echo "Checking Ray installation..."
    python3 -c "import ray; print(f'Ray version: {ray.__version__}')"
    echo "Available Ray workers configuration:"
    python3 -c "import ray; ray.init(); print(ray.cluster_resources()); ray.shutdown()"
fi

# Echo actual command to be run
echo "Running command:"
echo "train --preset $PRESET --name $EXPERIMENT_NAME --override \"--num-envs\" \"$NUM_ENVS\" \"--remote-processor-type\" \"ray\" \"--remote-processor-pool-size\" \"$POOL_SIZE\" \"--remote-processor-kwargs\" \"$RAY_CONFIG_ESCAPED\" \"--continue-training\" \"true\" \"--allow-cleanup\" \"true\""

# Ask for confirmation before running
read -p "Run this command? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Execute the training command
    if [ "$DEBUG_MODE" = true ]; then
        # Run with verbose logging in debug mode
        train --preset $PRESET --name $EXPERIMENT_NAME --override "--num-envs" "$NUM_ENVS" "--remote-processor-type" "ray" "--remote-processor-pool-size" "$POOL_SIZE" "--remote-processor-kwargs" "$RAY_CONFIG" "--continue-training" "true" "--allow-cleanup" "true" "--debug" "true" "--log-level" "debug"
    else
        train --preset $PRESET --name $EXPERIMENT_NAME --override "--num-envs" "$NUM_ENVS" "--remote-processor-type" "ray" "--remote-processor-pool-size" "$POOL_SIZE" "--remote-processor-kwargs" "$RAY_CONFIG" "--continue-training" "true" "--allow-cleanup" "true"
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

### Ray Training on M2 Pro Hardware
- Successfully ran Ray-based training optimized for MacBook M2 Pro (10 cores)
- Used $NUM_ENVS environments with $POOL_SIZE dedicated worker processors
- Configured each Ray actor to use 0.75 CPU cores with max concurrency of 2
- Modified ray_helper.py to better utilize M2 Pro's performance and efficiency cores
- Extended model caching to 2 hours to reduce serialization overhead
- Enabled shared actors to minimize resource requirements

$(cat CHANGELOG.md)
EOF
            mv $TMP_FILE CHANGELOG.md
            echo "CHANGELOG.md updated!"
        fi
    fi
else
    echo "Command not executed."
fi 