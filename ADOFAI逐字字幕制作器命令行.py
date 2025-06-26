from adobase import * 
import tkinter as tk
from tkinter import filedialog
import os

# 创建一个隐藏的主窗口用于文件对话框
root = tk.Tk()
root.withdraw()

print("请选择要打开的ADOFAI关卡文件")
file_path = filedialog.askopenfilename(title="选择ADOFAI关卡文件", 
                                     filetypes=[("ADOFAI关卡文件", "*.adofai")])

if not file_path:
    print("未选择文件，程序退出")
    exit()

# 获取输入文件的目录
input_dir = os.path.dirname(file_path)
default_output_name = os.path.splitext(os.path.basename(file_path))[0] + "_output.adofai"
print(f"默认输出文件名：{default_output_name}")
output_filename = input("请输入输出文件名（直接回车使用默认文件名）：").strip()
if not output_filename:
    output_filename = default_output_name
elif not output_filename.endswith('.adofai'):
    output_filename += '.adofai'

output_path = os.path.join(input_dir, output_filename)

# 检查文件是否存在
if os.path.exists(output_path):
    confirm = input(f"文件 {output_filename} 已存在，是否覆盖？(y/n): ").strip().lower()
    if confirm != 'y':
        print("操作已取消")
        exit()

# 读取文件内容
try:
    level = ADOFAILevel.load(file_path)
    print("ADOFAI关卡文件加载成功！")
except Exception as e:
    print(f"文件读取错误：{e}")
    exit()

print("请先调试好文字装饰及其标签！")
print("建议备份后多次尝试")
b=0 #循环次数
c=0 #字符
#基本信息
floor=int(input("请输入目标轨道："))
d=int(input("请输入初始轨道偏移："))
angleOffset=int(input("请输入轨道偏移（每个字符）："))

a=d-angleOffset 
tag=input("请输入目标装饰物标签:")
text=input("请输入一句话：")
#循环
while 1:
    level.add_event(floor,"SetText",decText=text[0:c],tag=tag,angleOffset=a)
    a=a+angleOffset #轨道偏移增加
    b=b+1 #循环次数增加
    c=c+1 #字符数增加
    if b == len(text)+1:
        break
level.export(output_path, as_original=True)
print(f"文件已保存至：{output_path}")