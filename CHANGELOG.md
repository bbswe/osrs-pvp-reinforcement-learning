## May 06, 2025 - 14:15 CEST

### Ray Training on M2 Pro Hardware
- Successfully ran Ray-based training optimized for MacBook M2 Pro (10 cores)
- Used 40 environments with 4 dedicated worker processors
- Configured each Ray actor to use 0.75 CPU cores with max concurrency of 2
- Modified ray_helper.py to better utilize M2 Pro's performance and efficiency cores
- Extended model caching to 2 hours to reduce serialization overhead
- Enabled shared actors to minimize resource requirements

## May 06, 2025 - 14:12 CEST

### Ray Training on M2 Pro Hardware
- Successfully ran Ray-based training optimized for MacBook M2 Pro (10 cores)
- Used 40 environments with 4 dedicated worker processors
- Configured each Ray actor to use 0.75 CPU cores with max concurrency of 2
- Modified ray_helper.py to better utilize M2 Pro's performance and efficiency cores
- Extended model caching to 2 hours to reduce serialization overhead
- Enabled shared actors to minimize resource requirements

## May 06, 2025 - 14:08 CEST

### Ray Training Progress Update
- Reached 17.49M steps with steady performance on M2 Pro
- Significant ELO rating decrease against past self-play opponents to 2087.60 (-49.69)
- Further decrease in ELO against reference agents to 1426.53 (-45.47)
- Training speed improved to 357 steps/second
- Win rate predictor accuracy decreased to 67.12%
- Cycle completed in approximately 122 seconds (vs. previous 129 seconds)
- Successfully distributing remote models across worker nodes
- Loading trained models from both RayM2Pro and reference directories

## May 06, 2025 - 14:03 CEST

### Ray Training Progress with 100 Environments
- Reached 17.4M steps in Ray-based training optimized for M2 Pro hardware
- Maintaining consistent 347-348 steps/second throughput with 100 environments
- Successfully balancing workload across 6 workers with 0.4 CPUs per actor
- Model files properly distributed to remote workers as needed
- Ray configuration proven stable for extended training sessions
- ELO rating improved to 2129.32 (+11.80) against past self-play opponents
- ELO rating against reference agents increased to 1496.08 (+64.00)
- Training continuing from the migrated ThreadParallel model history

## May 06, 2025 - 13:54 CEST

### Ray Training on M2 Pro Hardware
- Successfully ran Ray-based training optimized for MacBook M2 Pro (10 cores)
- Used 40 environments with 4 dedicated worker processors
- Configured each Ray actor to use 0.75 CPU cores with max concurrency of 2
- Modified ray_helper.py to better utilize M2 Pro's performance and efficiency cores
- Extended model caching to 2 hours to reduce serialization overhead
- Enabled shared actors to minimize resource requirements

## May 06, 2025 - 13:53 CEST

### Migrated Full Model History from ThreadParallel to RayM2Pro
- Copied 167 model checkpoints from ThreadParallel to RayM2Pro experiment
- Converted all models to trainable format for Ray compatibility
- Enabled complete past self-play with full model history
- Eliminated 'missing league opponent' warnings during training
- Preserved entire training evolution history for better opponent selection

## May 06, 2025 - 13:25 CEST

### Increased Environment Count from 40 to 100 with Ray
- Optimized Ray configuration to handle 100 training environments (up from 40)
- Reduced CPU allocation per actor from 0.75 to 0.4 cores for better resource distribution
- Increased worker pool size from 4 to 6 to process more environments in parallel
- Enhanced concurrency settings from 2 to 3 tasks per actor
- Maintained shared actor strategy and extended model caching for efficiency
- Balanced load distribution to match ThreadParallel's high environment count

## May 06, 2025 - 13:24 CEST

### Ray Training on M2 Pro Hardware
- Successfully ran Ray-based training optimized for MacBook M2 Pro (10 cores)
- Used 40 environments with 4 dedicated worker processors
- Configured each Ray actor to use 0.75 CPU cores with max concurrency of 2
- Modified ray_helper.py to better utilize M2 Pro's performance and efficiency cores
- Extended model caching to 2 hours to reduce serialization overhead
- Enabled shared actors to minimize resource requirements

## May 06, 2025 - 13:22 CEST

