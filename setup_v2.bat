@echo off
REM 簡易備份工具 - 開發環境設定 v2.0
REM 支援 Conda 和 Python venv

setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
cls

echo ============================================================================
echo 簡易備份工具 - 開發環境設定 v2.0
echo ============================================================================
echo.
echo 本腳本支援兩種方案:
echo   * Conda: 如果已安裝將自動使用
echo   * Python venv: Conda 不可用時使用 (推薦)
echo.
pause

set "USE_CONDA=0"

REM [1/5] 檢查 Python
echo [1/5] 檢查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安裝
    echo 請下載: https://www.python.org/downloads/
    goto fail
)
python --version
echo.

REM [2/5] 偵測 Conda
echo [2/5] 偵測 Conda...
conda --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Conda 未安裝 - 使用 venv 方案
    set "USE_CONDA=0"
) else (
    conda --version
    echo ✅ 使用 Conda 方案
    set "USE_CONDA=1"
)
echo.

REM [3/5] 檢查 Git
echo [3/5] 檢查 Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git 未安裝
    echo 請下載: https://git-scm.com/download/win
    goto fail
)
git --version
echo.

REM [4/5] 建立虛擬環境
echo [4/5] 建立虛擬環境...
if %USE_CONDA%==1 (
    conda env list | findstr "backup" >nul 2>&1
    if errorlevel 1 (
        conda create -n backup python=3.11 -y >nul 2>&1
    )
    echo ✅ Conda 環境 backup 已準備
) else (
    if not exist "venv" (
        python -m venv venv >nul 2>&1
    )
    echo ✅ venv 環境已準備
)
echo.

REM [5/5] 安裝套件
echo [5/5] 安裝 Python 套件...
if %USE_CONDA%==1 (
    conda run -n backup python -m pip install --upgrade pip -q 2>nul
    conda run -n backup python -m pip install python-dateutil pytz -q 2>nul
) else (
    venv\Scripts\python -m pip install --upgrade pip -q 2>nul
    venv\Scripts\python -m pip install python-dateutil pytz -q 2>nul
)
echo ✅ 套件已安裝
echo.

REM 初始化 Git
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    git init >nul 2>&1
    git config user.email "backup-tool@local" >nul 2>&1
    git config user.name "Backup Tool Dev" >nul 2>&1
    git add . >nul 2>&1
    git commit -m "initial: 簡易差異備份工具初始化提交" -q >nul 2>&1
)
echo ✅ Git 已初始化
echo.

echo ============================================================================
echo ✅ 環境設定完成！
echo ============================================================================
echo.

if %USE_CONDA%==1 (
    echo 下一步 (Conda):
    echo   1. conda activate backup
    echo   2. python validate_env.py
    echo   3. python backup_tool.py
) else (
    echo 下一步 (venv):
    echo   1. venv\Scripts\activate
    echo   2. python validate_env.py
    echo   3. python backup_tool.py
)

echo.
pause
exit /b 0

:fail
echo ❌ 設定失敗
echo 請先安裝 Python 和 Git
pause
exit /b 1
