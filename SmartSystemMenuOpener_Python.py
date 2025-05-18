import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys
import os
import platform
import webbrowser
import threading

class SmartSystemMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartSystemMenuOpener")
        self.root.geometry("800x500")
        self.root.resizable(True, True)
        
        # 设置中文字体
        self.font_family = "SimHei"
        
        # 用户信息
        self.username = "admin"
        self.password = "password"
        
        # 下载设置
        self.download_url = tk.StringVar(value="https://example.com/sample.zip")
        self.save_path = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads", "downloaded_file.zip"))
        
        # 检查系统兼容性
        self.system_info = self.get_system_info()
        
        # 显示登录页面
        self.show_login_page()
    
    def get_system_info(self):
        """获取系统信息"""
        system = platform.system()
        release = platform.release()
        version = platform.version()
        
        if system != "Windows":
            return f"不支持的系统: {system}"
        
        # 判断Windows版本
        win_version = "未知"
        if "10.0" in version:
            win_version = "Windows 10/11"
        elif "6.1" in version:
            win_version = "Windows 7"
        elif "6.0" in version:
            win_version = "Windows Vista"
        elif "6.2" in version or "6.3" in version:
            win_version = "Windows 8/8.1"
        
        return f"Windows {win_version} ({version})"
    
    def show_login_page(self):
        """显示登录页面"""
        # 清除现有窗口
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 创建登录框架
        login_frame = tk.Frame(self.root, padx=20, pady=20)
        login_frame.pack(expand=True)
        
        # 标题
        tk.Label(login_frame, text="SmartSystemMenuOpener", font=(self.font_family, 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        # 用户名
        tk.Label(login_frame, text="用户名:", font=(self.font_family, 12)).grid(row=1, column=0, sticky="e", pady=10)
        username_entry = tk.Entry(login_frame, font=(self.font_family, 12))
        username_entry.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
        
        # 密码
        tk.Label(login_frame, text="密码:", font=(self.font_family, 12)).grid(row=2, column=0, sticky="e", pady=10)
        password_entry = tk.Entry(login_frame, show="*", font=(self.font_family, 12))
        password_entry.grid(row=2, column=1, pady=10, padx=10, sticky="ew")
        
        # 登录按钮
        login_button = tk.Button(login_frame, text="登录", font=(self.font_family, 12), 
                               command=lambda: self.check_login(username_entry.get(), password_entry.get()))
        login_button.grid(row=3, column=0, columnspan=2, pady=20, ipadx=20)
        
        # 系统信息
        tk.Label(login_frame, text=self.system_info, font=(self.font_family, 10), fg="gray").grid(row=4, column=0, columnspan=2, pady=10)
        
        # 设置列宽
        login_frame.columnconfigure(1, weight=1)
    
    def check_login(self, username, password):
        """验证登录信息"""
        if username == self.username and password == self.password:
            self.show_main_page()
        else:
            messagebox.showerror("登录失败", "用户名或密码错误")
    
    def show_main_page(self):
        """显示主页面"""
        # 清除现有窗口
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 创建主框架
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建菜单栏
        self.create_menu(main_frame)
        
        # 初始显示系统菜单页面
        self.show_system_menu_page()
    
    def create_menu(self, parent):
        """创建菜单栏"""
        menu_frame = tk.Frame(parent, bg="#f0f0f0", height=40)
        menu_frame.pack(fill=tk.X)
        
        # 系统菜单按钮
        tk.Button(menu_frame, text="系统菜单", font=(self.font_family, 10), 
                 command=self.show_system_menu_page, bg="#f0f0f0", 
                 relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5, pady=5)
        
        # 下载管理按钮
        tk.Button(menu_frame, text="下载管理", font=(self.font_family, 10), 
                 command=self.show_download_manager_page, bg="#f0f0f0", 
                 relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5, pady=5)
        
        # 系统信息按钮
        tk.Button(menu_frame, text="系统信息", font=(self.font_family, 10), 
                 command=self.show_system_info_page, bg="#f0f0f0", 
                 relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5, pady=5)
        
        # 退出按钮
        tk.Button(menu_frame, text="退出", font=(self.font_family, 10), 
                 command=self.root.quit, bg="#f0f0f0", 
                 relief=tk.FLAT, padx=10).pack(side=tk.RIGHT, padx=5, pady=5)
    
    def show_system_menu_page(self):
        """显示系统菜单页面"""
        self.clear_content_frame()
        
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        tk.Label(content_frame, text="Smart System Menu", font=(self.font_family, 16, "bold")).pack(pady=20)
        
        # 描述
        description = """
        Smart System Menu 是 Windows 系统提供的一个便捷菜单，
        可以快速访问系统设置、任务管理器和其他系统功能。
        """
        tk.Label(content_frame, text=description, font=(self.font_family, 12), justify=tk.LEFT).pack(pady=10)
        
        # 系统菜单启动按钮
        start_button = tk.Button(content_frame, text="打开 Smart System Menu", font=(self.font_family, 14), 
                               command=self.open_smart_system_menu, bg="#4CAF50", fg="white", padx=20, pady=10)
        start_button.pack(pady=30)
        
        # 替代方法
        tk.Label(content_frame, text="替代方法:", font=(self.font_family, 12, "bold")).pack(anchor=tk.W, pady=(20, 5))
        
        # 命令提示符方法
        cmd_frame = tk.Frame(content_frame)
        cmd_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(cmd_frame, text="1. 在命令提示符中输入:", font=(self.font_family, 10)).pack(side=tk.LEFT, padx=5)
        
        cmd_text = "explorer.exe shell:::{BB06C0E4-D293-4f75-8A90-CB05B6477EEE}"
        cmd_entry = tk.Entry(cmd_frame, font=(self.font_family, 10), width=60)
        cmd_entry.insert(0, cmd_text)
        cmd_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(cmd_frame, text="复制", font=(self.font_family, 10), 
                command=lambda: self.root.clipboard_append(cmd_text)).pack(side=tk.LEFT, padx=5)
        
        # 快捷方式方法
        shortcut_frame = tk.Frame(content_frame)
        shortcut_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(shortcut_frame, text="2. 创建快捷方式:", font=(self.font_family, 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(shortcut_frame, text="生成快捷方式", font=(self.font_family, 10), 
                command=self.create_shortcut).pack(side=tk.LEFT, padx=5)
    
    def show_download_manager_page(self):
        """显示下载管理页面"""
        self.clear_content_frame()
        
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        tk.Label(content_frame, text="下载管理器", font=(self.font_family, 16, "bold")).pack(pady=20)
        
        # 下载链接
        url_frame = tk.Frame(content_frame)
        url_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(url_frame, text="下载链接:", font=(self.font_family, 12)).pack(side=tk.LEFT, padx=5, pady=5)
        
        url_entry = tk.Entry(url_frame, textvariable=self.download_url, font=(self.font_family, 12), width=50)
        url_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        tk.Button(url_frame, text="更改", font=(self.font_family, 10), 
                command=self.change_download_url).pack(side=tk.LEFT, padx=5, pady=5)
        
        # 保存路径
        path_frame = tk.Frame(content_frame)
        path_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(path_frame, text="保存路径:", font=(self.font_family, 12)).pack(side=tk.LEFT, padx=5, pady=5)
        
        path_entry = tk.Entry(path_frame, textvariable=self.save_path, font=(self.font_family, 12), width=50)
        path_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        tk.Button(path_frame, text="更改", font=(self.font_family, 10), 
                command=self.change_save_path).pack(side=tk.LEFT, padx=5, pady=5)
        
        # 下载按钮
        download_button = tk.Button(content_frame, text="开始下载", font=(self.font_family, 14), 
                                  command=self.start_download, bg="#2196F3", fg="white", padx=20, pady=10)
        download_button.pack(pady=30)
        
        # 下载进度
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(content_frame, variable=self.progress_var, length=500, mode='determinate')
        progress_bar.pack(pady=10)
        
        self.status_var = tk.StringVar(value="就绪")
        tk.Label(content_frame, textvariable=self.status_var, font=(self.font_family, 10)).pack(pady=5)
    
    def show_system_info_page(self):
        """显示系统信息页面"""
        self.clear_content_frame()
        
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        tk.Label(content_frame, text="系统信息", font=(self.font_family, 16, "bold")).pack(pady=20)
        
        # 系统信息内容
        info_text = f"""
        操作系统: {self.system_info}
        
        Smart System Menu 支持情况:
        """
        
        # 判断系统是否支持Smart System Menu
        if "Windows" in self.system_info:
            if "Windows 11" in self.system_info:
                support_status = "部分支持（Windows 11已简化系统菜单）"
            else:
                support_status = "完全支持"
        else:
            support_status = "不支持（非Windows系统）"
        
        info_text += f"  {support_status}\n\n"
        
        # 添加Python版本信息
        info_text += f"Python 版本: {platform.python_version()}\n\n"
        
        # 添加其他系统信息
        info_text += f"计算机名称: {platform.node()}\n"
        info_text += f"处理器: {platform.processor()}\n"
        info_text += f"架构: {platform.architecture()[0]}\n"
        
        # 创建文本框显示信息
        info_textbox = tk.Text(content_frame, font=(self.font_family, 12), width=60, height=15)
        info_textbox.insert(tk.END, info_text)
        info_textbox.config(state=tk.DISABLED)
        info_textbox.pack(pady=10)
        
        # 刷新按钮
        refresh_button = tk.Button(content_frame, text="刷新信息", font=(self.font_family, 12), 
                                 command=self.show_system_info_page)
        refresh_button.pack(pady=20)
    
    def clear_content_frame(self):
        """清除内容框架"""
        for widget in self.root.winfo_children():
            if widget.winfo_class() != "Menu":
                widget.destroy()
    
    def open_smart_system_menu(self):
        """打开Smart System Menu"""
        try:
            # 检查是否为Windows系统
            if platform.system() != "Windows":
                messagebox.showerror("错误", "Smart System Menu 仅适用于Windows系统")
                return
            
            # 执行命令打开Smart System Menu
            subprocess.run(["explorer.exe", "shell:::{BB06C0E4-D293-4f75-8A90-CB05B6477EEE}"])
            
            # 显示成功消息
            messagebox.showinfo("成功", "Smart System Menu 已打开")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开 Smart System Menu: {str(e)}")
    
    def create_shortcut(self):
        """创建快捷方式"""
        try:
            # 检查是否为Windows系统
            if platform.system() != "Windows":
                messagebox.showerror("错误", "快捷方式功能仅适用于Windows系统")
                return
            
            # 导入必要的模块
            import winreg
            from winreg import HKEY_CURRENT_USER
            
            # 创建快捷方式
            shortcut_path = os.path.join(os.path.expanduser("~"), "Desktop", "Smart System Menu.lnk")
            target = "explorer.exe shell:::{BB06C0E4-D293-4f75-8A90-CB05B6477EEE}"
            
            # 使用VBScript创建快捷方式
            vbs_script = f'''
            Set WshShell = CreateObject("WScript.Shell")
            Set Shortcut = WshShell.CreateShortcut("{shortcut_path}")
            Shortcut.TargetPath = "explorer.exe"
            Shortcut.Arguments = "shell:::{BB06C0E4-D293-4f75-8A90-CB05B6477EEE}"
            Shortcut.Description = "Smart System Menu"
            Shortcut.Save
            '''
            
            # 保存VBScript临时文件
            temp_vbs = os.path.join(os.environ['TEMP'], "createshortcut.vbs")
            with open(temp_vbs, "w") as f:
                f.write(vbs_script)
            
            # 执行VBScript
            subprocess.run(["cscript", "/nologo", temp_vbs])
            
            # 删除临时文件
            os.remove(temp_vbs)
            
            messagebox.showinfo("成功", f"快捷方式已创建在桌面: Smart System Menu.lnk")
        except Exception as e:
            messagebox.showerror("错误", f"无法创建快捷方式: {str(e)}")
    
    def change_download_url(self):
        """更改下载链接"""
        current_url = self.download_url.get()
        new_url = tk.simpledialog.askstring("更改下载链接", "请输入新的下载链接:", initialvalue=current_url)
        
        if new_url:
            self.download_url.set(new_url)
            messagebox.showinfo("成功", "下载链接已更新")
    
    def change_save_path(self):
        """更改保存路径"""
        current_path = self.save_path.get()
        new_path = tk.simpledialog.askstring("更改保存路径", "请输入新的保存路径:", initialvalue=current_path)
        
        if new_path:
            self.save_path.set(new_path)
            messagebox.showinfo("成功", "保存路径已更新")
    
    def start_download(self):
        """开始下载"""
        url = self.download_url.get()
        path = self.save_path.get()
        
        if not url:
            messagebox.showerror("错误", "请输入有效的下载链接")
            return
        
        if not path:
            messagebox.showerror("错误", "请输入有效的保存路径")
            return
        
        # 创建保存目录（如果不存在）
        save_dir = os.path.dirname(path)
        if not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir)
            except:
                messagebox.showerror("错误", f"无法创建保存目录: {save_dir}")
                return
        
        # 显示下载中状态
        self.status_var.set("下载中...")
        self.progress_var.set(0)
        
        # 在新线程中执行下载，避免阻塞UI
        download_thread = threading.Thread(target=self.download_file, args=(url, path))
        download_thread.daemon = True
        download_thread.start()
    
    def download_file(self, url, path):
        """下载文件（在后台线程中执行）"""
        try:
            # 检查是否有requests库
            try:
                import requests
            except ImportError:
                # 如果没有requests库，使用webbrowser打开链接
                webbrowser.open(url)
                self.status_var.set("已在浏览器中打开下载链接")
                self.progress_var.set(100)
                return
            
            # 使用requests下载文件并显示进度
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            downloaded_size = 0
            
            with open(path, 'wb') as file:
                for data in response.iter_content(block_size):
                    downloaded_size += len(data)
                    file.write(data)
                    progress = (downloaded_size / total_size) * 100
                    
                    # 更新UI（需要在主线程中执行）
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                    self.root.after(0, lambda s=f"下载中: {downloaded_size//1024}/{total_size//1024} KB": self.status_var.set(s))
            
            self.root.after(0, lambda: self.status_var.set("下载完成"))
            self.root.after(0, lambda: messagebox.showinfo("成功", f"文件已下载到: {path}"))
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set("下载失败"))
            self.root.after(0, lambda: messagebox.showerror("错误", f"下载失败: {str(e)}"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartSystemMenuApp(root)
    root.mainloop()
