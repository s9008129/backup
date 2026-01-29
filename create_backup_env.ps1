param([switch]$InitOnly = $false)

# Conda 環境修復和初始化腳本 - PowerShell 版

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

$minicondaPath = "C:\Users\ca0283\Miniconda3"
$condaExe = "$minicondaPath\_conda.exe"

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Conda 修復和環境建立工具" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# 步驟 1: 驗證 Miniconda
Write-Host "[1/4] 驗證 Miniconda 安裝" -ForegroundColor Yellow
if (-not (Test-Path $condaExe)) {
    Write-Host "錯誤: 未找到 $condaExe" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Miniconda 已安裝: $minicondaPath" -ForegroundColor Green
Write-Host ""

# 步驟 2: 驗證 conda 版本
Write-Host "[2/4] 檢查 Conda 版本" -ForegroundColor Yellow
$condaVersion = & $condaExe --version
Write-Host "✓ $condaVersion" -ForegroundColor Green
Write-Host ""

# 步驟 3: 初始化 PowerShell
Write-Host "[3/4] 初始化 PowerShell for Conda" -ForegroundColor Yellow
Write-Host "執行: conda init powershell" -ForegroundColor Cyan

try {
    & $condaExe init powershell 2>&1 | Out-Null
    Write-Host "✓ PowerShell 初始化完成" -ForegroundColor Green
    Write-Host "  (需要重啟 PowerShell 完全生效)" -ForegroundColor Yellow
} catch {
    Write-Host "警告: $_" -ForegroundColor Yellow
}
Write-Host ""

# 步驟 4: 建立 backup 虛擬環境
Write-Host "[4/4] 建立虛擬環境 'backup'" -ForegroundColor Yellow
Write-Host "執行: conda create -n backup python=3.11 -y" -ForegroundColor Cyan
Write-Host ""

try {
    & $condaExe create -n backup python=3.11 -y
    Write-Host ""
    Write-Host "✓ 虛擬環境建立完成" -ForegroundColor Green
} catch {
    Write-Host "錯誤: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "✓ 所有操作完成！" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""

# 列出現有環境
Write-Host "現有 Conda 環境:" -ForegroundColor Cyan
& $condaExe env list
Write-Host ""

Write-Host "下一步:" -ForegroundColor Yellow
Write-Host "  1. 重啟 PowerShell (重要!)" -ForegroundColor Blue
Write-Host "  2. 驗證: conda env list" -ForegroundColor Blue
Write-Host "  3. 啟動: conda activate backup" -ForegroundColor Blue
Write-Host ""
