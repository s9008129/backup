@echo off
REM 環境修復提交腳本
chcp 65001 >nul 2>&1
cd /d D:\dev\backup
python commit_fix.py
pause
