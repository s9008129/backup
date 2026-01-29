@echo off
REM Conda PATH 修復腳本 - 簡單版
REM ================================================================

setlocal enabledelayedexpansion

echo.
echo ================================================================
echo Conda PATH 修復工具
echo ================================================================
echo.

REM 設定 Miniconda 路徑
set MINICONDA_PATH=%USERPROFILE%\Miniconda3

echo [1/3] 檢查 Miniconda 安裝...
if exist "%MINICONDA_PATH%\_conda.exe" (
    echo ✓ 找到 Miniconda: %MINICONDA_PATH%
) else (
    echo ✗ 未找到 Miniconda
    exit /b 1
)

echo.
echo [2/3] 嘗試初始化 Conda...
REM 使用 _conda.exe 執行 init
"%MINICONDA_PATH%\_conda.exe" init cmd.exe

echo.
echo [3/3] 建立虛擬環境...
REM 啟動 conda
call "%MINICONDA_PATH%\Scripts\activate.bat" base

REM 建立 backup 環境
"%MINICONDA_PATH%\_conda.exe" create -n backup python=3.11 -y

echo.
echo ================================================================
echo ✓ 修復完成！
echo ================================================================
echo.
echo 下一步:
echo   1. 關閉並重新打開 PowerShell
echo   2. 執行: conda env list
echo   3. 執行: conda activate backup
echo.
pause
