# 完整自動化設定腳本 - 中文支援版
# =========================================================================
# 功能: 
#   1. 檢查並安裝 Git
#   2. 檢查並安裝 Conda (Miniconda)
#   3. 建立虛擬環境 (backup)
#   4. 安裝依賴套件
# =========================================================================

# 設定編碼為 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         簡易備份工具 - 完整自動化環境設定 v4.0              ║" -ForegroundColor Cyan
Write-Host "║            Complete Automated Setup (中文支援)               ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 建立日誌
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logPath = "$PSScriptRoot\setup_log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

function Log-Message {
    param([string]$message, [string]$color = "White")
    Write-Host $message -ForegroundColor $color
    Add-Content -Path $logPath -Value "[$timestamp] $message" -Encoding UTF8
}

Log-Message "════════════════════════════════════════════════════════════════" "Cyan"
Log-Message "設定日誌已建立: $logPath" "Yellow"
Log-Message "════════════════════════════════════════════════════════════════" "Cyan"
Write-Host ""

# 函數: 檢查命令是否存在
function Test-Command {
    param([string]$cmd)
    try {
        if (Get-Command $cmd -ErrorAction Stop) {
            return $true
        }
    } catch {
        return $false
    }
}

# =========================================================================
# 步驟 1: 檢查/安裝 Git
# =========================================================================
Write-Host "[1/4] Git 環境" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray

if (Test-Command git) {
    $gitVersion = git --version
    Write-Host "✅ Git 已安裝: $gitVersion" -ForegroundColor Green
    Log-Message "✅ Git 已安裝: $gitVersion"
} else {
    Write-Host "❌ Git 未安裝" -ForegroundColor Red
    Log-Message "❌ Git 未安裝"
    Write-Host ""
    Write-Host "📝 安裝 Git 的選項:" -ForegroundColor Cyan
    Write-Host "   方式 1: 下載安裝器" -ForegroundColor Yellow
    Write-Host "          https://git-scm.com/download/win" -ForegroundColor Blue
    Write-Host ""
    Write-Host "   方式 2: 使用 Chocolatey (如已安裝)" -ForegroundColor Yellow
    Write-Host "          choco install git -y" -ForegroundColor Blue
    Write-Host ""
    Write-Host "   方式 3: 使用 Windows Package Manager" -ForegroundColor Yellow
    Write-Host "          winget install Git.Git" -ForegroundColor Blue
    Write-Host ""
    Write-Host "⏳ 請先安裝 Git，然後重新執行此腳本" -ForegroundColor Yellow
    Log-Message "⚠️  請使用者手動安裝 Git"
    exit
}

Write-Host ""

# =========================================================================
# 步驟 2: 檢查/安裝 Conda
# =========================================================================
Write-Host "[2/4] Conda 環境" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray

if (Test-Command conda) {
    $condaVersion = conda --version
    Write-Host "✅ Conda 已安裝: $condaVersion" -ForegroundColor Green
    Log-Message "✅ Conda 已安裝: $condaVersion"
} else {
    Write-Host "❌ Conda 未安裝" -ForegroundColor Red
    Log-Message "❌ Conda 未安裝"
    Write-Host ""
    Write-Host "📝 自動下載並安裝 Miniconda..." -ForegroundColor Cyan
    
    $minicondaUrl = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
    $minicondaInstaller = "$env:TEMP\Miniconda3-latest-Windows-x86_64.exe"
    
    try {
        Write-Host "⬇️  正在下載 Miniconda..." -ForegroundColor Yellow
        Log-Message "⬇️  正在下載 Miniconda from $minicondaUrl"
        
        # 使用 ProgressPreference 隱藏進度條避免編碼問題
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $minicondaUrl -OutFile $minicondaInstaller -TimeoutSec 300
        
        Write-Host "✅ 下載完成" -ForegroundColor Green
        Log-Message "✅ Miniconda 下載完成"
        
        Write-Host "⚙️  正在安裝 Miniconda..." -ForegroundColor Yellow
        Log-Message "⚙️  正在安裝 Miniconda..."
        
        # 無聲安裝 Miniconda
        & $minicondaInstaller /InstallationType=JustMe /RegisterPython=0 /S /D="$env:USERPROFILE\Miniconda3" | Out-Null
        
        Write-Host "✅ Miniconda 安裝完成" -ForegroundColor Green
        Log-Message "✅ Miniconda 安裝完成"
        
        # 重新整理 PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        
        # 驗證 Conda
        if (Test-Command conda) {
            $condaVersion = conda --version
            Write-Host "✅ Conda 驗證成功: $condaVersion" -ForegroundColor Green
            Log-Message "✅ Conda 驗證成功: $condaVersion"
        } else {
            Write-Host "⚠️  Conda 安裝後仍無法找到，請手動重啟 PowerShell" -ForegroundColor Yellow
            Log-Message "⚠️  需要手動重啟 PowerShell"
        }
    } catch {
        Write-Host "❌ 安裝失敗: $_" -ForegroundColor Red
        Log-Message "❌ Miniconda 安裝失敗: $_"
        exit
    }
}

