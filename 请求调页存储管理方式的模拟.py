import random
from collections import deque
import tkinter as tk
from tkinter import ttk
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
        
    def create_window(self, title="页面置换算法动画演示"):
        """创建动画窗口"""
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 标题
        title_label = ttk.Label(main_frame, text=title, font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 创建画布
        self.canvas = tk.Canvas(main_frame, width=750, height=400, bg='white', 
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
            ('action', '操作:')
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
        self.canvas.create_text(375, 30, text="内存块状态", font=('Arial', 14, 'bold'), 
                              fill='#333333', tags="memory_blocks")
        
        # 绘制4个内存块
        block_width = 150
        block_height = 80
        start_x = 50
        start_y = 60
        
        for i in range(4):
            x = start_x + i * (block_width + 20)
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
            self.canvas.create_text(x + block_width//2, y + 15, 
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
    
    def highlight_current_page(self, page_number):
        """高亮显示当前访问的页面"""
        self.canvas.delete("highlight")
        
        if page_number in self.simulator.memory:
            # 找到页面在内存中的位置
            block_index = self.simulator.memory.index(page_number)
            block_width = 150
            block_height = 80
            start_x = 50
            start_y = 60
            
            x = start_x + block_index * (block_width + 20)
            y = start_y
            
            # 绘制高亮边框
            self.canvas.create_rectangle(x-3, y-3, x + block_width+3, y + block_height+3, 
                                       outline='#FF5722', width=3, tags="highlight")
            
            # 添加命中标记
            self.canvas.create_text(x + block_width + 10, y + block_height//2, 
                                  text="✓", font=('Arial', 16, 'bold'), 
                                  fill='#4CAF50', tags="highlight")
    
    def show_page_fault_animation(self, page_number):
        """显示缺页动画"""
        self.canvas.delete("page_fault")
        
        # 显示缺页图标
        self.canvas.create_text(375, 200, text="⚠", font=('Arial', 48), 
                              fill='#FF9800', tags="page_fault")
        
        # 显示缺页信息
        self.canvas.create_text(375, 250, text="缺页中断", font=('Arial', 16, 'bold'), 
                              fill='#FF5722', tags="page_fault")
        
        # 显示加载信息
        if len(self.simulator.memory) < self.simulator.memory_blocks:
            text = f"加载页面 {page_number} 到空闲内存块"
        else:
            # 显示被置换的页面信息
            if hasattr(self, 'algorithm_type') and self.algorithm_type == 'OPT':
                victim_page = self.simulator._find_optimal_victim(self.current_step)
                victim_index = self.simulator.memory.index(victim_page)
                text = f"OPT算法：置换页面 {victim_page}，加载页面 {page_number} 到内存块{victim_index}"
            else:  # FIFO
                # 在FIFO中，被置换的是最早进入的页面
                victim_page = self.simulator.fifo_queue[0]  # 即将被置换的页面
                victim_index = self.simulator.memory.index(victim_page)
                text = f"FIFO算法：置换页面 {victim_page}，加载页面 {page_number} 到内存块{victim_index}"
        
        self.canvas.create_text(375, 280, text=text, font=('Arial', 12), 
                              fill='#666666', tags="page_fault")
    
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
            self.info_labels['status'].config(text="缺页中断", foreground='red')
            
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
            
            self.show_page_fault_animation(page_number)
        else:
            self.info_labels['status'].config(text="页面命中", foreground='green')
            self.info_labels['action'].config(text="直接访问")
            self.highlight_current_page(page_number)
    
    def step_animation(self):
        """执行一步动画"""
        if self.current_step >= len(self.simulator.sequence) or not self.is_running:
            return
        
        # 执行算法步骤
        logical_address = self.simulator.sequence[self.current_step]
        page_number, page_offset = calculate_page_info(logical_address, self.simulator.page_size)
        
        if page_number not in self.simulator.memory:
            if len(self.simulator.memory) < self.simulator.memory_blocks:
                # 还有空闲块，直接加载
                self.simulator.memory.append(page_number)
                if hasattr(self, 'algorithm_type') and self.algorithm_type == 'FIFO':
                    self.simulator.fifo_queue.append(page_number)
            else:
                # 需要置换
                if hasattr(self, 'algorithm_type') and self.algorithm_type == 'OPT':
                    # OPT算法：选择未来最长时间不会被使用的页面进行置换
                    victim_page = self.simulator._find_optimal_victim(self.current_step)
                    victim_index = self.simulator.memory.index(victim_page)
                    self.simulator.memory[victim_index] = page_number  # 直接替换
                else:  # FIFO算法：选择最早进入内存的页面进行置换
                    # 从FIFO队列中获取最早进入的页面
                    victim_page = self.simulator.fifo_queue[0]
                    self.simulator.fifo_queue.pop(0)  # 移除最早进入的页面
                    victim_index = self.simulator.memory.index(victim_page)
                    self.simulator.memory[victim_index] = page_number  # 直接替换
                    self.simulator.fifo_queue.append(page_number)  # 新页面加入队列
            self.simulator.page_faults += 1
        
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
        
        # 显示完成信息
        self.canvas.delete("page_fault")
        self.canvas.create_text(375, 200, text="✓", font=('Arial', 48), 
                              fill='#4CAF50', tags="finished")
        self.canvas.create_text(375, 250, text="动画演示完成", font=('Arial', 16, 'bold'), 
                              fill='#4CAF50', tags="finished")
        self.canvas.create_text(375, 280, text=f"总缺页次数: {self.simulator.page_faults}", 
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

# 测试函数
if __name__ == "__main__":
    # 生成随机序列
    random_sequence = generate_random_sequence()

    simulator = PageReplacementSimulator(total_instructions=320, page_size=10, memory_blocks=4, sequence=random_sequence)
    
    print("请选择运行模式：")
    print("1. 文本模式（详细输出）")
    print("2. Tkinter动画模式（推荐）")
    print("3. 两种模式都运行")
    
    choice = input("请输入选择（1/2/3）: ").strip()
    
    if choice == "1":
        print("=== 执行FIFO算法 ===")
        fifo_faults = simulator.FIFO()
        print(f"FIFO算法缺页次数: {fifo_faults}")
        
        print("\n=== 重置模拟器 ===")
        simulator.reset()
        
        print("\n=== 执行OPT算法 ===")
        opt_faults = simulator.OPT()
        print(f"OPT算法缺页次数: {opt_faults}")
        
        print("\n=== 算法性能比较 ===")
        print(f"FIFO算法缺页次数: {fifo_faults}")
        print(f"OPT算法缺页次数: {opt_faults}")
        if fifo_faults > opt_faults:
            improvement = ((fifo_faults - opt_faults) / fifo_faults) * 100
            print(f"OPT算法相比FIFO算法减少了 {improvement:.2f}% 的缺页")
        else:
            print("FIFO算法表现更好（理论上不应该发生）")
    
    elif choice == "2":
        print("=== Tkinter动画演示模式 ===")
        tk_animator = TkinterPageAnimation(simulator)
        
        print("正在启动FIFO算法动画...")
        fifo_faults = tk_animator.animate_fifo()
        print(f"FIFO算法缺页次数: {fifo_faults}")
        
        print("\n正在启动OPT算法动画...")
        opt_faults = tk_animator.animate_opt()
        print(f"OPT算法缺页次数: {opt_faults}")
        
        print("\n=== 算法性能比较 ===")
        print(f"FIFO算法缺页次数: {fifo_faults}")
        print(f"OPT算法缺页次数: {opt_faults}")
        if fifo_faults > opt_faults:
            improvement = ((fifo_faults - opt_faults) / fifo_faults) * 100
            print(f"OPT算法相比FIFO算法减少了 {improvement:.2f}% 的缺页")
        else:
            print("FIFO算法表现更好（理论上不应该发生）")
    
    elif choice == "3":
        print("=== 文本模式 ===")
        print("=== 执行FIFO算法 ===")
        fifo_faults = simulator.FIFO()
        print(f"FIFO算法缺页次数: {fifo_faults}")
        
        print("\n=== 重置模拟器 ===")
        simulator.reset()
        
        print("\n=== 执行OPT算法 ===")
        opt_faults = simulator.OPT()
        print(f"OPT算法缺页次数: {opt_faults}")
        
        print("\n=== Tkinter动画演示模式 ===")
        tk_animator = TkinterPageAnimation(simulator)
        
        print("正在启动FIFO算法动画...")
        fifo_faults_tk = tk_animator.animate_fifo()
        print(f"FIFO算法缺页次数: {fifo_faults_tk}")
        
        print("\n正在启动OPT算法动画...")
        opt_faults_tk = tk_animator.animate_opt()
        print(f"OPT算法缺页次数: {opt_faults_tk}")
        
        print("\n=== 算法性能比较 ===")
        print(f"FIFO算法缺页次数: {fifo_faults}")
        print(f"OPT算法缺页次数: {opt_faults}")
        if fifo_faults > opt_faults:
            improvement = ((fifo_faults - opt_faults) / fifo_faults) * 100
            print(f"OPT算法相比FIFO算法减少了 {improvement:.2f}% 的缺页")
        else:
            print("FIFO算法表现更好（理论上不应该发生）")
    
    else:
        print("无效选择，默认运行Tkinter动画模式")
        print("=== Tkinter动画演示模式 ===")
        tk_animator = TkinterPageAnimation(simulator)
        
        print("正在启动FIFO算法动画...")
        fifo_faults = tk_animator.animate_fifo()
        print(f"FIFO算法缺页次数: {fifo_faults}")
        
        print("\n正在启动OPT算法动画...")
        opt_faults = tk_animator.animate_opt()
        print(f"OPT算法缺页次数: {opt_faults}")
        
        print("\n=== 算法性能比较 ===")
        print(f"FIFO算法缺页次数: {fifo_faults}")
        print(f"OPT算法缺页次数: {opt_faults}")
        if fifo_faults > opt_faults:
            improvement = ((fifo_faults - opt_faults) / fifo_faults) * 100
            print(f"OPT算法相比FIFO算法减少了 {improvement:.2f}% 的缺页")
        else:
            print("FIFO算法表现更好（理论上不应该发生）")

    

