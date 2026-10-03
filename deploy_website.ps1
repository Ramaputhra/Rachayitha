# PowerShell deployment script for Rachayitha
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Deploying Rachayitha Website to GitHub & Vercel" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

Set-Location $PSScriptRoot

Write-Host "`n[1/4] Ensuring Rachayitha_Setup_V2.exe and Rachayitha_v2.exe binaries are synced..." -ForegroundColor Yellow
$setupV2Src = "$PSScriptRoot\rachayitha code files\installer_output\Rachayitha_Setup_V2.exe"
if (Test-Path $setupV2Src) {
    Copy-Item $setupV2Src "$PSScriptRoot\Rachayitha_Setup_V2.exe" -Force -ErrorAction SilentlyContinue
    Copy-Item $setupV2Src "$PSScriptRoot\Rachayitha_Setup.exe" -Force -ErrorAction SilentlyContinue
    Copy-Item $setupV2Src "$PSScriptRoot\WebSite\Rachayitha_Setup_V2.exe" -Force -ErrorAction SilentlyContinue
    Copy-Item $setupV2Src "$PSScriptRoot\WebSite\Rachayitha_Setup.exe" -Force -ErrorAction SilentlyContinue
}
Copy-Item "$PSScriptRoot\Rachayitha.exe" "$PSScriptRoot\Rachayitha_v2.exe" -Force -ErrorAction SilentlyContinue
Copy-Item "$PSScriptRoot\Rachayitha.exe" "$PSScriptRoot\WebSite\Rachayitha_v2.exe" -Force -ErrorAction SilentlyContinue

Write-Host "`n[2/4] Staging changes..." -ForegroundColor Yellow
git add -A

Write-Host "`n[3/4] Committing changes..." -ForegroundColor Yellow
git commit -m "feat(v2.0): update official release links to Rachayitha_Setup_V2.exe and clean website CTA"

Write-Host "`n[4/4] Pushing to GitHub (main branch)..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n========================================================" -ForegroundColor Green
    Write-Host "  [SUCCESS] Pushed to GitHub successfully!" -ForegroundColor Green
    Write-Host "  Vercel is now automatically deploying your website." -ForegroundColor Green
    Write-Host "========================================================" -ForegroundColor Green
} else {
    Write-Host "`n[ERROR] Push failed. Please check git credentials." -ForegroundColor Red
}
