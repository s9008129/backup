import subprocess
import sys
from pathlib import Path

os.chdir(r'D:\dev\backup')

# 1. Status
print("\n[1] Git Status")
print("=" * 50)
subprocess.run(['git', 'status', '--short'])

# 2. Add
print("\n[2] Git Add")
print("=" * 50)
result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
print("✅ Files staged" if result.returncode == 0 else f"❌ Error: {result.stderr}")

# 3. Commit
print("\n[3] Git Commit")
print("=" * 50)

msg = """refactor: 簡化環境設定 - 回歸手動 Conda 方案

【變更說明】
✅ SETUP_GUIDE_v2.md 完全重寫
   - 移除自動偵測邏輯
   - 採用明確手動 Conda 方案
   - 5 個清楚的逐步說明
   - 簡化的常見問題解答

✅ 設計原則
   - 簡單優於複雜
   - 手動優於自動
   - 明確優於隱含

✅ 使用者體驗
   - 明確的前置要求
   - 逐步的設定流程
   - 清晰的命令示範
   - 易懂的檢查清單

此設計更符合使用者需求。"""

result = subprocess.run(['git', 'commit', '-m', msg], capture_output=True, text=True)
print("✅ Commit successful" if result.returncode == 0 else f"❌ Error")

# 4. Log
print("\n[4] Git Log")
print("=" * 50)
subprocess.run(['git', 'log', '--oneline', '-3'])

print("\n" + "=" * 50)
print("✅ Git operations completed!")
