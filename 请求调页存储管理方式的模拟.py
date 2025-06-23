import random
from collections import deque

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

    def reset(self):
        """
        重置模拟器到初始状态
        """
        self.memory = []  # 清空内存
        self.page_faults = 0  # 重置缺页次数
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
                    print(f"页面{page_number}被加载到内存")
                else:
                    page_of_out = self.memory.pop(0)
                    print(f"页面{page_of_out}被置换出内存")
                    self.memory.append(page_number)
                    print(f"页面{page_number}被加载到内存")
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
                    self.memory.remove(victim_page)
                    print(f"页面{victim_page}被置换出内存（OPT算法）")
                    self.memory.append(page_number)
                    print(f"页面{page_number}被加载到内存")
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

# 测试函数
if __name__ == "__main__":
    # 生成随机序列
    random_sequence = generate_random_sequence()

    simulator = PageReplacementSimulator(total_instructions=320, page_size=10, memory_blocks=4, sequence=random_sequence)
    
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

    

