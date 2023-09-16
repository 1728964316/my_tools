import sys
from time import sleep

import keyboard
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication

import simulation
from untitled import Ui_MainWindow


class check_thread(QThread):
	def __init__(self, parent=None):
		super(check_thread, self).__init__(parent)


	def run(self):
		self.check = simulation.check()
		self.check.start()

	def stop_run(self):
		if self.check.flag !=0:
			self.check.t.paused.clear()

class keyb_thread(QThread):
	change_statue = pyqtSignal(str)
	def __init__(self, parent=None):
		super(keyb_thread, self).__init__(parent)

	def on_press(self, key):
		if(key.name==']'):
			self.change_statue.emit('change')
			# print(key)

	def keyb(self):
		keyboard.on_press(self.on_press)

	def run(self):
		self.keyb()

class dialog_state_thread(QThread):
	dialog_state_signal = pyqtSignal(str)
	def __init__(self, parent=None):
		super(dialog_state_thread,self).__init__(parent)

	def set_init(self,p):
		self.p=p

	def run(self):
		while True:
			# print(self.p.check.flag)
			if self.p.check.flag == 1 or self.p.check.flag == 3:
				self.dialog_state_signal.emit('对话中')
			elif self.p.check.flag == 2 :
				self.dialog_state_signal.emit('')
			sleep(1)

class main(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.init_connect()
		self.check_keyb()


	def init_connect(self):
		self.open_btn.stateChanged.connect(self.state_changed)

	def check_keyb(self):
		self.keyb_t1 = keyb_thread()
		self.keyb_t1.start()
		self.keyb_t1.change_statue.connect(self.change_state)

	def change_state(self,str):
		if (self.open_btn.isChecked()):
			self.open_btn.setChecked(False)
		else:
			self.open_btn.setChecked(True)

	def state_changed(self):
		self.flag = 0
		# print(self.open_btn.isChecked())
		if (self.open_btn.isChecked()):
			print('kaishi')
			self.check_t1 = check_thread()
			self.check_t1.start()
			self.check_t2 = dialog_state_thread()
			self.check_t2.start()
			self.check_t2.set_init(self.check_t1)
			self.check_t2.dialog_state_signal.connect(self.change_dialog_state)
			self.statue.setText("识别中")
		else:
			print('guanbi                       ')
			self.stop_check_thread()
			self.statue.setText("暂停识别")

	def change_dialog_state(self,str):
		self.dialog_statue.setText(str)
	def stop_check_thread(self):
		self.check_t2.terminate()
		self.check_t1.stop_run()
		self.check_t1.terminate()
		self.change_dialog_state('')
		self.statue.setText("识别结束")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = main()
	main.show()
	sys.exit(app.exec())
