$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root
$userScripts = python -c "import site, pathlib; print(pathlib.Path(site.getuserbase()) / 'Scripts')"
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")

Write-Host "Installing IFoundYou from local release package..."
python -m pip install --user .

if (-not (Test-Path $userScripts)) {
    New-Item -ItemType Directory -Path $userScripts | Out-Null
}

Copy-Item ".\\ifoundyou.cmd" (Join-Path $userScripts "ifoundyou.cmd") -Force

if (($userPath -split ';' | Where-Object { $_ -eq $userScripts }).Count -eq 0) {
    $newUserPath = if ([string]::IsNullOrWhiteSpace($userPath)) { $userScripts } else { "$userPath;$userScripts" }
    [Environment]::SetEnvironmentVariable("Path", $newUserPath, "User")
    $env:Path = "$env:Path;$userScripts"
}

Write-Host ""
Write-Host "Installed. Main command:"
Write-Host "  ifoundyou github.com"
Write-Host ""
Write-Host "If this terminal was open before installation, open a new PowerShell window."
