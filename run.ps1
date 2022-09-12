<# Shortcut script for running the bot #>

$START_IN = Join-Path $home "repos\localbot"

# Assert that script is run with current directory at $START_IN
if ((Get-Location).ToString() -ne $START_IN) {
    Write-Host "Script must be run at $START_IN, aborted." -ForegroundColor Red
    exit 1
}

# Assert that script is run with the project venv active
if (!$env:VIRTUAL_ENV -or (Split-Path $env:VIRTUAL_ENV -Parent) -ne $START_IN) {
    Write-Host "Script must be run with the project venv active, aborted." -ForegroundColor Red
    exit 1
}

# Execute the bot package
python -m bot
exit 0
