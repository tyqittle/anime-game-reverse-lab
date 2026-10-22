# Usage: create an empty GitHub repository first, then:
# powershell -ExecutionPolicy Bypass -File scripts\publish-to-github.ps1 -RepositoryUrl https://github.com/USER/anime-game-reverse-lab.git
param([Parameter(Mandatory=$true)][string]$RepositoryUrl)
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "需要先安装 Git for Windows" }
if (-not (Test-Path .git)) { git init -b main; if ($LASTEXITCODE -ne 0) { throw "git init failed" } }
$remotes = @(git remote)
if ($remotes -contains "origin") {
  $origin = git remote get-url origin
  if ($origin.Trim() -ne $RepositoryUrl.Trim()) { throw "已有其他 origin，拒绝覆盖；请手动检查 git remote -v" }
} else { git remote add origin $RepositoryUrl }
git add README.md CHANGELOG.md CONTRIBUTING.md LICENSE .gitignore pyproject.toml src tests docs games scripts examples .github
if ($LASTEXITCODE -ne 0) { throw "git add failed" }
Write-Host "请检查即将提交的文件："
git diff --cached --stat
git diff --cached --quiet
$diffStatus = $LASTEXITCODE
if ($diffStatus -gt 1) { throw "git diff failed" }
if ($diffStatus -eq 1) {
  git commit -m "Initialize anime game reverse research lab"
  if ($LASTEXITCODE -ne 0) { throw "commit failed" }
}
git branch -M main
# Do not force push or rewrite any existing remote history.
git push -u origin main
if ($LASTEXITCODE -ne 0) { throw "push failed；请检查 GitHub 登录状态及远程仓库是否为空" }
Write-Host "代码已推送至 $RepositoryUrl"
