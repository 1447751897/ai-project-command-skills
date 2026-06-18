param(
    [string]$TargetRoot = (Join-Path $env:USERPROFILE ".agents\skills")
)

$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsSource = Join-Path $PackageRoot "skills"

if (-not (Test-Path $SkillsSource)) {
    throw "Missing skills directory: $SkillsSource"
}

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

$SkillNames = @(
    "init",
    "goal",
    "super",
    "feature",
    "change",
    "fix",
    "tech",
    "deploy",
    "handoff",
    "roadmap",
    "plan",
    "status",
    "continue",
    "upgrade",
    "project-kickoff-docs"
)

foreach ($Name in $SkillNames) {
    $Source = Join-Path $SkillsSource $Name
    $Target = Join-Path $TargetRoot $Name

    if (-not (Test-Path $Source)) {
        Write-Warning "Skip missing skill: $Name"
        continue
    }

    if (Test-Path $Target) {
        Remove-Item -Recurse -Force -LiteralPath $Target
    }

    Copy-Item -Recurse -Force -Path $Source -Destination $Target
    Write-Host "Installed: $Name"
}

Write-Host ""
Write-Host "Done. Restart Codex desktop, then try /init, /goal, /goal --super, /feature, /fix, /tech, /deploy, /handoff, /roadmap, /plan, /status, /continue, or /upgrade. /super is also available as a compatibility alias."
