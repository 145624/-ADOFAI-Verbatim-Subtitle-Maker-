# ADOFAI 逐子字幕制作器
# 注意：这个程序完全由TraeAI编写
（没错，这个readme也是他写的）

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![ADObase](https://img.shields.io/badge/ADObase-0.1.0-blue.svg)](https://pypi.org/project/ADOBase/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个用于制作《冰与火之舞》(ADOFAI) 游戏逐字字幕的可视化工具。

## 注意事项

如果关卡中含有非标准控制字符，显示读取失败，可以先创建新关卡然后把字幕复制进去

## 📺 预览

```
┌─────────────────────────────────────────────────────┐
│              ADOFAI 逐子字幕制作器                    │
├──────────────┬──────────────────────────────────────┤
│   📁 文件选择 │         ⚙️ 基本参数                  │
│  [文件路径]  │    轨道数: [____] 标签: [____]       │
│  [浏览...]   │    文字: [_______________]           │
│              │    字体: [下拉选择____▼]              │
│  ℹ️ 使用说明 │                                      │
│  1.选择文件  │         📍 位置与旋转                 │
│  2.设置参数  │    X偏移: [____] Y偏移: [____]       │
│  3.配置样式  │    旋转: [____]                      │
│  4.启用动画  │                                      │
│  5.生成字幕  │         🎨 样式设置                   │
│              │    X大小: [____] Y大小: [____]       │
│              │    颜色: [ffffff] 深度: [__]         │
│              │    ☐锁定旋转 ☐锁定大小               │
│              │                                      │
│              │         👁️ 视差效果                   │
│              │    X/Y视差、视差偏移设置              │
│              │                                      │
│              │         ✨ 动画设置                   │
│              │    ☐启用逐字动画                     │
│              │    [展开更多动画选项...]              │
│              │                                      │
│              │         🚀 执行操作                   │
│              │    [生成字幕]    [重置表单]          │
└──────────────┴──────────────────────────────────────┘
```

## ✨ 功能特性

### 核心功能
- ✅ **图形化界面** - 直观的可视化操作界面
- ✅ **文件管理** - 便捷的 ADOFAI 关卡文件选择
- ✅ **参数配置** - 全面的字幕参数设置
- ✅ **动画效果** - 丰富的逐字动画效果
- ✅ **随机机制** - 支持随机位置和随机缓动函数

### 动画特性
- **逐字出现效果** - 字符依次出现
- **随机字符位置** - 每个字符随机分散
- **随机缓动函数** - 随机选择动画曲线
- **33种缓动函数** - Linear、In/Out/Bounce/Elastic 等
- **视差效果** - 支持视差滚动
- **角度偏移** - 每个字符独立角度

## 📋 安装要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | 3.6+ | 运行环境 |
| Tkinter | 标准库 | GUI 框架 |
| adobase | 最新版 | ADOFAI 文件处理 |



## 📖 使用方法

### 基本操作流程

1. **选择关卡文件**
   - 点击左侧面板的"浏览"按钮
   - 选择 `.adofai` 格式的关卡文件

2. **设置基本参数**
   - 轨道数：装饰物所在的轨道编号
   - 装饰物标签：用于标识装饰物
   - 显示文字：要显示的字幕内容
   - 字体：选择文字字体

3. **配置位置与旋转**
   - X/Y 位置偏移
   - 旋转角度

4. **设置样式**
   - X/Y 大小
   - 颜色代码（六位十六进制）
   - 深度值
   - 锁定选项

5. **配置视差效果（可选）**
   - X/Y 视差值
   - X/Y 视差偏移

6. **启用动画（可选）**
   - 勾选"启用逐字动画"
   - 设置每个字符出现时间
   - 配置角度偏移
   - 可选：随机字符位置
   - 可选：随机缓动函数

7. **生成字幕**
   - 点击"生成字幕"按钮
   - 字幕将添加到关卡文件中

### 参数说明

#### 基本参数
| 参数 | 说明 | 示例 |
|------|------|------|
| 轨道数 | 装饰物所在的轨道 | 1 |
| 装饰物标签 | 唯一标识符 | subtitle |
| 显示文字 | 字幕内容 | Hello |
| 字体 | 文字字体 | Arial |

#### 位置参数
| 参数 | 说明 | 示例 |
|------|------|------|
| X位置偏移 | 水平位置 | 0 |
| Y位置偏移 | 垂直位置 | 0 |
| 旋转角度 | 旋转角度 | 0 |

#### 样式参数
| 参数 | 说明 | 示例 |
|------|------|------|
| X大小 | 水平缩放 | 1 |
| Y大小 | 垂直缩放 | 1 |
| 颜色代码 | 十六进制颜色 | ffffff |
| 深度 | 渲染深度 | 0 |

#### 动画参数
| 参数 | 说明 | 示例 |
|------|------|------|
| 字符间隔 | 每字符出现时间(拍) | 1 |
| 初始角度偏移 | 起始角度 | 0 |
| 角度偏移增量 | 每字符角度增量 | 0 |
| 文字间隔 | 字符间距 | 10 |

### 缓动函数列表

```
Linear        | InSine       | OutSine      | InOutSine
InQuad       | InCubic      | InQuart      | InQuint
InExpo       | InCirc       | InBack       | OutQuad
OutCubic     | OutQuart     | OutQuint     | OutExpo
OutCirc      | OutBack      | InBounce     | InElastic
Flash        | InFlash      | OutBounce    | OutElastic
OutFlash     | InOutQuad    | InOutCubic   | InOutQuart
InOutQuint   | InOutExpo    | InOutCirc    | InOutBack
InOutElastic | InOutFlash
```

## 📂 项目结构

```
.
├── ADOFAI逐子字幕制作器_GUI.py    # GUI 主程序
├── ADOFAI逐子字幕制作器命令行.py   # 命令行版本
├── README.md                      # 项目文档
└── images/                        # 资源目录
```

## 🔧 开发指南

### 运行开发版本
```bash
# 克隆仓库
git clone https://github.com/your-repo/adofai-subtitle-generator.git

# 进入目录
cd adofai-subtitle-generator

# 安装依赖
pip install -r requirements.txt

# 运行程序
python ADOFAI逐子字幕制作器_GUI.py
```

### 打包为可执行文件
```bash
pip install pyinstaller

pyinstaller --onefile --windowed ADOFAI逐子字幕制作器_GUI.py
```


## 📄 许可证

本项目采用 MIT 许可证。


---

**Enjoy creating amazing subtitles for your ADOFAI levels! 🎵**

