import sys
from PyQt5.QtWidgets import (
	QApplication, QMainWindow, QPushButton, QAction, QLabel, QCheckBox,
	QProgressBar, QMessageBox, QComboBox, QDial, QHBoxLayout,
	QVBoxLayout, QTabWidget, QWidget, QDialog, QDialogButtonBox,QStyleFactory,
	QGridLayout, QLineEdit, QActionGroup, QStatusBar,QToolBar)
# technically could've used the functions as they are inherited by QMainWindow instead of using QStatusBar and QToolBar directly
from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import (Qt, QObject, QSettings)


class wrapper(object):
	def __init__ (self, func, *args):
		self.func = func
		self.args = args

	def call (self): return self.func(*self.args)
# self.func(*self.args)

extendedBools=[0,1,"t","T","f","F","true","True","false","False"]
statusTips={
    "fusion":"Set window style to Fusion",
    "windows":"Set window style to Windows",
    "vista":"Set window style to Windows Vista",
    "XP":"Set window style to Windows XP"
    }
validStyles=["Windows", "Windowsxp", "Windowsvista", "Fusion"]
defaultWindowGeometry=b'\x01\xd9\xd0\xcb\x00\x02\x00\x00\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x00\x00\x00\x00\x00\x00\x07\x80'

class window(QMainWindow):
	def __init__ (self):
		super(window, self).__init__()
		print("Starting to do things")
		self.setObjectName("Mother Window")# print("I am the "+ self.objectName())
		self.setAttribute(Qt.WA_QuitOnClose, True)#Ensures that closing the main window also closes the preferences window

					#Configs
		self.settings = QSettings("D:\Projects\Python\SwitchBoard\MySwitchboard.cfg", QSettings.IniFormat)
		self.settings.setPath(
				QSettings.IniFormat, QSettings.UserScope,"D:\Projects\Python\SwitchBoard\MySwitchboard.cfg"
		)
		# self.settingsPath = QSettings("D:\Projects\Python\SwitchBoard\MySwitchboard.cfg", QSettings.NativeFormat)
		# self.settings.setPath(QSettings.IniFormat,QSettings.UserScope,"D:\Projects\Python\SwitchBoard\MySwitchboard.cfg")
		self.initSettings()
		# DEBUG: LIST ALL CONFIG KEYS
		# print("Listing all config keys:" + str(self.settings.allKeys())); print("Config file is" + self.settings.fileName())

		# setup window aspects
		self.setWindowTitle(self.settings.value("cfgWindowTitle"))
		#self.defaultTitle = str(self.windowTitle())
		self.setWindowIcon(QIcon('logo.png'))#TODO: Edit the image to make the white background transparent
		self.setStatusBar(QStatusBar(self))
		self.declareActions()

		self.topMenu()
		self.mainToolBar = QObject

		self.preferencesDialog = QDialog()

		self.setupToolBars()
		#NOTE: for QMainWindow, do a find for things with menu, status, tab, tool

		# TODO:
		#   Mutually exclusive checkboxes/toggle buttons for battery settings
		#   Histograph of motherboard, CPU, HDD, and SSD temperatures.
		#   Display indicating current CPU clock speed. maybe only update every 5-10 seconds?
		#   Display indicating CPU usage % and #of processes
		#   Display indicating current RAM usage. probably in the form of a vertical bar AND a text label.
		# ?   Quick launch button for Discord+Hexchat?
		#   Display of (local/computer) date and time. local weather if arrangeable
		# ?   Display of current network I/O ?
		#   keep on top capability
		#DONE		retain previous settings
		# ?   allow adjusting colors of histograph/chart/progress bar attributes through a (menu accessed popup or tab?) application preferences (menu?)
		#   universal color picker function. WITH A PIPETTE TOOL
		#   application close confirmation popup (disableable in preferences)
		#   Button to clear system clipboard
		# ?  snipping tool quick launch button?
		#   make status bar at bottom of page have clearly defined edges
		#   Create a list of QActions to have initialized in some kind of loop?
		#   give main toolbar its own context menu with a CHECKABLE option to lock/unlock the toolbar
		#DONE		sync settings TO config before close?
		pop=self.basicButton('test', self.popup, None, 25, 100)

		box = self.basicCheckBox(self.editTitle)

		self.bar = self.progressBar(325, 75, 160, 28)
		self.doProgress = self.basicButton('Increment Progress', self.progress, "", 200, 75)

		Dial=self.dial(1, 100, 300)

		self.pageBar = QTabWidget(self)  # TabWidget is a QWidget
		self.tab1 = QWidget()  # ;self.tab1.adjustSize()
		self.tab2 = QWidget()  # ;self.tab2.adjustSize()


		tab2Layout= QVBoxLayout()
		tab2Layout.addStretch(1)
		tab2Layout.addWidget(pop)
		tab2Layout.addWidget(box)
		tab2Layout.addWidget(Dial)

		progressBox = QHBoxLayout()
		progressBox.addStretch(1)
		progressBox.addWidget(self.doProgress)
		progressBox.addWidget(self.bar)

		self.tab1.setLayout(tab2Layout)
		self.tab2.setLayout(progressBox)#previously took progressBox as param


		self.pageBar.addTab(self.tab1, "tab1")
		self.pageBar.addTab(self.tab2, "tab2")
		# self.mainToolBar

		# tesT=QVBoxLayout()
		# tesT.addWidget(self.mainToolBar)
		# tesT.addWidget(self.pageBar)
		# self.setLayout(tesT)
		self.mainToolBar.addWidget(self.pageBar)
		# self.mainToolBar.addAction(self.actCopy)
		# self.mainToolBar.setLayout=QHBoxLayout(self)

		# make the pageBar occupy everything below the toolbar.
		# anything else being displayed must be part of a tab,
		# otherwise it will end up being rendered behind the pageBar
		# self.setCentralWidget()

		tempPref=self.basicButton('Options', self.appPreferences, None, 300, 300)

		self.restoreGeometry(self.settings.value("mainWindowGeometry"))
		print("done init")
	#Declare application wide Actions
	# noinspection PyUnresolvedReferences
	def declareActions (self):  # WIP
		# cut
		self.actCut = QAction("Cut", self)
		self.actCut.setShortcut("Ctrl+x")

		def Link (): wrapper(testPrint, "Cut").call()

		self.actCut.triggered.connect(Link)
		# copy
		self.actCopy = QAction("Copy", self)
		self.actCopy.setShortcut("Ctrl+c")

		def Link (): wrapper(testPrint, "Copy").call()

		self.actCopy.triggered.connect(Link)
		# paste
		self.actPaste = QAction("Paste", self)
		self.actPaste.setShortcut("Ctrl+v")

		def Link (): wrapper(testPrint, "Paste").call()

		self.actPaste.triggered.connect(Link)

		# quit
		self.actQuit = QAction("Quit", self)
		self.actQuit.setShortcut("Ctrl+q")
		# self.actQuit.triggered.connect(endProgram)
		self.actQuit.triggered.connect(self.closeEvent)

	#Simple button with default parameters for position, label, and tooltip(none)
	# noinspection PyUnresolvedReferences
	def basicButton (self, text = 'test', func = None, tip = None, X = 200, Y = 200):
		btn = QPushButton(text, self)
		btn.adjustSize()
		btn.move(X, Y)
		btn.setToolTip(tip)

		if isinstance(func, wrapper):
			def link ():    func.call()
			# print("Calling wrapped function according to button press")
			btn.triggered.connect(link)
		# might need to be clicked instead of triggered
		elif func is not None:  btn.clicked.connect(func)
		else:   print("no function");   pass
		return btn

	#Tri-state checkbox     WIP
	def triCheckBox (self, func = None, text = 'test', X = 25, Y = 75):
		self.basicCheckBox(func, text, X, Y, True)

	#Simple checkbox with default parameters for position and label, and handling for tri-state boxes
	# noinspection PyUnresolvedReferences
	def basicCheckBox (self, func = None, text = 'test', X = 25, Y = 75, isTri = False):
		checkBox = QCheckBox(text, self)
		checkBox.adjustSize()
		checkBox.move(X, Y)
		if isTri == True:   checkBox.setTristate(True)
		if func is not None:    checkBox.stateChanged.connect(func)
		return checkBox

	# Round dial/knob        WIP
	def dial (self, func = None, X = 200, Y = 200, radius = 50, wrap = False):
		knob = QDial(self)
		knob.move(X, Y)
		knob.resize(radius, radius)
		knob.setWrapping(wrap)

		if func is not None:
			func
		# TODO:something something show number in a box nearby

		return knob
	# "Template" function for a toolbar button with an icon
	def toolBar_Icon (self, icon, func, tooltip, statustip = "Null"):
		item = QAction(QIcon(icon), tooltip, self)
		if statustip != "Null": item.setStatusTip(statustip)
		# noinspection PyUnresolvedReferences
		if func is not None:item.triggered.connect(func)
		else: print("One or more icon type items on your toolbar has no function")
		return item

	# "Template" function for a text-only toolbar button
	def toolBar_Text (self, text, func):
		item = QAction(text, self)
		# noinspection PyUnresolvedReferences
		if func is not None:item.triggered.connect(func)
		else: print("One or more text type items on your toolbar has no function")
		return item

	# Add toolbars and populate them with buttons
	def setupToolBars (self):
		# Make buttons
		iconB = self.toolBar_Icon(
				"logo.png", testPrint, "icon", "Do something"
		)
		textB = self.toolBar_Text("&Textual Button", testPrint)

		# Make toolbars
		self.mainToolBar = QToolBar("Main Toolbar")

		# Add toolbars to window. CRITICAL STEP
		mainToolBarPosition=int(self.settings.value("MainToolbar/mainToolBarPosition"))
		print("Main toolbar pos: " + str(mainToolBarPosition))
		self.addToolBar(mainToolBarPosition, self.mainToolBar)

		# Add buttons to toolbars
		self.mainToolBar.addAction(iconB)
		self.mainToolBar.addAction(textB)

	# "Template" function for a simple menu item
	def menuItem (self, func, name, tip = None, shortcut = "Null", isToggle=False, group=None):
		item = QAction(name, self)  # self reminder: item is now a QAction
		item.setStatusTip(tip)
		if shortcut != "Null": item.setShortcut(shortcut) # ;else: print("no shortcut for menu item \""+name+"\"")
		if isToggle !=False: item.setCheckable(True)
		if group is not None: group.addAction(item)

		if isinstance(func, wrapper):
			def link ():	func.call()
			# noinspection PyUnresolvedReferences
			item.triggered.connect(link)
		elif func is not None:
			#print(func.__name__ + " is not a wrapper. It is a " + type(func).__name__)
			# noinspection PyUnresolvedReferences
			item.triggered.connect(func)
		else: print("Menu item \"" + name + "\" has no function")
		return item

	# Add menus and populate them with actions
	def topMenu (self):
		# self.statusBar()
		mainMenu = self.menuBar()

		# Make menu items
		prefs = self.menuItem(
				# wrapper(testPrint, "Preferences menu item selected")
				# , "Preferences")
				self.appPreferences, "Preferences")
		prefs.setMenuRole(QAction.PreferencesRole)

		styleGroup=QActionGroup(mainMenu)
		windows = wrapper(self.themeControl, "Windows")
		winVista = wrapper(self.themeControl, "Windowsvista")
		winXP = wrapper(self.themeControl, "Windowsxp")
		fusion = wrapper(self.themeControl, "Fusion")
		style1 = self.menuItem(fusion, "Fusion", statusTips["fusion"], isToggle=True, group=styleGroup)
		style2 = self.menuItem(windows, "Windows", statusTips["windows"], isToggle=True, group=styleGroup)
		style3 = self.menuItem(winVista, "Windows Vista", statusTips["vista"], isToggle=True, group=styleGroup);style3.setText(style3.text() + " (Default)")
		style4 = self.menuItem(winXP, "Windows XP", statusTips["XP"], isToggle=True, group=styleGroup)



		# TODO: Reset layout of window to default?
		#resetPlacement = self.menuItem(None, "Reset Window Layout", "Reset the window layout to default")

		# Make menus
		fileMenu = mainMenu.addMenu("File")
		editMenu = mainMenu.addMenu("Edit")
		viewMenu = mainMenu.addMenu("View")
		styleMenu = viewMenu.addMenu("Styles")

		layoutMenu = viewMenu.addMenu("Layout")
		layoutMenu.addAction(self.menuItem(testPrint, None))  # TODO:give meaningful functions later
		# Add actions to menus
		fileMenu.addAction(self.actQuit)  # TODO:add a status tip to this, "Close the application"
		fileMenu.addAction(prefs)  # TODO:add a status tip to this, "View and edit application settings"

		editMenu.addAction(self.actCopy)
		editMenu.addAction(self.actCut)
		editMenu.addAction(self.actPaste)

		styleMenu.addAction(style1)
		styleMenu.addAction(style2)
		styleMenu.addAction(style3)
		styleMenu.addAction(style4)
		# print(style1.trigger())
		#if style2.trigger():print("FFF")
		#viewMenu.addAction(resetPlacement)
	def themeControl (self, text):
		print("Setting style to " + text)
		QApplication.setStyle(QStyleFactory.create(text))
		self.settings.setValue("primaryStyle",text)

	# Progress bar           WIP
	def progressBar (self, X = 25, Y = 75, length = 100, height = 30):
		bar = QProgressBar(self)
		bar.setGeometry(X, Y, length, height)

		return bar

	# A box you can enter text in        WIP/TODO
	def textBox (self, text = None, X = 200, Y = 200, length = 100, height = 30):pass
	# Writes text directly onto the window       WIP/TODO
	def displayText (self, text = None):    pass
	# Creates a tab for page switching       WIP/TODO
	def pageTab (self):
		# every tab will be a widget, and the widget is assigned a name
		# and added to the tab bar somewhere else
		pass

