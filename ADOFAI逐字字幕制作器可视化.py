from adobase import * 
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, scrolledtext
import os

class ModernButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_enter(self, e):
        self['style'] = 'Accent.TButton'
    
    def on_leave(self, e):
        self['style'] = 'TButton'

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ADOFAI 逐字字幕制作器")
        self.root.geometry("900x650")
        self.root.configure(bg='#F0F0F0')
        
        self.setup_styles()
        self.create_variables()
        self.create_ui()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure('TFrame', background='#F0F0F0')
        style.configure('TLabelframe', background='#F0F0F0')
        style.configure('TLabelframe.Label', font=('Microsoft YaHei UI', 10), background='#F0F0F0')
        style.configure('TButton',
            font=('Microsoft YaHei UI', 10),
            padding=10,
            background='#FFFFFF',
            relief='flat'
        )
        style.configure('Accent.TButton',
            font=('Microsoft YaHei UI', 10),
            padding=10,
            background='#0078D4',
            foreground='white'
        )
        style.configure('TLabel',
            font=('Microsoft YaHei UI', 10),
            background='#F0F0F0'
        )
        style.configure('Title.TLabel',
            font=('Microsoft YaHei UI', 16, 'bold'),
            background='#F0F0F0',
            foreground='#0078D4'
        )
        style.configure('Status.TLabel',
            font=('Microsoft YaHei UI', 10),
            background='#F0F0F0',
            foreground='#0078D4'
        )
        style.configure('TEntry',
            font=('Microsoft YaHei UI', 10),
            padding=5
        )
    
    def create_variables(self):
        self.file_path_var = tk.StringVar()
        self.text_var = tk.StringVar()
        self.output_name_var = tk.StringVar()
        self.show_preview_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="等待操作...")
        
        self.param_vars = {}
        self.params = [
            ("目标轨道：", "floor_var", "1", 10),
            ("初始轨道偏移：", "initial_offset_var", "0", 10),
            ("轨道偏移（每个字符）：", "angle_offset_var", "15", 10),
            ("装饰物标签：", "tag_var", "", 50),
        ]
        
        for _, var_name, default, _ in self.params:
            self.param_vars[var_name] = tk.StringVar(value=default)
    
    def create_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20", style='TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="ADOFAI 逐字字幕制作器", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=tk.W)
        
        # 创建左右分栏
        left_frame = ttk.Frame(main_frame, padding="10", style='TFrame')
        right_frame = ttk.Frame(main_frame, padding="10", style='TFrame')
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=2)
        
        self.create_left_panel(left_frame)
        self.create_right_panel(right_frame)
        
        # 状态栏
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, style='Status.TLabel')
        self.status_label.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        # 绑定事件
        self.file_path_var.trace_add("write", self.update_default_output_name)
        self.text_var.trace_add("write", lambda *args: self.update_preview())
        for var in self.param_vars.values():
            var.trace_add("write", lambda *args: self.update_preview())
    
    def create_left_panel(self, frame):
        # 文件选择部分
        file_frame = ttk.LabelFrame(frame, text="文件选择", padding="15", style='TLabelframe')
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        frame.columnconfigure(0, weight=1)
        
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=50).grid(row=0, column=0, padx=(0, 10))
        ModernButton(file_frame, text="选择文件", command=self.select_file).grid(row=0, column=1)
        
        # 基本参数设置
        param_frame = ttk.LabelFrame(frame, text="基本参数", padding="15", style='TLabelframe')
        param_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        for i, (label, var_name, _, width) in enumerate(self.params):
            ttk.Label(param_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            ttk.Entry(param_frame, textvariable=self.param_vars[var_name], width=width).grid(row=i, column=1, sticky=tk.W, pady=5)
        
        # 高级选项
        advanced_frame = ttk.LabelFrame(frame, text="高级选项", padding="15", style='TLabelframe')
        advanced_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Checkbutton(advanced_frame, text="实时预览", variable=self.show_preview_var).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(advanced_frame, text="输出文件名：").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(advanced_frame, textvariable=self.output_name_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Label(advanced_frame, text=".adofai").grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # 文本输入区域
        text_frame = ttk.LabelFrame(frame, text="输入文字", padding="15", style='TLabelframe')
        text_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Entry(text_frame, textvariable=self.text_var, width=50).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        ModernButton(text_frame, text="生成字幕", command=self.process, width=20).grid(row=1, column=0, pady=10)
    
    def create_right_panel(self, frame):
        # 预览区域
        preview_frame = ttk.LabelFrame(frame, text="预览", padding="15", style='TLabelframe')
        preview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame, 
            width=40, 
            height=20,
            font=('Microsoft YaHei UI', 10),
            background='white',
            relief='flat'
        )
        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.preview_text.insert(tk.END, "请选择文件并设置参数...")
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="选择ADOFAI关卡文件",
            filetypes=[("ADOFAI关卡文件", "*.adofai")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.status_var.set("已选择文件：" + os.path.basename(file_path))
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, "文件已加载，请设置参数后点击预览")
    
    def update_default_output_name(self, *args):
        if self.file_path_var.get():
            default_name = os.path.splitext(os.path.basename(self.file_path_var.get()))[0] + "_output"
            self.output_name_var.set(default_name)
    
    def update_preview(self):
        if not self.show_preview_var.get():
            return
            
        try:
            floor = int(self.param_vars["floor_var"].get())
            initial_offset = int(self.param_vars["initial_offset_var"].get())
            angle_offset = int(self.param_vars["angle_offset_var"].get())
            tag = self.param_vars["tag_var"].get().strip()
            text = self.text_var.get().strip()
            
            if not text:
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.insert(tk.END, "请输入要添加的文字...")
                return
                
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, "预览效果：\n\n")
            
            # 从第一个字符开始
            a = initial_offset
            preview_line = f'Floor: {floor}, Text: "{text[0]}", Tag: "{tag}", Offset: {a}\n'
            self.preview_text.insert(tk.END, preview_line)
            a += angle_offset
            
            # 后续字符
            for i in range(2, len(text) + 1):
                preview_line = f'Floor: {floor}, Text: "{text[0:i]}", Tag: "{tag}", Offset: {a}\n'
                self.preview_text.insert(tk.END, preview_line)
                a += angle_offset
                
        except ValueError:
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, "参数格式错误，请检查输入...")
    
    def process(self):
        try:
            # 获取输入值
            file_path = self.file_path_var.get()
            if not file_path:
                messagebox.showerror("错误", "请先选择关卡文件！")
                return
                
            floor = int(self.param_vars["floor_var"].get())
            initial_offset = int(self.param_vars["initial_offset_var"].get())
            angle_offset = int(self.param_vars["angle_offset_var"].get())
            tag = self.param_vars["tag_var"].get().strip()
            text = self.text_var.get().strip()
            output_name = self.output_name_var.get().strip()
            
            if not tag:
                messagebox.showerror("错误", "请输入装饰物标签！")
                return
            if not text:
                messagebox.showerror("错误", "请输入要添加的文字！")
                return
            if not output_name:
                messagebox.showerror("错误", "请输入输出文件名！")
                return
            
            # 读取关卡文件
            try:
                level = ADOFAILevel.load(file_path)
            except Exception as e:
                messagebox.showerror("错误", f"无法读取关卡文件：{str(e)}")
                return
            
            # 处理输出文件名
            input_dir = os.path.dirname(file_path)
            output_path = os.path.join(input_dir, output_name + ".adofai")
            
            if os.path.exists(output_path):
                if not messagebox.askyesno("确认", f"文件 {output_name}.adofai 已存在，是否覆盖？"):
                    return
            
            # 添加事件，从第一个字符开始
            a = initial_offset
            level.add_event(floor, "SetText", decText=text[0], tag=tag, angleOffset=a)
            a += angle_offset
            
            # 添加后续字符
            for i in range(2, len(text) + 1):
                level.add_event(floor, "SetText", decText=text[0:i], tag=tag, angleOffset=a)
                a += angle_offset
            
            # 保存文件
            level.export(output_path, as_original=True)
            self.status_var.set(f"成功！文件已保存至：{output_path}")
            messagebox.showinfo("成功", f"文件已保存至：\n{output_path}")
            
        except ValueError as e:
            messagebox.showerror("错误", "请确保所有数值输入正确！")
            self.status_var.set("错误：数值输入格式错误")
        except Exception as e:
            messagebox.showerror("错误", f"处理过程中出现错误：{str(e)}")
            self.status_var.set("错误：处理失败")

def main():
    # 设置DPI感知
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    root = tk.Tk()
    root.state('zoomed')  # 添加最大化命令
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()