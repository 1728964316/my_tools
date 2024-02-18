import pyautogui
import time


# 设置pyautogui的每个操作之间的延迟
# pyautogui.PAUSE = 0.3

class StarsAuto:
	def __init__(self):
		self.active = True  # 初始状态设为非激活

	def start(self):
		while True:
			try:
				if self.active:
					if pyautogui.locateOnScreen('img/img1.png', confidence=0.8):
						a = pyautogui.locateCenterOnScreen('img/img5.png', confidence=0.8)
						if a:
							pyautogui.click(a)
						a = pyautogui.locateCenterOnScreen('img/img2.png', confidence=0.8)
						if a:
							pyautogui.click(a)
						pyautogui.keyDown('space')
						time.sleep(0.05)
						pyautogui.keyUp('space')
						screenWidth, screenHeight = pyautogui.size()  # 获取屏幕的宽度和高度
						pyautogui.moveTo(screenWidth / 2, 0)
			except Exception as e:
				print(f"start: {e}")
				break  # 退出循环


if __name__ == '__main__':
	starsAuto = StarsAuto()
	starsAuto.start()
