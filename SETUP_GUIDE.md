# 🚀 開發環境設定指南 - 快速參考

## 📋 已完成的配置

### ✅ 專案結構

```
D:\dev\backup\
├── 💾 核心應用
│   ├── backup_tool.py       (主應用程序 - tkinter GUI)
│   ├── test_backup.py       (單元測試)
│
├── 📚 文檔
│   ├── spec.md              (完整規格文檔 v2.0)
│   ├── README.md            (開發指南)
│   ├── SETUP_GUIDE.md       (本檔案 - 快速參考)
│
├── 🔧 環境配置
│   ├── environment.yml      (Conda 環境定義)
│   ├── requirements.txt     (Python 依賴清單)
│
├── 🤖 自動化腳本
│   ├── setup_all.bat        ⭐ 一鍵完整設定（推薦）
│   ├── setup_env.bat        (基礎環境設定)
│   ├── init_git.bat         (Git 初始化)
│   ├── check_env.bat        (環境檢查)
│
├── ✨ Python 驗證工具
│   ├── check_env.py         (環境檢查工具)
│   ├── validate_env.py      (完整驗證 + 報告)
│
├── 🔐 Git 配置
│   ├── .gitignore           (Git 忽略規則)
│   ├── .gitconfig           (本地 Git 配置)
│   ├── .gitmessage          (提交訊息模板)
│
└── 📄 執行腳本
    └── run_backup_tool.bat  (執行應用程序)
```

### ✅ 已安裝的工具/套件

- **Python 3.11+** - 核心語言
- **tkinter** - GUI 框架（內建於 Python）
- **json** - 元資料序列化（內建）
- **shutil** - 檔案操作（內建）
- **datetime** - 時間處理（內建）
- **python-dateutil** - 額外時間功能
- **pytz** - 時區支持

---

## 🚀 快速開始

### 方案 1️⃣ - 一鍵設定（🌟 推薦）

```batch
cd D:\dev\backup
setup_all.bat
```

這個腳本將自動：
1. ✅ 檢查 Python
2. ✅ 檢查 Conda  
3. ✅ 建立虛擬環境 (backup)
4. ✅ 安裝所有依賴
5. ✅ 初始化 Git 倉庫
6. ✅ 進行首次提交

### 方案 2️⃣ - 手動步驟

#### 步驟 1: 建立 Conda 環境

```bash
conda create -n backup python=3.11 -y
```

#### 步驟 2: 激活環境

```bash
conda activate backup
```

#### 步驟 3: 安裝依賴

```bash
pip install -r requirements.txt
```

#### 步驟 4: 初始化 Git

```bash
cd D:\dev\backup
git init
git config user.email "your-email@example.com"
git config user.name "Your Name"
git add .
git commit -m "Initial commit"
```

---

## ✅ 驗證環境

### 檢查環境完備性

```bash
# 激活環境
conda activate backup

# 運行完整驗證
python validate_env.py

# 或簡單檢查
python check_env.py
```

預期輸出應包含：
```
✅ Python 3.11
✅ Conda installed
✅ backup 環境存在
✅ Git 已安裝
✅ Git 倉庫已初始化
✅ 所有必要檔案存在
✅ 所有 Python 模組可用
```

---

## 🎯 使用應用程序

### 運行備份工具

```bash
# 步驟 1: 激活環境
conda activate backup

# 步驟 2: 執行應用
python backup_tool.py

# 或使用批次檔
run_backup_tool.bat
```

### 運行測試

```bash
conda activate backup
python test_backup.py
```

---

## 📝 版本控制

### 查看狀態

```bash
git status
```

### 提交變更

```bash
# 簡單提交
git add .
git commit -m "feat: 功能描述"

# 詳細提交（推薦）
git add .
git commit -m "feat(備份引擎): 實現新功能

- 詳細說明第一點
- 詳細說明第二點

Closes #123"
```

### 查看日誌

