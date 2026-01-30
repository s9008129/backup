#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡易差異備份工具 (Simple Delta Backup Tool)
功能：手動備份、差異檢測、檔案恢復、日誌記錄
"""

import os
import sys
import json
import shutil
import hashlib
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
import traceback


class BackupIntegrityError(Exception):
    """備份完整性錯誤"""
    pass


class BackupManifest:
    """備份元資料管理"""
    def __init__(self, manifest_path):
        self.manifest_path = manifest_path
        self.data = self._load()
    
    def _load(self):
        """載入元資料"""
        if os.path.exists(self.manifest_path):
            try:
                with open(self.manifest_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"載入元資料失敗: {e}")
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
    
    def save(self):
        """原子性儲存元資料（使用臨時檔案 + 原子重命名）"""
        try:
            # 使用臨時檔案
            manifest_dir = os.path.dirname(self.manifest_path)
            os.makedirs(manifest_dir, exist_ok=True)
            
            # 建立臨時檔案
            temp_fd, temp_path = tempfile.mkstemp(
                dir=manifest_dir,
                suffix='.tmp',
                prefix='.manifest_'
            )
            
            try:
                # 寫入臨時檔案
                with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=2)
                
                # 驗證臨時檔案有效
                with open(temp_path, 'r', encoding='utf-8') as f:
                    json.load(f)
                
                # 原子重命名（操作系統層級保證）
                os.replace(temp_path, self.manifest_path)
                
            except Exception as e:
                # 清理失敗的臨時檔案
                try:
                    os.close(temp_fd)
                except:
                    pass
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                raise e
                
        except Exception as e:
            raise Exception(f"儲存元資料失敗: {e}")
    
    def get_files_dict(self):
        """取得檔案字典（path -> {size, modified}）"""
        result = {}
        for file_info in self.data.get('filesList', []):
            result[file_info['path']] = {
                'size': file_info['size'],
                'modified': file_info['modified']
            }
        return result
    
    def update(self, source_folder, target_folder, files_info):
        """更新元資料"""
        self.data = {
            "lastBackupTime": datetime.now().isoformat(),
            "sourceFolder": source_folder,
            "targetFolder": target_folder,
            "filesCount": len(files_info),
            "totalSize": sum(f['size'] for f in files_info.values()),
            "filesList": [
                {"path": path, "size": info['size'], "modified": info['modified']}
                for path, info in files_info.items()
            ]
        }
        self.save()
    
    def reset(self):
        """重置元資料（清除備份紀錄）"""
        self.data = self._default_manifest()
        self.save()


class DeltaBackupEngine:
    """差異備份引擎"""
    
    @staticmethod
    def get_file_info(file_path):
        """取得檔案資訊"""
        stat = os.stat(file_path)
        return {
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
    
    @staticmethod
    def scan_folder(folder_path):
        """掃描資料夾並取得所有檔案資訊"""
        result = {}
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, folder_path)
                    try:
                        result[rel_path] = DeltaBackupEngine.get_file_info(file_path)
                    except Exception as e:
                        print(f"無法讀取檔案 {rel_path}: {e}")
            return result
        except Exception as e:
            raise Exception(f"掃描資料夾失敗: {e}")
    
    @staticmethod
    def detect_changes(old_files, new_files):
        """檢測檔案異動"""
        added = {}
        modified = {}
        deleted = {}
        
        # 新增和修改的檔案
        for path, info in new_files.items():
            if path not in old_files:
                added[path] = info
            elif (old_files[path]['size'] != info['size'] or 
                  old_files[path]['modified'] != info['modified']):
                modified[path] = info
        
        # 已刪除的檔案
        for path in old_files:
            if path not in new_files:
                deleted[path] = old_files[path]
        
        return added, modified, deleted
    
    @staticmethod
    def copy_file(src, dst):
        """複製檔案並驗證"""
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        # 複製
        shutil.copy2(src, dst)
        
        # 驗證大小
        src_size = os.path.getsize(src)
        dst_size = os.path.getsize(dst)
        if src_size != dst_size:
            raise Exception(f"檔案驗證失敗: {src} (大小不符)")
    
    @staticmethod
    def delete_file(dst_path):
        """刪除檔案"""
        if os.path.exists(dst_path):
            try:
                os.remove(dst_path)
            except Exception as e:
                raise Exception(f"檔案刪除失敗: {dst_path} - {str(e)}")
    
    @staticmethod
    def verify_backup(source_folder, target_folder, files_to_check):
        """驗證備份完整性"""
        errors = []
        for rel_path in files_to_check:
            src = os.path.join(source_folder, rel_path)
            dst = os.path.join(target_folder, rel_path)
            
            if os.path.exists(src) and os.path.exists(dst):
                if os.path.getsize(src) != os.path.getsize(dst):
                    errors.append(f"大小不符: {rel_path}")
        
        return errors
    
    @staticmethod
    def verify_backup_integrity(manifest_files, backup_folder):
        """驗證備份是否與 manifest 一致 (P1-1)"""
        # 掃描實際備份
        actual_files = DeltaBackupEngine.scan_folder(backup_folder)
        actual_keys = set(actual_files.keys())
        manifest_keys = set(manifest_files.keys())
        
        # 檢查缺失的檔案
        missing = manifest_keys - actual_keys
        if missing:
            missing_list = list(missing)[:5]  # 只顯示前5個
            raise BackupIntegrityError(
                f"❌ 備份不完整: 預期 {len(manifest_keys)} 個檔案，"
                f"實際只有 {len(actual_keys)} 個。"
                f"缺少 {len(missing)} 個檔案。"
                f"示例: {', '.join(missing_list)}"
                + (f" ... 等{len(missing)-5}個" if len(missing) > 5 else "")
            )
        
        return True
    
    @staticmethod
    def check_disk_space(source_folder, target_folder):
        """檢查磁碟空間是否充足 (P1-3)"""
        try:
            # 計算源資料夾總大小
            total_size = sum(
                f['size'] for f in 
                DeltaBackupEngine.scan_folder(source_folder).values()
            )
            
            # 取得目標磁碟可用空間
            available = shutil.disk_usage(target_folder).free
            
            # 保留 20% 緩衝
            required_with_buffer = total_size / 0.8
            
            if required_with_buffer > available:
                available_gb = available / 1e9
                required_gb = required_with_buffer / 1e9
                raise Exception(
                    f"❌ 磁碟空間不足！\n"
                    f"需要: {required_gb:.2f} GB (含 20% 緩衝)\n"
                    f"可用: {available_gb:.2f} GB"
                )
            
            return True
        except Exception as e:
            if isinstance(e, Exception) and "磁碟空間不足" in str(e):
                raise
            raise Exception(f"檢查磁碟空間失敗: {str(e)}")


class BackupLogger:
    """備份日誌管理"""
    def __init__(self, log_path):
        self.log_path = log_path
        self.history = self._load_history()
    
    def _load_history(self):
        """載入歷史紀錄"""
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def add_record(self, record):
        """新增紀錄"""
        self.history.insert(0, record)
        # 只保留最近100筆
        self.history = self.history[:100]
        self._save_history()
    
    def _save_history(self):
        """儲存歷史紀錄"""
        try:
            with open(self.log_path, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def get_recent(self, count=5):
        """取得最近的紀錄"""
        return self.history[:count]


class BackupToolGUI:
    """備份工具GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("簡易差異備份工具 v1.0")
        self.root.geometry("650x750")
        self.root.resizable(False, False)
        
        # 初始化備份引擎
        self.source_folder = tk.StringVar()
        self.target_folder = tk.StringVar()
        self.backup_running = False
        
        # 初始化日誌和清單
        self.log_dir = os.path.expanduser("~\\.backup_tool")
        os.makedirs(self.log_dir, exist_ok=True)
        self.manifest = BackupManifest(os.path.join(self.log_dir, "manifest.json"))
        self.logger = BackupLogger(os.path.join(self.log_dir, "history.json"))
        
        # 載入上次設定
        self._load_settings()
        
        # 構建UI
        self._build_ui()
        
        # 清理過期備份（在主執行緒）
        self.root.after(100, self._cleanup_old_backups)
    
    def _load_settings(self):
        """載入上次的設定"""
        if self.manifest.data.get('sourceFolder'):
            self.source_folder.set(self.manifest.data['sourceFolder'])
        if self.manifest.data.get('targetFolder'):
            self.target_folder.set(self.manifest.data['targetFolder'])
    
    def _build_ui(self):
        """構建使用者介面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === 設定區域 ===
        settings_label = ttk.Label(main_frame, text="📁 設定", font=("微軟正黑體", 11, "bold"))
        settings_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 來源資料夾
        ttk.Label(main_frame, text="來源資料夾：").pack(anchor=tk.W)
        source_frame = ttk.Frame(main_frame)
        source_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Entry(source_frame, textvariable=self.source_folder, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(source_frame, text="瀏覽", width=8, command=self._browse_source).pack(side=tk.LEFT, padx=(5, 0))
        
        # 目標位置
        ttk.Label(main_frame, text="目標位置（外接裝置）：").pack(anchor=tk.W)
        target_frame = ttk.Frame(main_frame)
        target_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Entry(target_frame, textvariable=self.target_folder, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(target_frame, text="瀏覽", width=8, command=self._browse_target).pack(side=tk.LEFT, padx=(5, 0))
        
        # === 操作區域 ===
        action_label = ttk.Label(main_frame, text="🎯 操作", font=("微軟正黑體", 11, "bold"))
        action_label.pack(anchor=tk.W, pady=(0, 5))
        
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.backup_btn = ttk.Button(action_frame, text="開始備份", command=self._on_backup_click, width=20)
        self.backup_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.restore_btn = ttk.Button(action_frame, text="恢復檔案", command=self._on_restore_click, width=20)
        self.restore_btn.pack(side=tk.LEFT)
        
        # === 最新結果區域 ===
        result_label = ttk.Label(main_frame, text="📋 最新結果", font=("微軟正黑體", 11, "bold"))
        result_label.pack(anchor=tk.W, pady=(0, 5))
        
        result_frame = ttk.LabelFrame(main_frame, text="", height=80)
        result_frame.pack(fill=tk.X, pady=(0, 15))
        result_frame.pack_propagate(False)
        
        self.result_text = tk.Text(result_frame, height=4, width=70, font=("Courier New", 9), 
                                   state=tk.DISABLED, wrap=tk.WORD, relief=tk.FLAT, bd=0)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # === 備份歷史區域 ===
        history_label = ttk.Label(main_frame, text="📜 備份歷史（最近5次）", font=("微軟正黑體", 11, "bold"))
        history_label.pack(anchor=tk.W, pady=(0, 5))
        
        history_frame = ttk.LabelFrame(main_frame, text="", height=150)
        history_frame.pack(fill=tk.BOTH, expand=True)
        history_frame.pack_propagate(False)
        
        # 歷史清單（無scrollbar）
        self.history_text = tk.Text(history_frame, height=8, width=70, font=("Courier New", 8),
                                    state=tk.DISABLED, wrap=tk.WORD, relief=tk.FLAT, bd=0)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 初始化結果和歷史顯示
        self._update_result_display()
        self._update_history_display()
    
    def _browse_source(self):
        """瀏覽來源資料夾"""
        folder = filedialog.askdirectory(title="選擇來源資料夾")
        if folder:
            self.source_folder.set(folder)
    
    def _browse_target(self):
        """瀏覽目標資料夾"""
        folder = filedialog.askdirectory(title="選擇目標位置（外接裝置）")
        if folder:
            self.target_folder.set(folder)
    
    def _on_backup_click(self):
        """開始備份按鈕點擊"""
        if self.backup_running:
            messagebox.showwarning("警告", "備份正在進行中，請稍候...")
            return
        
        source = self.source_folder.get().strip()
        target = self.target_folder.get().strip()
        
        if not source or not target:
            messagebox.showerror("錯誤", "請設定來源和目標資料夾")
            return
        
        if not os.path.isdir(source):
            messagebox.showerror("錯誤", f"來源資料夾不存在: {source}")
            return
        
        # 在背景執行備份
        thread = Thread(target=self._backup_worker, args=(source, target), daemon=True)
        thread.start()
    
    def _backup_worker(self, source, target):
        """備份工作執行緒"""
        self.backup_running = True
        self.backup_btn.config(state=tk.DISABLED)
        self.restore_btn.config(state=tk.DISABLED)
        
        record = {
            "timestamp": datetime.now().isoformat(),
            "status": "進行中",
            "changedFiles": 0,
            "error": ""
        }
        
        try:
            # 檢查目標裝置連接
            if not os.path.exists(target):
                raise Exception("❌ 目標位置不存在 - 請檢查外接裝置是否已連接")
            
            # P1-3: 空間預檢查（在複製前驗證）
            try:
                DeltaBackupEngine.check_disk_space(source, target)
            except Exception as e:
                raise Exception(str(e))
            
            # 建立目標資料夾
            backup_folder = os.path.join(target, "backup_data")
            os.makedirs(backup_folder, exist_ok=True)
            
            manifest_path = os.path.join(target, ".backup_manifest")
            manifest = BackupManifest(manifest_path)
            
            # P1-2: 源路徑驗證（防止同步錯誤資料夾）
            stored_source = manifest.data.get('sourceFolder', '')
            if stored_source and stored_source != source:
                # 源路徑已改變
                response = messagebox.askyesno(
                    "⚠️ 來源資料夾已改變",
                    f"來源資料夾已改變：\n"
                    f"舊: {stored_source}\n"
                    f"新: {source}\n\n"
                    f"將執行完整備份（舊備份紀錄會被清除）。\n"
                    f"確認繼續？"
                )
                if response:
                    manifest.reset()  # 清除舊紀錄
                    old_files = {}
                else:
                    raise Exception("使用者取消備份")
            else:
                # P1-1: 備份完整性檢查（驗證上次備份是否真實存在）
                manifest_files = manifest.get_files_dict()
                if manifest_files:  # 只有在有舊紀錄時才檢查
                    try:
                        DeltaBackupEngine.verify_backup_integrity(manifest_files, backup_folder)
                    except BackupIntegrityError as e:
                        # 備份不完整，提醒使用者
                        response = messagebox.askyesno(
                            "⚠️ 備份不完整",
                            f"{str(e)}\n\n"
                            f"備份可能已損毀或被刪除。\n"
                            f"要重新執行完整備份嗎？"
                        )
                        if response:
                            manifest.reset()  # 清除損毀紀錄
                            old_files = {}
                        else:
                            raise Exception("使用者取消備份")
                else:
                    old_files = {}
            
            # 掃描來源資料夾
            new_files = DeltaBackupEngine.scan_folder(source)
            
            # 取得舊的檔案清單（如果尚未取得）
            if 'old_files' not in locals():
                old_files = manifest.get_files_dict()
            
            # 檢測變化
            added, modified, deleted = DeltaBackupEngine.detect_changes(old_files, new_files)
            
            # 複製新增和修改的檔案
            backup_files = {}
            error_list = []
            
            for rel_path in added:
                try:
                    src = os.path.join(source, rel_path)
                    dst = os.path.join(backup_folder, rel_path)
                    DeltaBackupEngine.copy_file(src, dst)
                    backup_files[rel_path] = new_files[rel_path]
                except Exception as e:
                    error_list.append(f"複製失敗: {rel_path} - {str(e)}")
            
            for rel_path in modified:
                try:
                    src = os.path.join(source, rel_path)
                    dst = os.path.join(backup_folder, rel_path)
                    DeltaBackupEngine.copy_file(src, dst)
                    backup_files[rel_path] = new_files[rel_path]
                except Exception as e:
                    error_list.append(f"更新失敗: {rel_path} - {str(e)}")
            
            # 刪除已刪除的檔案（同步策略）
            for rel_path in deleted:
                try:
                    dst = os.path.join(backup_folder, rel_path)
                    DeltaBackupEngine.delete_file(dst)
                except Exception as e:
                    error_list.append(f"刪除失敗: {rel_path} - {str(e)}")
            
            # 記錄所有仍存在的檔案
            for rel_path in new_files:
                if rel_path not in error_list:
                    backup_files[rel_path] = new_files[rel_path]
            
            # 驗證備份
            verify_errors = DeltaBackupEngine.verify_backup(source, backup_folder, added.keys())
            if verify_errors:
                error_list.extend(verify_errors)
            
            # 更新元資料
            manifest.update(source, target, backup_files)
            
            # 記錄成功狀態
            changed_count = len(added) + len(modified) + len(deleted)
            record["status"] = "✅ 備份完成"
            record["changedFiles"] = changed_count
            record["addedFiles"] = len(added)
            record["modifiedFiles"] = len(modified)
            record["deletedFiles"] = len(deleted)
            
            if error_list:
                record["error"] = "; ".join(error_list[:3])  # 只記錄前3個錯誤
                if len(error_list) > 3:
                    record["error"] += f" ... 等{len(error_list)-3}個錯誤"
                record["status"] = "⚠️ 備份完成（有錯誤）"
            
            self.logger.add_record(record)
            
            # 在主執行緒更新UI
            self.root.after(0, self._update_result_display)
            self.root.after(0, self._update_history_display)
            
        except Exception as e:
            record["status"] = "❌ 備份失敗"
            record["error"] = str(e)
            self.logger.add_record(record)
            self.root.after(0, self._update_result_display)
            self.root.after(0, self._update_history_display)
            self.root.after(0, lambda: messagebox.showerror("備份錯誤", str(e)))
        
        finally:
            self.backup_running = False
            self.backup_btn.config(state=tk.NORMAL)
            self.restore_btn.config(state=tk.NORMAL)
    
    def _on_restore_click(self):
        """恢復檔案按鈕點擊"""
        target = self.target_folder.get().strip()
        
        if not target or not os.path.exists(target):
            messagebox.showerror("錯誤", "請先設定並連接目標位置（外接裝置）")
            return
        
        backup_folder = os.path.join(target, "backup_data")
        if not os.path.exists(backup_folder):
            messagebox.showerror("錯誤", "備份資料不存在")
            return
        
        # 開啟恢復嚮導
        self._show_restore_wizard(backup_folder)
    
    def _show_restore_wizard(self, backup_folder):
        """恢復嚮導"""
        restore_window = tk.Toplevel(self.root)
        restore_window.title("恢復檔案")
        restore_window.geometry("600x500")
        
        # 選擇要恢復的資料夾
        ttk.Label(restore_window, text="選擇要恢復的資料夾或檔案：", font=("微軟正黑體", 10, "bold")).pack(anchor=tk.W, padx=10, pady=10)
        
        # 檔案樹
        tree_frame = ttk.Frame(restore_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(tree_frame, height=15)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # 填充檔案樹
        def populate_tree(parent, path, item=''):
            for item_name in os.listdir(path):
                item_path = os.path.join(path, item_name)
                node = tree.insert(item, 'end', text=item_name, open=False)
                if os.path.isdir(item_path):
                    populate_tree(item_path, node)
        
        try:
            populate_tree('', backup_folder)
        except:
            messagebox.showerror("錯誤", "無法讀取備份資料")
            restore_window.destroy()
            return
        
        # 選擇目標位置
        ttk.Label(restore_window, text="恢復到：", font=("微軟正黑體", 10)).pack(anchor=tk.W, padx=10)
        
        restore_to = tk.StringVar()
        restore_frame = ttk.Frame(restore_window)
        restore_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Entry(restore_frame, textvariable=restore_to, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        def browse_restore():
            folder = filedialog.askdirectory(title="選擇恢復位置")
            if folder:
                restore_to.set(folder)
        
        ttk.Button(restore_frame, text="瀏覽", width=8, command=browse_restore).pack(side=tk.LEFT, padx=(5, 0))
        
        # 恢復按鈕
        button_frame = ttk.Frame(restore_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def do_restore():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("警告", "請選擇要恢復的項目")
                return
            
            restore_path = restore_to.get().strip()
            if not restore_path:
                messagebox.showwarning("警告", "請選擇恢復位置")
                return
            
            # 簡單實現：複製選中項目
            try:
                for item in selection:
                    item_text = tree.item(item, 'text')
                    src_path = os.path.join(backup_folder, item_text)
                    dst_path = os.path.join(restore_path, item_text)
                    
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                        shutil.copy2(src_path, dst_path)
                
                messagebox.showinfo("成功", "檔案恢復完成")
                restore_window.destroy()
            except Exception as e:
                messagebox.showerror("錯誤", f"恢復失敗: {str(e)}")
        
        ttk.Button(button_frame, text="確認恢復", command=do_restore).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=restore_window.destroy).pack(side=tk.LEFT)
    
    def _update_result_display(self):
        """更新最新結果顯示"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        records = self.logger.get_recent(1)
        if records:
            record = records[0]
            time_str = datetime.fromisoformat(record['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            added_str = str(record.get('addedFiles', 0))
            modified_str = str(record.get('modifiedFiles', 0))
            deleted_str = str(record.get('deletedFiles', 0))
            status_str = record.get('status', '未知')
            error_str = record.get('error', '無')
            
            text = f"日期時間: {time_str}\n"
            text += f"新增: {added_str} | 修改: {modified_str} | 刪除: {deleted_str}\n"
            text += f"狀態: {status_str} | 錯誤: {error_str}"
            
            self.result_text.insert(1.0, text)
        else:
            self.result_text.insert(1.0, "還未執行過備份")
        
        self.result_text.config(state=tk.DISABLED)
    
    def _update_history_display(self):
        """更新歷史記錄顯示"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        records = self.logger.get_recent(5)
        if records:
            for record in records:
                time_str = datetime.fromisoformat(record['timestamp']).strftime("%m-%d %H:%M")
                added_str = str(record.get('addedFiles', 0))
                modified_str = str(record.get('modifiedFiles', 0))
                deleted_str = str(record.get('deletedFiles', 0))
                status_str = record.get('status', '未知')
                
                line = f"{time_str} | 新+{added_str} 改~{modified_str} 刪-{deleted_str} | {status_str}\n"
                self.history_text.insert(tk.END, line)
        else:
            self.history_text.insert(1.0, "暫無歷史記錄")
        
        self.history_text.config(state=tk.DISABLED)
    
    def _cleanup_old_backups(self):
        """清理超過1年的備份"""
        try:
            target = self.target_folder.get().strip()
            if not target or not os.path.exists(target):
                return
            
            backup_folder = os.path.join(target, "backup_data")
            if not os.path.exists(backup_folder):
                return
            
            one_year_ago = datetime.now() - timedelta(days=365)
            
            for root, dirs, files in os.walk(backup_folder, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if file_time < one_year_ago:
                            os.remove(file_path)
                    except:
                        pass
        except:
            pass


def main():
    root = tk.Tk()
    app = BackupToolGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
