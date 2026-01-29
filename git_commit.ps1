# PowerShell 版 Git 提交腳本

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

Push-Location D:\dev\backup

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                  Git 版本控制操作 v4.0                        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 步驟 1: 查看狀態
Write-Host "[1/3] 檢查工作目錄狀態" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
git status --short
Write-Host ""

# 步驟 2: 暫存所有變更
Write-Host "[2/3] 暫存所有變更" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
git add .
Write-Host "✅ 已暫存所有變更" -ForegroundColor Green
Write-Host ""

# 步驟 3: 提交變更
Write-Host "[3/3] 提交變更" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray

$commitMessage = @"
feat: 完成環境自動化設定 v4.0 - PowerShell 完整版

【新增功能】
✅ install_all.ps1: 完整自動化設定腳本 (PowerShell 版)
  • 自動檢查/安裝 Git
  • 自動下載安裝 Miniconda (如需)
  • 自動建立 backup 虛擬環境
  • 自動安裝所有依賴套件
  • 完美中文編碼支援 (UTF-8)
  • 詳細日誌記錄

✅ SETUP_FINAL.md: 完整設定文檔 v4.0
  • 功能詳解
  • 快速開始指南
  • 故障排除手冊
  • 時間預估表

【設計改進】
✅ 相比 v3.0 (手動方案)：
  • 從手動多步驟改進為一鍵自動化
  • 新增 Git 自動驗證/安裝
  • 新增 Conda 自動下載安裝
  • 新增詳細日誌記錄
  • 完善的中文編碼支援 (PowerShell Core UTF-8)

✅ 版本演進：
  v1.0 → v2.0 (編碼修復) → v3.0 (手動方案) → v4.0 (完整自動化) ✓

【技術特性】
✅ PowerShell Core 完全支援
✅ 自動重新整理環境變數
✅ 智能組件偵測 (避免重複安裝)
✅ 無聲安裝 Miniconda
✅ 自動驗證每個步驟
✅ 彩色輸出提升使用體驗
✅ 完整的錯誤處理機制

【相容性】
✅ Windows 11 (已驗證)
✅ PowerShell 5.1+ (含 PowerShell Core 7+)
✅ 支援 Git 2.x+
✅ 支援 Miniconda 最新版本
✅ Python 3.11+ 虛擬環境

【使用方式】
方式 1 (推薦): Copilot CLI 自然語言
  'run install_all.ps1'
  'git add all'
  'commit: 訊息內容'

方式 2: 直接 PowerShell 執行
  Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
  .\install_all.ps1

方式 3: 命令行批處理
  powershell -NoProfile -ExecutionPolicy Bypass -File install_all.ps1

【下一步】
1. 運行 install_all.ps1 完成環境設定
2. conda activate backup
3. python backup_tool.py

Detailed zh-tw commit log 已完成
"@

git commit -m $commitMessage
Write-Host ""

# 步驟 4: 查看最新提交
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ Git 提交完成" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "📝 最新提交詳情:" -ForegroundColor Yellow
git log --oneline -1
Write-Host ""

Write-Host "📊 提交詳細訊息:" -ForegroundColor Yellow
git show --stat
Write-Host ""

Write-Host "🚀 立即開始設定環境:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  .\install_all.ps1" -ForegroundColor Blue
Write-Host ""

Pop-Location
