@echo off
REM Git 版控操作
cd /d D:\dev\backup

echo ============================================================
echo Git 版控操作
echo ============================================================
echo.

echo [1] 檢查狀態
git status --short
echo.

echo [2] 暫存所有變更
git add .
echo 已暫存
echo.

echo [3] 提交
git commit -m "refactor: 簡化環境設定 - 回歸手動 Conda 方案

- 更新 SETUP_GUIDE_v2.md 為簡化版
- 移除自動環境偵測邏輯
- 採用明確的手動 Conda 方案
- 5 個清楚的逐步設定說明
- 支援在 Copilot CLI 中自然語言進行 Git 操作"

echo.
echo [4] 查看最新提交
git log --oneline -1
echo.

echo ============================================================
echo ✅ Git 提交完成！
echo ============================================================
pause