#Section####################################### Start Settings Handling ###############################################
	def appPreferences (self):
		config=self.settings
		settingsPage=self.preferencesDialog
		settingsPage.setWindowTitle("Settings")

		# Refresh field values
		def getCurrentValues():
			for setting in settingsList:
				if setting.isModified():  # TODO:Handle different types, consider handling special cases
					print(setting.cfgName + " has been changed. Refreshing field value.")
					if type(setting) == QLineEdit:
						setting.setText(config.value(setting.cfgName))
					elif type(setting) == QCheckBox:
						pass
					elif type(setting) == QPushButton:
						pass
					else:
						print("Setting \"" + setting.cfgName + "\" matches no handled type. Its type is " + str(type(setting)))

		# Update config file contents to match field values
		def updateModifiedValues():
			for setting in settingsList:
				if setting.isModified():	#TODO:Handle different types, consider handling special cases
					print(setting.cfgName + " has been modified. Now saving.")
					if type(setting)==QLineEdit:	config.setValue(setting.cfgName, setting.text())
					elif type(setting)==QCheckBox: pass
					elif type(setting)==QPushButton: pass
					else:	print("Setting \""+setting.cfgName + "\" matches no handled type. Its type is "+ str(type(setting)))

		# settingsPage.update()
		# self.showEvent, update
		parentLayout=QVBoxLayout()

		# something to get the saved preferences
		responses = QDialogButtonBox(QDialogButtonBox.NoButton, Qt.Horizontal)
		responses.apply=responses.addButton("Accept Changes", QDialogButtonBox.AcceptRole)
		responses.good=responses.addButton("Okay", QDialogButtonBox.ActionRole)
		responses.discard=responses.addButton("Discard Changes", QDialogButtonBox.RejectRole)

		# Give these actual functions
		def accResp():
			wrapper(testPrint, "Accepting Changes...").call()
			# Check for and save any changed settings
			updateModifiedValues()
			# print(winTitle.text()); #text, textChanged, textEdited, setValidator, setText. setTooltip. QLineEdit,displayText
			#settingsPage.accept()
			config.sync()

		def rejResp ():
			wrapper(testPrint, "Discarding Changes...").call()
			getCurrentValues()
			settingsPage.reject()

		def good():
			# settingsPage.setResult(QDialog.accepted())
			# settingsPage.done(QDialog.accepted())
			settingsPage.accept()
			getCurrentValues()
			print("Leaving Settings")
		#responses.accepted.connect(good)
		#responses.accepted.connect(accResp)
		#responses.rejected.connect(rejResp)

		#Using this to allow an OK and an Accept button with separate resulting operations
		def onClicked ():
			sender = self.sender()
			if sender.text()== "Accept Changes" :
				accResp()
			elif sender.text()=="Discard Changes":
				rejResp()
			elif sender.text()=="Okay":
				good()
		responses.apply.clicked.connect(onClicked)
		responses.discard.clicked.connect(onClicked)
		responses.good.clicked.connect(onClicked)

		# add content to this
		#TODO: probably need to use a byte array to store current settings on opening preferences window. that would be used to restore discarded changes
		#TODO: apply doesnt just need to sync, it needs to update too
		winTitle=QLineEdit(config.value("cfgWindowTitle"))
		winTitle.cfgName="cfgWindowTitle"#CRITICAL FOR AUTOMATIC SETTING SAVE
		labelWinTitle=QLabel("Window Title:")
		labelWinTitle.setBuddy(winTitle)

		settingsList=[winTitle]#DONT FORGET TO ADD TO THIS

		horiz1=QHBoxLayout()
		horiz1.addWidget(labelWinTitle)
		horiz1.addWidget(winTitle)

		parentLayout.addLayout(horiz1)

		parentLayout.addWidget(responses)
		# parentLayout.insertStretch(0)
		settingsPage.setLayout(parentLayout)
		settingsPage.show();
		#responses.receivers(PYQT_SIGNAL = accResp)
		#responses.clicked(responses.apply)
		# responses.isSignalConnected(responses.clicked(responses.apply))
		# if responses.clicked(QAbstractButton = apply):print("YES")
		# settingsPage.closeEvent()
	# QDialog.customEvent(),event,eventFilter, installEventFilter, leaveEvent,mask, showEvent, signalsBlocked
	# responses.finished.connect(something to save?)???     sender      senderSignalIndex       result? signals?
	##something that saves preferences when the OK button is pressed
	def initSettings(self):
		# NOTE:Is toolbar moveable or locked in place. Is it floatable. Maybe if i figure out how to let the user adjust contents,
		# NOTE: add an option to disable that ability? Enable/disable certain widgets?
		# TODO: Figure out how to add descriptive text into the config file, if at all possible

		config= self.settings	# test=config.setValue("test", 3);    print("test=" + str(config.value("test")))

		#Style Configs
		cfgStyle=config.value("primaryStyle")
		if str(config.value("primaryStyle")).capitalize().replace(" ","") not in validStyles:
			config.setValue("primaryStyle", "Windows Vista")
			print("Resetting style to hard default")
		self.themeControl(str(config.value("primaryStyle")).replace(" ",""))#Sets the window style to the configured value

		#Main Toolbar Configs
		config.beginGroup("MainToolbar")
		cfgMainToolBarPos=config.value("mainToolBarPosition")
		if cfgMainToolBarPos == "\n" or cfgMainToolBarPos not in ["1","2","4","8"]:
			config.setValue("mainToolBarPosition", Qt.LeftToolBarArea)#Default toolbar position is on the left side

		# Currently Non Functional
		cfgMainToolBarMoveable=config.value("isMainToolBarMovable")
		# if cfgMainToolBarMoveable == "\n" or type(cfgMainToolBarMoveable)!=bool:
		if cfgMainToolBarMoveable not in extendedBools:
				config.setValue("isMainToolBarMovable",True)#Main toolbar is movable by default
		elif cfgMainToolBarMoveable in [1,"t","T", "true", "True"]:config.setValue("isMainToolBarMovable",True)
		elif cfgMainToolBarMoveable in [0,"f","F", "false","False"]:config.setValue("isMainToolBarMovable",False)
		# Currently Non Functional
		cfgMainToolBarFloatable=config.value("isMainToolBarFloatable")
		if cfgMainToolBarFloatable not in extendedBools:
			config.setValue("isMainToolBarFloatable",True)#Main toolbar is floatable by default
		elif cfgMainToolBarFloatable in [1,"t","T", "true", "True"]:config.setValue("isMainToolBarFloatable",True)
		elif cfgMainToolBarFloatable in [0,"f","F", "false","False"]:config.setValue("isMainToolBarFloatable",False)
		config.endGroup()

		#Other Configs
		cfgTitle=config.value("cfgWindowTitle")
		if cfgTitle == "\n":     config.setValue("cfgWindowTitle", "I am a window")

			#Makes sure that default window geometry value is available in case there isn't one in the config
		cfgWindowGeometry= config.value("mainWindowGeometry")
		if type(cfgWindowGeometry) is None or cfgWindowGeometry=="\n" or cfgWindowGeometry=="":
			config.setValue("mainWindowGeometry", defaultWindowGeometry)
			print("Defaulting geometry")
		# if cfgWindowGeometry=='\n':print("IS BLANK")
		else:
			# print("Geo: "+str((type(cfgWindowGeometry)))); print(cfgWindowGeometry)
			pass
	pass#Little fix for a pet peeve of mine in PyCharm, where comments on the ends of functions are sometimes folded with the function
