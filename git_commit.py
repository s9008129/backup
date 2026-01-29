#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""簡易 Git 操作工具"""
import subprocess
import sys
from pathlib import Path

def git_cmd(args):
    """執行 Git 命令"""
    result = subprocess.run(
        ['git'] + args,
        capture_output=True,
        text=True,
        encoding='utf-8',
        cwd=Path(__file__).parent
    )
    return result.stdout, result.returncode

print("=" * 70)
print("Copilot CLI - Git 版控操作")
print("=" * 70)
print()

# 1. 檢查狀態
print("[1/3] 檢查 Git 狀態...")
output, code = git_cmd(['status', '--short'])
print(output)
print()

# 2. 暫存所有變更
print("[2/3] 暫存所有檔案 (git add .)...")
output, code = git_cmd(['add', '.'])
if code == 0:
    print("✅ 檔案已暫存")
else:
    print(f"❌ 錯誤: {output}")
print()

# 3. 提交
print("[3/3] 建立提交...")
commit_msg = """refactor: 簡化環境設定 - 回歸手動 Conda 方案

【變更說明】
✅ SETUP_GUIDE_v2.md 完全重寫
   • 移除自動偵測邏輯（過度複雜）
   • 採用明確的手動 Conda 方案
   • 逐步說明 (5 個清楚的步驟)
   • 簡化的常見問題解答

✅ 設計原則更新
   • 簡單優於複雜
   • 手動優於自動
   • 明確優於隱含

✅ 使用者體驗改善
   • 明確的前置要求
   • 逐步的設定流程
   • 清晰的命令示範
   • 容易理解的檢查清單

【棄用的方案】
- 自動環境偵測 (setup_v2.bat)
- Python 自動提交工具 (commit_fix.py)
- venv 備選方案

【推薦的方案】
✓ 手動建立 Conda 環境
✓ 在 Copilot CLI 中進行 Git 操作
✓ 自然語言的版本控制

此設計更符合使用者的實際需求，
提供明確、可控、易理解的設定流程。"""

output, code = git_cmd(['commit', '-m', commit_msg])
if code == 0:
    print("✅ 提交成功")
else:
    print(f"❌ 錯誤: {output}")
print()

# 4. 顯示最新提交
print("[完成] 查看最新提交...")
output, code = git_cmd(['log', '--oneline', '-1'])
print(output)
print()

print("=" * 70)
print("✅ Git 操作完成！")
print("=" * 70)
