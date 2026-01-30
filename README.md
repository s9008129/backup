# 簡易差異備份工具

一個為 Windows 使用者設計的簡潔高效的差異備份工具。

## ✨ 核心功能

- **一鍵備份** - 簡單直觀的 GUI 介面
- **智能差異檢測** - 只備份已改動的檔案  
- **檔案恢復** - 方便的復原功能
- **備份日誌** - 完整的操作歷史記錄

## 🚀 快速開始

### 環境要求

- Windows 11
- Python 3.11+
- Conda (或 venv)

### 安裝步驟

```bash
# 1. 啟動 Conda 虛擬環境
conda activate backup

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 執行應用
python src/backup_tool.py
```

## 📖 使用方式

### 首次備份

1. 執行應用：`python src/backup_tool.py`
2. 選擇來源資料夾（要備份的檔案位置）
3. 選擇備份目的地（外接硬碟路徑）
4. 點擊「開始備份」按鈕

### 後續備份

應用會自動偵測改動，只備份新增或修改的檔案，節省時間和空間。

### 恢復檔案

1. 執行應用
2. 在恢復面板選擇備份資料夾
3. 選擇要恢復的檔案或資料夾
4. 點擊「恢復」按鈕

## 📁 專案結構

```
backup/
├── src/
│   └── backup_tool.py         # 主應用程序
├── tests/
│   └── test_backup.py         # 單元測試
├── docs/
│   ├── 操作指南.md            # 使用者手冊
│   └── 開發指南.md            # 開發文檔
├── .github/
│   └── copilot-instructions.md # AI 指導原則
├── spec.md                    # 功能規格文件
├── requirements.txt           # 依賴清單
├── environment.yml            # Conda 環境定義
└── README.md                  # 本檔案
```

## 🧪 測試

```bash
# 執行單元測試
python tests/test_backup.py

# 預期結果：✅ 所有測試通過
```

## 📝 配置檔案

| 檔案 | 用途 |
|------|------|
| `requirements.txt` | Python 依賴包 |
| `environment.yml` | Conda 環境定義 |
| `pyproject.toml` | 專案設定 |

## ⚙️ 資料位置

- **元資料**: `~\.backup_tool\manifest.json`
- **歷史日誌**: `~\.backup_tool\history.json`
- **備份內容**: 使用者指定的外接裝置

## 🔐 安全性

✅ 備份前自動驗證檔案完整性  
✅ 恢復前顯示預覽清單  
✅ 所有操作均有詳細日誌  
✅ 元資料以 JSON 格式儲存便於稽核  

## 📚 文檔

- **spec.md** - 完整的功能規格文件
- **docs/操作指南.md** - 非技術人員使用指南
- **docs/開發指南.md** - 開發人員參考

## 🐛 常見問題

**Q: 備份中斷後如何繼續？**  
A: 應用會自動檢測已備份的檔案，重新執行時只備份未完成的部分。

**Q: 如何清理舊備份？**  
A: 備份資料夾可直接删除，應用使用自動清理機制（1年保留政策）。

**Q: 可以備份到網路硬碟嗎？**  
A: 建議使用本地外接硬碟。網路硬碟可能導致速度緩慢或連線中斷。

## 📄 授權

MIT License

---

**最後更新**: 2026-01-30  
**版本**: v1.0
