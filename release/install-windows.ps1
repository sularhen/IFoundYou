$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "Installing IFoundYou from local release package..."
python -m pip install .

Write-Host ""
Write-Host "Installed. Run it with:"
Write-Host "  python -m ifoundyou github.com"
Write-Host ""
Write-Host "Optional wrapper:"
Write-Host "  .\\whereareyou.ps1 github.com"
