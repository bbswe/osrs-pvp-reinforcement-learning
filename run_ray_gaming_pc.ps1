# PowerShell script for setting up Ray head node on Windows gaming PC
# For Ryzen 9 7950X3D CPU and RTX 4090 GPU

# Parse command-line parameters
param(
    [string]$IpAddress,
    [int]$Port = 6379,
    [switch]$HeadOnly
)

# Navigate to the pvp-ml directory (required for train command to work)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PvpMlPath = Join-Path -Path $ScriptDir -ChildPath "pvp-ml"
Set-Location -Path $PvpMlPath
Write-Host "Changed directory to: $(Get-Location)"

# Configuration settings
$GamingPcIp = "192.168.1.105"  # REPLACE with your actual gaming PC IP
$RayPort = 6379
$NumEnvs = 160
$PoolSize = 16
$ExperimentName = "RayDistributed"
$Preset = "PastSelfPlay"

# Override defaults with command-line parameters if provided
if ($IpAddress) { $GamingPcIp = $IpAddress }
if ($Port -ne 6379) { $RayPort = $Port }

# Ray configuration for high-end gaming PC
$RayConfig = @{
    cpus_per_actor = 1.5
    max_concurrency = 4
    shared = $true
    expiration_check_interval_seconds = 300
    expiry_time_seconds = 14400
} | ConvertTo-Json -Compress

# Stop any existing Ray processes
Write-Host "Stopping any existing Ray processes..."
ray stop

# Start Ray head node
Write-Host "Starting Ray head node on $GamingPcIp`:$RayPort"
ray start --head --port=$RayPort --num-cpus=32 --num-gpus=1

# If head-only mode, just start the ray node and exit
if ($HeadOnly) {
    Write-Host "Ray head node is running. Other machines can connect using:"
    Write-Host "ray start --address=$GamingPcIp`:$RayPort"
    exit 0
}

# Set RAY_ADDRESS for the training script
$env:RAY_ADDRESS = "$GamingPcIp`:$RayPort"

# Create the training command
$TrainCommand = "python -m pvp_ml.run_train_job --preset $Preset --name $ExperimentName --override --num-envs $NumEnvs --remote-processor-type ray --remote-processor-pool-size $PoolSize --remote-processor-kwargs '$RayConfig' --remote-processor-device cuda --continue-training true --allow-cleanup true"

# Echo actual command to be run
Write-Host "Running command with RAY_ADDRESS=$env:RAY_ADDRESS"
Write-Host $TrainCommand

# Ask for confirmation before running
$Confirm = Read-Host "Run this command? (y/n)"
if ($Confirm -eq 'y') {
    # Execute the training command
    Write-Host "Starting training..."
    Invoke-Expression $TrainCommand
} else {
    Write-Host "Training not started. Ray head node is still running."
    Write-Host "Other machines can connect using: ray start --address=$GamingPcIp`:$RayPort"
} 