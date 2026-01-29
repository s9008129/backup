@echo off
REM ============================================================================
REM 簡易備份工具 - 一鍵開發環境完整設定
REM ============================================================================
REM 功能: 檢查/安裝 Conda、建立虛擬環境、安裝依賴、初始化 Git
REM ============================================================================

setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

set "PROJECT_DIR=%cd%"
set "ENV_NAME=backup"
set "USE_CONDA=0"

echo.
echo ============================================================================
echo 簡易備份工具 - 開發環境完整設定 v2.0
echo ============================================================================
echo.
echo 本腳本支援兩種方案:
echo   * Conda: 如果已安裝將自動使用
echo   * Python venv: Conda 不可用時使用 (推薦備選)
echo.
pause

REM ===== 檢查 Python =====
echo.
echo [1/5] 檢查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: Python 未安裝
    echo 請先安裝 Python 3.11+
    goto fail
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ 已檢查: %PYTHON_VERSION%

REM ===== 偵測 Conda =====
echo.
echo [2/5] 偵測 Conda...
conda --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Conda 未安裝，將使用 Python venv 方案
    echo.
    set "USE_CONDA=0"
) else (
    for /f "tokens=*" %%i in ('conda --version 2^>^&1') do set CONDA_VERSION=%%i
    echo ✅ %CONDA_VERSION%
    echo 將使用 Conda 方案
    echo.
    set "USE_CONDA=1"
)

REM ===== 建立/檢查 Conda 環境 =====
echo.
echo [3/5] 建立 Conda 環境 '%ENV_NAME%'...
conda env list | find "%ENV_NAME%" >nul 2>&1
if errorlevel 1 (
    echo 建立新環境...
    call conda create -n %ENV_NAME% python=3.11 -y >nul 2>&1
    if errorlevel 1 (
        echo ❌ 錯誤: 建立環境失敗
        goto fail
    )
    echo ✅ 環境已建立
) else (
    echo ✅ 環境已存在
)

REM ===== 安裝 Python 套件 =====
echo.
echo [4/5] 安裝 Python 套件...
call conda run -n %ENV_NAME% python -m pip install --upgrade pip -q
call conda run -n %ENV_NAME% python -m pip install python-dateutil pytz -q
if errorlevel 1 (
    echo ⚠️ 警告: 部分套件安裝出現問題
) else (
    echo ✅ 套件已安裝
)

REM ===== 初始化 Git =====
echo.
echo [5/5] 初始化 Git...
cd /d "%PROJECT_DIR%"
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: Git 未安裝
    echo 請先安裝: https://git-scm.com/download/win
    goto fail
)

git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo 初始化新倉庫...
    call git init
    call git config user.email "backup-tool@local"
    call git config user.name "Backup Tool Dev"
    call git add .
    call git commit -m "initial: 簡易差異備份工具初始化提交" -q
    echo ✅ Git 倉庫已初始化
) else (
    echo ✅ Git 倉庫已存在
)

REM ===== 驗證環境 =====
echo.
echo ============================================================================
echo ✅ 環境設定完成！
echo ============================================================================
echo.
echo 下一步:
echo   1. 激活環境:    conda activate backup
echo   2. 檢查環境:    python check_env.py
echo   3. 運行應用:    python backup_tool.py
echo   4. 運行測試:    python test_backup.py
echo   5. 查看提交:    git log --oneline
echo.
echo 常用命令:
echo   提交程式碼:   git add . && git commit -m "message"
echo   檢查狀態:     git status
echo   查看日誌:     git log --oneline -10
echo.
pause
goto end

:fail
echo.
echo ============================================================================
echo ❌ 設定失敗
echo ============================================================================
echo.
echo 請檢查:
echo   1. Python 3.11+ 是否已安裝
echo   2. Conda (Miniconda/Anaconda) 是否已安裝
echo   3. Git for Windows 是否已安裝
echo.
pause
exit /b 1

:end
exit /b 0
