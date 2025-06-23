# 请求调页存储管理方式模拟系统

## 项目简介

这是一个用Python实现的请求调页存储管理方式模拟系统，用于演示和比较不同的页面置换算法。

## 功能特性

- **页面置换算法**：实现了FIFO（先进先出）和OPT（最佳置换）两种算法
- **地址转换**：支持逻辑地址到物理地址的转换
- **缺页统计**：统计和计算缺页率
- **详细过程输出**：详细打印每一步置换过程，便于学习和分析

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
├── .gitignore                     # Git忽略文件配置
└── requirements.txt               # 项目依赖（可选）
```

## 使用方法

### 运行程序

```bash
python 请求调页存储管理方式的模拟.py
```

- **无需额外依赖包，直接运行即可。**

### 主要功能

1. **生成随机指令序列**：生成320条不重复的随机指令访问序列
2. **FIFO算法模拟**：使用先进先出算法进行页面置换
3. **OPT算法模拟**：使用最佳置换算法进行页面置换
4. **性能比较**：比较两种算法的缺页率

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
- **特点**：实现简单，但性能可能不是最优

### OPT（最佳置换）算法
- **原理**：选择未来最长时间不会被使用的页面进行置换
- **特点**：理论上最优，但需要预知未来访问模式

## 输出示例

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

## 开发环境

- Python 3.6+
- 无需额外依赖包

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

## 作者

JianjiaGuan

## 许可证

本项目仅用于学习和研究目的。 