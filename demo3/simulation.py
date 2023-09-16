import threading
import time

import pydirectinput
from pynput import keyboard, mouse
import pyautogui
from pynput.keyboard import Controller, Key

pyautogui.PAUSE = 0.15


class clicked_task(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.paused = threading.Event()
		self.paused.set()  # 初始化时直接设置事件
		self.control = keyboard.Controller()
		self.ctr = mouse.Controller()

	def run(self):
		keyboard = Controller()
		# num=0
		while True:
			# num+=1
			# if num%25==0:
			# 	print(num)
			# 	self.ctr.click(mouse.Button.left)
			# 	num=1
			# 按下空格
			keyboard.press(Key.space)
			keyboard.release(Key.space)
			# pyautogui.click()
			time.sleep(0.05)
			# print(1)
			# pyautogui.press('space')
			# self.control.press('space')
			# pydirectinput.press('space')
			# pyautogui.keyDown('space')  # 按下a不释放
			# pyautogui.keyUp('space')  # 释放a

			self.paused.wait()  # 等待事件,暂停线程


class check():

	def start(self):
		self.check_dialog()

	# 检测到对话
	def check_dialog(self):
		self.flag = 0
		flag_list = [0, 0, 0]

		while True:
			# print(pyautogui.locateOnScreen('img/test.png', confidence=0.6, grayscale=True))
			if pyautogui.locateOnScreen('img/img1.png', confidence=0.8, grayscale=True) or \
					pyautogui.locateOnScreen('img/img3.png', confidence=0.8, grayscale=True):
				if self.flag == 0:
					self.check_auto()
					self.flag = 1
				if self.flag == 2:
					self.check_auto()
					self.flag = 3

				# pydirectinput.press('space')
				self.check_option()
			elif self.flag > 0:
				self.flag = 2

			if self.flag == 1 and flag_list[0] == 0:

				flag_list[0] = 1
				print('kaishi')
				self.t = clicked_task()
				self.t.start()
			if self.flag == 2 and flag_list[1] == 0:
				flag_list[1] = 1
				flag_list[2] = 0
				# 暂停线程
				print('zanting')
				self.t.paused.clear()
			if self.flag == 3 and flag_list[2] == 0:
				flag_list[2] = 1
				flag_list[1] = 0
				print('huifu')
				# 恢复线程
				self.t.paused.set()

	def check_auto(self):
		# print(pyautogui.pixelMatchesColor(1700, 60, (136, 139, 147), tolerance=10))
		# print(pyautogui.pixel(1657, 60))  # 获取指定位置的色值
		# btm = pyautogui.locateOnScreen('img/img5.png', confidence=0.8)
		# print(pyautogui.pixelMatchesColor(1657, 60, (140,140,144), tolerance=10))
		btm1 = pyautogui.pixel(1700, 60)
		pyautogui.sleep(0.75)
		btm2=pyautogui.pixel(1700, 60)
		print(btm1,btm2)
		if btm1==btm2:
			# color = pyautogui.pixel(1700, 60)  # 获取指定位置的色值
			# print(pyautogui.pixelMatchesColor(1700, 60, (136, 139, 147), tolerance=10))
			# print(pyautogui.center(btm))
			# btm = pyautogui.locateOnScreen('img/img4.png', confidence=0.6)
			# pyautogui.moveTo(pyautogui.center(btm), duration=0.01)
			pyautogui.moveTo(1700,62, duration=0.01)
			pyautogui.click()

	# 检测对话框
	def check_option(self):
		btm2_list = list(
			pyautogui.locateAllOnScreen('img/img2.png', confidence=0.8, grayscale=True, region=(1320, 655, 500, 400)))
		if len(btm2_list) > 0:
			# print(btm2_list[0])
			# print(pyautogui.center(btm2_list[0]))
			pyautogui.moveTo(pyautogui.center(btm2_list[0]), duration=0.01)
			pyautogui.click()