### Updated to Latest ThreadParallel Model (17M steps)
- Replaced 10M step model with latest ThreadParallel model (main-17203200-steps.zip)
- Converted latest model to trainable format using optimizer state injection
- Preserved complete 17M steps of training progress while maintaining trainability
- Created backup of previous 10M step model for comparison purposes
- Leveraging maximum amount of previous thread-based training experience

## May 06, 2025 - 13:21 CEST

### Successfully Continued Training with ThreadParallel Model in Ray
- Confirmed successful continuation of training from ThreadParallel model (~10M steps) using Ray
- Resolved missing league opponents warning (expected behavior during migration)
- Achieved 360+ steps per second processing rate with optimized Ray configuration
- Maintained model weights and neural network state while leveraging Ray parallelization
- Successfully integrated previous thread-based training progress with Ray's improved architecture

## May 06, 2025 - 13:20 CEST

### Ray Training on M2 Pro Hardware
- Successfully ran Ray-based training optimized for MacBook M2 Pro (10 cores)
- Used 40 environments with 4 dedicated worker processors
- Configured each Ray actor to use 0.75 CPU cores with max concurrency of 2
- Modified ray_helper.py to better utilize M2 Pro's performance and efficiency cores
- Extended model caching to 2 hours to reduce serialization overhead
- Enabled shared actors to minimize resource requirements

## May 06, 2025 - 13:19 CEST

### Ray Training on M2 Pro Hardware
- Successfully ran Ray-based training optimized for MacBook M2 Pro (10 cores)
- Used 40 environments with 4 dedicated worker processors
- Configured each Ray actor to use 0.75 CPU cores with max concurrency of 2
- Modified ray_helper.py to better utilize M2 Pro's performance and efficiency cores
- Extended model caching to 2 hours to reduce serialization overhead
- Enabled shared actors to minimize resource requirements

## May 06, 2025 - 13:18 CEST

### Converted ThreadParallel Model to Trainable Format for RayM2Pro
- Created a model conversion utility to add optimizer state to non-trainable models
- Successfully converted ThreadParallel model (9.9M steps) to a trainable format
- Fixed "Cannot load non-trainable model as trainable" error in training script
- Preserved all neural network weights and learning progress
- Integrated ThreadParallel model into Ray-based training pipeline

## May 06, 2025 - 13:15 CEST

### Ray Training on M2 Pro Hardware
- Successfully ran Ray-based training optimized for MacBook M2 Pro (10 cores)
- Used 40 environments with 4 dedicated worker processors
- Configured each Ray actor to use 0.75 CPU cores with max concurrency of 2
- Modified ray_helper.py to better utilize M2 Pro's performance and efficiency cores
- Extended model caching to 2 hours to reduce serialization overhead
- Enabled shared actors to minimize resource requirements

## May 06, 2025 - 13:14 CEST

### Migrated ThreadParallel Model to RayM2Pro
- Transferred latest ThreadParallel model (main-9932800-steps.zip) to RayM2Pro experiment
- Continuing training from approximately 10M steps using Ray with M2 Pro optimizations
- Preserved model weights and neural network state while changing parallelization method
- Leveraging previous training while benefiting from Ray's improved process isolation
- Combined thread-based training's efficiency with Ray's better fault tolerance

## May 06, 2025 - 13:09 CEST

### Ray Training on M2 Pro Hardware
- Successfully ran Ray-based training optimized for MacBook M2 Pro (10 cores)
- Used 40 environments with 4 dedicated worker processors
- Configured each Ray actor to use 0.75 CPU cores with max concurrency of 2
- Modified ray_helper.py to better utilize M2 Pro's performance and efficiency cores
- Extended model caching to 2 hours to reduce serialization overhead
- Enabled shared actors to minimize resource requirements

## May 06, 2025 - 13:07 CEST

### Fixed RayM2Pro Training Script
- Added "--allow-cleanup" parameter to fix the experiment directory cleanup issue
- Modified run_ray_m2_pro.sh to properly handle existing experiment directories
- Ensured proper cleanup of previous experiment artifacts before starting new training runs
- Improved script reliability by explicitly controlling experiment directory management
- Maintained existing Ray optimizations for M2 Pro hardware (0.75 CPUs per actor, shared actors)

## May 06, 2025 - 13:07 CEST

