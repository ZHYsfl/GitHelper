import tkinter as tk
from tkinter import filedialog, messagebox
from git import Repo, GitCommandError
import os
import subprocess

class GitHelper:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Git助手")
        self.window.geometry("600x500")  # 增加窗口高度
        
        # 仓库路径
        self.repo_path = None
        
        # 创建主框架
        self.main_frame = tk.Frame(self.window, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill='both')
        
        # 选择仓库按钮
        self.select_button = tk.Button(
            self.main_frame,
            text="选择代码文件夹",
            command=self.select_repository,
            height=2
        )
        self.select_button.pack(fill='x', pady=5)
        
        # 显示当前路径
        self.path_label = tk.Label(self.main_frame, text="当前未选择仓库", wraplength=500)
        self.path_label.pack(pady=10)
        
        # Git操作按钮
        self.init_button = tk.Button(
            self.main_frame,
            text="初始化Git仓库",
            command=self.init_repository,
            height=2
        )
        self.init_button.pack(fill='x', pady=5)
        
        # 设置远程仓库（移到这里）
        self.remote_frame = tk.Frame(self.main_frame)
        self.remote_frame.pack(fill='x', pady=5)
        
        self.remote_label = tk.Label(self.remote_frame, text="远程仓库URL：")
        self.remote_label.pack(side='left')
        
        self.remote_entry = tk.Entry(self.remote_frame)
        self.remote_entry.pack(side='left', expand=True, fill='x')
        
        self.set_remote_button = tk.Button(
            self.main_frame,
            text="设置远程仓库 (git remote add origin)",
            command=self.set_remote,
            height=2
        )
        self.set_remote_button.pack(fill='x', pady=5)
        
        self.add_button = tk.Button(
            self.main_frame,
            text="添加所有更改 (git add .)",
            command=self.add_all,
            height=2
        )
        self.add_button.pack(fill='x', pady=5)
        
        # Commit信息输入框
        self.commit_frame = tk.Frame(self.main_frame)
        self.commit_frame.pack(fill='x', pady=5)
        
        self.commit_label = tk.Label(self.commit_frame, text="提交信息：")
        self.commit_label.pack(side='left')
        
        self.commit_entry = tk.Entry(self.commit_frame)
        self.commit_entry.pack(side='left', expand=True, fill='x')
        
        self.commit_button = tk.Button(
            self.main_frame,
            text="提交更改 (git commit)",
            command=self.commit,
            height=2
        )
        self.commit_button.pack(fill='x', pady=5)
        
        # 指定推送分支的输入框
        self.branch_frame = tk.Frame(self.main_frame)
        self.branch_frame.pack(fill='x', pady=5)
        
        self.branch_label = tk.Label(self.branch_frame, text="推送到分支：")
        self.branch_label.pack(side='left')
        
        self.branch_entry = tk.Entry(self.branch_frame)
        self.branch_entry.pack(side='left', expand=True, fill='x')
        
        # Push按钮
        self.push_button = tk.Button(
            self.main_frame,
            text="推送到GitHub (git push)",
            command=self.push,
            height=2
        )
        self.push_button.pack(fill='x', pady=5)

    def select_repository(self):
        self.repo_path = filedialog.askdirectory()
        if self.repo_path:
            self.path_label.config(text=f"当前选择的文件夹: {self.repo_path}")
    
    def init_repository(self):
        if not self.repo_path:
            messagebox.showerror("错误", "请先选择代码文件夹！")
            return
        
        try:
            # 检查是否已经是Git仓库
            if os.path.exists(os.path.join(self.repo_path, '.git')):
                messagebox.showinfo("提示", "该文件夹已经是Git仓库，无需重新初始化！")
                return
                    
            Repo.init(self.repo_path)
            messagebox.showinfo("成功", "Git仓库初始化成功！")
        except Exception as e:
            messagebox.showerror("错误", f"初始化失败：{str(e)}")
    
    def add_all(self):
        if not self.repo_path:
            messagebox.showerror("错误", "请先选择代码文件夹！")
            return
        
        try:
            repo = Repo(self.repo_path)
            repo.git.add('.');
            messagebox.showinfo("成功", "已添加所有更改！")
        except Exception as e:
            messagebox.showerror("错误", f"添加失败：{str(e)}")
    
    def commit(self):
        if not self.repo_path:
            messagebox.showerror("错误", "请先选择代码文件夹！")
            return
        
        commit_message = self.commit_entry.get()
        if not commit_message:
            messagebox.showerror("错误", "请输入提交信息！")
            return
        
        try:
            repo = Repo(self.repo_path)
            repo.index.commit(commit_message)
            messagebox.showinfo("成功", "提交成功！")
            self.commit_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("错误", f"提交失败：{str(e)}")
    
    def push(self):
        if not self.repo_path:
            messagebox.showerror("错误", "请先选择代码文件夹！")
            return
        
        branch_name = self.branch_entry.get() or 'main'  # 改为默认main分支
        
        try:
            repo = Repo(self.repo_path)
            
            # 检查是否设置了远程仓库
            try:
                origin = repo.remote(name='origin')
            except ValueError:
                messagebox.showerror("错误", "未设置远程仓库，请先设置远程仓库！")
                return

            # 检查当前分支是否有提交
            if not repo.heads:
                messagebox.showerror("错误", "仓库中没有任何提交，请先进行提交！")
                return

            # 检查工作区是否干净
            if repo.is_dirty():
                messagebox.showerror("错误", "有未提交的更改，请先提交更改！")
                return

            try:
                # 确保分支存在或创建新分支
                if branch_name not in repo.branches:
                    repo.git.checkout('-b', branch_name)
                else:
                    repo.heads[branch_name].checkout()

                # 使用subprocess执行git命令，这样可以看到详细的错误信息
                try:
                    # 首次推送，设置上游分支
                    push_command = ['git', 'push', '-u', 'origin', branch_name]
                    result = subprocess.run(
                        push_command,
                        cwd=self.repo_path,
                        capture_output=True,
                        text=True,
                        check=True  # 这会在命令失败时抛出异常
                    )
                    
                    if "Everything up-to-date" in result.stderr:
                        messagebox.showinfo("提示", "所有更改已经是最新的，无需推送")
                    else:
                        messagebox.showinfo("成功", f"成功推送到远程仓库的 {branch_name} 分支！")
                
                except subprocess.CalledProcessError as e:
                    error_output = e.stderr.lower()
                    if "repository not found" in error_output:
                        messagebox.showerror("错误", "找不到远程仓库，请检查仓库URL是否正确")
                    elif "permission denied" in error_output:
                        messagebox.showerror("错误", "权限被拒绝，请检查SSH密钥配置")
                    elif "rejected" in error_output:
                        # 如果推送被拒绝，尝试先拉取
                        try:
                            repo.git.pull('origin', branch_name, '--allow-unrelated-histories')
                            # 再次尝试推送
                            repo.git.push('--set-upstream', 'origin', branch_name)
                            messagebox.showinfo("成功", "成功推送到远程仓库！")
                        except Exception as pull_error:
                            messagebox.showerror("错误", f"拉取/推送失败：{str(pull_error)}")
                    else:
                        messagebox.showerror("错误", f"推送失败：{e.stderr}")
                
            except Exception as e:
                messagebox.showerror("错误", f"分支操作失败：{str(e)}")
                
        except Exception as e:
            messagebox.showerror("错误", f"操作失败：{str(e)}")
            
    def set_remote(self):
        if not self.repo_path:
            messagebox.showerror("错误", "请先选择代码文件夹！")
            return
        
        remote_url = self.remote_entry.get()
        if not remote_url:
            messagebox.showerror("错误", "请输入远程仓库URL！")
            return
        
        try:
            repo = Repo(self.repo_path)
            # 检查是否已经存在远程仓库
            if 'origin' in [remote.name for remote in repo.remotes]:
                # 如果存在，先删除再添加
                repo.delete_remote('origin')
            
            # 测试远程连接
            try:
                subprocess.check_output(['git', 'ls-remote', remote_url], stderr=subprocess.STDOUT)
                repo.create_remote('origin', remote_url)
                messagebox.showinfo("成功", "远程仓库设置成功！")
            except subprocess.CalledProcessError as e:
                if "Permission denied" in str(e.output):
                    messagebox.showerror("错误", "权限被拒绝，请检查SSH密钥配置")
                else:
                    messagebox.showerror("错误", "远程仓库URL无效或无法访问！")
        except Exception as e:
            messagebox.showerror("错误", f"设置远程仓库失败：{str(e)}")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = GitHelper()
    app.run() 

#git@github.com:ZHYsfl/xxxxxxxx.git