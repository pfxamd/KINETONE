$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repo = 'pfxamd/KINETONE'
$source = Split-Path -Parent $MyInvocation.MyCommand.Path

function Require-Command($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    throw "Missing required command: $name. Install Git and GitHub CLI first."
  }
}

Require-Command git
Require-Command gh

if (-not (Test-Path (Join-Path $source 'docs\index.html'))) {
  throw 'Missing generated website in docs.'
}
if ((Get-ChildItem (Join-Path $source 'docs\assets\img') -File -Filter '*.webp' | Measure-Object).Count -ne 28) {
  throw 'Expected 28 photographs in docs/assets/img.'
}

$temp = Join-Path ([IO.Path]::GetTempPath()) ('kinetone-publish-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $temp | Out-Null

function Invoke-GhSafe([string[]]$Arguments) {
  # PowerShell 5.1 treats redirected native stderr as an error.
  # Capturing it through Start-Process avoids aborting on an expected 404.
  $outFile = Join-Path $temp 'gh-stdout.txt'
  $errFile = Join-Path $temp 'gh-stderr.txt'
  $proc = Start-Process -FilePath (Get-Command gh).Source `
    -ArgumentList $Arguments -NoNewWindow -Wait -PassThru `
    -RedirectStandardOutput $outFile -RedirectStandardError $errFile
  return @{
    Code = $proc.ExitCode
    Output = [IO.File]::ReadAllText($outFile)
    Error = [IO.File]::ReadAllText($errFile)
  }
}

try {
  $auth = Invoke-GhSafe -Arguments @('auth', 'status')
  if ($auth.Code -ne 0) { throw 'Please run gh auth login first.' }

  $clone = Join-Path $temp 'KINETONE'
  & git clone "https://github.com/$repo.git" $clone
  if ($LASTEXITCODE -ne 0) { throw 'Git clone failed.' }

  Push-Location $clone
  try {
    & git checkout -B main
    if ($LASTEXITCODE -ne 0) { throw 'Cannot select main branch.' }

    # A fresh repository has no HEAD commit. show-ref returns 1 without
    # writing a fatal error to stderr, so this works on Windows PowerShell.
    & git show-ref --verify --quiet refs/heads/main
    if ($LASTEXITCODE -ne 0) {
      Set-Content -Path README.md -Value '# KINETONE' -Encoding UTF8
      & git add README.md
      & git -c user.name=pfxamd -c user.email=pfxamd@users.noreply.github.com `
        commit -m 'Initialize KINETONE repository'
      if ($LASTEXITCODE -ne 0) { throw 'Repository initialization failed.' }
      & git push -u origin main
      if ($LASTEXITCODE -ne 0) { throw 'Repository initialization push failed.' }
    }

    # Configure GitHub Pages before pushing the website workflow so that
    # the first production push can deploy immediately.
    $pages = Invoke-GhSafe -Arguments @('api', "repos/$repo/pages")
    if ($pages.Code -ne 0) {
      $create = Invoke-GhSafe -Arguments @('api', '-X', 'POST', "repos/$repo/pages", '-f', 'build_type=workflow')
      if ($create.Code -ne 0) {
        throw ("GitHub Pages setup failed: " + $create.Error.Trim())
      }
      Write-Host 'GitHub Pages enabled for Actions deployment.' -ForegroundColor Green
    }
    else {
      $pagesData = $pages.Output | ConvertFrom-Json
      if ($pagesData.build_type -ne 'workflow') {
        $update = Invoke-GhSafe -Arguments @('api', '-X', 'PUT', "repos/$repo/pages", '-f', 'build_type=workflow')
        if ($update.Code -ne 0) {
          throw ("GitHub Pages configuration failed: " + $update.Error.Trim())
        }
      }
    }

    $items = @(
      'docs', 'assets', 'tools', '.github', 'README.md', '.gitignore',
      'publish-pages.ps1', 'publish-pages.bat', 'publish-pages.sh'
    )
    foreach ($item in $items) {
      $original = Join-Path $source $item
      if (Test-Path $original) {
        $dest = Join-Path $clone $item
        if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
        Copy-Item -Path $original -Destination $dest -Recurse -Force
      }
    }

    & git add -A
    if ($LASTEXITCODE -ne 0) { throw 'Git add failed.' }
    & git diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
      & git -c user.name=pfxamd -c user.email=pfxamd@users.noreply.github.com `
        commit -m 'Launch complete KINETONE interactive website'
      if ($LASTEXITCODE -ne 0) { throw 'Website commit failed.' }
    }
    & git push -u origin main
    if ($LASTEXITCODE -ne 0) { throw 'Website push failed.' }

    Write-Host 'KINETONE uploaded. GitHub Pages deployment started.' -ForegroundColor Green
    Write-Host "Deployment status: https://github.com/$repo/actions"
    Write-Host 'Website: https://pfxamd.github.io/KINETONE/'
  }
  finally { Pop-Location }
}
finally {
  Remove-Item -Recurse -Force $temp -ErrorAction SilentlyContinue
}
