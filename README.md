# 请求调页存储管理方式模拟系统

## 项目简介

这是一个用Python实现的请求调页存储管理方式模拟系统，用于演示和比较不同的页面置换算法。系统支持文本模式和Tkinter动画可视化模式两种运行方式，提供直观的页面置换过程演示。

## 功能特性

- **页面置换算法**：实现了FIFO（先进先出）和OPT（最佳置换）两种算法
- **地址转换**：支持逻辑地址到物理地址的转换
- **缺页统计**：统计和计算缺页率
- **详细过程输出**：详细打印每一步置换过程，便于学习和分析
- **动画可视化**：美观的Tkinter GUI界面，支持交互控制，实时动画演示页面置换过程
- **多种运行模式**：支持文本模式、Tkinter动画模式和混合模式
- **正确的FIFO实现**：使用队列维护页面进入顺序，实现真正的先进先出置换

## 系统参数

- **总指令数**：320条
- **每页指令数**：10条
- **内存块数**：4个
- **总页数**：32页

## 文件结构

```
page-replacement-simulator/
├── 请求调页存储管理方式的模拟.py  # 主程序文件
├── README.md                      # 项目说明文档
├── requirements.txt               # 项目依赖
└── .gitignore                     # Git忽略文件配置
```

## 安装依赖

```bash
# 本项目无需额外依赖，Tkinter是Python内置的GUI库
# 直接运行即可
```

## 使用方法

### 运行程序

```bash
python 请求调页存储管理方式的模拟.py
```

运行后会提示选择运行模式：
1. **文本模式（详细输出）**：传统的命令行输出，显示详细的置换过程
2. **Tkinter动画模式（推荐）**：美观的GUI界面，支持交互控制，实时动画演示
3. **两种模式都运行**：先运行文本模式，再运行Tkinter动画模式

### 主要功能

1. **生成随机指令序列**：生成320条不重复的随机指令访问序列
2. **FIFO算法模拟**：使用先进先出算法进行页面置换
3. **OPT算法模拟**：使用最佳置换算法进行页面置换
4. **性能比较**：比较两种算法的缺页率
5. **动画演示**：可视化展示页面置换过程，包括：
   - 美观的GUI界面，支持开始/暂停/重置控制
   - 可调节动画速度
   - 实时显示内存块状态、缺页次数、当前指令等信息
   - 进度条显示执行进度
   - 高亮显示页面命中/缺页状态
   - 正确显示被置换页面和加载位置

## 核心类和方法

### PageReplacementSimulator类

```python
simulator = PageReplacementSimulator(
    total_instructions=320,  # 总指令数
    page_size=10,           # 每页指令数
    memory_blocks=4,        # 内存块数
    sequence=random_sequence # 指令访问序列
)

fifo_faults = simulator.FIFO()  # 执行FIFO算法，返回缺页次数
simulator.reset()               # 重置模拟器状态
opt_faults = simulator.OPT()    # 执行OPT算法，返回缺页次数
```

#### 构造参数说明
- `total_instructions`：总指令数（默认320）
- `page_size`：每页指令数（默认10）
- `memory_blocks`：内存块数（默认4）
- `sequence`：指令访问序列（长度为320的逻辑地址列表）

#### 主要方法
- `FIFO()`：先进先出页面置换算法，详细打印每一步，返回缺页次数
- `OPT()`：最佳置换算法，详细打印每一步，返回缺页次数
- `reset()`：重置模拟器状态

#### 数据结构
- `memory`：当前在内存中的页面列表
- `page_faults`：缺页次数统计
- `fifo_queue`：FIFO队列，维护页面进入内存的顺序

### PageReplacementAnimation类

```python
animator = PageReplacementAnimation(simulator)
fifo_faults = animator.animate_fifo()  # FIFO算法动画演示
opt_faults = animator.animate_opt()    # OPT算法动画演示
```

#### 主要方法
- `animate_fifo()`：FIFO算法的动画演示，返回缺页次数
- `animate_opt()`：OPT算法的动画演示，返回缺页次数
- `setup_animation()`：设置动画界面
- `update_animation(frame)`：更新动画帧

### TkinterPageAnimation类

```python
tk_animator = TkinterPageAnimation(simulator)
fifo_faults = tk_animator.animate_fifo()  # FIFO算法Tkinter动画演示
opt_faults = tk_animator.animate_opt()    # OPT算法Tkinter动画演示
```

#### 主要方法
- `animate_fifo()`：FIFO算法的Tkinter动画演示，返回缺页次数
- `animate_opt()`：OPT算法的Tkinter动画演示，返回缺页次数
- `create_window(title)`：创建动画窗口
- `draw_memory_blocks()`：绘制内存块
- `start_animation()`：开始动画
- `pause_animation()`：暂停动画
- `reset_animation()`：重置动画

