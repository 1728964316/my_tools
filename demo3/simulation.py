import cv2
import numpy as np
import pyautogui
import threading
import time
from pynput.keyboard import Controller, Key

# 图像检测模块
class Check():
	def __init__(self):
		self.flag = 0  # 标志位，用于跟踪对话框的状态
		self.flag_list = [0, 0, 0]  # 标志列表，用于跟踪对话框的不同状态
		self.t = clicked_task()  # 创建按键模拟线程的实例

	def start(self):
		# 开始对话框检测循环
		self.check_dialog()

	def check_dialog(self):
		# 检测屏幕上的对话框并相应地改变状态
		while True:
			if self.locate_on_screen('img/img1.png') or self.locate_on_screen('img/img3.png'):
				# 检测到特定图像时改变标志位
				if self.flag == 0:
					self.check_auto()
					self.flag = 1
				if self.flag == 2:
					self.check_auto()
					self.flag = 3

				self.check_option()
			elif self.flag > 0:
				self.flag = 2

			# 根据标志位的状态启动或暂停按键模拟线程
			if self.flag == 1 and self.flag_list[0] == 0:
				self.flag_list[0] = 1
				print('开始')
				self.t.start()
			elif self.flag == 2 and self.flag_list[1] == 0:
				self.flag_list[1] = 1
				self.flag_list[2] = 0
				print('暂停')
				self.t.paused.clear()
			elif self.flag == 3 and self.flag_list[2] == 0:
				self.flag_list[2] = 1
				self.flag_list[1] = 0
				print('恢复')
				self.t.paused.set()
			time.sleep(0.5)

	def locate_on_screen(self, image_path, threshold=0.8):
		# 在屏幕上查找给定图像，返回找到图像的位置
		try:
			screen = np.array(pyautogui.screenshot())
			screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
			template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
			res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
			loc = np.where(res >= threshold)
			return any(zip(*loc[::-1]))
		except Exception as e:
			print(f"发生异常：{e}")
			return False

	def check_auto(self):
		# 自动检查屏幕上特定像素的颜色并执行点击动作
		try:
			btm1 = pyautogui.pixel(1700, 60)
			pyautogui.sleep(0.75)
			btm2 = pyautogui.pixel(1700, 60)
			print(btm1, btm2)
			if btm1 == btm2:
				pyautogui.moveTo(1700, 62, duration=0.01)
				pyautogui.click()
		except Exception as e:
			print(f"自动检查过程中发生异常：{e}")

	def check_option(self):
		try:
			# 截取屏幕指定区域的图像
			screen = np.array(pyautogui.screenshot(region=(1320, 655, 500, 400)))
			screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
			template = cv2.imread('img/img2.png', cv2.IMREAD_GRAYSCALE)
			res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
			threshold = 0.8
			loc = np.where(res >= threshold)

			# 检查是否找到了匹配项
			if np.any(res >= threshold):
				# 获取第一个匹配位置的坐标
				y, x = loc[0][0], loc[1][0]
				# 将坐标转换为相对于整个屏幕的位置，并执行点击操作
				pyautogui.moveTo(x + 1320 + template.shape[1] // 2, y + 655 + template.shape[0] // 2, duration=0.01)
				pyautogui.click()
		except Exception as e:
			print(f"检测对话框选项时发生异常：{e}")


# 按键模拟线程类
class clicked_task(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.paused = threading.Event()  # 线程暂停的事件
		self.paused.set()  # 设置事件的初始状态为“已设置”
		self.control = Controller()  # 创建键盘控制器实例

	def run(self):
		# 线程执行的主体函数，模拟按键操作
		while True:
			self.control.press(Key.space)  # 模拟按下空格键
			self.control.release(Key.space)  # 模拟释放空格键
			time.sleep(0.05)  # 暂停0.05秒
			self.paused.wait()  # 如果事件状态为“已清除”，线程将暂停
