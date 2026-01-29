#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
環境驗證工具 - 檢查開發環境是否完備
"""

import sys
import os
import json
import subprocess
from pathlib import Path

class EnvironmentChecker:
    """環境檢查器"""
    
    def __init__(self):
        self.results = []
        self.issues = []
    
    def check(self, name, condition, message=""):
        """檢查項目"""
        status = "✅" if condition else "❌"
        self.results.append(f"{status} {name}")
        if not condition:
            self.issues.append(f"{name}: {message}")
    
    def check_python(self):
        """檢查 Python"""
        print("\n🐍 Python 環境")
        print("-" * 50)
        
        self.check("Python 版本", 
                   sys.version_info >= (3, 9),
                   f"需要 3.9+，現在是 {sys.version_info.major}.{sys.version_info.minor}")
        
        print(f"   版本: {sys.version.split()[0]}")
        print(f"   路徑: {sys.executable}")
    
    def check_modules(self):
        """檢查必要模組"""
        print("\n📦 Python 模組")
        print("-" * 50)
        
        required_modules = {
            'json': '元資料序列化',
            'tkinter': 'GUI 介面',
            'shutil': '檔案操作',
            'datetime': '時間處理',
            'pathlib': '路徑管理',
            'threading': '背景執行',
            'os': '系統操作'
        }
        
        for module, description in required_modules.items():
            try:
                __import__(module)
                self.check(module, True)
                print(f"   ✓ {module}: {description}")
            except ImportError:
                self.check(module, False, f"{description} - 無法導入")
    
    def check_files(self):
        """檢查專案檔案"""
        print("\n📁 專案檔案")
        print("-" * 50)
        
        required_files = {
            'backup_tool.py': '主應用程序',
            'test_backup.py': '單元測試',
            'spec.md': '規格文件',
            'environment.yml': 'Conda 環境',
            'requirements.txt': 'pip 依賴',
            'README.md': '說明文檔',
            '.gitignore': 'Git 忽略規則'
        }
        
        project_path = Path(__file__).parent
        
        for filename, description in required_files.items():
            filepath = project_path / filename
            exists = filepath.exists()
            self.check(filename, exists, f"{description} - 檔案不存在")
            if exists:
                size = filepath.stat().st_size
                print(f"   ✓ {filename} ({size} bytes)")
    
    def check_git(self):
        """檢查 Git"""
        print("\n🔧 Git 版控")
        print("-" * 50)
        
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            self.check("Git 安裝", result.returncode == 0)
            if result.returncode == 0:
                print(f"   {result.stdout.strip()}")
        except Exception as e:
            self.check("Git 安裝", False, str(e))
        
        try:
            result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                                  capture_output=True, text=True, timeout=5,
                                  cwd=Path(__file__).parent)
            is_git_repo = result.returncode == 0
            self.check("Git 倉庫", is_git_repo)
            if is_git_repo:
                print(f"   ✓ 倉庫路徑: {result.stdout.strip()}")
        except:
            self.check("Git 倉庫", False, "不是有效的 Git 倉庫")
    
    def check_conda(self):
        """檢查 Conda"""
        print("\n🔬 Conda 環境")
        print("-" * 50)
        
        try:
            result = subprocess.run(['conda', '--version'],
                                  capture_output=True, text=True, timeout=5)
            self.check("Conda 安裝", result.returncode == 0)
            if result.returncode == 0:
                print(f"   {result.stdout.strip()}")
        except Exception as e:
            self.check("Conda 安裝", False, str(e))
        
        try:
            result = subprocess.run(['conda', 'env', 'list'],
                                  capture_output=True, text=True, timeout=10)
            has_backup_env = 'backup' in result.stdout
            self.check("Conda 'backup' 環境", has_backup_env,
                      "需要執行: conda create -n backup python=3.11")
            if result.returncode == 0 and 'backup' in result.stdout:
                for line in result.stdout.split('\n'):
                    if 'backup' in line:
                        print(f"   ✓ {line.strip()}")
        except:
            self.check("Conda 'backup' 環境", False, "無法列出 Conda 環境")
    
    def run_all_checks(self):
        """執行所有檢查"""
        print("\n" + "=" * 60)
        print("📊 開發環境完備性檢查")
        print("=" * 60)
        
        self.check_python()
        self.check_modules()
        self.check_files()
        self.check_git()
        self.check_conda()
        
        print("\n" + "=" * 60)
        print("📋 檢查結果摘要")
        print("=" * 60)
        
        for result in self.results:
            print(result)
        
        print("\n" + "=" * 60)
        if self.issues:
            print(f"⚠️  發現 {len(self.issues)} 個問題:")
            print("=" * 60)
            for i, issue in enumerate(self.issues, 1):
                print(f"{i}. {issue}")
            print("\n💡 解決建議:")
            print("   1. 執行: python setup_env.bat (自動設定)")
            print("   2. 或手動: conda env create -f environment.yml")
            print("   3. 然後: conda activate backup")
            print("   4. 最後: pip install -r requirements.txt")
        else:
            print("✅ 環境完備，可以開始開發！")
            print("=" * 60)
            print("\n快速開始:")
            print("   1. 激活環境: conda activate backup")
            print("   2. 執行應用: python backup_tool.py")
            print("   3. 運行測試: python test_backup.py")
            print("   4. 提交程式碼: git add . && git commit -m 'message'")


if __name__ == "__main__":
    checker = EnvironmentChecker()
    checker.run_all_checks()
    
    sys.exit(0 if not checker.issues else 1)
