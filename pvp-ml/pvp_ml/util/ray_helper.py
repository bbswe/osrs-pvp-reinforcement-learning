import logging
import os

logger = logging.getLogger(__name__)


def init() -> None:
    import ray

    if not ray.is_initialized():
        logger.info(f"Initializing ray - RAY_ADDRESS={os.getenv('RAY_ADDRESS')}")
        
        # Check if connecting to existing cluster
        if os.getenv('RAY_ADDRESS'):
            # Connect to existing Ray cluster
            ray.init(
                namespace="pvp-ml",
                # Reduce logging noise
                logging_level=logging.WARNING,
                # Handle reinitialization gracefully
                ignore_reinit_error=True,
            )
        else:
            # Initialize new Ray cluster with optimized settings
            # Optimized for M2 Pro with 10 cores (6 performance, 4 efficiency)
            ray.init(
                namespace="pvp-ml",
                # Configure reasonable object store size for 16GB system
                object_store_memory=2 * 1024 * 1024 * 1024,  # 2GB object store
                # System config optimized for M2 Pro
                _system_config={
                    # Reduce memory pressure
                    "object_spilling_threshold": 0.8,
                    # More time for Ray to start actors on M2 chips
                    "worker_register_timeout_seconds": 60,
                },
                # Reduce logging noise
                logging_level=logging.WARNING,
                # Dashboard uses resources and isn't needed for training
                include_dashboard=False,
                # Handle reinitialization gracefully
                ignore_reinit_error=True,
            )
