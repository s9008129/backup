@echo off
REM Git 初始化與首次提交腳本
chcp 65001 >nul

cd /d D:\dev\backup

echo.
echo ================================================
echo 簡易備份工具 - Git 初始化
echo ================================================
echo.

REM 檢查 git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: Git 未安裝或未在 PATH
    echo 請安裝: https://git-scm.com/download/win
    goto error
)

echo ✅ Git 已安裝
git --version
echo.

REM 檢查是否已初始化
git rev-parse --git-dir >nul 2>&1
if not errorlevel 1 (
    echo ✅ Git 倉庫已初始化
    echo.
    echo 現有提交:
    git log --oneline | head -5
    goto end
)

echo 初始化新的 Git 倉庫...
git init

echo.
echo 配置 Git 使用者信息...
git config user.email "backup-tool@local"
git config user.name "Backup Tool Dev"

echo.
echo 新增所有檔案到暫存區...
git add .

echo.
echo 創建首次提交...
git commit -m "feat: 簡易差異備份工具初始化提交

核心功能:
- 手動差異備份（一鍵開始）
- 自動檔案變化偵測
- 簡易檔案恢復嚮導
- 備份歷史日誌記錄
- 1年自動保留政策

環境配置:
- Python 3.11 環境（conda）
- tkinter GUI 框架
- 完整的測試套件

文檔:
- spec.md: 完整規格文檔
- README.md: 開發指南
- 元資料管理: .backup_manifest

所有功能都已實現並準備進行測試。"

echo.
echo ================================================
echo ✅ Git 初始化完成！
echo ================================================
echo.
git log -1 --stat

goto end

:error
echo.
echo ❌ 初始化失敗
goto end

:end
pause
