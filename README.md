# 簡易差異備份工具 (Simple Delta Backup Tool)

## 📋 專案概述

一個為 Windows 使用者設計的簡潔、高效的差異備份工具。功能包括：
- ✅ 手動備份（一鍵開始）
- ✅ 差異檢測（只備份異動檔案）
- ✅ 檔案恢復（簡單易用的恢復嚮導）
- ✅ 日誌記錄（備份歷史追蹤）
- ✅ 自動清理（1年保留政策）

## 🛠️ 開發環境設定

### 前置要求

- **Windows 11**
- **Python 3.11+** (必須)
  - 下載: https://www.python.org/downloads/
- **Git** (必須)
  - 下載: https://git-scm.com/download/win
- **Conda** (可選)
  - 下載: https://docs.conda.io/projects/miniconda/en/latest/
  - 若未安裝，本工具自動使用 Python venv

### 快速開始

#### 1️⃣ 自動設定（推薦）

```bash
cd D:\dev\backup
setup_v2.bat
```

此腳本會自動：
- 檢查 Python 和 Git
- 偵測 Conda（有則用，無則用 venv）
- 建立虛擬環境
- 安裝所有依賴
- 初始化 Git

#### 2️⃣ 手動設定 (Conda)

如果已安裝 Conda：

```bash
conda env create -f environment.yml
conda activate backup
pip install -r requirements.txt
```

#### 3️⃣ 手動設定 (Python venv)

使用 Python 內建虛擬環境：

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### 4️⃣ 初始化 Git

```bash
git init
git config user.email "your-email@example.com"
git config user.name "Your Name"
git add .
git commit -m "Initial commit"
```

## 🚀 使用方式

### 執行備份工具

```bash
# 激活環境 (Conda)
conda activate backup

# 或激活環境 (venv)
venv\Scripts\activate

# 運行應用程序
python backup_tool.py
```

### 運行測試

```bash
# 激活環境
conda activate backup    # 或 venv\Scripts\activate

# 執行測試
python test_backup.py
```

### 驗證環境

```bash
# 激活環境後執行
python validate_env.py
```

## 📦 環境依賴

| 套件 | 版本 | 用途 |
|------|------|------|
| Python | 3.11+ | 核心語言 |
| tkinter | 系統套件 | GUI介面 |
| json | 內建 | 元資料序列化 |
| shutil | 內建 | 檔案操作 |
| threading | 內建 | 背景執行 |
| python-dateutil | 2.8.2+ | 時間處理 |
| pytz | 2023.3+ | 時區支持 |

## 📁 專案結構

```
D:\dev\backup\
├── backup_tool.py           # 主應用程序
├── test_backup.py           # 單元測試
├── spec.md                  # 規格文件
├── environment.yml          # Conda 環境定義
├── requirements.txt         # pip 依賴清單
├── setup_env.bat            # 自動化設定腳本
├── run_backup_tool.bat      # 執行腳本
├── README.md                # 本檔案
└── .gitignore              # Git 忽略規則
```

## 🔧 開發流程

### 版本控制

```bash
# 查看狀態
git status

# 提交變更
git add .
git commit -m "feat: 新功能描述

詳細說明...
- 列點1
- 列點2
"

# 查看日誌
git log --oneline
```

### 編碼規範

- 使用 UTF-8 編碼
- 函數文件字串用中文或英文註解
- 類別名稱: PascalCase
- 函數/變數名稱: snake_case
- 常數名稱: UPPER_SNAKE_CASE

### 測試

```bash
# 運行單元測試
python test_backup.py

# 測試通過
✅ 所有測試通過!
```

## 📚 主要模組

### `BackupManifest` 類
管理備份元資料（`.backup_manifest` 檔案）

### `DeltaBackupEngine` 類
實現差異檢測和備份邏輯

### `BackupLogger` 類
管理備份歷史日誌

### `BackupToolGUI` 類
提供使用者介面

## 🐛 常見問題

### Q: 如何重新建立環境？
```bash
conda env remove -n backup
conda env create -f environment.yml
```

### Q: 如何清理快取？
```bash
conda clean --all
rm -rf __pycache__ .pytest_cache
```

### Q: 如何檢查環境套件？
```bash
conda activate backup
pip list
```

## 📝 記錄位置

- **元資料**: `~/.backup_tool/manifest.json`
- **歷史**: `~\.backup_tool\history.json`
- **備份**: 使用者指定的外接裝置

## 🔒 安全性考量

- 元資料以 JSON 格式儲存（易於稽核）
- 備份時自動驗證檔案完整性
- 恢復前顯示預覽清單
- 所有操作都有詳細日誌

## 📞 技術支援

遇到問題請：
1. 查看 `.backup_tool/history.json` 中的錯誤日誌
2. 確認外接裝置連接正常
3. 檢查檔案夾權限設定

## 📜 版本歷史

- **v1.0** (2026-01-29)
  - 初始版本
  - 差異備份功能
  - 檔案恢復功能
  - 日誌記錄系統

## 📄 授權

MIT License - 自由使用和修改

---

**最後更新**: 2026-01-29  
**狀態**: 開發中 🚀
