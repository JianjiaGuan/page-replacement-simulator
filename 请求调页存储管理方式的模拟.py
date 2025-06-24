import random
from collections import deque
import tkinter as tk
from tkinter import ttk, messagebox
import threading

def generate_random_sequence():
    """生成一个包含0-319的随机数且互不相等的320长度列表"""
    # 使用random.shuffle来生成0-319的随机排列
    sequence = list(range(320))  # 0-319的列表
    random.shuffle(sequence)     # 随机打乱
    return sequence

def calculate_page_info(logical_address, page_size=10):
    """
    计算页号和页内地址
    
    Args:
        logical_address: 逻辑地址（0-319）
        page_size: 每页大小（默认10）
    
    Returns:
        tuple: (页号, 页内地址)
    """
    page_number = logical_address // page_size
    page_offset = logical_address % page_size
    return page_number, page_offset

def calculate_physical_address(page_offset, frame_number, page_size=10):
    """
    计算内存物理地址
    
    Args:
        page_offset: 页内地址
        frame_number: 内存块号（帧号）
        page_size: 每页大小（默认10）
    
    Returns:
        int: 物理地址
    """
    return frame_number * page_size + page_offset

class PageReplacementSimulator:
    def __init__(self, total_instructions=320, page_size=10, memory_blocks=4,sequence=[]):
        """
        初始化页面置换模拟器
        
        Args:
            total_instructions: 总指令数
            page_size: 每页指令数
            memory_blocks: 内存块数
            sequence: 指令访问序列
        """
        self.total_instructions = total_instructions
        self.page_size = page_size
        self.memory_blocks = memory_blocks
        self.total_pages = total_instructions // page_size  # 32页
        self.sequence = sequence #对应每条指令的逻辑地址

        # 内存状态
        self.memory = []  # 当前在内存中的页面
        self.page_faults = 0  # 缺页次数
        self.fifo_queue = []  # FIFO队列，记录页面进入内存的顺序

    def reset(self):
        """
        重置模拟器到初始状态
        """
        self.memory = []  # 清空内存
        self.page_faults = 0  # 重置缺页次数
        self.fifo_queue = []  # 重置FIFO队列
        print("模拟器已重置到初始状态")

    def FIFO(self):
        """
        先进先出页面置换算法
        """
        for i in range(self.total_instructions):
            print("--------------------------------")
            print(f"指令：{i}，逻辑地址为：{self.sequence[i]}")
            page_number, page_offset = calculate_page_info(self.sequence[i], self.page_size)
            print(f"页号：{page_number}，页内地址：{page_offset}")
            print(f"内存中页面：{self.memory}")
            if page_number not in self.memory:
                print("发生缺页中断")
                if len(self.memory) < self.memory_blocks:
                    self.memory.append(page_number)
                    self.fifo_queue.append(page_number)
                    print(f"页面{page_number}被加载到内存")
                else:
                    # FIFO算法：选择最早进入内存的页面进行置换
                    page_of_out = self.fifo_queue[0]  # 最早进入的页面
                    self.fifo_queue.pop(0)
                    self.memory[self.memory.index(page_of_out)] = page_number  # 直接替换
                    self.fifo_queue.append(page_number)
                    print(f"页面{page_of_out}被置换出内存")
                    print(f"页面{page_number}被加载到内存块{self.memory.index(page_number)}")
                self.page_faults += 1
                print(f"更换后内存中页面：{self.memory}")
            else:
                print(f"指令：{i}在内存中，其在内存中物理地址为：{calculate_physical_address(page_offset, self.memory.index(page_number), self.page_size)}")
            print("--------------------------------")

        return self.page_faults

    def OPT(self):
        """
        最佳置换算法
        """
        for i in range(self.total_instructions):
            print("--------------------------------")
            print(f"指令：{i}，逻辑地址为：{self.sequence[i]}")
            page_number, page_offset = calculate_page_info(self.sequence[i], self.page_size)
            print(f"页号：{page_number}，页内地址：{page_offset}")
            print(f"内存中页面：{self.memory}")
            if page_number not in self.memory:
                print("发生缺页中断")
                if len(self.memory) < self.memory_blocks:
                    self.memory.append(page_number)
                    print(f"页面{page_number}被加载到内存")
                else:
                    # OPT算法：选择未来最长时间不会被使用的页面进行置换
                    victim_page = self._find_optimal_victim(i)
                    victim_index = self.memory.index(victim_page)
                    self.memory[victim_index] = page_number  # 直接替换
                    print(f"页面{victim_page}被置换出内存（OPT算法）")
                    print(f"页面{page_number}被加载到内存块{victim_index}")
                self.page_faults += 1
                print(f"更换后内存中页面：{self.memory}")
            else:
                print(f"指令：{i}在内存中，其在内存中物理地址为：{calculate_physical_address(page_offset, self.memory.index(page_number), self.page_size)}")
            print("--------------------------------")

        return self.page_faults

    def _find_optimal_victim(self, current_index):
        """
        找到最佳置换的页面（未来最长时间不会被使用的页面）
        
        Args:
            current_index: 当前指令索引
            
        Returns:
            int: 被置换的页号
        """
        future_usage = {}
        
        # 初始化所有内存中页面的未来使用时间
        for page in self.memory:
            future_usage[page] = float('inf')  # 默认无穷大
        
        # 检查未来指令序列
        for i in range(current_index + 1, len(self.sequence)):
            future_page = calculate_page_info(self.sequence[i], self.page_size)[0]
            if future_page in future_usage and future_usage[future_page] == float('inf'):
                future_usage[future_page] = i
        
        # 选择最晚使用的页面进行置换
        victim_page = max(future_usage, key=future_usage.get)
        return victim_page

