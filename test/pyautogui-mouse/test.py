import pyautogui

def move_mouse(x, y):
    pyautogui.moveTo(x, y, duration=1)
    print(f"Mouse moved to ({x}, {y})")

def click_mouse(button='left'):
    pyautogui.click(button=button)
    print(f"{button} click")

def scroll_mouse(amount):
    pyautogui.scroll(amount)
    print(f"Scrolled {amount} units")

while True:
    command = input("Entre com o comando (move x y / click [left/right] / scroll amount / exit / kill): ")
    if command.startswith("move"):
        _, x, y = command.split()
        move_mouse(int(x), int(y))
    elif command.startswith("click"):
        parts = command.split()
        button = parts[1] if len(parts) > 1 else 'left'
        click_mouse(button)
    elif command.startswith("scroll"):
        _, amount = command.split()
        scroll_mouse(int(amount))
    elif command == "exit":
        break
    elif command == "kill":
        move_mouse(1350, 670)
        button = 'left'
        click_mouse(button)
    else:
        print("Invalid command")
try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')