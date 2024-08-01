import time
from pynput.mouse import Button, Controller

# 初始化鼠标控制器
mouse = Controller()

# 设定点击的坐标 (x, y)
x, y = 27, 1055

# 点击间隔时间（秒）
click_interval = 1

# 点击次数（设置为 -1 表示无限循环）
click_count = 10  # 你可以将其设置为你需要的次数，或者使用 -1 进行无限循环

def click_mouse(x, y):
    # 移动到指定位置
    mouse.position = (x, y)
    # 执行点击操作
    mouse.click(Button.left)

if click_count == -1:
    count = 0
    print(f"开始无限循环点击，间隔时间为 {click_interval} 秒")
    while True:
        click_mouse(x, y)
        count += 1
        print(f"已点击 {count} 次")
        time.sleep(click_interval)
else:
    print(f"开始点击，目标位置: ({x}, {y})，点击间隔: {click_interval} 秒，总点击次数: {click_count}")
    for i in range(click_count):
        click_mouse(x, y)
        print(f"已点击 {i + 1} 次，剩余 {click_count - i - 1} 次")
        time.sleep(click_interval)
    print("点击完成")
