# PowerShell deployment script for Rachayitha
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Deploying Rachayitha Website to GitHub & Vercel" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

Set-Location $PSScriptRoot

Write-Host "`n[1/3] Staging changes..." -ForegroundColor Yellow
git add WebSite/ All.md deploy_website.bat deploy_website.ps1

Write-Host "`n[2/3] Committing changes..." -ForegroundColor Yellow
git commit -m "fix(vercel): configure outputDirectory and disable buildCommand for static site"

Write-Host "`n[3/3] Pushing to GitHub (main branch)..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n========================================================" -ForegroundColor Green
    Write-Host "  [SUCCESS] Pushed to GitHub successfully!" -ForegroundColor Green
    Write-Host "  Vercel is now automatically deploying your website." -ForegroundColor Green
    Write-Host "========================================================" -ForegroundColor Green
} else {
    Write-Host "`n[ERROR] Push failed. Please check git credentials." -ForegroundColor Red
}