#### 界面特性
- **控制面板**：开始、暂停、重置按钮
- **进度条**：显示执行进度
- **速度控制**：可调节动画速度（100-3000毫秒）
- **信息显示**：实时显示当前指令、逻辑地址、页号、内存状态等
- **内存块可视化**：4个内存块的实时状态显示
- **状态指示**：页面命中（绿色）vs 缺页中断（红色）
- **置换信息**：显示被置换页面和加载位置

### 工具函数

```python
random_sequence = generate_random_sequence()  # 生成随机指令序列
page_number, page_offset = calculate_page_info(logical_address, page_size=10)  # 计算页号和页内地址
physical_address = calculate_physical_address(page_offset, frame_number, page_size=10)  # 计算物理地址
```

- `generate_random_sequence()`：生成0-319的随机排列，长度为320
- `calculate_page_info(logical_address, page_size=10)`：输入逻辑地址，返回(页号, 页内地址)
- `calculate_physical_address(page_offset, frame_number, page_size=10)`：输入页内地址和帧号，返回物理地址

## 算法说明

### FIFO（先进先出）算法
- **原理**：选择最早进入内存的页面进行置换
- **实现**：使用队列维护页面进入内存的顺序
- **置换策略**：当发生缺页且内存已满时，选择队列头部（最早进入）的页面进行置换
- **位置替换**：新页面放在被置换页面的内存块位置
- **特点**：实现简单，但性能可能不是最优

### OPT（最佳置换）算法
- **原理**：选择未来最长时间不会被使用的页面进行置换
- **置换策略**：当发生缺页且内存已满时，选择未来最晚使用的页面进行置换
- **位置替换**：新页面放在被置换页面的内存块位置
- **特点**：理论上最优，但需要预知未来访问模式

## 页面置换过程

### 置换触发条件
- 访问的页面不在内存中（缺页中断）
- 内存块已满（需要置换）

### 置换步骤
1. **选择被置换页面**：
   - FIFO：选择最早进入内存的页面
   - OPT：选择未来最长时间不会被使用的页面
2. **位置替换**：新页面放在被置换页面的内存块位置
3. **更新数据结构**：
   - FIFO：更新队列（移除被置换页面，添加新页面）
   - OPT：直接替换页面

## 动画演示特性

### 可视化元素
- **内存块显示**：4个内存块的实时状态
- **页面信息**：显示当前访问的页面号
- **状态指示**：缺页中断（红色）vs 页面命中（绿色）
- **置换信息**：显示页面加载和置换过程
- **缺页计数**：实时更新缺页次数

### 颜色编码
- **绿色高亮**：新加载的页面
- **蓝色高亮**：命中的页面
- **灰色**：内存中的其他页面
- **红色文字**：缺页中断状态

### 交互控制
- **开始/暂停**：控制动画播放
- **重置**：重新开始动画
- **速度调节**：调整动画播放速度
- **进度显示**：实时显示执行进度

## 输出示例

### 文本模式输出
```
=== 执行FIFO算法 ===
--------------------------------
指令：0，逻辑地址为：156
页号：15，页内地址：6
内存中页面：[]
发生缺页中断
页面15被加载到内存
更换后内存中页面：[15]
--------------------------------
...
FIFO算法缺页次数: 124

=== 重置模拟器 ===
模拟器已重置到初始状态

=== 执行OPT算法 ===
...
OPT算法缺页次数: 101

=== 算法性能比较 ===
FIFO算法缺页次数: 124
OPT算法缺页次数: 101
OPT算法相比FIFO算法减少了 18.55% 的缺页
```

### 动画模式
动画模式会打开图形窗口，实时显示：
- 内存块状态变化
- 页面访问过程
- 缺页和命中情况
- 置换过程动画
- 被置换页面和加载位置信息

## 开发环境

- Python 3.6+
- Tkinter（Python内置）

## 版本控制

使用Git进行版本控制：

```bash
# 查看状态
git status

# 添加文件
git add .

# 提交更改
git commit -m "添加页面置换模拟系统"

# 查看提交历史
git log
```

## 更新日志

### v2.0 (最新)
- 修复FIFO算法的页面置换逻辑
- 添加FIFO队列维护页面进入顺序
- 实现正确的先进先出置换策略
- 改进动画显示，正确显示被置换页面和加载位置
- 优化用户界面和交互体验

### v1.0
- 实现基本的页面置换算法
- 添加Tkinter动画演示
- 支持文本和动画两种运行模式

## 作者

JianjiaGuan

## 许可证

本项目仅用于学习和研究目的。 