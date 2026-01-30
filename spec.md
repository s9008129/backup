# 簡易差異備份工具 (Simple Delta Backup Tool) - 規格文件

**版本**: v1.0  
**狀態**: 發布  
**最後更新**: 2026-01-30  
**目標**: 規格驅動開發 (Specification-Driven Development)

> 本文件定義了完整的功能需求、技術規範和驗收標準。  
> **驗收標準**: 持有此文件即可在任何地方完全重建此專案。

---

## 📋 目錄

1. [專案定位](#專案定位)
2. [核心功能](#核心功能)
3. [技術架構](#技術架構)
4. [資料模型](#資料模型)
5. [使用者情境](#使用者情境)
6. [驗收準則](#驗收準則)
7. [環境需求](#環境需求)

---

## 專案定位

### 定義

**簡易差異備份工具**是一個 Windows 專用的自動化檔案備份系統，用於保護用戶的重要檔案。

- **目標用戶**: Windows 11 使用者（個人和企業）
- **核心價值**: 智能差異檢測 + 簡單易用 + 完整日誌
- **技術棧**: Python 3.11 + Tkinter GUI + JSON 元資料
- **部署方式**: 獨立 Python 應用程序

### 關鍵特性

| 特性 | 描述 | 優先級 |
|------|------|--------|
| 手動備份 | 使用者主動啟動，一鍵完成 | P0 |
| 差異檢測 | 只備份新增/修改的檔案 | P0 |
| 檔案恢復 | 簡單的復原嚮導 | P1 |
| 日誌記錄 | 完整的操作歷史 | P1 |
| 自動清理 | 1 年保留政策 | P2 |

---

## 核心功能

### F1: 備份流程

#### 功能描述
使用者選擇來源和目的地後，系統自動掃描、檢測差異、複製檔案並驗證。

#### 執行流程

**步驟 1-3**: UI 操作
- 選擇來源資料夾
- 選擇目的地
- 點擊「開始備份」

**步驟 4**: 掃描
- 遞迴掃描來源資料夾
- 取得每個檔案: 相對路徑、大小、修改時間

**步驟 5**: 差異檢測
- 讀取 .backup_manifest 的上次備份紀錄
- 比較新舊檔案列表
- 分類: added, modified, deleted

**步驟 6**: 複製
- 複製 added 和 modified 檔案到目的地
- 驗證大小一致
- 顯示進度

**步驟 7**: 元資料更新
- 更新 .backup_manifest
- 儲存新檔案列表

**步驟 8**: 日誌記錄
- 寫入 history.json
- 顯示完成訊息

#### 驗收準則

- [x] 首次備份時複製所有檔案
- [x] 第二次備份只複製新增/修改的檔案
- [x] 複製後驗證大小完全一致
- [x] .backup_manifest 正確更新
- [x] 備份時間記錄到 history.json
- [x] 進度顯示準確
- [x] 備份中斷可繼續

---

### F2: 差異檢測

#### 算法

```
detect_changes(old_files, new_files):
    added = {}
    modified = {}
    deleted = {}
    
    for path, info in new_files:
        if path not in old_files:
            added[path] = info
        elif (old_files[path].size != info.size OR
              old_files[path].modified != info.modified):
            modified[path] = info
    
    for path in old_files:
        if path not in new_files:
            deleted[path] = old_files[path]
    
    return added, modified, deleted
```

#### 檢測標準

檔案被認定為「修改」的條件之一成立：
- 檔案大小不同
- 修改時間戳記不同

#### 驗收準則

- [x] 新增檔案被正確識別
- [x] 修改檔案被正確識別
- [x] 已刪除檔案被識別但不在備份中刪除
- [x] 未改動的檔案被正確跳過

---

### F3: 檔案恢復

#### 功能描述

使用者選擇備份資料夾，系統列出所有備份的檔案，使用者勾選要恢復的檔案後復原。

#### 執行流程

1. 使用者點擊「恢復」標籤
2. 選擇備份來源資料夾
3. 系統列出備份中的檔案
4. 使用者勾選要恢復的檔案
5. 選擇恢復目的地
6. 點擊「恢復」按鈕
7. 系統複製勾選的檔案
8. 顯示恢復摘要

#### 驗收準則

- [x] 正確列出備份中的所有檔案
- [x] 使用者可選擇部分檔案恢復
- [x] 恢復後檔案內容完全相同
- [x] 目錄結構被正確恢復

---

### F4: 日誌記錄

#### 元資料結構 (.backup_manifest)

```json
{
  "lastBackupTime": "2026-01-30T14:30:45.123456",
  "sourceFolder": "C:\\Users\\user\\Documents",
  "targetFolder": "D:\\Backup",
  "filesCount": 1234,
  "totalSize": 5368709120,
  "filesList": [
    {
      "path": "reports/2026/january.pdf",
      "size": 2097152,
      "modified": "2026-01-30T10:20:30.000000"
    }
  ]
}
```

#### 歷史日誌結構 (history.json)

```json
{
  "backups": [
    {
      "backupTime": "2026-01-30T14:30:45.123456",
      "status": "success",
      "filesAdded": 45,
      "filesModified": 12,
      "filesDeleted": 3,
      "totalSize": 536870912,
      "duration": 120,
      "errors": []
    }
  ]
}
```

#### 驗收準則

- [x] 每次備份後 .backup_manifest 被正確更新
- [x] history.json 記錄每次備份的詳細信息
- [x] 時間戳記以 ISO 8601 格式儲存
- [x] 檔案可被外部工具讀取和分析

---

## 技術架構

### 代碼結構

```
src/backup_tool.py

BackupManifest
├── _load() - 載入 manifest.json
├── save() - 儲存 manifest
├── get_files_dict() - 取得檔案字典
└── update() - 更新元資料

DeltaBackupEngine
├── get_file_info() - 取得檔案大小和時間
├── scan_folder() - 掃描資料夾
├── detect_changes() - 檢測差異
├── copy_file() - 複製並驗證
├── verify_backup() - 驗證備份完整性
└── execute_backup() - 執行備份流程

BackupLogger
├── get_log_path() - 取得日誌路徑
├── _load_history() - 載入歷史
├── log_backup() - 記錄備份
└── get_history() - 取得歷史

BackupToolGUI
├── __init__() - 初始化 UI
├── create_widgets() - 建立 UI 元素
├── browse_source() - 選擇來源
├── browse_destination() - 選擇目的地
├── start_backup() - 啟動備份
├── update_progress() - 更新進度
└── show_result() - 顯示結果
```

### GUI 佈局

單一畫面設計，包含：
- 備份/恢復標籤切換
- 來源和目的地選擇
- 進度顯示
- 結果摘要
- 控制按鈕

---

## 資料模型

### 檔案信息

```python
FileInfo = {
    'path': str,           # 相對路徑
    'size': int,           # 位元組
    'modified': str        # ISO 8601 時間戳記
}
```

### 備份記錄

```python
BackupRecord = {
    'backupTime': str,       # ISO 8601 時間戳記
    'status': str,           # 'success', 'warning', 'failed'
    'filesAdded': int,
    'filesModified': int,
    'filesDeleted': int,
    'totalSize': int,
    'duration': int,
    'errors': [str]
}
```

---

## 使用者情境

### US1: 首次備份

1. 執行 `python src/backup_tool.py`
2. 選擇來源資料夾
3. 選擇目的地
4. 點擊「開始備份」
5. 所有檔案被複製
6. 顯示完成訊息

### US2: 增量備份

1. 編輯 10 個檔案，新增 5 個
2. 再次執行備份
3. 系統只複製 15 個異動檔案
4. 備份完成（大幅加快）

### US3: 檔案恢復

1. 意外刪除了重要檔案
2. 執行軟體，點擊「恢復」
3. 選擇備份資料夾
4. 勾選要恢復的檔案
5. 檔案被復原

---

## 驗收準則

### 功能驗收

| 功能 | 驗收準則 | 狀態 |
|------|--------|------|
| 備份流程 | 首次備份複製所有檔案，增量備份只複製異動 | ✅ |
| 差異檢測 | 準確識別新增、修改、刪除的檔案 | ✅ |
| 檔案恢復 | 可恢復任意備份的檔案 | ✅ |
| 日誌記錄 | 記錄每次備份的詳細信息 | ✅ |
| 元資料管理 | .backup_manifest 正確更新 | ✅ |
| GUI 介面 | 單一畫面顯示所有功能 | ✅ |

### 性能要求

| 場景 | 要求 | 實際 |
|------|------|------|
| 備份 1,000 個檔案 | < 10 分鐘 | ✅ |
| 增量備份 10% 檔案 | < 2 分鐘 | ✅ |
| 恢復 100 個檔案 | < 2 分鐘 | ✅ |

### 穩定性要求

- [x] 備份中斷可繼續
- [x] 檔案被鎖定時顯示警告
- [x] 目的地空間不足時提示
- [x] 所有異常都有詳細錯誤訊息

---

## 環境需求

### 系統要求

| 項目 | 要求 |
|------|------|
| 作業系統 | Windows 11 |
| Python | 3.11+ |
| 記憶體 | 最少 256 MB |
| 磁碟空間 | 50 MB (應用) + 備份大小 |

### 依賴套件

| 套件 | 版本 |
|------|------|
| tkinter | 內建 |
| json | 內建 |
| shutil | 內建 |
| pathlib | 內建 |
| datetime | 內建 |
| threading | 內建 |

### 開發環境

```
Conda 虛擬環境: backup
Python: 3.11
依賴: requirements.txt
測試: tests/test_backup.py
```

---

## 部署檢查清單

使用此清單重建專案：

- [ ] 1. 安裝 Python 3.11+
- [ ] 2. 建立 Conda 虛擬環境
- [ ] 3. 激活環境
- [ ] 4. 安裝依賴
- [ ] 5. 執行測試
- [ ] 6. 執行應用
- [ ] 7. 測試首次備份
- [ ] 8. 測試增量備份
- [ ] 9. 測試檔案恢復
- [ ] 10. 驗證日誌記錄

---

**版本**: v1.0  
**完成度**: 100%  
**最後審查**: 2026-01-30

此文件確保了在任何環境中都能完全重建此專案。
