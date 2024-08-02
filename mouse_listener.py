import tkinter as tk
from tkinter import font as tkfont
from pynput import mouse, keyboard

# 计算新的窗口宽度（原宽度 300 像素增加 15%）
original_width = 300
new_width = int(original_width * 1.15)

# 创建主窗口
root = tk.Tk()
root.title("鼠标坐标显示")
root.geometry(f"{new_width}x120")  # 调整窗口宽度
root.attributes("-topmost", True)  # 窗口始终在最上层

# 设置统一字体样式
font_style = tkfont.Font(family="Microsoft YaHei", size=12)  # 更改为微软雅黑

# 创建标签显示说明文字
instruction_label = tk.Label(root, text="鼠标移动到目标位置后按下 Ctrl 键选定坐标", font=font_style)
instruction_label.pack(pady=5)

# 创建文本框，宽度调整为适合显示坐标
text_box = tk.Entry(root, font=font_style, justify='center', width=20)  # 窄一些的文本框
text_box.pack(pady=(0, 5), padx=10)

# 创建按钮
def copy_to_clipboard():
    root.clipboard_clear()  # 清空剪贴板
    root.clipboard_append(text_box.get())  # 复制文本框中的内容到剪贴板

copy_button = tk.Button(root, text="复制坐标", command=copy_to_clipboard, font=font_style)
copy_button.pack(pady=5)

# 当前坐标和控制状态
last_x = 0
last_y = 0
stop_update = False  # 控制坐标更新的标志

def on_move(x, y):
    global last_x, last_y, stop_update
    if not stop_update:  # 只有当停止更新标志为 False 时才更新坐标
        last_x, last_y = x, y
        text_box.delete(0, tk.END)  # 清空文本框
        text_box.insert(0, f"({x}, {y})")  # 插入新坐标

def on_click(x, y, button, pressed):
    # 鼠标点击事件可以不处理
    pass

def on_press(key):
    global stop_update
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        stop_update = True
        text_box.delete(0, tk.END)  # 清空文本框
        text_box.insert(0, f"({last_x}, {last_y})")  # 显示最终坐标

def on_release(key):
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        # Ctrl 键释放后，仍然不更新坐标
        pass

# 设置鼠标监听器
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
mouse_listener.start()

# 设置键盘监听器
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()

# 启动主事件循环
root.mainloop()
