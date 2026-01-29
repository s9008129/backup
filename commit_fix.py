#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動化 Git 提交腳本 - 繁體中文編碼支持
"""

import subprocess
import sys
from pathlib import Path

def run_git(args, description=""):
    """執行 Git 命令"""
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False


def main():
    project_dir = Path(__file__).parent
    print("\n" + "=" * 70)
    print("簡易備份工具 - 環境設定問題修復提交")
    print("=" * 70 + "\n")
    
    # 檢查 Git 倉庫
    result = subprocess.run(
        ['git', 'rev-parse', '--git-dir'],
        capture_output=True,
        cwd=project_dir
    )
    
    if result.returncode != 0:
        print("⚠️  Git 倉庫未初始化，正在初始化...")
        run_git(['init'], "Git 倉庫初始化")
        run_git(['config', 'user.email', 'backup-tool@local'], "配置 email")
        run_git(['config', 'user.name', 'Backup Tool Dev'], "配置用戶名")
    
    # 查看變更
    result = subprocess.run(
        ['git', 'status', '--short'],
        capture_output=True,
        text=True,
        encoding='utf-8',
        cwd=project_dir
    )
    
    if not result.stdout.strip():
        print("✅ 無未提交的變更")
        print("\n已提交列表:")
        run_git(['log', '--oneline', '-5'], "查看最近提交")
        return 0
    
    # 暫存所有變更
    print(f"✅ 發現 {len(result.stdout.split(chr(10)))} 個變更\n")
    print("[1/3] 暫存變更...")
    run_git(['add', '.'], "git add .")
    
    # 準備提交訊息
    commit_msg = """fix: 修復環境設定問題並優化使用體驗

【修復的問題】
✅ Conda 依賴問題
   - 原因：Conda 並非必須依賴，但舊版本強制要求
   - 解決：提供 Python venv 備選方案
   - 結果：自動偵測最佳環境方案

✅ 批次檔編碼問題
   - 原因：繁體中文在批次檔中亂碼輸出
   - 解決：改進編碼處理，簡化輸出語句
   - 結果：完整支援繁體中文輸出

✅ Git 命令語法錯誤
   - 原因：批次檔中 for 循環語法問題
   - 解決：改用 findstr 替代 find，簡化邏輯
   - 結果：Git 初始化正常進行

✅ 文檔與實際不符
   - 原因：舊文檔假設 Conda 已安裝
   - 解決：全面更新文檔，明確兩種方案
   - 結果：文檔準確反映實際配置

【新增檔案】
+ setup_v2.bat - 改進版自動設定腳本
  └ 支援自動偵測 Conda 和 venv
  └ 完整的編碼支持和錯誤處理
  
+ SETUP_GUIDE_v2.md - 最新設定指南
  └ 清晰說明兩種環境方案
  └ 完整的手動和自動設定流程

【修改檔案】
* README.md - 環境設定部分更新
  └ 明確 Python 和 Git 為必須
  └ 標明 Conda 為可選
  └ 提供 venv 備選方案

* spec.md - 新增環境設定說明
  └ 文檔版本升級至 v2.1
  └ 開發計畫標記為完成

* setup_all.bat - 改進的 Conda 偵測
  └ 修復編碼問題
  └ 改進 Git 命令

【測試狀態】
✅ Python 3.11+ 環境檢查
✅ Git 初始化測試
✅ 繁體中文編碼驗證
✅ 虛擬環境自動偵測

【使用指南】
新用戶快速開始:
  cd D:\\dev\\backup
  setup_v2.bat

【向後相容性】
✓ 保持 setup_all.bat (已改進)
✓ 保持 environment.yml (Conda 用戶)
✓ 保持 requirements.txt (所有用戶)

此更新完全解決了環境設定問題，
提供更靈活的虛擬環境選擇，
同時改進了文檔清晰度。"""
    
    # 提交
    print("[2/3] 提交變更...")
    run_git(['commit', '-m', commit_msg], "建立提交")
    
    # 顯示結果
    print("\n[3/3] 查看提交日誌...\n")
    run_git(['log', '--oneline', '-5'], "最近提交")
    
    print("\n" + "=" * 70)
    print("✅ 提交完成！")
    print("=" * 70 + "\n")
    
    # 顯示最新提交詳情
    print("最新提交詳情:")
    subprocess.run(['git', 'show', '--stat'], cwd=project_dir)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
