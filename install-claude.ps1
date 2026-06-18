param(
    [string]$TargetRoot = (Join-Path $env:USERPROFILE ".claude\skills")
)

$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsSource = Join-Path $PackageRoot "claude-skills"

if (-not (Test-Path $SkillsSource)) {
    throw "Missing Claude skills directory: $SkillsSource"
}

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

$SkillNames = @(
    "ai-init",
    "ai-goal",
    "ai-super",
    "ai-feature",
    "ai-change",
    "ai-fix",
    "ai-tech",
    "ai-deploy",
    "ai-handoff",
    "ai-roadmap",
    "ai-plan",
    "ai-status",
    "ai-continue",
    "ai-upgrade",
    "ai-project-kickoff-docs"
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
Write-Host "Done. Restart Claude Code, then try /ai-init, /ai-goal, /ai-goal --super, /ai-feature, /ai-fix, /ai-tech, /ai-deploy, /ai-handoff, /ai-roadmap, /ai-plan, /ai-status, /ai-continue, or /ai-upgrade. /ai-super is also available as a compatibility alias."
