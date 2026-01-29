# Conda PATH 診斷和修復腳本

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         Conda PATH 診斷和修復工具 - 中文完美支援             ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# =========================================================================
# 步驟 1: 診斷 - 檢查 Miniconda 安裝位置
# =========================================================================
Write-Host "[1/5] 診斷 Miniconda 安裝位置" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray

$possiblePaths = @(
    "$env:USERPROFILE\Miniconda3",
    "$env:USERPROFILE\Anaconda3",
    "$env:PROGRAMFILES\Miniconda3",
    "$env:PROGRAMFILES\Anaconda3",
    "C:\Miniconda3",
    "C:\Anaconda3"
)

$condaPath = $null
foreach ($path in $possiblePaths) {
    if (Test-Path "$path\Scripts\conda.exe") {
        $condaPath = $path
        Write-Host "✅ 找到 Miniconda/Anaconda 安裝位置:" -ForegroundColor Green
        Write-Host "   $condaPath" -ForegroundColor Blue
        break
    }
}

if (-not $condaPath) {
    Write-Host "❌ 未找到 Miniconda/Anaconda 安裝位置" -ForegroundColor Red
    Write-Host "檢查過的路徑:" -ForegroundColor Yellow
    foreach ($path in $possiblePaths) {
        Write-Host "   ❌ $path" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "請確認:" -ForegroundColor Yellow
    Write-Host "  1. Miniconda 已安裝" -ForegroundColor Gray
    Write-Host "  2. 安裝路徑正確" -ForegroundColor Gray
    Write-Host "  3. 運行此腳本時有管理員權限" -ForegroundColor Gray
    exit
}

Write-Host ""

# =========================================================================
# 步驟 2: 檢查 PATH 環境變數
# =========================================================================
Write-Host "[2/5] 檢查 PATH 環境變數" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray

$currentPath = $env:Path
$condaInPath = $currentPath -match [regex]::Escape("$condaPath")

if ($condaInPath) {
    Write-Host "✅ Conda 路徑已在 PATH 中" -ForegroundColor Green
} else {
    Write-Host "❌ Conda 路徑不在 PATH 中 (需要修復)" -ForegroundColor Red
    Write-Host "   將添加: $condaPath\Scripts" -ForegroundColor Yellow
}

Write-Host ""

# =========================================================================
# 步驟 3: 添加到 PATH (臨時)
# =========================================================================
Write-Host "[3/5] 更新 PATH 環境變數" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray

# 臨時添加到當前 Session
$condaScriptsPath = "$condaPath\Scripts"
$condaBinPath = "$condaPath\Library\mingw-w64\bin"

if ($env:Path -notlike "*$condaScriptsPath*") {
    $env:Path = "$condaScriptsPath;$condaBinPath;$env:Path"
    Write-Host "✅ 已臨時更新 PATH (當前 Session)" -ForegroundColor Green
} else {
    Write-Host "✅ PATH 已包含 Conda 路徑" -ForegroundColor Green
}

Write-Host ""

# =========================================================================
# 步驟 4: 驗證 conda 命令
# =========================================================================
Write-Host "[4/5] 驗證 conda 命令" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray

try {
    $condaVersion = conda --version
    Write-Host "✅ Conda 命令可用: $condaVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Conda 命令仍不可用: $_" -ForegroundColor Red
    exit
}

Write-Host ""

# =========================================================================
# 步驟 5: 初始化 PowerShell for Conda
# =========================================================================
Write-Host "[5/5] 初始化 PowerShell for Conda" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray

try {
    Write-Host "正在執行: conda init powershell" -ForegroundColor Cyan
    conda init powershell 2>&1 | Out-Null
    Write-Host "✅ Conda 已初始化 PowerShell" -ForegroundColor Green
    Write-Host "   (需要重啟 PowerShell 才能完全生效)" -ForegroundColor Yellow
} catch {
    Write-Host "⚠️  初始化時出現警告: $_" -ForegroundColor Yellow
}

Write-Host ""

# =========================================================================
# 完成
# =========================================================================
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                  ✅ 診斷和修復完成！                          ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "📝 摘要:" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "  ✅ Miniconda 位置: $condaPath" -ForegroundColor Green
Write-Host "  ✅ PATH 已更新 (當前 Session)" -ForegroundColor Green
Write-Host "  ✅ Conda 版本: $condaVersion" -ForegroundColor Green
Write-Host "  ✅ PowerShell 已初始化" -ForegroundColor Green
Write-Host ""

Write-Host "🔄 下一步:" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "  1. 重啟 PowerShell (關閉並重新打開)" -ForegroundColor Blue
Write-Host "  2. 驗證 conda: conda --version" -ForegroundColor Blue
Write-Host "  3. 建立環境: conda create -n backup python=3.11 -y" -ForegroundColor Blue
Write-Host ""

Write-Host "💡 現在測試 (當前 Session):" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "  conda env list" -ForegroundColor Blue
Write-Host ""

# 立即顯示環境清單
Write-Host "📊 現有 Conda 環境:" -ForegroundColor Cyan
conda env list

Write-Host ""
Write-Host "✨ 修復完成！重啟 PowerShell 後所有命令將永久生效。" -ForegroundColor Green