class TkinterPageAnimation:
    def __init__(self, simulator):
        """
        使用Tkinter的页面置换算法动画演示类
        
        Args:
            simulator: PageReplacementSimulator实例
        """
        self.simulator = simulator
        self.root = None
        self.canvas = None
        self.current_step = 0
        self.animation_speed = 1000  # 毫秒
        self.is_running = False
        self.animation_thread = None
        self.algorithm_type = None
        self.fifo_faults = 0
        self.opt_faults = 0
        
    def create_selection_window(self):
        """创建算法选择界面"""
        self.root = tk.Tk()
        self.root.title("页面置换算法选择")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="页面置换算法模拟器")
        title_label.pack(pady=(0, 30))
        
        # 算法选择区域
        algorithm_frame = ttk.LabelFrame(main_frame, text="选择算法", padding=20)
        algorithm_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.algorithm_var = tk.StringVar(value="both")
        
        ttk.Radiobutton(algorithm_frame, text="FIFO算法", variable=self.algorithm_var, 
                       value="fifo").pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(algorithm_frame, text="OPT算法", variable=self.algorithm_var, 
                       value="opt").pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(algorithm_frame, text="两种算法都执行", variable=self.algorithm_var, 
                       value="both").pack(anchor=tk.W, pady=5)
        
        # 参数设置区域
        params_frame = ttk.LabelFrame(main_frame, text="参数设置", padding=20)
        params_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 指令序列长度
        ttk.Label(params_frame, text="指令序列长度:").pack(anchor=tk.W)
        self.sequence_length_var = tk.IntVar(value=320)
        sequence_length_entry = ttk.Entry(params_frame, textvariable=self.sequence_length_var, width=10)
        sequence_length_entry.pack(anchor=tk.W, pady=(5, 10))
        
        # 内存块数
        ttk.Label(params_frame, text="内存块数:").pack(anchor=tk.W)
        self.memory_blocks_var = tk.IntVar(value=4)
        memory_blocks_entry = ttk.Entry(params_frame, textvariable=self.memory_blocks_var, width=10)
        memory_blocks_entry.pack(anchor=tk.W, pady=(5, 10))
        
        # 页大小
        ttk.Label(params_frame, text="页大小:").pack(anchor=tk.W)
        self.page_size_var = tk.IntVar(value=10)
        page_size_entry = ttk.Entry(params_frame, textvariable=self.page_size_var, width=10)
        page_size_entry.pack(anchor=tk.W, pady=(5, 10))
        
        # 结果显示区域
        results_frame = ttk.LabelFrame(main_frame, text="计算结果", padding=20)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 创建结果显示的文本框
        self.results_text = tk.Text(results_frame, height=10, font=('Arial', 10), wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.calculate_button = ttk.Button(button_frame, text="计算算法性能", 
                                         command=self.calculate_algorithms)
        self.calculate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.animate_button = ttk.Button(button_frame, text="启动动画演示", 
                                       command=self.start_animation_demo)
        self.animate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="清空结果", 
                                     command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT)
        
        # 初始化结果显示
        self.results_text.insert(tk.END, "请选择算法并点击'计算算法性能'按钮开始计算...\n")
        self.results_text.config(state=tk.DISABLED)
        
    def calculate_algorithms(self):
        """计算选定算法的性能"""
        try:
            # 获取参数
            sequence_length = self.sequence_length_var.get()
            memory_blocks = self.memory_blocks_var.get()
            page_size = self.page_size_var.get()
            algorithm_choice = self.algorithm_var.get()
            
            # 生成新的随机序列
            new_sequence = generate_random_sequence()[:sequence_length]
            
            # 创建新的模拟器实例
            new_simulator = PageReplacementSimulator(
                total_instructions=sequence_length,
                page_size=page_size,
                memory_blocks=memory_blocks,
                sequence=new_sequence
            )
            
            # 清空结果显示
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            
            # 显示参数信息
            self.results_text.insert(tk.END, f"=== 参数设置 ===\n")
            self.results_text.insert(tk.END, f"指令序列长度: {sequence_length}\n")
            self.results_text.insert(tk.END, f"内存块数: {memory_blocks}\n")
            self.results_text.insert(tk.END, f"页大小: {page_size}\n")
            self.results_text.insert(tk.END, f"总页数: {sequence_length // page_size}\n")
            self.results_text.insert(tk.END, f"算法选择: {algorithm_choice}\n\n")
            
            # 计算选定的算法
            if algorithm_choice in ["fifo", "both"]:
                # 计算FIFO
                fifo_simulator = PageReplacementSimulator(
                    total_instructions=sequence_length,
                    page_size=page_size,
                    memory_blocks=memory_blocks,
                    sequence=new_sequence.copy()
                )
                self.fifo_faults = fifo_simulator.FIFO()
                fifo_rate = (self.fifo_faults / sequence_length) * 100
                
                self.results_text.insert(tk.END, f"=== FIFO算法结果 ===\n")
                self.results_text.insert(tk.END, f"缺页次数: {self.fifo_faults}\n")
                self.results_text.insert(tk.END, f"缺页率: {fifo_rate:.2f}%\n\n")
            
            if algorithm_choice in ["opt", "both"]:
                # 计算OPT
                opt_simulator = PageReplacementSimulator(
                    total_instructions=sequence_length,
                    page_size=page_size,
                    memory_blocks=memory_blocks,
                    sequence=new_sequence.copy()
                )
                self.opt_faults = opt_simulator.OPT()
                opt_rate = (self.opt_faults / sequence_length) * 100
                
                self.results_text.insert(tk.END, f"=== OPT算法结果 ===\n")
                self.results_text.insert(tk.END, f"缺页次数: {self.opt_faults}\n")
                self.results_text.insert(tk.END, f"缺页率: {opt_rate:.2f}%\n\n")
            
            # 比较结果
            if algorithm_choice == "both":
                self.results_text.insert(tk.END, f"=== 算法性能比较 ===\n")
                self.results_text.insert(tk.END, f"FIFO算法缺页次数: {self.fifo_faults}\n")
                self.results_text.insert(tk.END, f"OPT算法缺页次数: {self.opt_faults}\n")
                
                if self.fifo_faults > self.opt_faults:
                    improvement = ((self.fifo_faults - self.opt_faults) / self.fifo_faults) * 100
                    self.results_text.insert(tk.END, f"OPT算法相比FIFO算法减少了 {improvement:.2f}% 的缺页\n")
                elif self.fifo_faults < self.opt_faults:
                    degradation = ((self.opt_faults - self.fifo_faults) / self.opt_faults) * 100
                    self.results_text.insert(tk.END, f"FIFO算法相比OPT算法减少了 {degradation:.2f}% 的缺页\n")
                else:
                    self.results_text.insert(tk.END, f"两种算法性能相同\n")
            
            # 更新模拟器实例
            self.simulator = new_simulator
            
            self.results_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.results_text.config(state=tk.NORMAL)
            self.results_text.insert(tk.END, f"计算过程中出现错误: {str(e)}\n")
            self.results_text.config(state=tk.DISABLED)
    
    def clear_results(self):
        """清空结果显示"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "请选择算法并点击'计算算法性能'按钮开始计算...\n")
        self.results_text.config(state=tk.DISABLED)
    
    def start_animation_demo(self):
        """启动动画演示"""
        algorithm_choice = self.algorithm_var.get()
        
        if algorithm_choice == "fifo":
            self.algorithm_type = 'FIFO'
            self.create_window("FIFO页面置换算法动画演示")
            self.draw_memory_blocks()
            self.root.mainloop()
        elif algorithm_choice == "opt":
            self.algorithm_type = 'OPT'
            self.create_window("OPT页面置换算法动画演示")
            self.draw_memory_blocks()
            self.root.mainloop()
        elif algorithm_choice == "both":
            # 创建选择窗口
            self.create_animation_selection_window()
        else:
            tk.messagebox.showwarning("警告", "请先选择算法！")
    
    def create_animation_selection_window(self):
        """创建动画选择窗口"""
        animation_window = tk.Toplevel(self.root)
        animation_window.title("选择动画演示算法")
        animation_window.geometry("400x300")
        animation_window.configure(bg='#f0f0f0')
        
        # 主框架
        main_frame = ttk.Frame(animation_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="选择要演示的算法")
        title_label.pack(pady=(0, 30))
        
        # 按钮
        fifo_button = ttk.Button(main_frame, text="FIFO算法动画", 
                               command=lambda: self.start_specific_animation('FIFO', animation_window))
        fifo_button.pack(pady=10)
        
        opt_button = ttk.Button(main_frame, text="OPT算法动画", 
                              command=lambda: self.start_specific_animation('OPT', animation_window))
        opt_button.pack(pady=10)
        
        # 关闭按钮
        close_button = ttk.Button(main_frame, text="关闭", 
                                command=animation_window.destroy)
        close_button.pack(pady=20)
    
    def start_specific_animation(self, algorithm, window):
        """启动特定的算法动画"""
        window.destroy()
        
        if algorithm == 'FIFO':
            self.algorithm_type = 'FIFO'
            self.create_window("FIFO页面置换算法动画演示")
        else:
            self.algorithm_type = 'OPT'
            self.create_window("OPT页面置换算法动画演示")
        
        self.draw_memory_blocks()
        self.root.mainloop()

    def create_window(self, title="页面置换算法动画演示"):
        """创建动画窗口"""
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("1200x800")  # 增加窗口大小
        self.root.configure(bg='#f0f0f0')
        
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 标题
        title_label = ttk.Label(main_frame, text=title, font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 创建画布
        self.canvas = tk.Canvas(main_frame, width=1150, height=500, bg='white', 
                              relief=tk.RAISED, bd=2)
        self.canvas.pack(pady=(0, 20))
        
        # 控制面板
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, 
                                          maximum=len(self.simulator.sequence))
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # 控制按钮
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT)
        
        self.start_button = ttk.Button(button_frame, text="开始", command=self.start_animation)
        self.start_button.pack(side=tk.LEFT, padx=2)
        
        self.pause_button = ttk.Button(button_frame, text="暂停", command=self.pause_animation, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=2)
        
        self.reset_button = ttk.Button(button_frame, text="重置", command=self.reset_animation)
        self.reset_button.pack(side=tk.LEFT, padx=2)
        
        # 速度控制
        speed_frame = ttk.Frame(main_frame)
        speed_frame.pack(fill=tk.X)
        
        ttk.Label(speed_frame, text="动画速度:").pack(side=tk.LEFT)
        self.speed_var = tk.IntVar(value=1000)
        speed_scale = ttk.Scale(speed_frame, from_=100, to=3000, variable=self.speed_var, 
                               orient=tk.HORIZONTAL, length=200)
        speed_scale.pack(side=tk.LEFT, padx=(10, 0))
        
        # 信息显示区域
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 创建信息标签
        self.info_labels = {}
        info_items = [
            ('current_instruction', '当前指令:'),
            ('logical_address', '逻辑地址:'),
            ('page_number', '页号:'),
            ('page_offset', '页内地址:'),
            ('memory_status', '内存状态:'),
            ('page_faults', '缺页次数:'),
            ('status', '状态:'),
            ('action', '操作:'),
            ('physical_address', '物理地址:'),
            ('address_conversion', '地址转换:')
        ]
        
        for i, (key, text) in enumerate(info_items):
            row = i // 2
            col = i % 2
            
            frame = ttk.Frame(info_frame)
            frame.grid(row=row, column=col, sticky='ew', padx=5, pady=2)
            
            ttk.Label(frame, text=text, font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
            label = ttk.Label(frame, text='-', font=('Arial', 10))
            label.pack(side=tk.LEFT, padx=(5, 0))
            self.info_labels[key] = label
        
        # 配置网格权重
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)
        
    def draw_memory_blocks(self):
        """绘制内存块"""
        self.canvas.delete("memory_blocks")
        
        # 内存块标题
        self.canvas.create_text(575, 30, text="内存块状态", font=('Arial', 14, 'bold'), 
                              fill='#333333', tags="memory_blocks")
        
        # 绘制4个内存块
        block_width = 180
        block_height = 100
        start_x = 50
        start_y = 60
        
        for i in range(4):
            x = start_x + i * (block_width + 30)
            y = start_y
            
            # 内存块背景
            if i < len(self.simulator.memory):
                # 有页面的块
                fill_color = '#e8f5e8'  # 浅绿色
                outline_color = '#4CAF50'  # 绿色边框
            else:
                # 空块
                fill_color = '#f5f5f5'  # 浅灰色
                outline_color = '#cccccc'  # 灰色边框
            
            # 绘制内存块
            self.canvas.create_rectangle(x, y, x + block_width, y + block_height, 
                                       fill=fill_color, outline=outline_color, 
                                       width=2, tags="memory_blocks")
            
            # 块号
            self.canvas.create_text(x + block_width//2, y + 20, 
                                  text=f"内存块 {i}", font=('Arial', 10, 'bold'), 
                                  fill='#666666', tags="memory_blocks")
            
            # 页面内容
            if i < len(self.simulator.memory):
                page_num = self.simulator.memory[i]
                self.canvas.create_text(x + block_width//2, y + block_height//2, 
                                      text=f"页面 {page_num}", font=('Arial', 12, 'bold'), 
                                      fill='#2E7D32', tags="memory_blocks")
            else:
                self.canvas.create_text(x + block_width//2, y + block_height//2, 
                                      text="空闲", font=('Arial', 10), 
                                      fill='#999999', tags="memory_blocks")
        
        # 绘制地址转换区域
        self.draw_address_conversion_area()
    
    def draw_address_conversion_area(self):
        """绘制地址转换区域"""
        # 地址转换区域标题
        self.canvas.create_text(575, 200, text="地址转换过程", font=('Arial', 14, 'bold'), 
                              fill='#333333', tags="address_area")
        
        # 绘制地址转换流程图
        # 逻辑地址框
        self.canvas.create_rectangle(50, 220, 220, 280, fill='#E3F2FD', outline='#2196F3', 
                                   width=2, tags="address_area")
        self.canvas.create_text(135, 235, text="逻辑地址", font=('Arial', 10, 'bold'), 
                              fill='#1976D2', tags="address_area")
        self.logical_addr_text = self.canvas.create_text(135, 255, text="", 
                                                       font=('Arial', 12), fill='#1976D2', 
                                                       tags="address_area")
        
        # 箭头1
        self.canvas.create_text(245, 250, text="→", font=('Arial', 16, 'bold'), 
                              fill='#666666', tags="address_area")
        
        # 页号框
        self.canvas.create_rectangle(270, 220, 370, 280, fill='#FFF3E0', outline='#FF9800', 
                                   width=2, tags="address_area")
        self.canvas.create_text(320, 235, text="页号", font=('Arial', 10, 'bold'), 
                              fill='#E65100', tags="address_area")
        self.page_num_text = self.canvas.create_text(320, 255, text="", 
                                                   font=('Arial', 12), fill='#E65100', 
                                                   tags="address_area")
        
        # 箭头2
        self.canvas.create_text(395, 250, text="→", font=('Arial', 16, 'bold'), 
                              fill='#666666', tags="address_area")
        
        # 内存块号框
        self.canvas.create_rectangle(420, 220, 520, 280, fill='#E8F5E8', outline='#4CAF50', 
                                   width=2, tags="address_area")
        self.canvas.create_text(470, 235, text="内存块号", font=('Arial', 10, 'bold'), 
                              fill='#2E7D32', tags="address_area")
        self.frame_num_text = self.canvas.create_text(470, 255, text="", 
                                                    font=('Arial', 12), fill='#2E7D32', 
                                                    tags="address_area")
        
        # 箭头3
        self.canvas.create_text(545, 250, text="→", font=('Arial', 16, 'bold'), 
                              fill='#666666', tags="address_area")
        
        # 物理地址框
        self.canvas.create_rectangle(570, 220, 720, 280, fill='#F3E5F5', outline='#9C27B0', 
                                   width=2, tags="address_area")
        self.canvas.create_text(645, 235, text="物理地址", font=('Arial', 10, 'bold'), 
                              fill='#7B1FA2', tags="address_area")
        self.physical_addr_text = self.canvas.create_text(645, 255, text="", 
                                                        font=('Arial', 12), fill='#7B1FA2', 
                                                        tags="address_area")
        
        # 页内地址框
        self.canvas.create_rectangle(745, 220, 845, 280, fill='#FFF8E1', outline='#FFC107', 
                                   width=2, tags="address_area")
        self.canvas.create_text(795, 235, text="页内地址", font=('Arial', 10, 'bold'), 
                              fill='#F57F17', tags="address_area")
        self.page_offset_text = self.canvas.create_text(795, 255, text="", 
                                                      font=('Arial', 12), fill='#F57F17', 
                                                      tags="address_area")
        
        # 公式说明
        self.canvas.create_text(575, 310, text="物理地址 = 内存块号 × 页大小 + 页内地址", 
                              font=('Arial', 10), fill='#666666', tags="address_area")
    
    def update_address_conversion(self, logical_address, page_number, page_offset):
        """更新地址转换显示"""
        self.canvas.delete("address_conversion")
        
        # 更新逻辑地址
        self.canvas.itemconfig(self.logical_addr_text, text=str(logical_address))
        
        # 更新页号
        self.canvas.itemconfig(self.page_num_text, text=str(page_number))
        
        # 更新页内地址
        self.canvas.itemconfig(self.page_offset_text, text=str(page_offset))
        
        # 检查页面是否在内存中
        if page_number in self.simulator.memory:
            # 页面在内存中，计算物理地址
            frame_number = self.simulator.memory.index(page_number)
            physical_address = calculate_physical_address(page_offset, frame_number, self.simulator.page_size)
            
            # 更新内存块号
            self.canvas.itemconfig(self.frame_num_text, text=str(frame_number))
            
            # 更新物理地址
            self.canvas.itemconfig(self.physical_addr_text, text=str(physical_address))
            
            # 高亮显示转换过程
            self.canvas.create_text(575, 350, text=f"✓ 页面命中：逻辑地址{logical_address} → 物理地址{physical_address}", 
                                  font=('Arial', 12, 'bold'), fill='#4CAF50', tags="address_conversion")
        else:
            # 页面不在内存中
            self.canvas.itemconfig(self.frame_num_text, text="缺页")
            self.canvas.itemconfig(self.physical_addr_text, text="无法计算")
            
            # 检查是否有特殊状态
            current_status = self.info_labels['status'].cget("text")
            if current_status == "页面置换中":
                # 显示置换信息
                if hasattr(self, 'algorithm_type') and self.algorithm_type == 'OPT':
                    victim_page = self.simulator._find_optimal_victim(self.current_step)
                    algorithm_name = "OPT算法"
                else:  # FIFO
                    victim_page = self.simulator.fifo_queue[0]
                    algorithm_name = "FIFO算法"
                
                self.canvas.create_text(575, 350, text=f"🔄 {algorithm_name}：置换页面{victim_page}，加载页面{page_number}", 
                                      font=('Arial', 12, 'bold'), fill='#FF9800', tags="address_conversion")
            elif current_status == "页面加载中":
                # 显示加载信息
                self.canvas.create_text(575, 350, text=f"📥 页面加载：页面{page_number}加载到空闲块", 
                                      font=('Arial', 12, 'bold'), fill='#4CAF50', tags="address_conversion")
            else:
                # 显示缺页信息
                self.canvas.create_text(575, 350, text=f"✗ 缺页中断：页面{page_number}不在内存中", 
                                      font=('Arial', 12, 'bold'), fill='#F44336', tags="address_conversion")
    
    def highlight_current_page(self, page_number):
        """高亮显示当前访问的页面"""
        self.canvas.delete("highlight")
        
        if page_number in self.simulator.memory:
            # 找到页面在内存中的位置
            block_index = self.simulator.memory.index(page_number)
            block_width = 180
            block_height = 100
            start_x = 50
            start_y = 60
            
            x = start_x + block_index * (block_width + 30)
            y = start_y
            
            # 绘制高亮边框
            self.canvas.create_rectangle(x-3, y-3, x + block_width+3, y + block_height+3, 
                                       outline='#FF5722', width=3, tags="highlight")
            
            # 添加命中标记
            self.canvas.create_text(x + block_width + 10, y + block_height//2, 
                                  text="✓", font=('Arial', 16, 'bold'), 
                                  fill='#4CAF50', tags="highlight")
    
    def show_page_check_animation(self, page_number):
        """显示页面检查动画"""
        # 清除所有动画图标
        self.canvas.delete("page_check")
        self.canvas.delete("free_block")
        self.canvas.delete("replacement")
        self.canvas.delete("page_hit")
        
        # 显示检查过程
        self.canvas.create_text(575, 380, text="🔍", font=('Arial', 48), 
                              fill='#2196F3', tags="page_check")
        self.canvas.create_text(575, 430, text="正在检查页面...", font=('Arial', 16, 'bold'), 
                              fill='#2196F3', tags="page_check")
        self.canvas.create_text(575, 460, text=f"检查页面 {page_number} 是否在内存中", 
                              font=('Arial', 12), fill='#666666', tags="page_check")
    
    def process_page_access(self, page_number, page_offset):
        """处理页面访问"""
        if page_number not in self.simulator.memory:
            # 缺页处理
            self.handle_page_fault(page_number, page_offset)
            
            # 更新置换过程中的状态显示
            if len(self.simulator.memory) >= self.simulator.memory_blocks:
                # 需要置换的情况
                if hasattr(self, 'algorithm_type') and self.algorithm_type == 'OPT':
                    victim_page = self.simulator._find_optimal_victim(self.current_step)
                    victim_index = self.simulator.memory.index(victim_page)
                    self.info_labels['status'].config(text="页面置换中", foreground='orange')
                    self.info_labels['action'].config(text=f"OPT: 置换页面{victim_page}，加载页面{page_number}到内存块{victim_index}")
                else:  # FIFO
                    victim_page = self.simulator.fifo_queue[0]
                    victim_index = self.simulator.memory.index(victim_page)
                    self.info_labels['status'].config(text="页面置换中", foreground='orange')
                    self.info_labels['action'].config(text=f"FIFO: 置换页面{victim_page}，加载页面{page_number}到内存块{victim_index}")
            else:
                # 空闲块加载
                self.info_labels['status'].config(text="页面加载中", foreground='blue')
                self.info_labels['action'].config(text=f"加载页面 {page_number} 到空闲块")
        else:
            # 页面命中
            self.handle_page_hit(page_number, page_offset)
        
        # 更新显示
        self.draw_memory_blocks()
        self.update_info_display(self.current_step)
        self.progress_var.set(self.current_step + 1)
        
        self.current_step += 1
        
        # 继续下一步
        if self.current_step < len(self.simulator.sequence) and self.is_running:
            self.root.after(self.speed_var.get(), self.step_animation)
        else:
            self.animation_finished()
    
    def handle_page_fault(self, page_number, page_offset):
        """处理缺页中断"""
        if len(self.simulator.memory) < self.simulator.memory_blocks:
            # 还有空闲块
            self.show_free_block_animation(page_number)
            self.simulator.memory.append(page_number)
            if hasattr(self, 'algorithm_type') and self.algorithm_type == 'FIFO':
                self.simulator.fifo_queue.append(page_number)
        else:
            # 需要置换
            self.show_page_replacement_animation(page_number)
            
            if hasattr(self, 'algorithm_type') and self.algorithm_type == 'OPT':
                # OPT算法
                victim_page = self.simulator._find_optimal_victim(self.current_step)
                victim_index = self.simulator.memory.index(victim_page)
                self.simulator.memory[victim_index] = page_number
            else:  # FIFO算法
                victim_page = self.simulator.fifo_queue[0]
                self.simulator.fifo_queue.pop(0)
                victim_index = self.simulator.memory.index(victim_page)
                self.simulator.memory[victim_index] = page_number
                self.simulator.fifo_queue.append(page_number)
        
        self.simulator.page_faults += 1
    
    def handle_page_hit(self, page_number, page_offset):
        """处理页面命中"""
        self.show_page_hit_animation(page_number)
    
    def show_free_block_animation(self, page_number):
        """显示空闲块加载动画"""
        # 清除所有动画图标
        self.canvas.delete("page_check")
        self.canvas.delete("free_block")
        self.canvas.delete("replacement")
        self.canvas.delete("page_hit")
        
        # 找到空闲块位置
        free_block_index = len(self.simulator.memory)
        
        # 显示加载过程
        self.canvas.create_text(575, 380, text="📥", font=('Arial', 48), 
                              fill='#4CAF50', tags="free_block")
        self.canvas.create_text(575, 430, text="加载页面到空闲块", font=('Arial', 16, 'bold'), 
                              fill='#4CAF50', tags="free_block")
        self.canvas.create_text(575, 460, text=f"页面 {page_number} 加载到内存块 {free_block_index}", 
                              font=('Arial', 12), fill='#666666', tags="free_block")
    
    def show_page_replacement_animation(self, page_number):
        """显示页面置换动画"""
        # 清除所有动画图标
        self.canvas.delete("page_check")
        self.canvas.delete("free_block")
        self.canvas.delete("replacement")
        self.canvas.delete("page_hit")
        
        # 确定被置换的页面
        if hasattr(self, 'algorithm_type') and self.algorithm_type == 'OPT':
            victim_page = self.simulator._find_optimal_victim(self.current_step)
            algorithm_name = "OPT算法"
        else:  # FIFO
            victim_page = self.simulator.fifo_queue[0]
            algorithm_name = "FIFO算法"
        
        victim_index = self.simulator.memory.index(victim_page)
        
        # 显示置换过程
        self.canvas.create_text(575, 380, text="🔄", font=('Arial', 48), 
                              fill='#FF9800', tags="replacement")
        self.canvas.create_text(575, 430, text="页面置换过程", font=('Arial', 16, 'bold'), 
                              fill='#FF9800', tags="replacement")
        
        # 显示详细的置换信息
        self.canvas.create_text(575, 460, text=f"{algorithm_name}：置换页面 {victim_page}，加载页面 {page_number}", 
                              font=('Arial', 12), fill='#666666', tags="replacement")
        self.canvas.create_text(575, 480, text=f"置换位置：内存块 {victim_index}", 
                              font=('Arial', 12), fill='#666666', tags="replacement")
    
    def show_page_hit_animation(self, page_number):
        """显示页面命中动画"""
        # 清除所有动画图标
        self.canvas.delete("page_check")
        self.canvas.delete("free_block")
        self.canvas.delete("replacement")
        self.canvas.delete("page_hit")
        
        # 显示命中过程
        self.canvas.create_text(575, 380, text="✅", font=('Arial', 48), 
                              fill='#4CAF50', tags="page_hit")
        self.canvas.create_text(575, 430, text="页面命中", font=('Arial', 16, 'bold'), 
                              fill='#4CAF50', tags="page_hit")
        self.canvas.create_text(575, 460, text=f"页面 {page_number} 已在内存中，直接访问", 
                              font=('Arial', 12), fill='#666666', tags="page_hit")
    
    def start_animation(self):
        """开始动画"""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.step_animation()
    
    def pause_animation(self):
        """暂停动画"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
    
    def reset_animation(self):
        """重置动画"""
        self.is_running = False
        self.current_step = 0
        self.simulator.reset()
        self.progress_var.set(0)
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        
        # 清空画布
        self.canvas.delete("all")
        self.draw_memory_blocks()
        
        # 重置信息显示
        for label in self.info_labels.values():
            label.config(text='-', foreground='black')
    
    def animation_finished(self):
        """动画完成"""
        self.is_running = False
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED)
        
        # 清除所有动画图标
        self.canvas.delete("page_check")
        self.canvas.delete("free_block")
        self.canvas.delete("replacement")
        self.canvas.delete("page_hit")
        
        # 显示完成信息
        self.canvas.create_text(575, 380, text="✓", font=('Arial', 48), 
                              fill='#4CAF50', tags="finished")
        self.canvas.create_text(575, 430, text="动画演示完成", font=('Arial', 16, 'bold'), 
                              fill='#4CAF50', tags="finished")
        self.canvas.create_text(575, 460, text=f"总缺页次数: {self.simulator.page_faults}", 
                              font=('Arial', 12), fill='#666666', tags="finished")
    
    def animate_fifo(self):
        """FIFO算法动画"""
        self.simulator.reset()
        self.algorithm_type = 'FIFO'
        self.create_window("FIFO页面置换算法动画演示")
        self.draw_memory_blocks()
        self.root.mainloop()
        return self.simulator.page_faults
    
    def animate_opt(self):
        """OPT算法动画"""
        self.simulator.reset()
        self.algorithm_type = 'OPT'
        self.create_window("OPT页面置换算法动画演示")
        self.draw_memory_blocks()
        self.root.mainloop()
        return self.simulator.page_faults

    def update_info_display(self, step):
        """更新信息显示"""
        if step >= len(self.simulator.sequence):
            return
            
        logical_address = self.simulator.sequence[step]
        page_number, page_offset = calculate_page_info(logical_address, self.simulator.page_size)
        
        # 更新信息标签
        self.info_labels['current_instruction'].config(text=f"{step}")
        self.info_labels['logical_address'].config(text=f"{logical_address}")
        self.info_labels['page_number'].config(text=f"{page_number}")
        self.info_labels['page_offset'].config(text=f"{page_offset}")
        self.info_labels['memory_status'].config(text=str(self.simulator.memory))
        self.info_labels['page_faults'].config(text=f"{self.simulator.page_faults}")
        
        # 检查是否缺页
        if page_number not in self.simulator.memory:
            # 只有在没有特殊状态时才更新状态显示
            current_status = self.info_labels['status'].cget("text")
            if current_status not in ["页面置换中", "页面加载中"]:
                self.info_labels['status'].config(text="页面未命中", foreground='red')
                self.info_labels['physical_address'].config(text="无法计算")
                self.info_labels['address_conversion'].config(text="页面不在内存中")
                
                # 显示详细的操作信息
                if len(self.simulator.memory) < self.simulator.memory_blocks:
                    self.info_labels['action'].config(text=f"加载页面 {page_number}")
                else:
                    if hasattr(self, 'algorithm_type') and self.algorithm_type == 'OPT':
                        victim_page = self.simulator._find_optimal_victim(step)
                        victim_index = self.simulator.memory.index(victim_page)
                        self.info_labels['action'].config(text=f"OPT: 置换页面{victim_page}，加载页面{page_number}到内存块{victim_index}")
                    else:  # FIFO
                        victim_page = self.simulator.fifo_queue[0]
                        victim_index = self.simulator.memory.index(victim_page)
                        self.info_labels['action'].config(text=f"FIFO: 置换页面{victim_page}，加载页面{page_number}到内存块{victim_index}")
        else:
            # 页面命中，计算物理地址
            frame_number = self.simulator.memory.index(page_number)
            physical_address = calculate_physical_address(page_offset, frame_number, self.simulator.page_size)
            
            self.info_labels['status'].config(text="页面命中", foreground='green')
            self.info_labels['physical_address'].config(text=f"{physical_address}")
            self.info_labels['address_conversion'].config(text=f"内存块{frame_number} × 10 + {page_offset} = {physical_address}")
            self.info_labels['action'].config(text="直接访问")
            self.highlight_current_page(page_number)
        
        # 更新地址转换可视化
        self.update_address_conversion(logical_address, page_number, page_offset)
    
    def step_animation(self):
        """执行一步动画"""
        if self.current_step >= len(self.simulator.sequence) or not self.is_running:
            return
        
        # 执行算法步骤
        logical_address = self.simulator.sequence[self.current_step]
        page_number, page_offset = calculate_page_info(logical_address, self.simulator.page_size)
        
        # 先显示页面检查过程
        self.show_page_check_animation(page_number)
        
        # 延迟显示结果
        self.root.after(800, lambda: self.process_page_access(page_number, page_offset))

# 测试函数
if __name__ == "__main__":
    # 生成随机序列
    random_sequence = generate_random_sequence()

    simulator = PageReplacementSimulator(total_instructions=320, page_size=10, memory_blocks=4, sequence=random_sequence)
    
    print("=== 页面置换算法模拟器 ===")
    print("正在启动交互界面...")
    
    # 创建动画演示器并启动选择界面
    tk_animator = TkinterPageAnimation(simulator)
    tk_animator.create_selection_window()
    tk_animator.root.mainloop()

    