Write-Host ""

# =========================================================================
# 步驟 3: 建立虛擬環境
# =========================================================================
Write-Host "[3/4] 虛擬環境設定" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray

$envName = "backup"
Write-Host "📦 環境名稱: $envName" -ForegroundColor Cyan

# 檢查環境是否存在
$envExists = conda env list | Select-String $envName
if ($envExists) {
    Write-Host "✅ 虛擬環境已存在: $envName" -ForegroundColor Green
    Log-Message "✅ 虛擬環境已存在: $envName"
} else {
    Write-Host "🔨 建立虛擬環境: $envName (Python 3.11)..." -ForegroundColor Yellow
    Log-Message "🔨 建立虛擬環境: $envName"
    
    try {
        conda create -n $envName python=3.11 -y 2>&1 | Tee-Object -FilePath $logPath -Append
        Write-Host "✅ 虛擬環境建立成功" -ForegroundColor Green
        Log-Message "✅ 虛擬環境建立成功"
    } catch {
        Write-Host "❌ 虛擬環境建立失敗: $_" -ForegroundColor Red
        Log-Message "❌ 虛擬環境建立失敗: $_"
        exit
    }
}

Write-Host ""

# =========================================================================
# 步驟 4: 安裝依賴套件
# =========================================================================
Write-Host "[4/4] 安裝依賴套件" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray

$projectPath = $PSScriptRoot
$reqFile = "$projectPath\requirements.txt"

if (Test-Path $reqFile) {
    Write-Host "📋 需求檔案: $reqFile" -ForegroundColor Cyan
    Write-Host "🔨 正在安裝依賴套件..." -ForegroundColor Yellow
    Log-Message "🔨 正在安裝依賴套件 from $reqFile"
    
    try {
        # 啟動環境並安裝
        & conda run -n $envName pip install -r $reqFile -q 2>&1 | Tee-Object -FilePath $logPath -Append
        Write-Host "✅ 依賴套件安裝完成" -ForegroundColor Green
        Log-Message "✅ 依賴套件安裝完成"
    } catch {
        Write-Host "⚠️  安裝時出現警告或錯誤: $_" -ForegroundColor Yellow
        Log-Message "⚠️  安裝警告: $_"
    }
} else {
    Write-Host "⚠️  需求檔案不存在: $reqFile" -ForegroundColor Yellow
    Log-Message "⚠️  需求檔案不存在"
}

Write-Host ""

# =========================================================================
# 驗證完整性
# =========================================================================
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    ✅ 環境設定完成！                          ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "📊 環境驗證摘要:" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "  ✅ Git:      $(if (Test-Command git) { '已安裝' } else { '未安裝' })" -ForegroundColor $(if (Test-Command git) { 'Green' } else { 'Red' })
Write-Host "  ✅ Conda:    $(if (Test-Command conda) { '已安裝' } else { '未安裝' })" -ForegroundColor $(if (Test-Command conda) { 'Green' } else { 'Red' })
Write-Host "  ✅ 環境:     $envName" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

Write-Host "🚀 立即開始:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  # 啟動虛擬環境" -ForegroundColor Cyan
Write-Host "  conda activate backup" -ForegroundColor Blue
Write-Host ""
Write-Host "  # 運行應用程序" -ForegroundColor Cyan
Write-Host "  python backup_tool.py" -ForegroundColor Blue
Write-Host ""
Write-Host "  # 執行測試" -ForegroundColor Cyan
Write-Host "  python test_backup.py" -ForegroundColor Blue
Write-Host ""

Write-Host "📝 設定日誌已保存: $logPath" -ForegroundColor Gray
Write-Host ""
Log-Message "════════════════════════════════════════════════════════════════"
Log-Message "✅ 環境設定完成"
Log-Message "════════════════════════════════════════════════════════════════"
