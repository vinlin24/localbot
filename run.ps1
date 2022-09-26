<# Shortcut script for running the bot #>

# Assert that script is run with cwd at file's location
if ((Get-Location).ToString() -ne $PSScriptRoot) {
    Write-Host "Script must be run from its directory, aborted." -ForegroundColor Red
    exit 1
}

# Assert that script is run with the project venv active
if (!$env:VIRTUAL_ENV -or (Split-Path $env:VIRTUAL_ENV -Parent) -ne $PSScriptRoot) {
    Write-Host "Script must be run with the project venv active, aborted." -ForegroundColor Red
    exit 1
}

# Execute the bot package
python -m bot
exit 0
