<#
.SYNOPSIS
    One-time setup script for Windows to persist Bitwarden secrets as system
    environment variables.

.DESCRIPTION
    Retrieves all secrets associated with a given Bitwarden project ID and
    writes them to machine-level environment variables.  This makes the
    secrets available to all users and processes on the system without
    requiring repeated ``bws run`` invocations.

    The script expects ``BWS_ACCESS_TOKEN`` to be defined in the parent
    environment.  Optionally specify ``BWS_PROJECT_ID`` or pass ``-ProjectId``
    explicitly when invoking the script.  Administrative privileges are
    required to modify machine-scoped environment variables.
#>

[CmdletBinding()]
param(
    [string]$ProjectId = $env:BWS_PROJECT_ID
)

if (-not $env:BWS_ACCESS_TOKEN) {
    Write-Error "BWS_ACCESS_TOKEN environment variable is not set. Exiting."
    exit 1
}

if (-not $ProjectId) {
    Write-Error "Project ID not provided and BWS_PROJECT_ID is not set. Exiting."
    exit 1
}

try {
    # Export secrets from Bitwarden as KEY=VALUE lines into a temporary file
    $envPath = Join-Path $env:TEMP "terass.env"
    bws secret list --project-id $ProjectId --output json `
        | ConvertFrom-Json `
        | ForEach-Object { "{0}={1}" -f $_.key, $_.value } `
        | Out-File -Encoding ascii -FilePath $envPath

    # Iterate over each KEY=VALUE line and set the machine environment variable
    Get-Content -Path $envPath | ForEach-Object {
        $kv = $_ -split '=', 2
        $key = $kv[0]
        $value = $kv[1]
        [System.Environment]::SetEnvironmentVariable($key, $value, 'Machine')
        Write-Host "Set $key"
    }

    Write-Host "Environment variables have been configured successfully."
    Write-Host "Restart your computer or log out and back in to apply the changes."
} catch {
    Write-Error "An error occurred: $_"
    exit 1
}