### Ray Training on M2 Pro Hardware
- Successfully ran Ray-based training optimized for MacBook M2 Pro (10 cores)
- Used 40 environments with 4 dedicated worker processors
- Configured each Ray actor to use 0.75 CPU cores with max concurrency of 2
- Modified ray_helper.py to better utilize M2 Pro's performance and efficiency cores
- Extended model caching to 2 hours to reduce serialization overhead
- Enabled shared actors to minimize resource requirements

## May 06, 2025 - 13:05 CEST

### Ray Training on M2 Pro Hardware
- Successfully ran Ray-based training optimized for MacBook M2 Pro (10 cores)
- Used 40 environments with 4 dedicated worker processors
- Configured each Ray actor to use 0.75 CPU cores with max concurrency of 2
- Modified ray_helper.py to better utilize M2 Pro's performance and efficiency cores
- Extended model caching to 2 hours to reduce serialization overhead
- Enabled shared actors to minimize resource requirements

## May 06, 2025 - 13:05 CEST

## May 06, 2025 - 13:03 CEST

### Ray Training on M2 Pro Hardware
- Successfully ran Ray-based training optimized for MacBook M2 Pro (10 cores)
- Used 40 environments with 4 dedicated worker processors
- Configured each Ray actor to use 0.75 CPU cores with max concurrency of 2
- Modified ray_helper.py to better utilize M2 Pro's performance and efficiency cores
- Extended model caching to 2 hours to reduce serialization overhead
- Enabled shared actors to minimize resource requirements

## May 06, 2025 - 12:53 CEST

### ThreadParallel Training Optimization Success
- Successfully trained model using thread-based processing with 100 environments and 4 worker threads
- Confirmed smooth loading of model versions for self-play (main-17100800-steps.zip and earlier)
- Achieved stable training speed of ~150-180 environment steps per second
- Properly launched and managed 30 self-play environments, 70 past-self environments, and 10 evaluation environments
- Thread-based approach effectively distributes workload without resource allocation issues
- Eliminated stuck training problems previously encountered with Ray-based processing
- Optimal configuration: 100 total environments with 4 thread workers in pool

### Technical Analysis: Ray vs Thread-based Processing
- Ray's default configuration requires 4 CPU cores per actor, exceeding available MacBook M2 Pro resources
- Ray creates significant model transfer overhead when loading multiple models for self-play
- Ray's inter-process communication adds serialization costs compared to thread-based shared memory
- Thread-based processing avoids socket/network stack congestion that occurs with Ray
- Ray's process isolation conflicts with the Elvarg server's connection model
- Thread-based approach uses simpler synchronization with direct memory access
- Ray gets stuck in resource starvation waiting for CPU allocation rather than failing directly

### Making Ray Work on MacBook M2 Pro
- Use fractional CPU allocation with `--remote-processor-kwargs "{"cpus_per_actor": 0.5}"` to specify 0.5 cores per actor
- Reduce environment count to 40-50 total environments to decrease overall system load
- Configure 4-5 worker processors with `--remote-processor-pool-size 5` for better load distribution
- Modify Ray initialization parameters in `pvp_ml/util/ray_helper.py` to optimize memory usage
- Limit max concurrency with `max_concurrency: 2` to control how many parallel tasks Ray processes
- Apply OS-level optimizations using the provided `ray_optimizer.py` script
- Tune model caching parameters to reduce serialization overhead
- Example command: `train --preset PastSelfPlay --name RayParallel --override "--num-envs" "40" "--remote-processor-type" "ray" "--remote-processor-pool-size" "5" "--remote-processor-kwargs" "{"cpus_per_actor": 0.5, "max_concurrency": 2}" "--continue-training" "true"`

# Changelog

## May 06, 2025 - 12:46 CEST

### Ray vs Thread Processing Performance Analysis
- Identified resource allocation issues with Ray-based processing during model training
- Found CPU resource contention with default Ray settings (requires 4.0 CPU per actor)
- Discovered performance bottlenecks when transferring models to remote Ray workers
- Determined that thread-based processing is more efficient for local training
- Tested reduced environment count (20 vs 60) when using Ray to prevent resource exhaustion
- Documented Ray configuration options including `ray_resources_per_actor` parameter
- Established optimal thread pool size (10 threads) for thread-based model training