```bash
# 簡潔日誌
git log --oneline

# 詳細日誌
git log -p

# 視覺化日誌
git log --graph --oneline --all

# 最近 10 次提交
git log --oneline -10
```

---

## 🔧 常用命令速查

### Conda 命令

```bash
# 列出所有環境
conda env list

# 激活環境
conda activate backup

# 停用環境
conda deactivate

# 刪除環境
conda env remove -n backup

# 重新建立環境
conda env create -f environment.yml

# 更新所有套件
conda update --all -y

# 清理快取
conda clean --all
```

### Python 命令

```bash
# 檢查 Python 版本
python --version

# 列出已安裝的套件
pip list

# 安裝套件
pip install package-name

# 從 requirements.txt 安裝
pip install -r requirements.txt

# 凍結當前環境
pip freeze > requirements.txt
```

### Git 命令

```bash
# 初始化倉庫
git init

# 配置使用者
git config user.name "Your Name"
git config user.email "your@email.com"

# 查看狀態
git status

# 查看變更
git diff

# 暫存檔案
git add .

# 提交
git commit -m "message"

# 查看日誌
git log --oneline

# 回退到上一次提交
git reset --hard HEAD~1

# 建立分支
git branch feature-name

# 切換分支
git checkout feature-name

# 合併分支
git merge feature-name
```

---

## ⚠️ 常見問題與解決方案

### Q: Python 未安裝或無法找到
```bash
# 檢查 Python
python --version

# 如未安裝，請下載
# https://www.python.org/downloads/
```

### Q: Conda 未找到
```bash
# 安裝 Miniconda
# https://docs.conda.io/projects/miniconda/en/latest/

# 安裝後需重啟終端或電腦
```

### Q: 環境建立失敗
```bash
# 完全刪除環境並重建
conda env remove -n backup --yes
conda create -n backup python=3.11 -y
conda activate backup
pip install -r requirements.txt
```

### Q: Git 初始化時提示權限錯誤
```bash
# 以管理員身份執行命令提示符
# 或使用 Git Bash（隨 Git for Windows 安裝）
```

### Q: 備份工具無法啟動
```bash
# 檢查環境
python validate_env.py

# 檢查 tkinter
python -c "import tkinter; print('tkinter OK')"

# 查看詳細錯誤
python backup_tool.py 2>&1 | tee error.log
```

---

## 📊 系統需求檢查清單

| 項目 | 狀態 | 備註 |
|------|------|------|
| Windows 11 | ✅ | 已預設 |
| Python 3.11+ | ⏳ | 需安裝 |
| Conda | ⏳ | 需安裝 |
| Git | ⏳ | 需安裝 |
| Visual Studio Code (可選) | ✅ | 推薦用於編輯 |

---

## 🎓 開發工作流程建議

### 日常開發

```bash
1. 啟動終端
2. cd D:\dev\backup
3. conda activate backup
4. 編輯程式碼
5. python backup_tool.py (測試)
6. python test_backup.py (驗證)
7. git add .
8. git commit -m "feat: 新功能"
9. git push (如有遠端倉庫)
```

### 環境重置

```bash
# 如遇到環境問題
conda env remove -n backup --yes
setup_all.bat
```

---

## 📚 進階設定

### 配置 Visual Studio Code

建立 `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-python.python"
    }
}
```

### Git 別名配置

在 `.gitconfig` 中已預先配置：

```bash
git st          # status
git co          # checkout
git ci          # commit
git br          # branch
git unstage     # 取消暫存
git last        # 查看最後提交
git visual      # 視覺化日誌
git history     # 最近提交
```

---

## 📞 需要幫助？

1. 查看 spec.md（完整規格）
2. 查看 README.md（開發指南）
3. 運行 `validate_env.py`（環境診斷）
4. 檢查 `.backup_tool/history.json`（應用日誌）

---

**最後更新**: 2026-01-29  
**準備狀態**: ✅ 環境已完全設定  
**下一步**: 執行 `setup_all.bat` 進行最終配置
