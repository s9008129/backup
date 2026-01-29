# 🚀 開發環境設定指南 - 手動 Conda 方案

## 📋 環境配置

### ✅ 簡單方案：手動建立 Conda 環境

本工具使用 **Conda 虛擬環境**，提供完全隔離的開發環境。

---

## 📝 前置要求

| 項目 | 狀態 | 下載連結 |
|------|------|---------|
| **Python 3.11+** | ✅ 必須 | https://www.python.org/downloads/ |
| **Conda** | ✅ 必須 | https://docs.conda.io/projects/miniconda/en/latest/ |
| **Git** | ✅ 必須 | https://git-scm.com/download/win |

---

## 🛠️ 逐步設定流程

### 步驟 1️⃣ - 驗證安裝

先確認所有必要工具已安裝：

```bash
# 檢查 Python
python --version
# 預期: Python 3.11.x 或更高

# 檢查 Conda
conda --version
# 預期: conda 23.x.x 或更高

# 檢查 Git
git --version
# 預期: git version 2.x.x
```

### 步驟 2️⃣ - 建立 Conda 環境

```bash
# 進入專案目錄
cd D:\dev\backup

# 建立虛擬環境 (Python 3.11)
conda create -n backup python=3.11 -y

# 耗時: 1-2 分鐘
```

### 步驟 3️⃣ - 激活環境

```bash
# 激活環境
conda activate backup

# 驗證激活成功 (提示字首應顯示 (backup))
# 預期: (backup) D:\dev\backup>
```

### 步驟 4️⃣ - 安裝 Python 依賴

```bash
# 確認環境已激活
conda activate backup

# 安裝依賴
pip install -r requirements.txt

# 耗時: 30-60 秒
```

### 步驟 5️⃣ - 驗證環境完備

```bash
# 激活環境後執行
python validate_env.py

# 預期結果應顯示:
# ✅ Python 環境正常
# ✅ 所有模組可用
# ✅ 環境完備，可以開始開發！
```

---

## ✅ 驗證完成

環境設定完成後，驗證以下項目：

```bash
# 列出已安裝套件
pip list

# 應該包含:
#   - python-dateutil
#   - pytz

# 查看檔案結構
dir backup_tool.py test_backup.py

# 應該看到主要檔案存在
```

---

## 🎯 啟動應用

### 運行備份工具

```bash
# 確認環境激活
conda activate backup

# 執行應用
python backup_tool.py

# 應該看到 GUI 視窗彈出
```

### 運行測試

```bash
# 確認環境激活
conda activate backup

# 執行測試
python test_backup.py

# 應該看到測試結果
```

---

## 📚 常用命令

### 環境管理

```bash
# 激活環境
conda activate backup

# 停用環境
conda deactivate

# 列出所有環境
conda env list

# 刪除環境 (如需要)
conda env remove -n backup
```

### Python 套件

```bash
# 列出已安裝
pip list

# 安裝套件
pip install package-name

# 從 requirements.txt 安裝
pip install -r requirements.txt

# 升級 pip
python -m pip install --upgrade pip
```

### 版本控制

```bash
# 檢查狀態
git status

# 查看變更
git diff

# 暫存檔案
git add .

# 提交變更
git commit -m "message"

# 查看日誌
git log --oneline -10

# 查看詳細提交
git show HEAD
```

---

## ⚠️ 常見問題

### Q: 環境激活失敗

**A:** 確認 Conda 已正確安裝：
```bash
conda --version
conda init
# 重啟終端機
```

### Q: pip install 失敗

**A:** 升級 pip 後重試：
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Q: 如何重新建立環境

**A:** 完全移除後重建：
```bash
conda env remove -n backup -y
conda create -n backup python=3.11 -y
conda activate backup
pip install -r requirements.txt
```

### Q: 如何查看環境資訊

**A:** 使用以下命令：
```bash
conda info
conda env list
pip list
python -c "import sys; print(sys.executable)"
```

---

## 📁 環境結構

```
D:\dev\backup\
├── backup_tool.py         # 主應用程序
├── test_backup.py         # 單元測試
├── validate_env.py        # 環境驗證工具
├── environment.yml        # Conda 環境定義 (參考)
├── requirements.txt       # pip 依賴清單
├── spec.md                # 規格文件
├── README.md              # 開發指南
└── .gitignore             # Git 忽略規則
```

---

## 📝 設定完成檢查清單

設定完成後，請確認：

- [ ] Python 3.11+ 已安裝且可用
- [ ] Conda 已安裝且可用
- [ ] Git 已安裝且可用
- [ ] backup Conda 環境已建立
- [ ] 環境激活後 pip list 顯示正確套件
- [ ] python validate_env.py 通過檢查
- [ ] python backup_tool.py 可以啟動
- [ ] python test_backup.py 可以執行
- [ ] git log 顯示提交歷史

✅ 所有項目完成 → 環境設定成功！

---

## 🚀 快速開始

1. **建立環境 (一次性)**
   ```bash
   conda create -n backup python=3.11 -y
   conda activate backup
   pip install -r requirements.txt
   ```

2. **啟動應用 (每次)**
   ```bash
   conda activate backup
   python backup_tool.py
   ```

3. **版本控制**
   ```bash
   git add .
   git commit -m "your message"
   git log --oneline
   ```

---

**最後更新**: 2026-01-29  
**版本**: 3.0 (簡化版 - 純手動 Conda)  
**狀態**: ✅ 明確簡潔