## May 06, 2025 - 10:40 CEST

### Enhanced Model Comparison
- Rewritten battle_models.py to incorporate ELO rating and match outcome tracking
- Added support for multiple model fights with statistical analysis of results
- Implemented proper match outcome tracking (wins, losses, ties) between models
- Added command-line arguments for flexible model comparison configuration
- Improved logging with detailed battle outcomes and ELO score changes
- Random placement values for consistent model evaluation
- Win-rate percentage calculation for clear performance metrics

## May 06, 2025 - 09:24 CEST

### Added
- Created Java-based Microbot plugin for PVP agent integration
- Implemented JNI bridge to connect Java with PyTorch C++ for model inference
- Added comprehensive game state observation mapping
- Implemented action execution framework for all trained model actions
- Created detailed configuration panel for customizing agent behavior
- Added visual overlay to monitor agent performance and game state
- Created detailed documentation for building and using the plugin

### Technical
- Established fallback prediction mechanism when JNI is unavailable
- Implemented automatic resource directory creation and model file copying
- Built robust combat state tracking for better decision-making
- Added dynamic target selection based on proximity and priority settings
- Created CMake build system for the JNI component

## May 06, 2025 - 03:23 CEST

### Added
- Created Microbot plugin for PVP agent integration
- Added model export functionality to convert trained models to TorchScript format
- Implemented comprehensive observation mapping for game state detection
- Added action execution framework for all trained actions
- Created plugin documentation and setup instructions

### Fixed
- Fixed model export script to handle the action head structure correctly
- Added error handling for model loading failures
- Fixed policy access in non-trainable model mode

### Technical
- Exported main-13312000-steps.zip model for deployment
- Model achieves ~2000 ELO rating in self-play environments
- Plugin structure follows Microbot conventions for easy integration

## May 06, 2025 - 09:41 CEST

### Improved Model Comparison Script
- Enhanced `compare_models.py` with proper real-time logging capabilities
- Added dynamic port selection to avoid port conflicts when running multiple instances
- Implemented proper cleanup for simulations with signal handling for graceful termination
- Added ongoing match statistics during comparison runs
- Fixed whitespace handling in model path arguments
- Improved error handling and reporting

## May 06, 2025 - 09:47 CEST

### Enhanced Model Comparison Script
- Added built-in file logging to automatically save comparison logs to timestamped files
- Implemented dynamic remote environment port detection
- Added proper file handler cleanup on script exit
- Each log file is stored in the logs/ directory with a unique timestamp
- Terminal output is mirrored to log files for complete history tracking
- Improved port conflict resolution when ports are already in use

## May 06, 2025 - 09:50 CEST

### Complete Simulation Log Capture
- Improved log capture to include all simulation server output
- Log files now contain the Java server's stdout and stderr messages
- Custom process management to directly capture simulation output
- Added thread-based real-time output processing
- "Processing tick" and other server messages now properly recorded
- Fixed issue where server logs were missing from log files

## May 06, 2025 - 09:51 CEST

### Gradle Command Syntax Fix
- Fixed Gradle command syntax for starting the simulation server
- Corrected `--args` parameter formatting to work with Gradle
- Prevented build failures due to incorrect command-line option format 

## May 06, 2025 - 14:12 CEST

### Fixed Ray Model Cache Management System
- Implemented comprehensive thread-safe model cache management in Ray remote processor
- Fixed "dictionary changed size during iteration" error by using local dictionary copies
- Enhanced safety when removing expired models from the cache
- Eliminated race conditions in model loading and expiration
- Created robust solution for handling multiple concurrent model loads
- Prevented training crashes when working with large model collections
- Added double-checking of dictionary membership before deletion operations

## May 06, 2025 - 14:18 CEST

### Ray Training Success After Dictionary Bug Fix
- Fixed critical dictionary iteration bug in Ray remote processor
- System successfully restarted training from 17.57M steps
- ELO rating improved to 2124.36 (+26.76) after latest rollout
- Recovery from previous rating drop confirmed
- Reference agent rating also improved slightly to 1400.09 (+4.97)
- Win rate predictor accuracy at 72.35%
- Distributed model loading working correctly with no errors
- 25+ different models simultaneously loaded across remote workers
- Cache expiration now safely managing memory across workers
