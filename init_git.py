#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動化 Git 初始化和首次提交腳本
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def run_cmd(cmd, cwd=None, description=""):
    """執行命令"""
    print(f"\n▶️  執行: {' '.join(cmd)}")
    if description:
        print(f"   {description}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ 成功")
            if result.stdout:
                for line in result.stdout.split('\n')[:5]:
                    if line.strip():
                        print(f"   {line}")
            return True
        else:
            print(f"❌ 失敗: {result.stderr}")
            return False
    
    except subprocess.TimeoutExpired:
        print(f"❌ 超時")
        return False
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False


def setup_git():
    """設定 Git"""
    project_dir = Path(__file__).parent
    
    print("\n" + "=" * 70)
    print("簡易備份工具 - Git 自動化設定")
    print("=" * 70)
    
    # 檢查 git
    print("\n[1/6] 檢查 Git 安裝...")
    result = subprocess.run(['git', '--version'], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ 錯誤: Git 未安裝")
        return False
    
    print(f"✅ {result.stdout.strip()}")
    
    # 檢查是否已初始化
    print("\n[2/6] 檢查 Git 倉庫...")
    result = subprocess.run(
        ['git', 'rev-parse', '--git-dir'],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("⏳ Git 倉庫不存在，正在初始化...")
        if not run_cmd(['git', 'init'], cwd=project_dir, description="初始化 Git 倉庫"):
            return False
    else:
        print(f"✅ Git 倉庫已存在: {result.stdout.strip()}")
    
    # 配置使用者信息
    print("\n[3/6] 配置 Git 使用者信息...")
    
    run_cmd(
        ['git', 'config', 'user.email', 'backup-tool@local'],
        cwd=project_dir,
        description="設定 email"
    )
    
    run_cmd(
        ['git', 'config', 'user.name', 'Backup Tool Dev'],
        cwd=project_dir,
        description="設定 name"
    )
    
    # 查看狀態
    print("\n[4/6] 檢查變更...")
    result = subprocess.run(
        ['git', 'status', '--short'],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print(f"✅ 發現變更 ({len(result.stdout.split(chr(10)))} 個檔案)")
        for line in result.stdout.split('\n')[:10]:
            if line.strip():
                print(f"   {line}")
    else:
        print("✅ 無未提交的變更")
        return True
    
    # 暫存所有檔案
    print("\n[5/6] 暫存所有變更...")
    if not run_cmd(['git', 'add', '.'], cwd=project_dir, description="git add ."):
        return False
    
    # 首次提交
    print("\n[6/6] 建立首次提交...")
    
    commit_message = """feat: 簡易差異備份工具初始化提交

核心功能實現:
- 手動差異備份（一鍵開始）
- 自動檔案變化偵測（修改時間戳+大小）
- 簡易檔案恢復嚮導
- 詳細備份歷史日誌
- 1年保留策略自動清理

開發環境配置:
- Python 3.11 隔離環境（Conda）
- tkinter GUI 框架
- 完整的單元測試

專案文檔:
- spec.md: 完整需求規格書 v2.0
- README.md: 開發指南
- SETUP_GUIDE.md: 快速參考
- environment.yml: Conda 環境定義
- pyproject.toml: 專案配置

工具腳本:
- setup_all.bat: 一鍵完整設定
- validate_env.py: 環境驗證工具
- check_env.py: 環境檢查工具

版本控制設定:
- .gitignore: Git 忽略規則
- .gitconfig: 本地 Git 配置
- .gitmessage: 提交訊息模板

所有功能均已實現並準備進行測試。
"""
    
    if run_cmd(['git', 'commit', '-m', commit_message], cwd=project_dir, description="建立首次提交"):
        print("\n✅ 首次提交成功")
    else:
        return False
    
    # 顯示提交日誌
    print("\n[結果] 查看提交日誌...")
    result = subprocess.run(
        ['git', 'log', '--oneline', '-1'],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ 最新提交:")
        print(f"   {result.stdout.strip()}")
    
    return True


def main():
    """主函式"""
    success = setup_git()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ Git 設定完成！")
        print("=" * 70)
        print("\n後續步驟:")
        print("   1. 激活環境: conda activate backup")
        print("   2. 驗證環境: python validate_env.py")
        print("   3. 運行應用: python backup_tool.py")
        print("   4. 運行測試: python test_backup.py")
        print("\n查看日誌:")
        print("   git log --oneline -10")
        print("   git log -1 --stat")
        return 0
    else:
        print("❌ Git 設定失敗")
        print("=" * 70)
        print("\n請檢查:")
        print("   1. Git 是否已安裝")
        print("   2. 磁碟是否有足夠空間")
        print("   3. 資料夾是否有正確的寫入權限")
        return 1


if __name__ == "__main__":
    sys.exit(main())
