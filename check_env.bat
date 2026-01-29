@echo off
REM 簡化版環境初始化腳本
chcp 65001 >nul

cd /d D:\dev\backup

echo.
echo ================================================
echo 簡易備份工具 - 開發環境檢查
echo ================================================
echo.

REM 檢查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: Python 未安裝
    echo 請安裝 Python 3.11+
    goto end
)

echo ✅ Python 已安裝
python --version

echo.
echo ================================================
echo 環境檢查詳細信息
echo ================================================
echo.

python check_env.py

:end
pause
