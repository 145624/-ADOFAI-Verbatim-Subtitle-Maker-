import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import random
from adobase import ADOFAILevel
import os

class ADOFAISubtitleGenerator:
    def __init__(self, root):
        self.root = root
        
        self.level = None
        self.filepath = None
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Microsoft YaHei', 16, 'bold'), foreground='#2c3e50')
        style.configure('Section.TLabel', font=('Microsoft YaHei', 12, 'bold'), foreground='#34495e')
        style.configure('TLabel', font=('Microsoft YaHei', 10), foreground='#2c3e50')
        style.configure('TButton', font=('Microsoft YaHei', 10), padding=5)
        style.configure('TCheckbutton', font=('Microsoft YaHei', 10))
        
        style.configure('Card.TFrame', background='#ecf0f1', relief='raised', borderwidth=2)
        
    def create_widgets(self):
        self.root.title("ADOFAI 逐子字幕制作器")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True)
        
        self.left_panel = ttk.Frame(main_container, width=250)
        self.left_panel.pack(side='left', fill='y', padx=10, pady=10)
        self.left_panel.pack_propagate(False)
        
        self.right_container = ttk.Frame(main_container)
        self.right_container.pack(side='right', fill='both', expand=True, padx=(0, 10), pady=10)
        
        title_label = ttk.Label(self.left_panel, text="🎵 ADOFAI\n逐子字幕制作器", style='Title.TLabel', justify='center')
        title_label.pack(pady=(0, 20))
        
        self._create_left_section()
        
        canvas = tk.Canvas(self.right_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.right_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding="5")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: self._update_scrollregion(canvas)
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        scrollable_frame.bind("<Configure>", _on_frame_configure)
        
        canvas.configure(yscrollcommand=self._sync_scrollbar(scrollbar))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill='y')
        
        self.canvas = canvas
        self.scrollable_frame = scrollable_frame
        
        self.bind_mousewheel(canvas, scrollable_frame)
        
        self.basic_frame = self.create_basic_section(scrollable_frame)
        self.position_frame = self.create_position_section(scrollable_frame)
        self.style_frame = self.create_style_section(scrollable_frame)
        self.parallax_frame = self.create_parallax_section(scrollable_frame)
        self.animation_frame = self.create_animation_section(scrollable_frame)
        self.action_frame = self.create_action_section(scrollable_frame)
    
    def _create_left_section(self):
        file_card = ttk.LabelFrame(self.left_panel, text="📁 文件选择", padding="10")
        file_card.pack(fill='x', pady=(0, 10))
        
        file_row = ttk.Frame(file_card)
        file_row.pack(fill='x')
        
        ttk.Label(file_row, text="关卡文件:").pack(anchor='w')
        
        self.file_entry = ttk.Entry(file_row, width=25)
        self.file_entry.pack(fill='x', pady=5)
        
        ttk.Button(file_row, text="浏览...", command=self.select_file).pack(fill='x')
        
        info_card = ttk.LabelFrame(self.left_panel, text="ℹ️ 使用说明", padding="10")
        info_card.pack(fill='both', expand=True)
        
        info_text = """1. 选择.adofai关卡文件
2. 设置基本参数
3. 配置位置和样式
4. 可选：启用动画
5. 点击生成字幕

提示：
• 轨道数：装饰物所在的轨道
• 标签：用于标识装饰物
• 启用动画后可设置逐字效果"""
        
        info_label = ttk.Label(info_card, text=info_text, justify='left', font=('Microsoft YaHei', 9))
        info_label.pack(anchor='w')
    
    def _update_scrollregion(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def _sync_scrollbar(self, scrollbar):
        def sync(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                scrollbar.pack_forget()
            else:
                scrollbar.pack(side="right", fill='y')
            scrollbar.set(first, last)
        return sync
    
    def bind_mousewheel(self, widget, scrollable_frame):
        def on_mousewheel(event):
            if widget.yview() != (0.0, 1.0):
                delta = -1 if event.delta > 0 else 1
                widget.yview_scroll(delta, "units")
                return "break"
        
        def on_shift_mousewheel(event):
            if widget.xview() != (0.0, 1.0):
                delta = -1 if event.delta > 0 else 1
                widget.xview_scroll(delta, "units")
                return "break"
        
        def on_button4(event):
            widget.yview_scroll(-1, "units")
            return "break"
        
        def on_button5(event):
            widget.yview_scroll(1, "units")
            return "break"
        
        widget.bind("<MouseWheel>", on_mousewheel)
        widget.bind("<Shift-MouseWheel>", on_shift_mousewheel)
        widget.bind("<Button-4>", on_button4)
        widget.bind("<Button-5>", on_button5)
        
    def create_card_frame(self, parent, title):
        card = ttk.LabelFrame(parent, text=title, padding="10", style='Card.TFrame')
        card.pack(fill='x', pady=5, padx=5)
        return card
    
    def create_file_section(self, parent):
        frame = self.create_card_frame(parent, "📁 文件选择")
        
        file_row = ttk.Frame(frame)
        file_row.pack(fill='x', pady=5)
        
        ttk.Label(file_row, text="关卡文件:").pack(side='left', padx=5)
        
        self.file_entry = ttk.Entry(file_row, width=50)
        self.file_entry.pack(side='left', padx=5, fill='x', expand=True)
        
        ttk.Button(file_row, text="浏览...", command=self.select_file).pack(side='left', padx=5)
        
        return frame
    
    def create_basic_section(self, parent):
        frame = self.create_card_frame(parent, "⚙️ 基本参数")
        
        row1 = ttk.Frame(frame)
        row1.pack(fill='x', pady=3)
        ttk.Label(row1, text="轨道数:").pack(side='left', padx=5)
        self.floor_entry = ttk.Entry(row1, width=15)
        self.floor_entry.pack(side='left', padx=5)
        
        row2 = ttk.Frame(frame)
        row2.pack(fill='x', pady=3)
        ttk.Label(row2, text="装饰物标签:").pack(side='left', padx=5)
        self.tag_entry = ttk.Entry(row2, width=20)
        self.tag_entry.pack(side='left', padx=5)
        
        row3 = ttk.Frame(frame)
        row3.pack(fill='x', pady=3)
        ttk.Label(row3, text="显示文字:").pack(side='left', padx=5)
        self.text_entry = ttk.Entry(row3, width=40)
        self.text_entry.pack(side='left', padx=5, fill='x', expand=True)
        
        row4 = ttk.Frame(frame)
        row4.pack(fill='x', pady=3)
        ttk.Label(row4, text="字体:").pack(side='left', padx=5)
        self.font_var = tk.StringVar(value="Default")
        font_combo = ttk.Combobox(row4, textvariable=self.font_var, width=18, state='readonly')
        font_combo['values'] = ('Default', 'Arial', 'ComicSansMS', 'CourierNew', 'Georgia', 'Helvetica', 'TimesNewRoman')
        font_combo.pack(side='left', padx=5)
        
        return frame
    
    def create_position_section(self, parent):
        frame = self.create_card_frame(parent, "📍 位置与旋转")
        
        row1 = ttk.Frame(frame)
        row1.pack(fill='x', pady=3)
        ttk.Label(row1, text="X位置偏移:").pack(side='left', padx=5)
        self.x_entry = ttk.Entry(row1, width=12)
        self.x_entry.pack(side='left', padx=5)
        self.x_entry.insert(0, "0")
        
        ttk.Label(row1, text="Y位置偏移:").pack(side='left', padx=15)
        self.y_entry = ttk.Entry(row1, width=12)
        self.y_entry.pack(side='left', padx=5)
        self.y_entry.insert(0, "0")
        
        row2 = ttk.Frame(frame)
        row2.pack(fill='x', pady=3)
        ttk.Label(row2, text="旋转角度:").pack(side='left', padx=5)
        self.rotation_entry = ttk.Entry(row2, width=12)
        self.rotation_entry.pack(side='left', padx=5)
        self.rotation_entry.insert(0, "0")
        
        return frame
    
    def create_style_section(self, parent):
        frame = self.create_card_frame(parent, "🎨 样式设置")
        
        row1 = ttk.Frame(frame)
        row1.pack(fill='x', pady=3)
        ttk.Label(row1, text="X大小:").pack(side='left', padx=5)
        self.scale_x_entry = ttk.Entry(row1, width=10)
        self.scale_x_entry.pack(side='left', padx=5)
        self.scale_x_entry.insert(0, "1")
        
        ttk.Label(row1, text="Y大小:").pack(side='left', padx=10)
        self.scale_y_entry = ttk.Entry(row1, width=10)
        self.scale_y_entry.pack(side='left', padx=5)
        self.scale_y_entry.insert(0, "1")
        
        row2 = ttk.Frame(frame)
        row2.pack(fill='x', pady=3)
        self.lock_rotation_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(row2, text="锁定旋转", variable=self.lock_rotation_var).pack(side='left', padx=5)
        
        self.lock_scale_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(row2, text="锁定大小", variable=self.lock_scale_var).pack(side='left', padx=15)
        
        row3 = ttk.Frame(frame)
        row3.pack(fill='x', pady=3)
        ttk.Label(row3, text="颜色代码:").pack(side='left', padx=5)
        self.color_entry = ttk.Entry(row3, width=10)
        self.color_entry.pack(side='left', padx=5)
        self.color_entry.insert(0, "ffffff")
        
        ttk.Label(row3, text="深度:").pack(side='left', padx=10)
        self.depth_entry = ttk.Entry(row3, width=10)
        self.depth_entry.pack(side='left', padx=5)
        self.depth_entry.insert(0, "0")
        
        return frame
    
    def create_parallax_section(self, parent):
        frame = self.create_card_frame(parent, "👁️ 视差效果")
        
        row1 = ttk.Frame(frame)
        row1.pack(fill='x', pady=3)
        ttk.Label(row1, text="X视差:").pack(side='left', padx=5)
        self.parallax_x_entry = ttk.Entry(row1, width=10)
        self.parallax_x_entry.pack(side='left', padx=5)
        self.parallax_x_entry.insert(0, "0")
        
        ttk.Label(row1, text="Y视差:").pack(side='left', padx=10)
        self.parallax_y_entry = ttk.Entry(row1, width=10)
        self.parallax_y_entry.pack(side='left', padx=5)
        self.parallax_y_entry.insert(0, "0")
        
        row2 = ttk.Frame(frame)
        row2.pack(fill='x', pady=3)
        ttk.Label(row2, text="X视差偏移:").pack(side='left', padx=5)
        self.parallax_offset_x_entry = ttk.Entry(row2, width=10)
        self.parallax_offset_x_entry.pack(side='left', padx=5)
        self.parallax_offset_x_entry.insert(0, "0")
        
        ttk.Label(row2, text="Y视差偏移:").pack(side='left', padx=10)
        self.parallax_offset_y_entry = ttk.Entry(row2, width=10)
        self.parallax_offset_y_entry.pack(side='left', padx=5)
        self.parallax_offset_y_entry.insert(0, "0")
        
        return frame
    
    def create_animation_section(self, parent):
        frame = self.create_card_frame(parent, "✨ 动画设置")
        
        row1 = ttk.Frame(frame)
        row1.pack(fill='x', pady=3)
        self.enable_animation_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(row1, text="启用逐字动画", variable=self.enable_animation_var, command=self.toggle_animation).pack(side='left', padx=5)
        
        self.animation_options_frame = ttk.Frame(frame)
        self.animation_options_frame.pack(fill='x', pady=5)
        self.animation_options_frame.pack_forget()
        
        anim_row1 = ttk.Frame(self.animation_options_frame)
        anim_row1.pack(fill='x', pady=2)
        ttk.Label(anim_row1, text="字符出现间隔(拍子):").pack(side='left', padx=5)
        self.duration_entry = ttk.Entry(anim_row1, width=10)
        self.duration_entry.pack(side='left', padx=5)
        self.duration_entry.insert(0, "1")
        
        anim_row2 = ttk.Frame(self.animation_options_frame)
        anim_row2.pack(fill='x', pady=2)
        ttk.Label(anim_row2, text="初始角度偏移:").pack(side='left', padx=5)
        self.angle_start_entry = ttk.Entry(anim_row2, width=10)
        self.angle_start_entry.pack(side='left', padx=5)
        self.angle_start_entry.insert(0, "0")
        
        ttk.Label(anim_row2, text="角度偏移增量:").pack(side='left', padx=10)
        self.angle_offset_entry = ttk.Entry(anim_row2, width=10)
        self.angle_offset_entry.pack(side='left', padx=5)
        self.angle_offset_entry.insert(0, "0")
        
        anim_row3 = ttk.Frame(self.animation_options_frame)
        anim_row3.pack(fill='x', pady=2)
        ttk.Label(anim_row3, text="X起始偏移:").pack(side='left', padx=5)
        self.x_start_entry = ttk.Entry(anim_row3, width=10)
        self.x_start_entry.pack(side='left', padx=5)
        self.x_start_entry.insert(0, "0")
        
        ttk.Label(anim_row3, text="Y起始偏移:").pack(side='left', padx=10)
        self.y_start_entry = ttk.Entry(anim_row3, width=10)
        self.y_start_entry.pack(side='left', padx=5)
        self.y_start_entry.insert(0, "0")
        
        anim_row4 = ttk.Frame(self.animation_options_frame)
        anim_row4.pack(fill='x', pady=2)
        ttk.Label(anim_row4, text="文字间隔:").pack(side='left', padx=5)
        self.text_gap_entry = ttk.Entry(anim_row4, width=10)
        self.text_gap_entry.pack(side='left', padx=5)
        self.text_gap_entry.insert(0, "0")
        
        anim_row5 = ttk.Frame(self.animation_options_frame)
        anim_row5.pack(fill='x', pady=2)
        ttk.Label(anim_row5, text="旋转偏移:").pack(side='left', padx=5)
        self.rotation_offset_entry = ttk.Entry(anim_row5, width=10)
        self.rotation_offset_entry.pack(side='left', padx=5)
        
        anim_row6 = ttk.Frame(self.animation_options_frame)
        anim_row6.pack(fill='x', pady=2)
        self.random_char_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(anim_row6, text="随机字符位置", variable=self.random_char_var, command=self.toggle_random_char).pack(side='left', padx=5)
        
        self.random_char_frame = ttk.Frame(self.animation_options_frame)
        self.random_char_frame.pack(fill='x', pady=2)
        self.random_char_frame.pack_forget()
        
        rc_row1 = ttk.Frame(self.random_char_frame)
        rc_row1.pack(fill='x', pady=2)
        ttk.Label(rc_row1, text="随机范围1:").pack(side='left', padx=5)
        self.random_range1_entry = ttk.Entry(rc_row1, width=8)
        self.random_range1_entry.pack(side='left', padx=5)
        self.random_range1_entry.insert(0, "-50")
        
        ttk.Label(rc_row1, text="随机范围2:").pack(side='left', padx=10)
        self.random_range2_entry = ttk.Entry(rc_row1, width=8)
        self.random_range2_entry.pack(side='left', padx=5)
        self.random_range2_entry.insert(0, "50")
        
        anim_row7 = ttk.Frame(self.animation_options_frame)
        anim_row7.pack(fill='x', pady=2)
        self.random_ease_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(anim_row7, text="随机缓动函数", variable=self.random_ease_var).pack(side='left', padx=5)
        
        self.ease_frame = ttk.Frame(self.animation_options_frame)
        self.ease_frame.pack(fill='x', pady=2)
        self.ease_frame.pack_forget()
        
        ttk.Label(self.ease_frame, text="缓动函数:").pack(side='left', padx=5)
        self.ease_var = tk.StringVar(value="Linear")
        ease_combo = ttk.Combobox(self.ease_frame, textvariable=self.ease_var, width=15, state='readonly')
        ease_combo['values'] = (
            'Linear', 'InSine', 'OutSine', 'InOutSine', 'InQuad', 'InCubic', 'InQuart', 
            'InQuint', 'InExpo', 'InCirc', 'InBack', 'OutQuad', 'OutCubic', 'OutQuart',
            'OutQuint', 'OutExpo', 'OutCirc', 'OutBack', 'InBounce', 'InElastic', 
            'Flash', 'InFlash', 'OutBounce', 'OutElastic', 'OutFlash', 'InOutQuad',
            'InOutCubic', 'InOutQuart', 'InOutQuint', 'InOutExpo', 'InOutCirc', 
            'InOutBack', 'InOutElastic', 'InOutFlash'
        )
        ease_combo.pack(side='left', padx=5)
        
        self.random_ease_frame = ttk.Frame(self.animation_options_frame)
        self.random_ease_frame.pack(fill='x', pady=2)
        self.random_ease_frame.pack_forget()
        
        ttk.Label(self.random_ease_frame, text="随机范围:").pack(side='left', padx=5)
        self.ease_type_var = tk.StringVar(value="inout")
        ease_type_combo = ttk.Combobox(self.random_ease_frame, textvariable=self.ease_type_var, width=10, state='readonly')
        ease_type_combo['values'] = ('in', 'out', 'inout')
        ease_type_combo.pack(side='left', padx=5)
        
        self.random_ease_var.trace('w', self.toggle_ease_selection)
        
        return frame
    
    def toggle_animation(self):
        if self.enable_animation_var.get():
            self.animation_options_frame.pack(fill='x', pady=5)
            self.toggle_ease_selection()
        else:
            self.animation_options_frame.pack_forget()
    
    def toggle_ease_selection(self, *args):
        if self.random_ease_var.get():
            self.ease_frame.pack_forget()
            self.random_ease_frame.pack(fill='x', pady=2)
        else:
            self.ease_frame.pack(fill='x', pady=2)
            self.random_ease_frame.pack_forget()
    
    def toggle_random_char(self):
        if self.random_char_var.get():
            self.random_char_frame.pack(fill='x', pady=2)
        else:
            self.random_char_frame.pack_forget()
    
    def create_action_section(self, parent):
        frame = self.create_card_frame(parent, "🚀 执行操作")
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        self.generate_btn = ttk.Button(button_frame, text="生成字幕", command=self.generate_subtitle, width=15)
        self.generate_btn.pack(side='left', padx=10)
        
        ttk.Button(button_frame, text="重置表单", command=self.reset_form, width=15).pack(side='left', padx=10)
        
        self.status_label = ttk.Label(frame, text="请选择关卡文件并设置参数", foreground='#7f8c8d')
        self.status_label.pack(pady=5)
        
        return frame
    
    def select_file(self):
        filepath = filedialog.askopenfilename(
            title="选择.adofai文件",
            filetypes=[("ADOFAI关卡文件", "*.adofai"), ("所有文件", "*.*")]
        )
        if filepath:
            self.filepath = filepath
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filepath)
            self.status_label.config(text=f"已选择: {os.path.basename(filepath)}", foreground='#27ae60')
            
            try:
                self.level = ADOFAILevel.load(filepath)
                self.status_label.config(text=f"已加载关卡: {os.path.basename(filepath)}", foreground='#27ae60')
            except Exception as e:
                messagebox.showerror("错误", f"无法加载关卡文件: {str(e)}")
                self.level = None
    
    def get_ease_function(self, ease_name):
        ease_map = {
            'Linear': 'Linear', 'InSine': 'InSine', 'OutSine': 'OutSine', 'InOutSine': 'InOutSine',
            'InQuad': 'InQuad', 'InCubic': 'InCubic', 'InQuart': 'InQuart', 'InQuint': 'InQuint',
            'InExpo': 'InExpo', 'InCirc': 'InCirc', 'InBack': 'InBack', 'OutQuad': 'OutQuad',
            'OutCubic': 'OutCubic', 'OutQuart': 'OutQuart', 'OutQuint': 'OutQuint', 'OutExpo': 'OutExpo',
            'OutCirc': 'OutCirc', 'OutBack': 'OutBack', 'InBounce': 'InBounce', 'InElastic': 'InElastic',
            'Flash': 'Flash', 'InFlash': 'InFlash', 'OutBounce': 'OutBounce', 'OutElastic': 'OutElastic',
            'OutFlash': 'OutFlash', 'InOutQuad': 'InOutQuad', 'InOutCubic': 'InOutCubic',
            'InOutQuart': 'InOutQuart', 'InOutQuint': 'InOutQuint', 'InOutExpo': 'InOutExpo',
            'InOutCirc': 'InOutCirc', 'InOutBack': 'InOutBack', 'InOutElastic': 'InOutElastic',
            'InOutFlash': 'InOutFlash'
        }
        return ease_map.get(ease_name, 'Linear')
    
    def get_random_ease(self, ease_type='inout'):
        in_eases = ['InSine', 'InCubic', 'InQuart', 'InQuint', 'InExpo', 'InCirc', 'InBack', 'InQuad']
        out_eases = ['OutSine', 'OutCubic', 'OutQuart', 'OutQuint', 'OutExpo', 'OutCirc', 'OutBack', 'OutQuad']
        inout_eases = ['InOutSine', 'InOutCubic', 'InOutQuart', 'InOutQuint', 'InOutExpo', 'InOutCirc', 'InOutBack', 'InOutQuad']
        
        if ease_type == 'in':
            return random.choice(in_eases)
        elif ease_type == 'out':
            return random.choice(out_eases)
        else:
            return random.choice(inout_eases)
    
    def generate_subtitle(self):
        if not self.level:
            messagebox.showwarning("警告", "请先选择关卡文件！")
            return
        
        try:
            floor = int(self.floor_entry.get())
            tag = self.tag_entry.get()
            text = self.text_entry.get()
            font = self.font_var.get()
            
            x = float(self.x_entry.get() or 0)
            y = float(self.y_entry.get() or 0)
            rotation = float(self.rotation_entry.get() or 0)
            
            scale_x = float(self.scale_x_entry.get() or 1)
            scale_y = float(self.scale_y_entry.get() or 1)
            lock_rotation = self.lock_rotation_var.get()
            lock_scale = self.lock_scale_var.get()
            color = self.color_entry.get() or "ffffff"
            depth = self.depth_entry.get() or "0"
            
            parallax_x = float(self.parallax_x_entry.get() or 0)
            parallax_y = float(self.parallax_y_entry.get() or 0)
            parallax_offset_x = float(self.parallax_offset_x_entry.get() or 0)
            parallax_offset_y = float(self.parallax_offset_y_entry.get() or 0)
            
            if not tag:
                messagebox.showwarning("警告", "请输入装饰物标签！")
                return
            
            if not text:
                messagebox.showwarning("警告", "请输入显示文字！")
                return
            
            if self.enable_animation_var.get():
                duration = float(self.duration_entry.get() or 1)
                angle_start = float(self.angle_start_entry.get() or 0)
                angle_offset = float(self.angle_offset_entry.get() or 0)
                x_start = float(self.x_start_entry.get() or 0)
                y_start = float(self.y_start_entry.get() or 0)
                text_gap = float(self.text_gap_entry.get() or 0)
                
                rotation_offset_input = self.rotation_offset_entry.get()
                rotation_offset = -rotation if rotation_offset_input == '' else float(rotation_offset_input)
                
                random_char = self.random_char_var.get()
                random_ease = self.random_ease_var.get()
                
                ease_type_var = self.ease_type_var.get() if random_ease else 'inout'
                
                if random_char:
                    random_range1 = int(self.random_range1_entry.get() or -50)
                    random_range2 = int(self.random_range2_entry.get() or 50)
                
                d = 1
                c1 = 0
                c = 1
                b = 0
                
                while b < len(text):
                    if random_char:
                        x1 = random.randint(random_range1, random_range2)
                        y1 = random.randint(random_range1, random_range2)
                    else:
                        x1 = x_start
                        y1 = y_start
                    
                    tag1 = f"{tag}_{d} {tag}"
                    tag2 = f"{tag}_{d}"
                    
                    if parallax_x != 0 or parallax_y != 0:
                        current_parallax_offset_x = parallax_offset_x + x1
                        current_parallax_offset_y = parallax_offset_y + y1
                    else:
                        current_parallax_offset_x = parallax_offset_x
                        current_parallax_offset_y = parallax_offset_y
                    
                    self.level.add_decoration(
                        floor, "AddText", decText=text[c1:c],
                        tag=tag1, font=font, position=[x + x1, y + y1],
                        relativeTo="Tile", pivotOffset=[0, 0], rotation=rotation,
                        lockRotation=lock_rotation, scale=[scale_x, scale_y],
                        lockScale=lock_scale, color=color, opacity=0, depth=depth,
                        parallax=[parallax_x, parallax_y],
                        parallaxOffset=[current_parallax_offset_x, current_parallax_offset_y]
                    )
                    
                    if random_ease:
                        ease = self.get_random_ease(ease_type_var)
                    else:
                        ease = self.get_ease_function(self.ease_var.get())
                    
                    self.level.add_event(
                        floor, "MoveDecorations", duration=duration,
                        positionOffset=[-x1, -y1], tag=tag2,
                        rotationOffset=rotation_offset, opacity=100,
                        angleOffset=angle_start, ease=ease,
                        parallaxOffset=[parallax_offset_x, parallax_offset_y]
                    )
                    
                    d += 1
                    c1 += 1
                    angle_start += angle_offset
                    c += 1
                    b += 1
                    
                    if not random_char:
                        x += text_gap
            else:
                self.level.add_decoration(
                    floor, "AddText", decText=text, tag=tag, font=font,
                    position=[x, y], relativeTo="Tile", pivotOffset=[0, 0],
                    rotation=rotation, lockRotation=lock_rotation,
                    scale=[scale_x, scale_y], lockScale=lock_scale,
                    color=color, opacity=0, depth=depth,
                    parallax=[parallax_x, parallax_y],
                    parallaxOffset=[parallax_offset_x, parallax_offset_y]
                )
                
                angle_start = float(self.angle_offset_entry.get() or 0) if self.enable_animation_var.get() else 0
                angle_offset = 0
                
                d = 0
                c = 1
                b = 0
                current_angle = 0
                
                while b < len(text):
                    self.level.add_event(
                        floor, "SetText", decText=text[0:c], tag=tag,
                        angleOffset=current_angle
                    )
                    current_angle += angle_offset
                    b += 1
                    c += 1
            
            self.level.export(self.filepath, as_original=True)
            
            messagebox.showinfo("成功", "字幕生成完成！")
            self.status_label.config(text="生成完成！", foreground='#27ae60')
            
        except ValueError as e:
            messagebox.showerror("错误", f"请检查输入的数值是否正确: {str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"生成失败: {str(e)}")
    
    def reset_form(self):
        self.file_entry.delete(0, tk.END)
        self.floor_entry.delete(0, tk.END)
        self.tag_entry.delete(0, tk.END)
        self.text_entry.delete(0, tk.END)
        self.font_var.set("Default")
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, "0")
        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(0, "0")
        self.rotation_entry.delete(0, tk.END)
        self.rotation_entry.insert(0, "0")
        self.scale_x_entry.delete(0, tk.END)
        self.scale_x_entry.insert(0, "1")
        self.scale_y_entry.delete(0, tk.END)
        self.scale_y_entry.insert(0, "1")
        self.lock_rotation_var.set(False)
        self.lock_scale_var.set(False)
        self.color_entry.delete(0, tk.END)
        self.color_entry.insert(0, "ffffff")
        self.depth_entry.delete(0, tk.END)
        self.depth_entry.insert(0, "0")
        self.parallax_x_entry.delete(0, tk.END)
        self.parallax_x_entry.insert(0, "0")
        self.parallax_y_entry.delete(0, tk.END)
        self.parallax_y_entry.insert(0, "0")
        self.parallax_offset_x_entry.delete(0, tk.END)
        self.parallax_offset_x_entry.insert(0, "0")
        self.parallax_offset_y_entry.delete(0, tk.END)
        self.parallax_offset_y_entry.insert(0, "0")
        self.enable_animation_var.set(False)
        self.toggle_animation()
        self.status_label.config(text="表单已重置", foreground='#7f8c8d')
        self.level = None
        self.filepath = None


def main():
    root = tk.Tk()
    app = ADOFAISubtitleGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
