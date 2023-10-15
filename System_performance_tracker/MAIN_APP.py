import sys
import os
import speedtest  
import GPUtil
import shutil
import traceback
from PySide2 import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from qt_material import *
import psutil
import PySide2extn
from multiprocessing import cpu_count
import datetime
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from time import sleep

import datetime
import mysql.connector
from mysql.connector import Error

#UI FILE CONVERTED FROM .ui to python file ui.py

from MAINUI import *
platforms = {'linux': 'Linux','linux1':'Linux','linux2':'Linux','darwin':'OS X','win32': 'Windows'}

class WorkerSingnals(QObject):
	finished = Signal()
	error = Signal(tuple)
	result = Signal(object)
	progress = Signal(int)

class Worker(QRunnable):
	def __init__(self,fn,*args,**kwargs):
		super(Worker,self).__init__()


		self.fn=fn
		self.args=args
		self.kwargs=kwargs
		self.signals=WorkerSingnals()

		self.kwargs['progress_callback']=self.signals.progress

	@Slot()
	def run(self):

		try:
			result=self.fn(*self.args,**self.kwargs)
		except:
			traceback.print_exc()
			exctype, value=sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
		else: 
			self.signals.result.emit(result)
		finally:
			self.signals.finished.emit()





class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		apply_stylesheet(app, theme='dark_blue.xml')
		win=self.ui.centralwidget
		self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

		'''self.setWindowFlags(QtCore.Qt.FramelessWindowHint)'''
		#self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		#self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
		
		
		
		
		self.shadow = QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(50)
		self.shadow.setXOffset(3)
		self.shadow.setYOffset(3)
		self.shadow.setColor(QtGui.QColor(0,92,157,550))

		win.setGraphicsEffect(self.shadow)

		self.setWindowIcon(QtGui.QIcon(":/black/icons/black/airplay.svg"))

		self.setWindowTitle("HEATSINK")
		QSizeGrip(self.ui.size_grip)      
		#minimize window
		self.ui.Minimize_window_button.clicked.connect(lambda:self.showMinimized())

		#close window
		self.ui.Close_window_button.clicked.connect(lambda:self.close())

		#restore/maximize window
		self.ui.Restore_window_button.clicked.connect(lambda: self.resize_win())
		
		#Navigation#################################
		self.ui.CPU_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.cpu_and_bat))
		self.ui.RAM_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.memory))
		self.ui.Disk_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.rom))
		self.ui.Wifi_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.network))
		self.ui.GPU_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.gpu))
		self.ui.System_info.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.system_info))
		self.ui.act_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.activity))
		self.ui.sensor_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.sensor))
		self.ui.battery_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.battery))
		self.ui.all_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.all))

		#move bar
		def moveWindow(e):
			if self.isMaximized()==False:
				if e.buttons() == Qt.LeftButton:
					self.move(self.pos() + e.globalPos() - self.clickPosition)
					self.clickPosition=e.globalPos()
					e.accept()

		self.ui.Header_frame.mouseMoveEvent = moveWindow		

		self.ui.menu.clicked.connect(lambda: self.slideLeftMenu())	

		###############styled menu
		for w in self.ui.menu_frame.findChildren(QPushButton):
			w.clicked.connect(self.applyButtonStyle)
		
		


		############################################
		self.threadpool= QThreadPool()
		#########################################################################
		########################FUNCTION CALLS###################################
		self.show()
		#self.cpu_ram( )
		self.system_info()
		#self.battery()
		self.activity()
		self.storage() 
		self.sensor()
		self.ui.refresh_btn.clicked.connect(self.ping)
		self.psutil_thread()
		"""while(1):
			print('jarus')
			sleep(1)"""
		###########################Hushhhhhhhh######################################
		#########################################################################

	##############################thread function###################33
	def psutil_thread(self):
		worker=Worker(self.cpu_ram)

		worker.signals.result.connect(self.print_output)
		worker.signals.finished.connect(self.thread_complete)
		worker.signals.progress.connect(self.progress_fn)

		self.threadpool.start(worker)

		battery_worker=Worker(self.battery)

		battery_worker.signals.result.connect(self.print_output)
		battery_worker.signals.finished.connect(self.thread_complete)
		battery_worker.signals.progress.connect(self.progress_fn)

		self.threadpool.start(battery_worker)

		gpu_worker=Worker(self.gpu)

		gpu_worker.signals.result.connect(self.print_output)
		gpu_worker.signals.finished.connect(self.thread_complete)
		gpu_worker.signals.progress.connect(self.progress_fn)

		self.threadpool.start(gpu_worker)
		
		net_worker=Worker(self.network)

		net_worker.signals.result.connect(self.print_output)
		net_worker.signals.finished.connect(self.thread_complete)
		net_worker.signals.progress.connect(self.progress_fn)

		self.threadpool.start(net_worker)



	def print_output(self,s):
		print(s)
	def thread_complete(self):
		print('Thread COMPLETE')
	def progress_fn(self,n):
		print("%d%% done" % n)







	###############################Function DEfinition#################

	def applyButtonStyle(self):
		for w in self.ui.menu_frame.findChildren(QPushButton):
			if w.objectName() != self.sender().objectName():
				w.setStyleSheet("border-bottom:2px solid black;")

		self.sender().setStyleSheet("border-bottom: 6px solid black;border-left:6px solid black;")
		

	def system_info(self):
		time = datetime.datetime.now().strftime("I:%M:%S %p")
		self.ui.system_date.setText(str(time))
		date = datetime.datetime.now().strftime("%Y-%m-%D")
		self.ui.system_time.setText(str(date))

		self.ui.system_machine.setText(platform.machine())
		self.ui.system_version.setText(platform.version())
		self.ui.system_platform.setText(platform.platform())
		self.ui.system_system.setText(platform.system())
		self.ui.system_processor.setText(platform.processor())


	#left slide
	def slideLeftMenu(self):


		# Get current left menu width
		width = self.ui.Left_menu_cont_frame.width()
		# If minimized
		if width== 110:
		# Expand menu
			newWidth= 300
		# If maximized
		else:
		# Restore menu
			newWidth = 110
		# Animate the transition
		self.animation = QPropertyAnimation (self.ui.Left_menu_cont_frame, b"minimumWidth") #Animate minimumwidht
		self.animation.setDuration(250)
		self.animation.setStartValue(width) #Start value is the current menu width
		self.animation.setEndValue(newWidth) #end value is the new menu width
		self.animation.setEasingCurve (QtCore.QEasingCurve.InOutQuart)
		self.animation.start()


	##mouse events##########################################
	def mousePressEvent(self,event):
		self.clickPosition=event.globalPos()
	#minimized
	def resize_win(self):
		if self.isMaximized():
			self.showNormal()
			self.ui.Restore_window_button.setIcon(QtGui.QIcon(u":/black/icons/black/maximize-2.svg"))
		else:
			self.showMaximized()
			self.ui.Restore_window_button.setIcon(QtGui.QIcon(u":/black/icons/black/minimize.svg"))


	







	#cpu and ram info################################################
	def cpu_ram(self, progress_callback):
		
		while True:
			self.max_cpu=0;
			self.max_ram=0;
			totalRam = 1.0
			totalRam = psutil.virtual_memory()[0] * totalRam
			totalRam = totalRam / (1024 * 1024 * 1024)

			availRam = 1.0
			availRam = psutil.virtual_memory()[1] * availRam
			availRam = availRam / (1024 * 1024 * 1024)
			
			self.ramUsed = 1.0
			self.ramUsed = psutil.virtual_memory()[3] * self.ramUsed
			self.ramUsed = self.ramUsed / (1024 * 1024 * 1024)

			ramFree = 1.0
			ramFree = psutil.virtual_memory()[4] * ramFree
			ramFree = ramFree / (1024 * 1024 * 1024)  
			
			ramUsages = str(psutil.virtual_memory()[2]) + '%'
			core = cpu_count()
			self.cpuPer = psutil.cpu_percent()
			




			cpuMainCore = psutil.cpu_count(logical = False)
			self.ui.total_ram.setText(str("{:.4f}".format(totalRam)+ ' GB'))
			self.ui.available_ram.setText(str("{:.4f}".format(availRam)+' GB'))
			self.ui.used_ram.setText(str("{:.4F}".format(self.ramUsed) + ' GB'))
			self.ui.free_ram.setText(str("{:.4f}".format(ramFree)+'GB'))
			self.ui.ram_usage.setText(str("{:.4f}".format(totalRam) + 'GB'))
			self.ui.cpu_count.setText(str(core))
			self.ui.cpu_per.setText(str(self.cpuPer)+" %")
			self.ui.cpu_main_core.setText(str(cpuMainCore))
			################################all
			self.ui.label_44.setText('Total Ram: '+str("{:.4f}".format(totalRam)+ ' GB'))
			self.ui.label_47.setText('Free Ram: '+str("{:.4f}".format(availRam)+' GB'))
			self.ui.label_48.setText('Used Ram: '+str("{:.4F}".format(self.ramUsed) + ' GB'))
			self.ui.label_56.setText("Ram Usage: "+str("{:.4f}".format(totalRam) + 'GB'))
	
			self.ui.label_23.setText('Threads: '+str(core))
			self.ui.label_22.setText('Cpu Usage: '+str(self.cpuPer)+" %")
			self.ui.label_16.setText('Cores: '+str(cpuMainCore))


			
			
			self.ui.cpu_percentage.rpb_setMaximum(100)
			self.ui.cpu_percentage.rpb_setValue(self.cpuPer)
			self.ui.cpu_percentage.rpb_setBarStyle('Hybrid2')
			self.ui.cpu_percentage.rpb_setLineColor((255,30,99))
			self.ui.cpu_percentage.rpb_setPieColor((45,74,83))
			self.ui.cpu_percentage.rpb_setTextColor((255,255,255))
			self.ui.cpu_percentage.rpb_setInitialPos('West')
			self.ui.cpu_percentage.rpb_setTextFormat('Percentage')
			self.ui.cpu_percentage.rpb_setTextFont('Arial')
			self.ui.cpu_percentage.rpb_setLineWidth(15)
			self.ui.cpu_percentage.rpb_setPathWidth(15)
			self.ui.cpu_percentage.rpb_setLineCap('RoundCap')
			######################all#####################
			self.ui.widget.rpb_setMaximum(100)
			self.ui.widget.rpb_setValue(self.cpuPer)
			self.ui.widget.rpb_setBarStyle('Hybrid2')
			self.ui.widget.rpb_setLineColor((255,30,99))
			self.ui.widget.rpb_setPieColor((45,74,83))
			self.ui.widget.rpb_setTextColor((255,255,255))
			self.ui.widget.rpb_setInitialPos('West')
			self.ui.widget.rpb_setTextFormat('Percentage')
			self.ui.widget.rpb_setTextFont('Arial')
			self.ui.widget.rpb_setLineWidth(15)
			self.ui.widget.rpb_setPathWidth(15)
			self.ui.widget.rpb_setLineCap('RoundCap')

			#setting min val
			self.ui.ram_percentage.spb_setMinimum((0 , 0, 0))
			#setting max value
			self.ui.ram_percentage.spb_setMaximum((totalRam, totalRam, totalRam))
			#setting progress val
			self.ui.ram_percentage.spb_setValue((availRam, self.ramUsed, ramFree))
			#set progress color
			self.ui.ram_percentage.spb_lineColor(((6,201,38),(233,6,100),(68, 138, 255)))

			self.ui.ram_percentage.spb_setInitialPos(('West','West','West'))
			self.ui.ram_percentage.spb_lineWidth(15)
			self.ui.ram_percentage.spb_setGap(15)
			self.ui.ram_percentage.spb_lineStyle(('SolidLine','SolidLine','SolidLine'))
			self.ui.ram_percentage.spb_lineCap(('RoundCap','RoundCap','RoundCap'))
			######################all#####################
			self.ui.widget_3.spb_setMinimum((0 , 0, 0))
			#setting max value
			self.ui.widget_3.spb_setMaximum((totalRam, totalRam, totalRam))
			#setting progress val
			self.ui.widget_3.spb_setValue((availRam, self.ramUsed, ramFree))
			#set progress color
			self.ui.widget_3.spb_lineColor(((6,201,38),(233,6,100),(68, 138, 255)))

			self.ui.widget_3.spb_setInitialPos(('West','West','West'))
			self.ui.widget_3.spb_lineWidth(15)
			self.ui.widget_3.spb_setGap(15)
			self.ui.widget_3.spb_lineStyle(('SolidLine','SolidLine','SolidLine'))
			self.ui.widget_3.spb_lineCap(('RoundCap','RoundCap','RoundCap'))

			

			sleep(1)
		


		#hide the path
		self.ui.ram_percentage.spb_setPathHidden(True)
		#######################################################
	
	
	
	
	#a function to convert seconds to hours#######################################
	def secs2hours(self,secs):
		mm, ss = divmod(secs, 60)
		hh, mm = divmod(mm, 60)
		return "%02d:%02d:%02d  (Hours:Mins:Secs)" % (hh, mm, ss)

	#battery info###############################33
	def battery(self, progress_callback):
		while True:
			batt=psutil.sensors_battery()
			
			if not hasattr(psutil, "sensors_battery"):
				self.ui.battery_status.setText("Platform not supported")
			
			if batt is None:
				self.ui.battery_status.setText("No battery installed")

			if batt.power_plugged:
				self.ui.battery_charge.setText(str(round(batt.percent,2))+"%")
				self.ui.label_63.setText("Percentage: "+str(round(batt.percent,2))+"%")
				self.ui.battery_time_left.setText("N/A")
				self.ui.label_64.setText("Time: "+"N/A")
				if batt.percent < 100:
					self.ui.battery_status.setText("Charging")
				else:
					self.ui.battery_status.setText("Fully Charged")
				self.ui.battery_plugged.setText("Yes")
				self.ui.label_58.setText("Plugged: "+"Yes")
			
			else:
				self.ui.battery_charge.setText(str(round(batt.percent,2))+"%")
				self.ui.label_63.setText("Percentage: "+str(round(batt.percent,2))+"%")
				self.ui.battery_time_left.setText(self.secs2hours(batt.secsleft))
				self.ui.label_64.setText("Time: "+self.secs2hours(batt.secsleft))
				if batt.percent < 100:
					self.ui.battery_status.setText("Discharging")
				else:
					self.ui.battery_status.setText("Fully Charged")
				self.ui.battery_plugged.setText("No")
				self.ui.label_58.setText("Plugged: "+"No")
			
		#battery power indicator
			self.ui.battery_usage.rpb_setMaximum(100)
			self.ui.battery_usage.rpb_setValue(batt.percent)
			self.ui.battery_usage.rpb_setBarStyle('Hybrid2')
			self.ui.battery_usage.rpb_setLineColor((255, 30, 99))
			self.ui.battery_usage.rpb_setPieColor((45, 74, 83))
			self.ui.battery_usage.rpb_setTextColor((255, 255, 255))
			self.ui.battery_usage.rpb_setInitialPos('West')
			self.ui.battery_usage.rpb_setTextFormat('Percentage')
			self.ui.battery_usage.rpb_setLineWidth(15) 
			self.ui.battery_usage.rpb_setPathWidth(15)
			self.ui.battery_usage.rpb_setLineCap('RoundCap')
			###############################allllllllll
			self.ui.widget_4.rpb_setMaximum(100)
			self.ui.widget_4.rpb_setValue(batt.percent)
			self.ui.widget_4.rpb_setBarStyle('Hybrid2')
			self.ui.widget_4.rpb_setLineColor((255, 30, 99))
			self.ui.widget_4.rpb_setPieColor((45, 74, 83))
			self.ui.widget_4.rpb_setTextColor((255, 255, 255))
			self.ui.widget_4.rpb_setInitialPos('West')
			self.ui.widget_4.rpb_setTextFormat('Percentage')
			self.ui.widget_4.rpb_setLineWidth(15) 
			self.ui.widget_4.rpb_setPathWidth(15)
			self.ui.widget_4.rpb_setLineCap('RoundCap')
			sleep(1)
	#########################################################################################

	############################activity#####################################################
	def create_table_widget(self,rowPosition,columnPosition,text,tableName):
		qtablewidgetitem=QTableWidgetItem()
		getattr(self.ui,tableName).setItem(rowPosition,columnPosition,qtablewidgetitem)
		qtablewidgetitem = getattr(self.ui,tableName).item(rowPosition,columnPosition)
		qtablewidgetitem.setText(text);

	def activity(self): 
		for x in psutil.pids():
			rowPosition=self.ui.act_table.rowCount()
			self.ui.act_table.insertRow(rowPosition)
			try:
				process = psutil.Process(x)

				self.create_table_widget(rowPosition,0,str(process.pid),"act_table")
				self.create_table_widget(rowPosition, 1, str(process.name()), "act_table")
				self.create_table_widget(rowPosition, 2, str(process.status()), "act_table")
				self.create_table_widget(rowPosition, 3, str(datetime.datetime.utcfromtimestamp(process.create_time()).strftime("%Y-%m-%d %H:%M:%S")), "act_table")


				suspend_btn=QPushButton(self.ui.act_table)
				suspend_btn.setText('Suspend')
				suspend_btn.setStyleSheet("color : brown")
				self.ui.act_table.setCellWidget(rowPosition,4,suspend_btn)

				resume_btn = QPushButton(self.ui.act_table)
				resume_btn.setText('Resume')
				resume_btn.setStyleSheet("color:green")
				self.ui.act_table.setCellWidget(rowPosition,6,resume_btn)

				terminate_btn = QPushButton(self.ui.act_table)
				terminate_btn.setText('Terminate')
				terminate_btn.setStyleSheet("color:orange")
				self.ui.act_table.setCellWidget(rowPosition, 5, terminate_btn)

				kill_btn = QPushButton(self.ui.act_table)
				kill_btn.setText('Kill')
				kill_btn.setStyleSheet("color:red")
				self.ui.act_table.setCellWidget(rowPosition, 7, kill_btn)
			except Exception as e:
				print(e)

		self.ui.activity_search.textChanged.connect(self.findName)

	def findName(self):
		name=self.ui.activity_search.text().lower()
		for row in range(self.ui.act_table.rowCount()):
			item=self.ui.act_table.item(row,1)
			self.ui.act_table.setRowHidden(row,name not in item.text().lower())
	#########################################################################################
	
    ##########################################################################################
    
	
	#############################################storage##############################################
	def storage(self):
		global platforms
		storage_device=psutil.disk_partitions(all=False)
		for x in storage_device:
			rowPosition=self.ui.store_table.rowCount()
			self.ui.store_table.insertRow(rowPosition)
			self.create_table_widget(rowPosition,0,x.device,"store_table")
			self.create_table_widget(rowPosition, 1, x.mountpoint, "store_table")
			self.create_table_widget(rowPosition, 2, x.fstype, "store_table")
			self.create_table_widget(rowPosition, 3, x.opts, "store_table")

			if sys.platform == 'linux' or sys.platform == 'linux1' or sys.platform=='linux2':
				self.create_table_widget(rowPosition, 3,str(x.maxfile), "store_table")
				self.create_table_widget(rowPosition, 4, str(x.maxpath), "store_table")
			else:
				self.create_table_widget(rowPosition,3,"Function not available on "+ platforms[sys.platform],"store_table")
				self.create_table_widget(rowPosition, 4, "Function not available on " + platforms[sys.platform],"store_table")
			disk_usage = shutil.disk_usage(x.mountpoint)
			self.create_table_widget(rowPosition,5,str((disk_usage.total/(1024*1024*1024)))+"GB","store_table")
			self.create_table_widget(rowPosition, 6, str((disk_usage.used / (1024 * 1024 * 1024))) + "GB", "store_table")
			self.create_table_widget(rowPosition, 7, str((disk_usage.free/ (1024 * 1024 * 1024))) + "GB", "store_table")

			full_disk = (disk_usage.used/disk_usage.total)*100
			progressBar = QProgressBar(self.ui.store_table)
			progressBar.setObjectName(u"progressBar")
			progressBar.setValue(full_disk)
			self.ui.store_table.setCellWidget(rowPosition,8,progressBar)

    ##########################################################################################
    
    ##########################################################################################
    #sensors
	def sensor(self):
		if sys.platform == 'linux' or sys.platform == 'linux1' or sys.platform=='linux2':
			for x in psutil.sensors_temperatures():
				for y in psutil.sensors_temperatures()[x]:
					rowPosition = self.ui.sensor_table.rowCount()
					self.ui.sensor_table.insertRow(rowPosition)
					self.create_table_widget(rowPosition,0,x,"sensor_table")
					self.create_table_widget(rowPosition, 1, y.label, "sensor_table")
					self.create_table_widget(rowPosition, 2, str(y.current), "sensor_table")
					self.create_table_widget(rowPosition, 3, str(y.high), "sensor_table")
					self.create_table_widget(rowPosition, 4, str(y.critical), "sensor_table")

					temp_per=(y.current/y.high)*100
					progressBar = QProgressBar(self.ui.sensor_table)
					progressBar.setObjectName(u"progressBar")
					progressBar.setValue(temp_per)
					self.ui.sensor_table.setCellWidget(rowPosition,5,progressBar)
		else:
			global platforms
			rowPosition=self.ui.sensor_table.rowCount()
			self.ui.sensor_table.insertRow(rowPosition)

			self.create_table_widget(rowPosition,0,"Function not supported on"+platforms[sys.platform],"sensor_table")
			self.create_table_widget(rowPosition, 1, "N/A" + platforms[sys.platform], "sensor_table")
			self.create_table_widget(rowPosition, 2, "N/A" + platforms[sys.platform], "sensor_table")
			self.create_table_widget(rowPosition, 3, "N/A" + platforms[sys.platform], "sensor_table")
			self.create_table_widget(rowPosition, 4, "N/A" + platforms[sys.platform], "sensor_table")
			self.create_table_widget(rowPosition, 5, "N/A" + platforms[sys.platform], "sensor_table")
	##########################################################################################
	def ping(self):
		speed_test = speedtest.Speedtest(secure=True)
		servernames =[]  

		speed_test.get_servers(servernames)  
		self.ui.ping.setText(str(speed_test.results.ping))
		print(speed_test.results.ping)
    ##########################################################################################
    #network
	def network(self ,progress_callback ):
		# speed_test = speedtest.Speedtest(secure=True)

		
		# self.max_net=0;
		# def bytes_to_mb(bytes):
		# 	KB = 1024  # One Kilobyte is 1024 bytes
		# 	MB = KB * 1024  # One MB is 1024 KB
		# 	return int(bytes / MB)

		# download_speed=bytes_to_mb(speed_test.download())
		# self.ui.downloadspeed.setText(str(download_speed)+"mbps")

		# upload_speed = bytes_to_mb(speed_test.upload())
		# self.ui.upspeed.setText(str(upload_speed)+"mbps")

		# self.total_speed = download_speed+upload_speed
		# self.ui.totalspeed.setText(str(self.total_speed)+"mbps")


		# servernames =[]  

		# speed_test.get_servers(servernames)  
		# self.ui.ping.setText(str(speed_test.results.ping))
		# print(speed_test.results.ping)
		last_recieved = psutil.net_io_counters().bytes_recv
		last_sent = psutil.net_io_counters().bytes_sent
		last_total = last_sent+last_recieved

		while True:
			bytes_recieved = psutil.net_io_counters().bytes_recv
			bytes_sent = psutil.net_io_counters().bytes_sent
			bytes_total = bytes_sent+bytes_recieved

			new_recieved = bytes_recieved-last_recieved
			new_sent = bytes_sent-last_sent
			new_total = bytes_total-last_total

			mb_new_recieved = new_recieved/(1024)
			mb_new_sent = new_sent/(1024)
			mb_new_total = new_total/(1024)

			#print(f"{mb_new_recieved:.2f} KB recieved,{mb_new_sent:.2f} KB sent,{mb_new_total:.2f} KB total", end='\r')
			self.ui.upspeed.setText(str(f'{mb_new_sent:.2f}')+"kbps")
			self.ui.label_34.setText("Upload: "+str(f'{mb_new_sent:.2f}')+"kbps")
			self.ui.downloadspeed.setText(str(f'{mb_new_recieved:.2f}')+"kbps")
			self.ui.label_35.setText("Download: "+str(f'{mb_new_recieved:.2f}')+"kbps")
			self.ui.totalspeed.setText(str(f'{mb_new_total:.2f}')+"kbps")
			self.ui.label_36.setText("Total: "+str(f'{mb_new_total:.2f}')+"kbps")
			last_recieved = bytes_recieved
			last_sent = bytes_sent
			last_total = bytes_total

			sleep(1)


			

			

    ##########################################################################################refresh_btn
	##########################################################################################
    ##########################################################################################
    #GPU
	def gpu(self,progress_callback):
		
		while True:
			gpus = GPUtil.getGPUs()
			for x in gpus:
				load=x.load*100
				self.ui.loadd.setText(str(load)+"Mb")

				free_memory=x.memoryFree
				self.ui.freememory.setText(str(free_memory)+"Mb")
				self.ui.label_25.setText("Free: "+str(free_memory)+"Mb")

				total_memory = x.memoryTotal
				self.ui.totalmemory.setText(str(total_memory)+"Mb")
				self.ui.label_24.setText("Total: "+str(total_memory)+"Mb")

				used_memory = x.memoryUsed
				self.ui.usedmemory.setText(str(used_memory)+"Mb")
				self.ui.label_26.setText("Used: "+str(used_memory)+"Mb")

				temp = x.temperature
				self.ui.temperature.setText(str(temp)+"celsius")
			self.gpuper=(used_memory/total_memory)*100
			

			self.ui.gpu_per.rpb_setMaximum(100)
			self.ui.gpu_per.rpb_setValue(self.gpuper)
			self.ui.gpu_per.rpb_setBarStyle('Hybrid2')
			self.ui.gpu_per.rpb_setLineColor((255,30,99))
			self.ui.gpu_per.rpb_setPieColor((45,74,83))
			self.ui.gpu_per.rpb_setTextColor((255,255,255))
			self.ui.gpu_per.rpb_setInitialPos('West')
			self.ui.gpu_per.rpb_setTextFormat('Percentage')
			self.ui.gpu_per.rpb_setTextFont('Arial')
			self.ui.gpu_per.rpb_setLineWidth(15)
			self.ui.gpu_per.rpb_setPathWidth(15)
			self.ui.gpu_per.rpb_setLineCap('RoundCap')
			##############alllllllllllllllll

			self.ui.widget_2.rpb_setMaximum(100)
			self.ui.widget_2.rpb_setValue(self.gpuper)
			self.ui.widget_2.rpb_setBarStyle('Hybrid2')
			self.ui.widget_2.rpb_setLineColor((255,30,99))
			self.ui.widget_2.rpb_setPieColor((45,74,83))
			self.ui.widget_2.rpb_setTextColor((255,255,255))
			self.ui.widget_2.rpb_setInitialPos('West')
			self.ui.widget_2.rpb_setTextFormat('Percentage')
			self.ui.widget_2.rpb_setTextFont('Arial')
			self.ui.widget_2.rpb_setLineWidth(15)
			self.ui.widget_2.rpb_setPathWidth(15)
			self.ui.widget_2.rpb_setLineCap('RoundCap')
			


			sleep(1)

	
	




    ##########################################################################################
	def create_connection(self,host_name,user_name,user_password,db):
		connection=None
		try:
			connection=mysql.connector.connect(
				host=host_name,
				user=user_name,
				passwd=user_password,
				database=db
			)
			print("connection successful")
			
		except Error as err:
			print(f"Error:'{err}'")

		return connection
    
	def sys_usage(self):
		self.conn=self.create_connection('localhost','root','ts432002','se')
		times = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		use="""insert into sys_usage values(%s,%s,%s,%s,%s)"""
		
		data=(self.max_cpu,self.max_gpu,self.max_ram,self.max,times)
		cur = self.conn.cursor()
		cur.execute(use,data)
		
    ##########################################################################################


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())