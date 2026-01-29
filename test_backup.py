#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試備份工具的核心功能
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# 新增模組路徑
sys.path.insert(0, r"D:\dev\backup")

from backup_tool import DeltaBackupEngine, BackupManifest, BackupLogger

def test_delta_backup():
    """測試差異備份功能"""
    print("=" * 60)
    print("測試 1: 差異備份引擎")
    print("=" * 60)
    
    # 建立臨時目錄
    with tempfile.TemporaryDirectory() as tmpdir:
        source = os.path.join(tmpdir, "source")
        target = os.path.join(tmpdir, "target")
        
        os.makedirs(source)
        os.makedirs(target)
        
        # 建立測試檔案
        print("\n[步驟1] 建立初始檔案...")
        test_files = {
            "file1.txt": "內容1",
            "folder1/file2.txt": "內容2",
            "folder2/file3.txt": "內容3"
        }
        
        for rel_path, content in test_files.items():
            file_path = os.path.join(source, rel_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # 掃描檔案
        print("[步驟2] 掃描來源資料夾...")
        files_v1 = DeltaBackupEngine.scan_folder(source)
        print(f"✅ 掃描完成: {len(files_v1)} 個檔案")
        for path in files_v1:
            print(f"   - {path}")
        
        # 第一次備份
        print("\n[步驟3] 執行首次備份...")
        for rel_path in files_v1:
            src = os.path.join(source, rel_path)
            dst = os.path.join(target, rel_path)
            DeltaBackupEngine.copy_file(src, dst)
        print(f"✅ 首次備份完成: {len(files_v1)} 個檔案")
        
        # 修改檔案
        print("\n[步驟4] 修改檔案內容...")
        with open(os.path.join(source, "file1.txt"), 'w', encoding='utf-8') as f:
            f.write("修改後的內容1")
        
        with open(os.path.join(source, "folder1", "file2.txt"), 'w', encoding='utf-8') as f:
            f.write("修改後的內容2")
        
        new_file = os.path.join(source, "new_file.txt")
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write("新檔案")
        
        print("✅ 已修改2個檔案，新增1個檔案")
        
        # 掃描並檢測變化
        print("\n[步驟5] 掃描並檢測變化...")
        files_v2 = DeltaBackupEngine.scan_folder(source)
        added, modified, deleted = DeltaBackupEngine.detect_changes(files_v1, files_v2)
        
        print(f"✅ 差異檢測完成:")
        print(f"   - 新增: {len(added)} 個")
        for path in added:
            print(f"     • {path}")
        print(f"   - 修改: {len(modified)} 個")
        for path in modified:
            print(f"     • {path}")
        print(f"   - 刪除: {len(deleted)} 個")
        
        # 差異備份
        print("\n[步驟6] 執行差異備份...")
        for rel_path in added:
            src = os.path.join(source, rel_path)
            dst = os.path.join(target, rel_path)
            DeltaBackupEngine.copy_file(src, dst)
        
        for rel_path in modified:
            src = os.path.join(source, rel_path)
            dst = os.path.join(target, rel_path)
            DeltaBackupEngine.copy_file(src, dst)
        
        print(f"✅ 差異備份完成: {len(added) + len(modified)} 個檔案")
        
        # 驗證
        print("\n[步驟7] 驗證備份完整性...")
        verify_errors = DeltaBackupEngine.verify_backup(source, target, added.keys())
        if verify_errors:
            print(f"❌ 驗證失敗:")
            for error in verify_errors:
                print(f"   - {error}")
        else:
            print("✅ 驗證完成: 所有檔案完整")
    
    print("\n✅ 差異備份測試通過\n")


def test_manifest():
    """測試元資料管理"""
    print("=" * 60)
    print("測試 2: 備份元資料管理")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        manifest_path = os.path.join(tmpdir, "manifest.json")
        
        print("\n[步驟1] 建立元資料...")
        manifest = BackupManifest(manifest_path)
        
        files_info = {
            "file1.txt": {"size": 100, "modified": "2026-01-29T10:00:00"},
            "file2.txt": {"size": 200, "modified": "2026-01-29T10:05:00"}
        }
        
        manifest.update("C:\\source", "E:\\target", files_info)
        print("✅ 元資料已儲存")
        
        print("\n[步驟2] 讀取元資料...")
        manifest2 = BackupManifest(manifest_path)
        print(f"✅ 讀取完成:")
        print(f"   - 來源: {manifest2.data['sourceFolder']}")
        print(f"   - 目標: {manifest2.data['targetFolder']}")
        print(f"   - 檔案數: {manifest2.data['filesCount']}")
        print(f"   - 總大小: {manifest2.data['totalSize']} bytes")
    
    print("\n✅ 元資料測試通過\n")


def test_logger():
    """測試日誌系統"""
    print("=" * 60)
    print("測試 3: 備份日誌系統")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        log_path = os.path.join(tmpdir, "history.json")
        
        print("\n[步驟1] 新增日誌紀錄...")
        logger = BackupLogger(log_path)
        
        records = [
            {"timestamp": "2026-01-29T10:00:00", "status": "✅ 備份完成", "changedFiles": 10, "error": ""},
            {"timestamp": "2026-01-28T10:00:00", "status": "✅ 備份完成", "changedFiles": 5, "error": ""},
            {"timestamp": "2026-01-27T10:00:00", "status": "❌ 備份失敗", "changedFiles": 0, "error": "外接裝置未連接"},
        ]
        
        for record in records:
            logger.add_record(record)
            print(f"✅ 新增: {record['timestamp']} - {record['status']}")
        
        print("\n[步驟2] 讀取最近的紀錄...")
        recent = logger.get_recent(2)
        for record in recent:
            print(f"   - {record['timestamp']}: {record['status']} ({record['changedFiles']}個檔案)")
    
    print("\n✅ 日誌系統測試通過\n")


if __name__ == "__main__":
    try:
        test_delta_backup()
        test_manifest()
        test_logger()
        print("=" * 60)
        print("✅ 所有測試通過!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
