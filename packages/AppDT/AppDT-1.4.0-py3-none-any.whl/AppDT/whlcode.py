s4y1lh4w=1 #此处是调试点，如需调试，请将等号后面的数字改为您要调试的模块序号（默认第一个）

def adt():
    from PyQt5.QtWidgets import QApplication, QFileDialog
    
    def open_file_dialog():
        # 创建QApplication实例（这是必需的）
        app = QApplication([])
        # 弹出文件选择窗口
        file_path, _ = QFileDialog.getOpenFileName(None, "请选择icon图标", "", "icon图标 (*.ico);;")
        
        
    
        # 这里可以添加处理文件路径的代码
        if file_path:
            return file_path
    
        # 注意：在这个示例中，主窗口实际上并没有显示，所以我们不需要显式地关闭它
        # 如果你想要在某个时候显示主窗口，你可以调用 root.deiconify() 来恢复它
    def open_file_dialog2():
        # 创建QApplication实例（这是必需的）
        app = QApplication([])
        # 弹出文件选择窗口
        file_path, _ = QFileDialog.getOpenFileName(None, "请选择包含简介和声明的文件", "", "Text Files (*.txt);;Markdown Files (*.md);;All Files (*.*)")
        
        
    
        # 这里可以添加处理文件路径的代码
        if file_path:
            return file_path
    
        # 注意：在这个示例中，主窗口实际上并没有显示，所以我们不需要显式地关闭它
        # 如果你想要在某个时候显示主窗口，你可以调用 root.deiconify() 来恢复它
    
    import os
    sysdir22=os.getenv("SystemDrive")+"\\"
        
    import random
    import re
    while True:

        def extract_integer_after_minus(s):
            # 正则表达式匹配减号后的整数
            pattern = r'-(\d+)'
            match = re.search(pattern, s)
            if match:
                return int(match.group(1))  # 返回整数
            else:
                return None  # 如果没有匹配到则返回None
        print("欢迎使用软件开发和生成安装包工具（App Development Tools），作者：xumouren225588")
        atype_list=["[1]新建","[2]打开","[3]封装","[4]删除项目","[5]打开作者主页"]
        for b in range(len(atype_list)):
            print(atype_list[b])
        atype=str(input("请输入您要选择的功能前的序号："))

        if atype=="1":
            importname_list=[]
            filename=None
            V=None
            while True:
                filename=str(input("请输入您要创建的项目的名称："))
                def contains_invalid_chars(s):
                    # 正则表达式匹配除数字、大小写英文字母和下划线以外的字符
                    pattern = r'[^0-9a-zA-Z_]'
                    return re.search(pattern, s) is not None
         
                def starts_with_digit(s):
                    # 正则表达式匹配以数字开头的字符串
                    pattern = r'^[0-9].*'
                    return re.match(pattern, s) is not None
                a=contains_invalid_chars(filename)
                b=starts_with_digit(filename)
                if a or b or not(filename):
                    print("您输入的内容包含其他符号或者以数字开头或为空！")
                else:
                    break
            while True:
                V=input("请输入您要创建的项目的版本号（示例：1.1.2 禁止输入非数字或小数点字符）：")
                def contains_non_numeric_characters(s):
                    return not re.match(r'^[0-9.]*$', s)
                c=contains_non_numeric_characters(V)
                if c:
                    print("输入了非数字或小数点字符！")
                else:
                    break
            
            ifenter=input("请按回车键开始构建")
    
            
            
     
            
     
    
            print("正在构建……")
            
     
            # 创建进度条对象，初始化时设置总迭代次数
            
              # 增加进度条的进度
            try:
                os.mkdir(sysdir22+'项目')
            except FileExistsError:
                None
    
            # 关闭进度条
    
            try:
                os.makedirs(sysdir22+'软件项目\\'+filename,exist_ok=True)
            except FileExistsError:
                print('文件夹已存在')
            
    
            
            
            
            
            
           
            
            with open(sysdir22+'软件项目\\'+filename+'\\'+filename+".py","w",encoding="utf-8") as f:
                f.write("")
                
            
    
    
            with open(sysdir22+'软件项目\\'+filename+'\\'+"规格参数.txt","w",encoding='utf-8') as f:
                f.write(filename+'\n')
                f.write(str(V)+'\n')
                
            print("构建完成！")
            
            import subprocess
    
            
            first_subfolder2 = sysdir22+'软件项目\\'+filename+'\\'
    
            # 判断操作系统，选择合适的命令
    
            
    
            # 获取当前工作目录
    
     
            # 打开资源管理器并导航到当前工作目录
            subprocess.run(['explorer', first_subfolder2])
    
        elif atype=="2":
    

            # 指定要检查的文件夹路径
            folder_path = sysdir22+'软件项目\\'
     
            # 检查文件夹是否存在
            if os.path.exists(folder_path):
        
    
                from pathlib import Path
         
                def get_folder_paths(base_dir):
                    """
                    获取给定目录下所有子文件夹的路径
                    """
                    return [str(p) for p in Path(base_dir).iterdir() if p.is_dir()]
         
                def select_folder_by_number(base_dir):
                    """
                    通过控制台输入序号选择文件夹
                    """
                    folder_paths = get_folder_paths(base_dir)
                    for i, folder_path in enumerate(folder_paths, 1):
                        print(f"{i}. {folder_path}")
            
                    while True:
                        try:
                            selection = input("请输入序号选择文件夹: ")
                    
                    
                            index = int(selection) - 1
                            if 0 <= index < len(folder_paths):
                                return folder_paths[index]
                            else:
                                print("无效的序号，请重新输入。")
                        except ValueError:
                            print("非法输入，请输入一个整数。")
         
                base_dir = sysdir22+'软件项目\\'  # 替换为您的基础目录路径
                selected_folder = select_folder_by_number(base_dir)
        
         
                # 打开资源管理器并导航到当前工作目录
                subprocess.run(['explorer', selected_folder])
            else:
                print("无项目")
    
        elif atype=="3":
            import os

            # 指定要检查的文件夹路径
            folder_path = sysdir22+'软件项目\\'
     
            # 检查文件夹是否存在
            if os.path.exists(folder_path):
        
                from pathlib import Path
         
                def get_folder_paths(base_dir):
                    """
                    获取给定目录下所有子文件夹的路径
                    """
                    return [str(p) for p in Path(base_dir).iterdir() if p.is_dir()]
         
                def select_folder_by_number(base_dir):
                    """
                    通过控制台输入序号选择文件夹
                    """
                    folder_paths = get_folder_paths(base_dir)
                    for i, folder_path in enumerate(folder_paths, 1):
                        print(f"{i}. {folder_path}")
            
                    while True:
                        try:
                            selection = input("请输入序号选择文件夹: ")
                    
                    
                            index = int(selection) - 1
                            if 0 <= index < len(folder_paths):
                                return folder_paths[index]
                            else:
                                print("无效的序号，请重新输入。")
                        except ValueError:
                            print("非法输入，请输入一个整数。")
         
                base_dir = sysdir22+'软件项目\\'  # 替换为您的基础目录路径
                selected_folder = select_folder_by_number(base_dir)
                cs35=selected_folder+"\\规格参数.txt"
                wdesktop=input("请输入您的项目的主程序在项目文件夹里的相对路径（包含后缀名）：")
                print("请选择您要添加的功能")
                def choose_set():
                    # 示例列表
                    items = ["生成快捷方式", "添加启动项", "设置安装程序图标", "添加声明文件"]
                    # 用于存储选中状态的字典，键为列表索引，值为True/False
                    selected = {i: False for i in range(len(items))}
                
                    while True:
                        # 清除屏幕（注意：在Windows中可能需要使用os.system('cls')）
                        
                        i2=1
                        # 显示列表和选中状态
                        for i, item in enumerate(items):
                            if selected[i]:
                                print("→"+str(i2)+item)
                            else:
                                print(" "+str(i2)+item)
                            i2+=1
                        # 允许用户输入
                        user_input = input("请输入序号选择项目（输入减号加序号清除选中，输入y保存并退出）：").strip()
                
                        # 处理用户输入
                        if user_input.lower() == 'y':
                            print("已保存选中项。")
                            return list(selected.values())
                            break
                        elif user_input.startswith('-'):
                            # 尝试清除选中状态
                            try:
                                index = int(user_input[1:])-1
                                if 0 <= index < len(items):
                                    selected[index] = False
                                else:
                                    print("无效的序号，请输入有效的序号。")
                            except ValueError:
                                print("无效的输入，请输入序号或y。")
                        else:
                            # 尝试选中项目
                            try:
                                index = int(user_input)-1
                                if 0 <= index < len(items):
                                    selected[index] = not selected[index]  # 切换选中状态
                                else:
                                    print("无效的序号，请输入有效的序号。")
                            except ValueError:
                                print("无效的输入，请输入序号或y。")

                set_list=choose_set()
                with open(cs35, "r", encoding='utf-8') as f:
                    lines = [line.rstrip('\n') for line in f]
                prname=lines[0]
                vers=lines[1]
                code1=None
                code2=None
                fp2=None
                fp3=None
                if set_list[0]:
                    code1=f"""
            import subprocess
            import os
            exe_name = os.path.join(extract_path, "{prname}\\\\{wdesktop}")
            # 创建一个VBScript脚本来创建快捷方式
            vbs_script = '''


Set oShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
' 指定文件的完整路径
strTargetFile = "%s"
' 快捷方式的完整路径和文件名
strShortcutPath = CreateObject("WScript.Shell").ExpandEnvironmentStrings("%%USERPROFILE%%") & "\\\\Desktop\\\\%s.lnk"
 
' 创建快捷方式
Set oShortcut = oShell.CreateShortcut(strShortcutPath)
 
' 设置快捷方式属性
oShortcut.TargetPath = strTargetFile
oShortcut.WindowStyle = 1 ' 正常窗口
oShortcut.Description = "%s"
oShortcut.WorkingDirectory = ""
 
' 保存快捷方式
oShortcut.Save
 
Set oShortcut = Nothing
Set oShell = Nothing
            '''%(exe_name,"{prname}","{prname}")

            # 将VBScript写入到一个临时文件中
            temp_vbs_file = os.path.join(os.environ['TEMP'], 'create_shortcut.vbs')
            with open(temp_vbs_file, 'w', encoding="cp936") as vbs_file:
                vbs_file.write(vbs_script)

            # 执行VBScript来创建快捷方式
            subprocess.run(['cscript', '//nologo', temp_vbs_file], check=True)

            # 删除临时VBScript文件
            os.remove(temp_vbs_file)

                    """
                else:
                    code1="            #code1"
                if set_list[1]:
                    code2="""
            import winreg as reg
            import os
            
            def add_exe_to_startup(exe_path, startup_key='Run'):
                '''
            将exe文件添加到Windows启动项。
            
            :param exe_path: exe文件的完整路径
            :param startup_key: 注册表中的启动项键名，默认为'Run'
            '''
                try:
                    # 确保exe文件存在
                    if not os.path.exists(exe_path):
                        messagebox.showerror("错误","文件不存在："+exe_path)
            
                    # 打开注册表项
                    with reg.ConnectRegistry(None, reg.HKEY_CURRENT_USER) as hkey:
                        with reg.OpenKey(hkey, 'Software\\\\Microsoft\\\\Windows\\\\CurrentVersion', 0, reg.KEY_WRITE) as base_key:
                            # 尝试打开启动项键，如果不存在则创建
                            try:
                                with reg.OpenKey(base_key, startup_key, 0, reg.KEY_WRITE) as run_key:
                                    # 如果exe已经作为启动项存在，则覆盖它
                                    reg.SetValueEx(run_key, os.path.basename(exe_path), 0, reg.REG_SZ, exe_path)
                                    
                            except FileNotFoundError:
                                # 如果启动项键不存在，则创建它并添加exe
                                with reg.CreateKey(base_key, startup_key) as run_key:
                                    reg.SetValueEx(run_key, os.path.basename(exe_path), 0, reg.REG_SZ, exe_path)
                                    
                except PermissionError:
                    messagebox.showerror("错误", "修改注册表需要管理员权限。")
                except Exception as e:
                    messagebox.showerror("错误", str(e))
            
            # 示例用法
            exe_path = exe_name  # 替换为你的exe文件路径
            add_exe_to_startup(exe_path)
                    """
                else:
                    code2="            #code2"
                if set_list[2]:
                    print("请选择安装程序图标")
                    fp2=open_file_dialog()
                else:
                    fp2=None
                if set_list[3]:
                    print("请选择介绍和声明文件")
                    fp3=open_file_dialog2()
                    import chardet

                    with open(fp3, 'rb') as f:
                        raw_data = f.read(10000)  # 读取文件的前10000个字节
                    
                    # 使用chardet检测编码
                    result = chardet.detect(raw_data)
                    encoding2 = result['encoding']  # 获取检测到的编码
                    with open(fp3,"r", encoding=encoding2) as f:
                        text2=f.read()
                    code3=f"""
        scrollable_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
        scrollable_text.grid(pady=20)
    
        # 向Text控件中插入一些文本
        scrollable_text.insert(tk.END, '''{text2}''')

                    """
                else:
                    code3="        #code3"
                ifenter=input(f"即将封装：{selected_folder}，请按回车键开始！")
                cs35=os.path.join(selected_folder, "规格参数.txt")
                

                import zipfile
                import os

                def make_zipfile(output_filename, source_dir):
                    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, dirs, files in os.walk(source_dir):
                            # 添加目录中的每一个文件
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, os.path.join(source_dir, '..'))
                                zipf.write(file_path, arcname)

                # 使用示例
                output_filename = 'build.zip'
                source_dir = selected_folder
                make_zipfile(output_filename, source_dir)
                with open('build.zip','rb') as f:
                    recode=f.read()
                import base64
                encoded_data = str(base64.b85encode(recode))
                
                with open(f"{prname}-{vers}-setup.py","w",encoding="utf-8") as f:
                    
                    f.write(f"""

DATA={encoded_data}

import os.path
import tempfile
from base64 import b85decode
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinter import scrolledtext
import os
import zipfile
import threading
import shutil


    


class SelfExtractingApp:
    def __init__(self, root):
        import os
        self.root = root
        self.root.title("{prname}-{vers}-安装程序")

        # 设置默认解压路径
        self.default_extract_path = os.environ.get('PROGRAMFILES', '')+"\\\\{prname}"

        # 创建UI组件
        self.create_widgets()

    def create_widgets(self):
{code3}
        # 解压路径输入框和按钮
        self.extract_path_label = tk.Label(self.root, text="选择安装路径：‌")
        self.extract_path_label.grid(pady=10)

        self.extract_path_entry = tk.Entry(self.root, width=50)
        self.extract_path_entry.grid(pady=10)
        self.extract_path_entry.insert(0, self.default_extract_path)

        self.browse_button = tk.Button(self.root, text="浏览", command=self.browse_folder)
        self.browse_button.grid(pady=10)

        # 解压按钮
        self.extract_button = tk.Button(self.root, text="现在安装", command=self.extract_files)
        self.extract_button.grid(pady=10)

        # 进度条
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(pady=10)

    def browse_folder(self):
        # 弹出对话框选择文件夹
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.extract_path_entry.delete(0, tk.END)
            self.extract_path_entry.insert(0, folder_selected)

    
    def extract_files(self):
        # 获取解压路径和zip文件路径
        
        
        
        extract_path = self.extract_path_entry.get()
        

        # 创建解压线程
        threading.Thread(target=self.extract, args=(extract_path,)).start()
    def extract(self, extract_path):
        import os
        # 解压文件并更新进度条
        # Create a temporary working directory
        tmpdir = tempfile.mkdtemp()

        # Unpack the zipfile into the temporary directory
        zip_file_path = os.path.join(tmpdir, "setup.zip")
        with open(zip_file_path, "wb") as fp:
            fp.write(b85decode(DATA))
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                total_files = len(zip_ref.namelist())
                extracted_files = 0
                for file in zip_ref.namelist():
                    zip_ref.extract(file, extract_path)
                    extracted_files += 1
                    self.progress_bar["value"] = (extracted_files / total_files) * 100
                    self.root.update_idletasks()
            if tmpdir:
                shutil.rmtree(tmpdir, ignore_errors=True)
{code1}
{code2}
            messagebox.showinfo("成功", "安装成功！‌")
            import sys
            sys.exit()
        except Exception as e:
            messagebox.showerror("错误", str(e))

    


if __name__ == "__main__":
    root = tk.Tk()
    app = SelfExtractingApp(root)
    root.mainloop()

    


                    """)
                try:
                    import subprocess
                    if fp2 is None:
                        subprocess.run(["pyinstaller","-F","-w",f"{prname}-{vers}-setup.py"], check=True)
                    else:
                       subprocess.run(["pyinstaller","-F","-w",f"--icon={fp2}",f"{prname}-{vers}-setup.py"], check=True)
                    import shutil
                    shutil.copy2(f"dist\\{prname}-{vers}-setup.exe",f"{prname}-{vers}-setup.exe")
                    
                    os.remove("build.zip")
                    os.remove(f"{prname}-{vers}-setup.py")
                    os.remove(f"{prname}-{vers}-setup.spec")
                    shutil.rmtree("build")
                    shutil.rmtree("dist")
                    
                    
                    print("封装完成！")
                except Exception as e:
                    print(f"发生错误：{e}")
            else:
                print("无项目")


    
        elif atype=="4":
            # 指定要检查的文件夹路径
            folder_path = sysdir22+'软件项目\\'
     
            # 检查文件夹是否存在
            if os.path.exists(folder_path):
                from pathlib import Path
         
                def get_folder_paths(base_dir):
                    """
                    获取给定目录下所有子文件夹的路径
                    """
                    return [str(p) for p in Path(base_dir).iterdir() if p.is_dir()]
         
                def select_folder_by_number(base_dir):
                    """
                    通过控制台输入序号选择文件夹
                    """
                    folder_paths = get_folder_paths(base_dir)
                    for i, folder_path in enumerate(folder_paths, 1):
                        print(f"{i}. {folder_path}")
            
                    while True:
                        try:
                            selection = input("请输入序号选择文件夹: ")
                    
                    
                            index = int(selection) - 1
                            if 0 <= index < len(folder_paths):
                                return folder_paths[index]
                            else:
                                print("无效的序号，请重新输入。")
                        except ValueError:
                            print("非法输入，请输入一个整数。")
         
                base_dir = sysdir22+'软件项目\\'  # 替换为您的基础目录路径
                selected_folder = select_folder_by_number(base_dir)
                
                import shutil
                shutil.rmtree(selected_folder)
                print("删除成功！")
        

                def has_subdirectories(folder_path):
                    for folder_name in os.listdir(folder_path):
                        if os.path.isdir(os.path.join(folder_path, folder_name)):
                            return True
                    return False
         
                # 使用示例
                folder_path = sysdir22+'软件项目\\'
                if has_subdirectories(folder_path):
                    None
                else:
                    import shutil
                    shutil.rmtree(folder_path)
                
            else:
                print("无项目")
        elif atype=="5":
            import webbrowser

            # 打开一个特定的网页
            webbrowser.open('https://www.douyin.com/user/MS4wLjABAAAARkk5zY-7-Et1347qxL_7rsHVzWHOh9NI1YbMAZZ8crI')
        else:
            print("无效命令！")
        
if __name__=="__main__" and s4y1lh4w==1: #序号：1
    adt()
def home_page():
    import webbrowser
    
    # 打开一个特定的网页
    webbrowser.open('https://www.douyin.com/user/MS4wLjABAAAARkk5zY-7-Et1347qxL_7rsHVzWHOh9NI1YbMAZZ8crI')
if __name__=="__main__" and s4y1lh4w==2: #序号：2
    home_page()
