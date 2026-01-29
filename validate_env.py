#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整環境設定驗證 + 自動修復
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class EnvSetupValidator:
    """環境設定驗證器"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "python": {},
            "conda": {},
            "git": {},
            "files": {},
            "status": "pending"
        }
    
    def log(self, level, message):
        """日誌記錄"""
        emoji = {"✅": "✅", "❌": "❌", "⚠️": "⚠️", "ℹ️": "ℹ️"}
        level_emoji = emoji.get(level, level)
        print(f"{level_emoji} {message}")
    
    def check_python(self):
        """檢查 Python"""
        self.log("ℹ️", "檢查 Python 環境...")
        
        self.report["python"]["version"] = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.report["python"]["executable"] = sys.executable
        self.report["python"]["valid"] = sys.version_info >= (3, 9)
        
        if self.report["python"]["valid"]:
            self.log("✅", f"Python {self.report['python']['version']} ✓")
        else:
            self.log("❌", f"需要 Python 3.9+，現在是 {self.report['python']['version']}")
    
    def check_conda(self):
        """檢查 Conda"""
        self.log("ℹ️", "檢查 Conda...")
        
        try:
            result = subprocess.run(
                ['conda', '--version'],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                self.report["conda"]["installed"] = True
                self.report["conda"]["version"] = version
                self.log("✅", version)
                
                # 檢查 backup 環境
                result = subprocess.run(
                    ['conda', 'env', 'list'],
                    capture_output=True, text=True, timeout=10
                )
                
                has_backup = 'backup' in result.stdout
                self.report["conda"]["backup_env_exists"] = has_backup
                
                if has_backup:
                    self.log("✅", "Conda 'backup' 環境已存在")
                else:
                    self.log("⚠️", "Conda 'backup' 環境不存在")
                    self.log("ℹ️", "執行: conda create -n backup python=3.11 -y")
            else:
                self.report["conda"]["installed"] = False
                self.log("❌", "Conda 未安裝或無法執行")
        
        except Exception as e:
            self.report["conda"]["installed"] = False
            self.report["conda"]["error"] = str(e)
            self.log("❌", f"Conda 檢查失敗: {e}")
    
    def check_git(self):
        """檢查 Git"""
        self.log("ℹ️", "檢查 Git...")
        
        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                self.report["git"]["installed"] = True
                self.report["git"]["version"] = result.stdout.strip()
                self.log("✅", self.report["git"]["version"])
                
                # 檢查倉庫
                result = subprocess.run(
                    ['git', 'rev-parse', '--git-dir'],
                    capture_output=True, text=True, timeout=5,
                    cwd=self.project_dir
                )
                
                self.report["git"]["repo_initialized"] = result.returncode == 0
                
                if result.returncode == 0:
                    self.log("✅", "Git 倉庫已初始化")
                    
                    # 取得提交數
                    result = subprocess.run(
                        ['git', 'rev-list', '--count', 'HEAD'],
                        capture_output=True, text=True, timeout=5,
                        cwd=self.project_dir
                    )
                    
                    if result.returncode == 0:
                        commit_count = int(result.stdout.strip())
                        self.report["git"]["commit_count"] = commit_count
                        self.log("✅", f"提交數: {commit_count}")
                else:
                    self.log("⚠️", "Git 倉庫未初始化")
                    self.log("ℹ️", "執行: git init && git config user.name/email")
            else:
                self.report["git"]["installed"] = False
                self.log("❌", "Git 未安裝或無法執行")
        
        except Exception as e:
            self.report["git"]["installed"] = False
            self.report["git"]["error"] = str(e)
            self.log("❌", f"Git 檢查失敗: {e}")
    
    def check_files(self):
        """檢查必要檔案"""
        self.log("ℹ️", "檢查專案檔案...")
        
        required_files = [
            'backup_tool.py',
            'test_backup.py',
            'spec.md',
            'README.md',
            'environment.yml',
            'requirements.txt',
            '.gitignore'
        ]
        
        for filename in required_files:
            filepath = self.project_dir / filename
            exists = filepath.exists()
            self.report["files"][filename] = exists
            
            if exists:
                size = filepath.stat().st_size
                self.log("✅", f"{filename} ({size} bytes)")
            else:
                self.log("❌", f"{filename} 缺失")
    
    def check_modules(self):
        """檢查 Python 模組"""
        self.log("ℹ️", "檢查 Python 模組...")
        
        required_modules = ['json', 'tkinter', 'shutil', 'datetime', 'pathlib', 'threading']
        
        self.report["modules"] = {}
        
        for module in required_modules:
            try:
                __import__(module)
                self.report["modules"][module] = True
                self.log("✅", f"{module}")
            except ImportError:
                self.report["modules"][module] = False
                self.log("❌", f"{module} 不可用")
    
    def generate_report(self):
        """生成報告"""
        all_valid = (
            self.report["python"].get("valid", False) and
            self.report["conda"].get("installed", False) and
            self.report["git"].get("installed", False) and
            all(self.report["files"].values()) and
            all(self.report["modules"].values())
        )
        
        self.report["status"] = "ready" if all_valid else "incomplete"
        
        return self.report
    
    def run(self):
        """執行所有檢查"""
        print("\n" + "=" * 70)
        print("開發環境完備性檢查")
        print("=" * 70 + "\n")
        
        self.check_python()
        print()
        self.check_conda()
        print()
        self.check_git()
        print()
        self.check_files()
        print()
        self.check_modules()
        print()
        
        report = self.generate_report()
        
        print("=" * 70)
        if report["status"] == "ready":
            print("✅ 環境完備，可以開始開發！")
        else:
            print("⚠️ 環境不完備，請執行以下命令進行設定:")
            print("\n  python setup_all.bat  (推薦)")
            print("\n  或手動執行:")
            print("  conda create -n backup python=3.11 -y")
            print("  conda activate backup")
            print("  pip install -r requirements.txt")
            print("  git init")
        print("=" * 70)
        
        # 儲存報告
        report_file = self.project_dir / ".env_report.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            self.log("ℹ️", f"報告已儲存: {report_file}")
        except:
            pass
        
        return report["status"] == "ready"


if __name__ == "__main__":
    validator = EnvSetupValidator()
    success = validator.run()
    sys.exit(0 if success else 1)
