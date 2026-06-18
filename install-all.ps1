param(
    [ValidateSet("auto", "codex", "claude", "all")]
    [string]$Tool = "auto",

    [ValidateSet("local", "github")]
    [string]$Source = "local",

    [string]$Repository = "1447751897/ai-project-command-skills",
    [string]$Branch = "master",
    [string]$CodexTargetRoot = (Join-Path $env:USERPROFILE ".agents\skills"),
    [string]$ClaudeTargetRoot = (Join-Path $env:USERPROFILE ".claude\skills"),
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$CodexSkillNames = @(
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

$ClaudeSkillNames = @(
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

function Test-CommandExists {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Test-CodexDetected {
    if ($env:CODEX_HOME) { return $true }
    if (Test-Path (Join-Path $env:USERPROFILE ".codex")) { return $true }
    if (Test-Path (Join-Path $env:USERPROFILE ".agents")) { return $true }
    if (Test-CommandExists "codex") { return $true }
    return $false
}

function Test-ClaudeDetected {
    if ($env:CLAUDE_CONFIG_DIR) { return $true }
    if (Test-Path (Join-Path $env:USERPROFILE ".claude")) { return $true }
    if (Test-CommandExists "claude") { return $true }
    return $false
}

function Get-PackageRoot {
    if ($Source -eq "local") {
        return (Split-Path -Parent $MyInvocation.ScriptName)
    }

    $TempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("ai-project-command-skills-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Force -Path $TempRoot | Out-Null
    $ZipPath = Join-Path $TempRoot "package.zip"
    $ExtractRoot = Join-Path $TempRoot "extract"
    New-Item -ItemType Directory -Force -Path $ExtractRoot | Out-Null

    $Url = "https://github.com/$Repository/archive/refs/heads/$Branch.zip"
    Write-Host "Downloading: $Url"
    Invoke-WebRequest -Uri $Url -OutFile $ZipPath -UseBasicParsing
    Expand-Archive -LiteralPath $ZipPath -DestinationPath $ExtractRoot -Force

    $Candidate = Get-ChildItem -Path $ExtractRoot -Directory | Where-Object {
        (Test-Path (Join-Path $_.FullName "skills")) -or
        (Test-Path (Join-Path $_.FullName "claude-skills"))
    } | Select-Object -First 1

    if (-not $Candidate) {
        throw "Downloaded package does not contain skills or claude-skills."
    }

    return $Candidate.FullName
}

function Get-SelectedTools {
    switch ($Tool) {
        "codex" { return @("codex") }
        "claude" { return @("claude") }
        "all" { return @("codex", "claude") }
    }

    $Detected = @()
    if (Test-CodexDetected) { $Detected += "codex" }
    if (Test-ClaudeDetected) { $Detected += "claude" }
    return $Detected
}

function Backup-ExistingSkills {
    param(
        [string]$TargetRoot,
        [string[]]$SkillNames
    )

    $Existing = @()
    foreach ($Name in $SkillNames) {
        $Path = Join-Path $TargetRoot $Name
        if (Test-Path $Path) { $Existing += $Path }
    }

    if ($Existing.Count -eq 0) {
        return $null
    }

    $BackupRoot = Join-Path $TargetRoot (Join-Path ".backup" ("ai-project-command-skills-" + (Get-Date -Format "yyyyMMdd-HHmmss")))
    New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
    foreach ($Path in $Existing) {
        Copy-Item -Recurse -Force -LiteralPath $Path -Destination (Join-Path $BackupRoot (Split-Path -Leaf $Path))
    }
    return $BackupRoot
}

function Install-SkillSet {
    param(
        [ValidateSet("codex", "claude")]
        [string]$Kind,
        [string]$PackageRoot
    )

    if ($Kind -eq "codex") {
        $SourceRoot = Join-Path $PackageRoot "skills"
        $TargetRoot = $CodexTargetRoot
        $SkillNames = $CodexSkillNames
        $RestartText = "Restart Codex desktop so the command menu can rescan skills."
    } else {
        $SourceRoot = Join-Path $PackageRoot "claude-skills"
        $TargetRoot = $ClaudeTargetRoot
        $SkillNames = $ClaudeSkillNames
        $RestartText = "Restart Claude Code so it can rescan skills."
    }

    if (-not (Test-Path $SourceRoot)) {
        throw "Missing $Kind source directory: $SourceRoot"
    }

    foreach ($Name in $SkillNames) {
        $SkillMd = Join-Path (Join-Path $SourceRoot $Name) "SKILL.md"
        if (-not (Test-Path $SkillMd)) {
            throw "Missing $Kind skill: $Name"
        }
    }

    Write-Host ""
    Write-Host "== $Kind =="
    Write-Host "Source: $SourceRoot"
    Write-Host "Target: $TargetRoot"

    if ($DryRun) {
        foreach ($Name in $SkillNames) {
            $Target = Join-Path $TargetRoot $Name
            $Action = if (Test-Path $Target) { "update" } else { "install" }
            Write-Host "Would $Action`: $Name -> $Target"
        }
        return
    }

    New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null
    $BackupRoot = Backup-ExistingSkills -TargetRoot $TargetRoot -SkillNames $SkillNames
    if ($BackupRoot) {
        Write-Host "Backup created: $BackupRoot"
    }

    foreach ($Name in $SkillNames) {
        $SourcePath = Join-Path $SourceRoot $Name
        $TargetPath = Join-Path $TargetRoot $Name
        if (Test-Path $TargetPath) {
            Remove-Item -Recurse -Force -LiteralPath $TargetPath
        }
        Copy-Item -Recurse -Force -Path $SourcePath -Destination $TargetPath
        Write-Host "Installed: $Name"
    }

    Write-Host $RestartText
}

$SelectedTools = Get-SelectedTools
if ($SelectedTools.Count -eq 0) {
    throw "No Codex or Claude Code installation was detected. Use -Tool codex, -Tool claude, or -Tool all to install anyway."
}

$PackageRoot = Get-PackageRoot
Write-Host "Package root: $PackageRoot"
Write-Host "Selected tools: $($SelectedTools -join ', ')"

foreach ($SelectedTool in $SelectedTools) {
    Install-SkillSet -Kind $SelectedTool -PackageRoot $PackageRoot
}

if ($DryRun) {
    Write-Host ""
    Write-Host "Dry run complete. No local skills were changed."
}
