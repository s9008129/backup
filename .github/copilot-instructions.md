# Copilot 協作指導原則 - 簡易差異備份工具

**版本**: v1.1  
**最後更新**: 2026-01-30  

> 本文件定義了與 GitHub Copilot 和 Claude AI 協作開發本專案時的最高指導原則。

---

## 🎯 第一性原則 (First Principles)

### 1. 用戶價值優先 (User Value First)

**原則**: 所有設計決策都應圍繞用戶的核心需求

**實踐**:
- 不追求完美，而追求**可用**
- 功能優先於代碼美觀性
- 用戶體驗優先於技術複雜性

**反例**: 為了實現複雜的加密算法而犧牲了備份速度

### 2. 簡潔性設計 (Simplicity First)

**原則**: 設計應該簡單，實現也應該簡單

**實踐**:
- 單一畫面展示所有功能
- 最小必要依賴（使用 Python 內建庫）
- 直觀的 GUI 設計，無需培訓

**反例**: 建立複雜的多層架構，導致代碼難以維護

### 3. 可靠性優先 (Reliability First)

**原則**: 寧可功能少，也要功能穩定

**實踐**:
- 完整的錯誤處理和恢復機制
- 備份中斷後可繼續
- 詳細的日誌記錄便於問題診斷
- 充分的測試覆蓋

**反例**: 支援 10 種新功能，但備份經常中斷

### 4. 透明性優先 (Transparency First)

**原則**: 所有決策和操作都應可追蹤

**實踐**:
- 記錄每次備份的詳細信息
- 使用 JSON 元資料，便於外部查詢
- 提供完整的操作日誌
- 顯示進度和統計信息

**反例**: 黑盒備份，用戶不知道發生了什麼

---

## 📋 協作最佳實踐

### 代碼審查 (Code Review)

✅ **明確指定**:
- 核心算法的邏輯
- 資料結構的定義
- 錯誤處理的方式

✅ **複述需求**:
- 在開始編碼前確認理解
- 提出設計方案並討論
- 明確驗收標準

❌ **不要**:
- 直接要求 "優化代碼"
- 不提供具體要求
- 半途改變設計

### 測試驅動開發 (TDD)

✅ **先寫測試**:
```python
def test_detect_changes():
    old = {'file.txt': {'size': 100, 'modified': '2026-01-01'}}
    new = {'file.txt': {'size': 150, 'modified': '2026-01-02'}}
    
    added, modified, deleted = detect_changes(old, new)
    
    assert len(modified) == 1
    assert 'file.txt' in modified
```

✅ **測試範圍**:
- 正常情況
- 邊界情況
- 錯誤情況

### 文檔優先 (Documentation First)

✅ **在代碼前**:
1. 寫 spec.md 定義需求
2. 寫測試定義預期行為
3. 寫代碼實現

### 自動化提交 (Auto Commit)

✅ **何時執行 Commit**:
- 完成一個獨立的功能或任務
- 修復一個 bug
- 更新文檔
- 重構代碼

✅ **Commit 訊息格式**:
```
<type>(<scope>): <簡短摘要 (zh-TW)>

## 意圖與情境
- 用戶想要達成什麼目標
- 在什麼背景下提出需求

## 執行內容
- 具體做了哪些修改
- 新增/修改/刪除了哪些檔案
- 核心邏輯變更

## 決策理由
- 為什麼選擇這個方案
- 第一性原理分析結果
- 優缺點分析

## 執行結果
- 達成了什麼效果
- 驗證方法和結果
- 符合的驗收標準

## 待確認工作
- 需要人類確認的事項
- 後續建議的行動
```

✅ **Type 規範**:
| Type | 用途 | 例子 |
|------|------|------|
| `feat` | 新功能 | `feat(backup): 新增備份進度顯示` |
| `fix` | 錯誤修復 | `fix(manifest): 修復 JSON 編碼問題` |
| `docs` | 文檔更新 | `docs(spec): 更新規格文件` |
| `refactor` | 重構代碼 | `refactor(engine): 優化差異檢測算法` |
| `test` | 測試相關 | `test: 新增單元測試` |
| `chore` | 雜項 | `chore: 更新依賴` |

