param(
    [string]$TargetRoot = (Join-Path $env:USERPROFILE ".claude\skills")
)

$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsSource = Join-Path $PackageRoot "skills"

if (-not (Test-Path $SkillsSource)) {
    throw "Missing Claude skills directory: $SkillsSource"
}

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

$SkillNames = @(
    "zno-init",
    "zno-goal",
    "zno-super",
    "zno-feature",
    "zno-change",
    "zno-fix",
    "zno-tech",
    "zno-deploy",
    "zno-handoff",
    "zno-roadmap",
    "zno-plan",
    "zno-status",
    "zno-continue",
    "zno-upgrade",
    "zno-project-kickoff-docs",
    "zno-evaluate",
    "zno-retro",
    "zno-review"
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
Write-Host "Done. Restart Claude Code, then try /zno-init, /zno-goal, /zno-goal --super, /zno-evaluate, /zno-review, /zno-retro, /zno-feature, /zno-fix, /zno-tech, /zno-deploy, /zno-handoff, /zno-roadmap, /zno-plan, /zno-status, /zno-continue, or /zno-upgrade. /zno-super is also available as a compatibility alias."