# Section####################################### End Settings Handling ###############################################

	# Basic,does nothing much, pop-up window prompt; probably wont make a template
	def popup (self):
		choice = QMessageBox(self)
		choice.setText("What do you do?")  # move to center of popup
		Boring = choice.addButton(
				"Don't push Arnold",
				QMessageBox.AcceptRole)
		Arnold = choice.addButton(
				"Push Arnold (you know you want to....)",
				QMessageBox.ActionRole)
		Exit = choice.addButton(QMessageBox.Cancel)
		Exit.hide()

		choice.setEscapeButton(Exit)
		choice.setDefaultButton(Arnold)
		choice.exec()

		if choice.clickedButton() is Arnold:    print("*Heavy Austrian accent* OUCH!")
		elif choice.clickedButton() is Boring:  print("Well you're no fun")		# ...yeah, I had gotten frustrated at that time, and decided to be a bit silly
	def editTitle (self, state):
		if state == Qt.Unchecked:   self.setWindowTitle("Temporary Title")
		else:   self.setWindowTitle(self.settings.value("cfgWindowTitle"))
	# there has to be a way to specify which progress bar this is for, but for the life of me I can't think of how.
	# Cross that bridge if/when I come to it
	def progress (self):
		if self.bar.value() < 100:
			self.bar.setValue(self.bar.value() + 1)
			if self.bar.value() == 100: 	print("Progress: Done")
			elif self.bar.value() % 10 == 0:    print("Progress: " + str(self.bar.value()))
		else: pass

	def closeEvent(self, *args, **kwargs):
		self.settings.setValue("mainWindowGeometry", self.saveGeometry())
		# print("Saving Geometry")
		# print(self.settings.value("mainWindowGeometry"))
		# print(self.saveGeometry())
		self.close()
#Section############################### Start Test Functions #######################################
	def clickButton (self, text = 'test', func = None, tip = None, X = 200, Y = 200):
		btn = QPushButton(text, self)
		btn.adjustSize()
		btn.move(X, Y)
		btn.setToolTip(tip)

		if isinstance(func, wrapper):
			def link ():func.call()
			btn.clicked.connect(link)
		else:print("no function");pass
		return btn
#Section############################### End Test Functions #######################################

def endProgram ():    print("Goodbye");  sys.exit()
def testPrint (text = "Debug"): print(text)

def run ():
	app = QApplication(sys.argv)
	app.setApplicationName("My Switchboard")
	#app.setApplicationDisplayName("My Switchboard")
	display = window()
	display.show()
	sys.exit(app.exec_())

run()