✅ **Commit 時機**:
- 每個小功能完成後（建議 1-2 小時提交一次）
- 避免累積大量改動後再提交
- 保持提交歷史清晰可追蹤

❌ **禁止行為**:
- 不要提交無意義的訊息（如 "update" 或 "fix bug"）
- 不要混合多個無關的功能在一次提交中
- 不要提交半完成的功能

✅ **代碼註解**:
- 解釋為什麼而非如何
- 記錄複雜算法的邏輯
- 提供使用示例

---

## 🏗️ 架構原則

### 模塊化設計

```python
# ✅ 好: 模組職責明確
BackupManifest      # 元資料管理
DeltaBackupEngine   # 備份邏輯
BackupLogger        # 日誌管理
BackupToolGUI       # 用戶介面

# ❌ 差: 職責混亂
BackupTool (做所有事情)
```

### 資料結構清晰

```python
# ✅ 好: 明確的資料結構
FileInfo = {
    'path': str,
    'size': int,
    'modified': str
}

# ❌ 差: 含糊的資料
file_info = (path, size, time_str)
```

### 錯誤處理完善

```python
# ✅ 好: 完善的錯誤處理
try:
    copy_file(src, dst)
except FileNotFoundError:
    logger.warn(f"來源檔案不存在: {src}")
except PermissionError:
    logger.error(f"無權限讀取: {src}")
except Exception as e:
    logger.error(f"複製失敗: {e}")

# ❌ 差: 忽略錯誤
shutil.copy(src, dst)
```

---

## 🔄 工作流程

### 需求理解 (Requirement Understanding)

1. **分析需求**
   - 讀 spec.md 理解完整需求
   - 識別優先級和邊界情況
   - 確認成功標準

2. **提出問題**
   - 有疑問立即提出
   - 不做假設
   - 與用戶確認理解

### 設計階段 (Design Phase)

1. **資料結構**
   - 定義清晰的資料模型
   - 列出關鍵字段和類型

2. **流程設計**
   - 描述各個步驟
   - 標示錯誤處理點
   - 確認性能要求

### 實現階段 (Implementation Phase)

1. **分解任務**
   - 將大任務分解為小函數
   - 每個函數只做一件事
   - 易於測試

2. **邊寫邊測**
   - 寫一點代碼就測試
   - 錯誤立即修復
   - 不積累技術債

### 驗證階段 (Verification Phase)

1. **功能驗證**
   - 所有驗收準則都通過
   - 邊界情況都考慮
   - 錯誤情況都處理

2. **性能驗證**
   - 備份速度達到要求
   - 記憶體使用合理
   - 無明顯 lag

---

## 🛡️ 質量標準

### 代碼質量

| 指標 | 標準 |
|------|------|
| 測試覆蓋 | ≥ 80% |
| 代碼複製 | 0 |
| 複雜度 | McCabe < 10 |
| 註解率 | 複雜邏輯需要註解 |

### 文檔質量

| 文檔 | 要求 |
|------|------|
| spec.md | 完整定義所有功能 |
| 代碼註解 | 解釋為什麼，不是如何 |
| README.md | 簡單明了，非技術人員可讀 |
| 操作指南.md | 無技術背景用戶可操作 |

### 可靠性

| 項目 | 要求 |
|------|------|
| 異常處理 | 100% 覆蓋 |
| 日誌記錄 | 所有重要操作都有日誌 |
| 錯誤訊息 | 清晰易懂 |
| 恢復能力 | 中斷後可繼續 |

---

## 📝 代碼風格

### Python 風格

