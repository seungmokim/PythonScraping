# pyautogui 모듈을 가져옵니다.
import pyautogui
# 마우스 이벤트를 후킹하기 위해 win32 모듈을 가져옵니다.
import win32api
# 마우스 좌표값을 게속해서 출력하기 위해 와일문을 만듭니다.

while True:
    # win32 api로 마우스의 상태를 가져옵니다.
    down = win32api.GetKeyState(0x01)
    # 마우스 상태가 다운이면 와일문을 탈출합니다.
    if down == 0:
        break
    # 마우스의 현재 좌표를 출력합니다..
    print(pyautogui.position())
# 마우스를 현재 위치에서 X 방향으로 200, Y 방향으로 200 이동합니다.
# 마지막 인자인 듀레이션 3을 넣으면 좌표로 3초동안 이동합니다.
# pyautogui.move(200, 200, 3)

# position 함수는 마우스의 현재 위치를 반환합니다.
# x, y = pyautogui.position()

# X 100, Y 100 좌표로 이동하기 위해
# 목표 위치에서 현재 위치를 빼줍니다.

# pyautogui.move(100 - x, 100 - y, 3)

# 절대 좌표 100, 100 위치로 마우스를 이동합니다.
# pyautogui.moveTo(100, 100, 3)

# pyautogui.moveTo(2256, 83, 3)
# pyautogui.click()

# 내문서를 마우스 오른쪽 클릭합니다.
# pyautogui.click(x=132, y=84, duration=3, button='right')

# 내문서를 마우스 더블클릭 클릭합니다.
pyautogui.doubleClick(x=132, y=84, duration=3)