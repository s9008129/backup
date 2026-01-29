@echo off
REM 自動化開發環境設定腳本 (Windows Batch)
REM 功能: 建立 Conda 環境、安裝套件、配置 Git

setlocal enabledelayedexpansion
chcp 65001 >nul

echo ================================================
echo 開發環境自動化設定腳本
echo ================================================
echo.

REM ===== 步驟 1: 檢查 Conda 是否已安裝 =====
echo [步驟 1] 檢查 Conda 安裝...
call conda --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: Conda 未安裝或未在 PATH 中
    echo 請先安裝 Miniconda 或 Anaconda
    echo 下載: https://docs.conda.io/projects/miniconda/en/latest/
    goto error_exit
)
for /f "tokens=*" %%i in ('conda --version') do set CONDA_VERSION=%%i
echo ✅ 已安裝: %CONDA_VERSION%
echo.

REM ===== 步驟 2: 檢查 Git 是否已安裝 =====
echo [步驟 2] 檢查 Git 安裝...
call git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: Git 未安裝或未在 PATH 中
    echo 請先安裝 Git: https://git-scm.com/download/win
    goto error_exit
)
for /f "tokens=*" %%i in ('git --version') do set GIT_VERSION=%%i
echo ✅ 已安裝: %GIT_VERSION%
echo.

REM ===== 步驟 3: 檢查 Python 是否已安裝 =====
echo [步驟 3] 檢查 Python 安裝...
call python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: Python 未安裝或未在 PATH 中
    goto error_exit
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ 已安裝: %PYTHON_VERSION%
echo.

REM ===== 步驟 4: 建立/激活 Conda 環境 =====
echo [步驟 4] 建立 Conda 環境 'backup'...
call conda env list | find "backup" >nul 2>&1
if errorlevel 1 (
    echo 建立新環境...
    call conda create -n backup python=3.11 -y
    if errorlevel 1 (
        echo ❌ 錯誤: 建立 Conda 環境失敗
        goto error_exit
    )
    echo ✅ 環境已建立
) else (
    echo ✅ 環境已存在
)
echo.

REM ===== 步驟 5: 激活環境並安裝必要套件 =====
echo [步驟 5] 激活環境並安裝套件...
call conda run -n backup python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️ 警告: 升級 pip 出現問題，繼續...
)

echo 安裝主要套件: tkinter, python-dateutil...
call conda run -n backup python -m pip install python-dateutil
echo.

REM ===== 步驟 6: 驗證環境 =====
echo [步驟 6] 驗證環境...
echo.
echo 環境中已安裝的套件:
call conda run -n backup python -m pip list | find "pip"
echo.

REM ===== 步驟 7: 初始化 Git 倉庫 =====
echo [步驟 7] 初始化 Git 倉庫...
cd /d D:\dev\backup
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo 初始化新的 Git 倉庫...
    call git init
    call git config user.email "backup-tool@local"
    call git config user.name "Backup Tool Dev"
    echo ✅ Git 倉庫已初始化
) else (
    echo ✅ Git 倉庫已存在
)
echo.

echo ================================================
echo ✅ 環境設定完成！
echo ================================================
echo.
echo 使用環境:
echo   激活: conda activate backup
echo   執行: python backup_tool.py
echo   提交: git add . && git commit -m "message"
echo.
goto success_exit

:error_exit
echo.
echo ================================================
echo ❌ 設定失敗
echo ================================================
exit /b 1

:success_exit
exit /b 0