```python
# ✅ 推薦風格

class BackupManifest:
    """備份元資料管理類"""
    
    def __init__(self, manifest_path):
        self.manifest_path = manifest_path
        self.data = self._load()
    
    def _load(self):
        """載入元資料，失敗時返回預設結構"""
        if os.path.exists(self.manifest_path):
            try:
                with open(self.manifest_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"警告: 載入元資料失敗 ({e})")
                return self._default_manifest()
        return self._default_manifest()
    
    @staticmethod
    def _default_manifest():
        """預設元資料結構"""
        return {
            "lastBackupTime": None,
            "sourceFolder": "",
            "targetFolder": "",
            "filesCount": 0,
            "totalSize": 0,
            "filesList": []
        }
```

### 命名規範

| 對象 | 規範 | 例子 |
|------|------|------|
| 類名 | PascalCase | BackupManifest |
| 函數/方法 | snake_case | get_file_info |
| 常數 | UPPER_SNAKE_CASE | MAX_RETRY_COUNT |
| 私有函數 | _leading_underscore | _load |

### 註解原則

```python
# ✅ 好: 解釋為什麼
# 使用修改時間戳記+大小來檢測變更，因為：
# 1. 時間戳記快速（不需計算 hash）
# 2. 大小變化肯定意味著內容變化
# 3. 兩個都不變 = 檔案未改動
if size_changed or mtime_changed:
    modified.append(file)

# ❌ 差: 說明如何（代碼已經說明了）
# if size changed or mtime changed
# add to modified list
if size_changed or mtime_changed:
    modified.append(file)
```

---

## 🔐 安全和隱私

### 資料安全

- ✅ 元資料以 JSON 儲存，明文可讀
- ✅ 備份內容不加密（用戶控制備份位置）
- ✅ 交由用戶管理 .backup_manifest 文件安全

### 隱私保護

- ✅ 不收集任何用戶信息
- ✅ 不發送任何數據到遠程
- ✅ 完全本地執行

---

## 🚀 發布和部署

### 版本管理

```
v1.0.0
├─ 主版本 (1) - 大功能變化
├─ 小版本 (0) - 新功能
└─ 修訂版 (0) - 錯誤修復
```

### 發布清單

- [ ] 所有測試通過
- [ ] 文檔更新
- [ ] spec.md 反應最新狀態
- [ ] README.md 和操作指南.md 更新
- [ ] Git tag 建立

---

## 🤝 與 AI 協作

### 明確的請求

✅ **好的請求**:
```
根據 spec.md 中的 F2 (差異檢測)，實現 detect_changes 函數。

需求:
1. 比較 old_files 和 new_files
2. 識別 added, modified, deleted 三類
3. modified 的條件: 大小或修改時間不同

請提供:
- 實現代碼
- 相應的單元測試
- 可能的邊界情況說明
```

❌ **不清楚的請求**:
```
幫我改進備份代碼
```

### 反饋循環

1. **提供上下文**
   - 附上相關代碼
   - 說明當前問題
   - 清楚描述期望結果

2. **評審生成的代碼**
   - 檢查是否符合要求
   - 檢查錯誤處理
   - 檢查是否遵循風格

3. **迭代改進**
   - 有問題立即反饋
   - 小改進可快速迭代
   - 大改進應該回到設計階段

---

## 📚 參考資源

### 內部文檔
- **spec.md** - 完整功能規格
- **操作指南.md** - 使用者手冊
- **README.md** - 開發指南

### 外部資源
- Python 官方文檔
- Tkinter 教程
- JSON 最佳實踐

---

## ✨ 成功的關鍵

1. **清晰的需求** - spec.md 是唯一真理
2. **充分的測試** - 代碼品質的保障
3. **完整的文檔** - 知識的傳承
4. **持續溝通** - 及早發現問題
5. **質量第一** - 不追求速度，追求可靠性

---

**版本**: v1.0  
**最後更新**: 2026-01-30

此文件是與 AI 協作的指導原則，確保所有決策都符合第一性原理和用戶價值。
