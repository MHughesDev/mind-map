$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

python "scripts/run_autonomous_paper.py" @args
exit $LASTEXITCODE
