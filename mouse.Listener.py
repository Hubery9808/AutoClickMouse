from pynput import mouse

def on_move(x, y):
    # 输出鼠标当前位置
    print(f"当前鼠标坐标: ({x}, {y})")

# 设置鼠标监听器
with mouse.Listener(on_move=on_move) as listener:
    listener.join()
from pynput import mouse

def on_move(x, y):
    # 输出鼠标当前位置
    print(f"当前鼠标坐标: ({x}, {y})")

# 设置鼠标监听器
with mouse.Listener(on_move=on_move) as listener:
    listener.join()
