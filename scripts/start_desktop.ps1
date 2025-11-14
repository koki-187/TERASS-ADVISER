# PowerShell launch script for the TERASS業動サポートAI desktop application.
#
# This script sets up a Python virtual environment if needed, installs
# required dependencies, and runs the Tkinter desktop version of the
# application. If the Bitwarden CLI (`bws`) is available, secrets are
# injected into the environment automatically. Otherwise, the script
# falls back to a normal launch and expects secrets to be provided
# directly via environment variables.

param(
    [string]$ProjectDir = (Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path)
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "==== Starting TERASS Desktop Application ===="

# Determine Python executable (python or py)
$pythonCmd = (Get-Command python -ErrorAction SilentlyContinue) ?? (Get-Command py -ErrorAction SilentlyContinue)
if (-not $pythonCmd) {
    throw "Python is not installed. Please install Python 3.x and try again."
}

# Create virtual environment if it doesn't exist
$venvPath = Join-Path $ProjectDir '.venv'
if (-not (Test-Path $venvPath)) {
    & $pythonCmd.Source -m venv $venvPath
}

# Activate virtual environment
. (Join-Path $venvPath 'Scripts/Activate.ps1')

# Upgrade pip and install dependencies if requirements.txt exists
pip install --upgrade pip
$requirements = Join-Path $ProjectDir 'requirements.txt'
if (Test-Path $requirements) {
    pip install -r $requirements
} else {
    # Fallback: install essential library
    pip install pillow
}

# Define the Python application entry point
$appFile = Join-Path $ProjectDir 'terass_assistant_with_scenarios.py'
if (-not (Test-Path $appFile)) {
    throw "$appFile not found. Please ensure you are running the script from the correct project directory."
}

# Check for Bitwarden CLI
$bws = Get-Command bws -ErrorAction SilentlyContinue
if ($bws) {
    Write-Host "Injecting secrets via Bitwarden..."
    & bws run -- python $appFile
} else {
    Write-Warning "Bitwarden CLI not found. Running application without secret injection."
    & python $appFile
}
