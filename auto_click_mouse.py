import tkinter as tk
from tkinter import messagebox
from pynput.mouse import Button, Controller
from pynput import keyboard
import time
from datetime import datetime, timedelta
import re

# 初始化鼠标控制器
mouse = Controller()

# 全局变量
paused = False
last_ctrl_time = 0  # 用于记录最近一次按下 Ctrl 的时间

def on_press(key):
    global paused, last_ctrl_time
    
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        current_time = time.time()
        
        # 检测双击 Ctrl 键
        if last_ctrl_time and (current_time - last_ctrl_time < 0.5):
            paused = not paused
            status = "暂停" if paused else "继续"
            print(f"当前状态: {status}")
            last_ctrl_time = 0  # 重置时间
        else:
            last_ctrl_time = current_time

def submit_action():
    try:
        # 获取输入数据
        coord_str = entry_coords.get().strip()
        click_count_str = entry_count.get().strip()
        hours_str = entry_hours.get().strip()
        minutes_str = entry_minutes.get().strip()
        seconds_str = entry_seconds.get().strip()
        milliseconds_str = entry_milliseconds.get().strip()
        
        # 处理点击次数
        click_count = int(click_count_str) if click_count_str else 0
        
        # 处理时间组件
        hours = int(hours_str) if hours_str else 0
        minutes = int(minutes_str) if minutes_str else 0
        seconds = int(seconds_str) if seconds_str else 0
        milliseconds = int(milliseconds_str) if milliseconds_str else 0
        
        click_interval = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        if click_interval <= 0:
            raise ValueError("点击间隔时间必须大于0秒")
        
        # 解析坐标
        match = re.match(r'\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)', coord_str)
        if not match:
            raise ValueError("坐标格式不正确，应该为 (x, y)")
        x = int(match.group(1))
        y = int(match.group(2))
        
        # 关闭对话框
        root.destroy()
        
        # 计算点击的初始时间
        next_click_time = datetime.now()

        # 执行点击操作
        if click_count == -1:
            count = 0
            print(f"开始无限循环点击，间隔时间为 {click_interval} 秒")
            while True:
                if not paused:
                    click_mouse(x, y)
                    count += 1
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    next_click_time += timedelta(seconds=click_interval)
                    print(f"已点击 {count} 次，当前时间: {current_time}")
                    print(f"下一次点击时间: {next_click_time.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    print("暂停中...")
                
                # 计算下一次点击的实际时间，确保在暂停时不会遗漏
                current_time = datetime.now()
                time_until_next_click = (next_click_time - current_time).total_seconds()
                if time_until_next_click > 0:
                    time.sleep(time_until_next_click)
        else:
            print(f"开始点击，目标位置: ({x}, {y})，点击间隔: {click_interval} 秒，总点击次数: {click_count}")
            for i in range(click_count):
                if not paused:
                    click_mouse(x, y)
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    next_click_time += timedelta(seconds=click_interval)
                    print(f"已点击 {i + 1} 次，剩余 {click_count - i - 1} 次，当前时间: {current_time}")
                    print(f"下一次点击时间: {next_click_time.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    print("暂停中...")
                
                # 计算下一次点击的实际时间
                current_time = datetime.now()
                time_until_next_click = (next_click_time - current_time).total_seconds()
                if time_until_next_click > 0:
                    time.sleep(time_until_next_click)
            print("点击完成")
        
    except ValueError as e:
        messagebox.showerror("输入错误", f"输入格式不正确：{e}\n请确保所有输入都为有效数字，坐标格式为 (x, y)。")

def click_mouse(x, y):
    # 移动到指定位置
    mouse.position = (x, y)
    # 执行点击操作
    mouse.click(Button.left)

# 创建主窗口
root = tk.Tk()
root.title("鼠标点击设置")

# 创建并放置提示标签
tk.Label(root, text="运行后双击 Ctrl 键可退出程序", fg="blue").grid(row=0, column=0, columnspan=2, padx=10, pady=5)

# 创建并放置标签和文本框
tk.Label(root, text="鼠标点击坐标 (格式: (x, y))：").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_coords = tk.Entry(root)
entry_coords.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="点击次数（-1 表示无限循环）：").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_count = tk.Entry(root)
entry_count.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="点击间隔时间 (时 分 秒 毫秒)：").grid(row=3, column=0, padx=10, pady=5, sticky="e")

# 创建小时、分钟、秒和毫秒的文本框并排放置
frame_time = tk.Frame(root)
frame_time.grid(row=3, column=1, padx=10, pady=5, sticky="w")

entry_hours = tk.Entry(frame_time, width=5)
entry_hours.grid(row=0, column=0, padx=2)

entry_minutes = tk.Entry(frame_time, width=5)
entry_minutes.grid(row=0, column=1, padx=2)

entry_seconds = tk.Entry(frame_time, width=5)
entry_seconds.grid(row=0, column=2, padx=2)

# 创建毫秒的文本框，设置为红色背景
entry_milliseconds = tk.Entry(frame_time, width=5, bg='red', fg='white')
entry_milliseconds.grid(row=0, column=3, padx=2)

# 移除红色“毫秒”标签
# tk.Label(frame_time, text="毫秒", fg='red').grid(row=1, column=3, padx=2)

# 创建提交按钮
submit_button = tk.Button(root, text="确定", command=submit_action)
submit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# 启动键盘监听
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# 启动 GUI 事件循环
root.mainloop()
