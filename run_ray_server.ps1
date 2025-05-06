# PowerShell script for connecting Dell PowerEdge R620 server to a Ray cluster as a worker node
# This script optimizes for server hardware with many cores but no GPU

# Configuration settings (adjust as needed)
$GamingPcIp = "192.168.1.100"  # REPLACE with your actual gaming PC IP
$RayPort = 6379
$ServerCpus = 24  # Adjust based on your R620 configuration (typically 16-24 cores)
$NumEnvs = 120  # Settings if you decide to run training directly on this node
$PoolSize = 8
$ExperimentName = "RayDistributed"
$Preset = "PastSelfPlay"

# Parse command-line parameters
param(
    [string]$IpAddress,
    [int]$Port = 6379,
    [int]$Cpus = 24
)

# Override defaults with command-line parameters if provided
if ($IpAddress) { $GamingPcIp = $IpAddress }
if ($Port -ne 6379) { $RayPort = $Port }
if ($Cpus -ne 24) { $ServerCpus = $Cpus }

# Ray configuration optimized for server hardware
$RayConfig = @{
    cpus_per_actor = 2.0
    max_concurrency = 3
    shared = $true
    expiration_check_interval_seconds = 300
    expiry_time_seconds = 14400
} | ConvertTo-Json -Compress

Write-Host "Connecting Dell PowerEdge R620 to Ray cluster..."

# Stop any existing Ray processes
Write-Host "Stopping any existing Ray processes..."
ray stop

# Connect to the Ray head node on the gaming PC
Write-Host "Connecting to Ray head node at $GamingPcIp`:$RayPort with $ServerCpus CPUs"
ray start --address="$GamingPcIp`:$RayPort" --num-cpus=$ServerCpus

# Set RAY_ADDRESS environment variable
$env:RAY_ADDRESS = "$GamingPcIp`:$RayPort"

Write-Host "Successfully connected to Ray cluster at $env:RAY_ADDRESS"
Write-Host "This server is now contributing $ServerCpus CPUs to the distributed training"
Write-Host ""
Write-Host "To run training from this server (optional), use:"
Write-Host "train --preset $Preset --name $ExperimentName --override --num-envs $NumEnvs --remote-processor-type ray --remote-processor-pool-size $PoolSize --remote-processor-kwargs '$RayConfig' --continue-training true --allow-cleanup true"
Write-Host ""
Write-Host "For optimal results, run the training on the gaming PC with GPU support"
Write-Host "The server is now available as a compute resource for the Ray cluster" 