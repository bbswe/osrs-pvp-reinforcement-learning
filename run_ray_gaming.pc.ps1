# PowerShell script for setting up Ray head node on Windows gaming PC
# For Ryzen 9 7950X3D CPU and RTX 4090 GPU
# Enable running scripts in powershell
#PowerShell -ExecutionPolicy Bypass -File run_ray_gaming_pc.ps1

# Configuration settings
$GamingPcIp = "192.168.1.100"  # REPLACE with your actual gaming PC IP
$RayPort = 6379
$NumEnvs = 160
$PoolSize = 16
$ExperimentName = "RayDistributed"
$Preset = "PastSelfPlay"

# Ray configuration for high-end gaming PC
$RayConfig = @{
    cpus_per_actor = 1.5
    max_concurrency = 4
    shared = $true
    expiration_check_interval_seconds = 300
    expiry_time_seconds = 14400
    use_gpu = $true
} | ConvertTo-Json -Compress

# Stop any existing Ray processes
Write-Host "Stopping any existing Ray processes..."
ray stop

# Start Ray head node
Write-Host "Starting Ray head node on $GamingPcIp`:$RayPort"
ray start --head --port=$RayPort --num-cpus=32 --num-gpus=1

# Set RAY_ADDRESS environment variable
$env:RAY_ADDRESS = "$GamingPcIp`:$RayPort"
Write-Host "Set RAY_ADDRESS=$env:RAY_ADDRESS"

# Run the training command
$TrainCommand = "train --preset $Preset --name $ExperimentName --override --num-envs $NumEnvs --remote-processor-type ray --remote-processor-pool-size $PoolSize --remote-processor-kwargs '$RayConfig' --remote-processor-device cuda --continue-training true --allow-cleanup true"

Write-Host "Ready to run training command:"
Write-Host $TrainCommand

$Confirm = Read-Host "Run this command? (y/n)"
if ($Confirm -eq 'y') {
    Write-Host "Starting training..."
    Invoke-Expression $TrainCommand
} else {
    Write-Host "Training not started. Ray head node is still running."
    Write-Host "Other machines can connect using: ray start --address=$GamingPcIp`:$RayPort"
}