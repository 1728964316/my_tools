import re  # 导入正则表达式库
import time  # 导入时间处理库

from DrissionPage import ChromiumPage  # 导入Web页面操作的类
from PyQt5.QtCore import QObject, pyqtSignal


class my_main(QObject):
	ratio = pyqtSignal(str)  # 定义ratio信号

	def __init__(self):
		super().__init__()
		self.destination = 999999  # 设定默认的目标时间
		self.class_list = None  # 初始的课程列表
		self.page = None  # 网页对象
		self.total_time = 0  # 已播放的视频总时间

	def start(self):
		# self.ratio=ratio
		# 开始执行的主方法
		self.page = ChromiumPage()  # 创建一个网页对象
		# 打开指定的URL
		self.page.get("https://2023dphub010171.xiaoben365.com/activity/elective/7")
		self.check_login()  # 检查是否已登录
		# self.find_init_class()  # 查找初始课程
		self.click_video()  # 点击并播放视频

	def check_alert(self):
		# 检查是否有弹窗提示并关闭它
		if self.page.ele('xpath://*[@id="comfirmModel"]/div[2]/div', timeout=1).style('position') != 'static':
			self.page.ele('xpath://*[@id="comfirmModel"]/div[2]/div/div[3]/div/button[1]').click()

		btn = self.page.ele('xpath://*[@id="p-A"]', timeout=1)
		if btn:
			btn.click()

	def check_video_status(self):
		# 监控视频的播放状态
		temp = 0
		while True:
			self.check_alert()  # 检查弹窗
			time.sleep(1)
			video = self.page.ele('xpath:/html/body/div[3]/div[1]/div/div[2]/div[1]/div/video')
			currentTime = video.run_js("return arguments[0].currentTime;", video)  # 获取视频的当前播放时间
			self.total_time += currentTime - temp if currentTime >= temp else 0  # 更新已播放的总时间
			temp = currentTime

			ended = (video.run_js("return arguments[0].duration;", video)-currentTime)<1.5
			self.ratio.emit(str(round(self.total_time / self.destination * 100, 1)))  # 发送ratio信号
			# print(self.ratio)
			# print(video.run_js("return arguments[0].currentTime;", video), video.run_js("return arguments["
			#                                                                             "0].duration;", video))
			print("{}:{}/{}:{}".format(int(self.total_time / 60), int(self.total_time % 60),
			                           int(self.destination / 60), int(self.destination % 60)))
			# print(int(self.total_time), '/', self.destination)  # 输出已播放时间和目标时间
			print(str(round(self.total_time / self.destination * 100, 1)) + '%')

			if self.total_time - 60 >= self.destination or ended:
				print(1)
				# self.class_list=self.class_list[1:]
				break  # 如果达到目标时间或视频播放结束，则退出循环
			if video.run_js("return arguments[0].paused;", video) and not ended:
				print("播放")
				video.run_js("arguments[0].play();", video)  # 如果视频暂停，则尝试播放

	def find_video_list(self):
		# 在页面上查找并播放视频列表
		video_list = self.page.eles('xpath://*[@id="navUl"]/li')[2:]  # 获取视频列表
		time.sleep(1)
		for i in video_list:
			print(i.click())
			small_video_list = i.eles('@class:clearfix')  # 获取小视频列表
			for j in small_video_list or [i]:  # 如果有小视频列表则遍历，否则直接使用当前元素
				# print(small_video_list.ele('text:第').text)
				print(j.text)
				j.click()  # 点击视频
				self.check_video_status()  # 检查视频播放状态
				if self.total_time - 60 >= self.destination:
					print(2)
					break  # 如果达到目标播放时间，则退出循环
			time.sleep(1)
			if self.total_time - 60 >= self.destination:
				print(3)
				break  # 如果达到目标播放时间，则退出循环

	def click_video(self):
		self.find_init_class()
		# 查找课程
		if not self.class_list:
			print('查找失败')
			return
		for i in self.class_list:
			# 获取课程的目标时间和总时间
			[destination, total_time] = i.eles('text:分钟')
			self.destination = int(re.findall(r"\d+", destination.text)[0]) * 60
			self.total_time = int(re.findall(r"\d+", total_time.text)[0]) * 60
			print(i.ele('@class=line-ellipsis').text)
			print(i.ele('@class:btn-primary').click())
			# i.ele('@class:btn-primary').click()  # 点击播放视频
			self.page.to_tab(self.page.latest_tab)  # 切换到最新打开的标签页
			self.find_video_list()  # 查找并播放视频列表
			if self.total_time - 60 >= self.destination:
				print("播放完成")  # 播放完成后输出提示信息
				self.page.close_tabs()  # 关闭所有标签页
				print('关闭当前页面')

	# try:
	# 	for i in self.class_list:
	# 		# 获取课程的目标时间和总时间
	# 		[destination, total_time] = i.eles('text:分钟')
	# 		self.destination = int(re.findall(r"\d+", destination.text)[0]) * 60
	# 		self.total_time = int(re.findall(r"\d+", total_time.text)[0]) * 60
	# 		print(i.ele('@class=line-ellipsis').text)
	# 		print(i.ele('@class:btn-primary').click())
	# 		# i.ele('@class:btn-primary').click()  # 点击播放视频
	# 		self.page.to_tab(self.page.latest_tab)  # 切换到最新打开的标签页
	# 		self.find_video_list()  # 查找并播放视频列表
	# 		if self.total_time - 60 >= self.destination:
	# 			print("播放完成")  # 播放完成后输出提示信息
	# 			self.page.close_tabs()  # 关闭所有标签页
	# 			print('关闭当前页面')
	# 			# time.sleep(3)
	# except:
	# 	print(4)
	# 	pass

	def find_init_class(self):
		# 查找课程列表
		try:
			self.page.ele('xpath://*[@id="allPagination"]/span[3]').click()
			time.sleep(1)
			all_class_list = self.page.eles('xpath://*[@id="courseList"]/li')
			print('登录成功')

			for i in range(len(all_class_list)):
				# 查找未完成的课程
				# print(all_class_list[i].ele('@class:reach').attr('class').find('noreach'))
				# print(all_class_list[i].ele('@class:reach').attr('class').find('noreach'))
				if all_class_list[i].ele('@class:reach').attr('class').find('noreach') != -1:
					self.class_list = all_class_list[i:]
					# print(len(self.class_list))
					return
		except:
			print("查询视频列表错误")

	def check_login(self):
		# 检查并尝试登录
		try:
			if self.page.ele('xpath://*[@id="passportWrap"]/div/div[1]', timeout=1):
				# 输入用户名和密码
				self.page.ele('xpath://*[@id="loginName"]').input('18986037976')
				self.page.ele('xpath://*[@id="password"]').input('123456')
				self.page.ele('xpath://*[@id="login"]/div[3]/button').click()  # 点击登录按钮
				print('登录中')
		except:
			print('登录失败')

def a():
	try:
		my_main_1 = my_main()  # 创建my_main类的实例
		my_main_1.start()  # 调用start方法开始执行
	except:
		a()

if __name__ == "__main__":
	# 当脚本作为主程序运行时
	a()
