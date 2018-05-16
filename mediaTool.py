#! /usr/bin/python

from Tkinter import *
import MySQLdb
from PIL import Image
import os
import vlc
import csv
import subprocess



class updateEntry:
	
	def __init__(self, master, table, uid):
		dataentry = Tk()
		
		frame = Frame(dataentry)
		frame.pack()
		
		self.getData(uid, table)
		
		data = []
		
		for row in entryData:
			for i in row:
				i = str(i)
				data.append(i)
		if table[0] == 'UID':
			table.pop(0)
		
		lenTable = len(table)
		
		rowNum = 0
		colNum = 0
		
		for i in table:
			self.label = Label(frame, text='%s'%i)
			self.label.grid(row = rowNum, column = colNum)
			rowNum = rowNum + 1
			
		colNum = 1	
		rowNum = 0
		global ent
		ent = []
		
		for row in entryData:
			for i in row:
				lenrow = len(row)
				if lenrow == 6:
					if i == row[0]:
						continue
					elif i == row[5]:
						continue
					else:
						entry = (Entry(frame))
						entry.insert(0, '%s'%i)
						entry.grid(row = rowNum, column = colNum)
						ent.append(entry)
						rowNum = rowNum + 1
				else:
					if i == row[0]:
						continue
					elif i == row[4]:
						continue
					else:
						entry = (Entry(frame))
						entry.insert(0, '%s'%i)
						entry.grid(row = rowNum, column = colNum)
						ent.append(entry)
						rowNum = rowNum + 1

					
		
			
		self.printButton = Button(frame, text='Update Entry', command = lambda: self.updateEntries(uid, table, ent, dataentry))
		self.printButton.grid(row = 5, column = 0)
		
		self.quitButton = Button(frame, text='Quit', command=dataentry.destroy)
		self.quitButton.grid(row = 5, column= 1)
		
					
	def updateEntries(self, uid, table, entries, window):
		
		if table == music:
			title = entries[0].get()
			artist = entries[1].get()
			album = entries[2].get()
			genre = entries[3].get()
			cursor.execute("UPDATE music SET TITLE= '%s', ARTIST= '%s', ALBUM= '%s', GENRE= '%s' WHERE UID='%s'" % (title, artist, album, genre, uid))
		elif table == pictures:
			title = entries[0].get()
			artist = entries[1].get()
			medium = entries[2].get()
			cursor.execute("UPDATE pictures SET TITLE= '%s', ARTIST= '%s', MEDIUM= '%s' WHERE UID='%s'" % (title, artist, medium, uid))
		elif table == movies:
			title = entries[0].get()
			director = entries[1].get()
			releaseyear = entries[2].get()
			genre = entries[3].get()
			cursor.execute("UPDATE movies SET TITLE= '%s', DIRECTOR= '%s', RELEASEYEAR= '%s', GENRE= '%s' WHERE UID='%s'" % (title, director, releaseyear, genre, uid))
		else:
			title = entries[0].get()
			developer = entries[1].get()
			genre = entries[2].get()
			cursor.execute("UPDATE games SET TITLE= '%s', DEVELOPER= '%s', GENRE= '%s', WHERE UID='%s'" % (title, developer, genre, uid))

			
		db.commit()
		window.destroy()	
		
	def getData(self, uid, table):
		if table == pictures:
			cursor.execute('SELECT UID, TITLE, ARTIST, MEDIUM, PATH FROM pictures WHERE UID= %s'%uid)
		elif table == movies:
			cursor.execute('SELECT UID, TITLE, DIRECTOR, RELEASEYEAR, GENRE, PATH FROM movies WHERE UID= %s'%uid)
		elif table == music:
			cursor.execute('SELECT UID, TITLE, ARTIST, ALBUM, GENRE, PATH FROM music WHERE UID= %s'%uid)
		else:
			cursor.execute('SELECT UID, TITLE, DEVELOPER, GENRE, PATH FROM games WHERE UID= %s'%uid)
			
		global entryData
		entryData = cursor.fetchall()	
	

		
class displayEntries:
	
	def __init__(self, master, table):
		master.destroy()
		frame = Frame(root)
		frame.pack()
	
		cursor = db.cursor()
	
		if table == pictures:
			cursor.execute('SELECT UID, TITLE, ARTIST, MEDIUM, PATH FROM pictures')
		elif table == movies:
			cursor.execute('SELECT UID, TITLE, DIRECTOR, RELEASEYEAR, GENRE, PATH FROM movies')
		elif table == music:
			cursor.execute('SELECT UID, TITLE, ARTIST, ALBUM, GENRE, PATH FROM music')
		else:
			cursor.execute('SELECT UID, TITLE, DEVELOPER, GENRE, PATH FROM games')


		data = cursor.fetchall()
		
		global var
		var = StringVar()
		itemNum = 0
		rowNum = 0
		colNum = 0

		for i in table:
			if i == table[0]:
				self.headerRow = Label(frame, text='%s'%table[itemNum], borderwidth = 2, height = '2')
				self.headerRow.grid(row = rowNum, column = colNum)
				itemNum = itemNum + 1
				colNum = colNum + 1
			else:
				self.headerRow = Label(frame, text='%s'%table[itemNum], borderwidth = 2, height = '2', width = '17')
				self.headerRow.grid(row = rowNum, column = colNum)
				itemNum = itemNum + 1
				colNum = colNum + 1	

		itemNum = 0
		rowNum = 1
		colNum = 0


		for row in data:
			row = row[:-1]
			for i in row:
				if i == row[0]:
					self.dataRows = Label(frame, text ='%s'%i, padx= 35, pady= 5, relief = 'sunken', width= 2)
					self.dataRows.grid(row = rowNum, column = colNum)
					colNum = colNum + 1
				else:
					self.dataRows = Label(frame, text ='%s'%i, padx= 35, pady= 5, relief = 'sunken', width= 25)
					self.dataRows.grid(row = rowNum, column = colNum)
					colNum = colNum + 1				
					testCol = colNum
						
						
						
			self.uidCheck = Radiobutton(frame, variable = var, value='%s'%row[0], command = lambda: self.selectedRB(table))
			self.uidCheck.grid(row = rowNum, column = colNum)
			
			rowNum = rowNum + 1
			colNum = 0	
		
		
		
		global dropstate
		dropstate = ''

		self.lookup = Button(frame, text='Look Up Selection', command= lambda: self.openDataEntry(radioSelect, table, entryData))
		self.lookup.grid(row = rowNum, column = 3, sticky = E)
		
		self.refresh = Button(frame, text='Refresh', command= lambda: self.closeRefresh(table, frame))
		self.refresh.grid(row = rowNum, column = 3, sticky = W)
		
		self.backToTables = Button(frame, text='Back', command = lambda: self.goBack(frame))
		self.backToTables.grid(row = rowNum, column = 0, sticky = W)
		
#		self.filter = Button(frame, text= 'Search', width = 10, command = lambda: self.testPrint(table, dropstate))
#		self.filter.grid(row = rowNum, column = 2, sticky = E)
		
#		self.srch = Entry(frame)
#		self.srch.grid(row = rowNum, column = 2, sticky = W)
		
#		self.choose = Label(frame, text = 'Choose Sort Value:      ')
#		self.choose.grid(row = rowNum, column = 1)
#		self.drop = OptionMenu(frame, var, *table, command = self.value)
#		self.drop.grid(row = rowNum, column = 1, sticky = E)
		
		

		
		
	def openDataEntry(self, uid, table, entryData):
		display = Tk()
		
		top = Label(display, text = '')
		top.grid(row = 0, column = 0, columnspan = 6)
		top2 = Label(display, text = '')
		top2.grid(row = 1, column = 0, columnspan = 6)
		
		
		rowNum = 2
		colNum = 0
		
		if table[0] == 'UID':
			table.pop(0)
		
		
		for i in table:
			i = str(i)
			label = Label(display, text='%s'%i, width = 15, height = 2)
			label.grid(row = rowNum, column = colNum)
			rowNum = rowNum + 1
		
		rowNum = 2
		colNum = 1	

		self.getData(uid, table)
		
		for row in entryData:	
			for i in row:
				lenrow = len(row)
				if lenrow == 6:
					if i == row[0]:
						continue
					elif i == row[5]:
						continue
					else:
						i = str(i)
						label = Label(display, text = '%s'%i, width = 40, height = 2, relief = 'sunken')
						label.grid(row = rowNum, column = colNum)			  
						rowNum = rowNum + 1		  
				else:
					if i == row[0]:
						continue
					elif i == row[4]:
						continue
					else:
						label = Label(display, text = '%s'%i, width = 40, height = 2, relief = 'sunken')
						label.grid(row = rowNum, column = colNum)			  
						rowNum = rowNum + 1		

			
		rowNum = 0
		
		for i in range(0, 4):
			styleLabel = Label(display, text = '', width = 5)
			styleLabel.grid(row = rowNum, column  = 3)
			rowNum = rowNum + 1
	
		bottom = Label(display, text = '')
		bottom.grid(row = 6, column = 0, columnspan = 6)
	
		nextButton = Button(display, text= 'Next', width = 7, command = lambda: self.openNextEntry(uid, table, display))
		nextButton.grid(row = 0, column = 4, sticky= E)
		prevButton = Button(display, text= 'Prev', width = 7, command = lambda: self.openPrevEntry(uid, table, display))
		prevButton.grid(row = 0, column = 0, sticky = W)
		editButton = Button(display, text= 'Edit', width = 7, command = lambda: updateEntry(root, table, uid))
		editButton.grid(row = 7, column = 1, sticky = W)
		openButton = Button(display, text= 'Open', width = 7, command = lambda: self.openFile(uid, table))
		openButton.grid(row = 7, column = 1, sticky = E)
		refreshButton = Button(display, text= 'Refresh', width = 7, command = lambda: self.refreshEntry(uid, table, display))
		refreshButton.grid(row = 7, column = 1)
		closeRefresh = Button(display, text = 'Close', width = 7, command = lambda: self.testClose(display))
		closeRefresh.grid(row = 7, column = 4)
	
	
	
	def value(self, value):
		global dropstate
		dropstate = value
		dropstate = str(dropstate)
		dropstate = dropstate.upper()
			
		
		
	
	def testPrint(self, table, drop):
		test = self.srch.get()
		self.getOne(table, drop, test) 
		for row in oneData:
			uID = row[0]
			self.openDataEntry(uID, table, entryData)
		

	
	def goBack(self, master):
		master.destroy()
		frame1 = Frame(root)
		frame1.pack()
		
		test = welcomeWindow(frame1)
		test.tableSelect(frame1)	
		
	def testClose(self, master):
		master.destroy()
		
	def getData(self, uid, table):
		print uid
		
		if table == pictures:
			cursor.execute('SELECT UID, TITLE, ARTIST, MEDIUM, PATH FROM pictures WHERE UID= %s'%uid)
		elif table == movies:
			cursor.execute('SELECT UID, TITLE, DIRECTOR, RELEASEYEAR, GENRE, PATH FROM movies WHERE UID= %s'%uid)
		elif table == music:
			cursor.execute('SELECT UID, TITLE, ARTIST, ALBUM, GENRE, PATH FROM music WHERE UID= %s'%uid)
		else:
			cursor.execute('SELECT UID, TITLE, DEVELOPER, GENRE, PATH FROM games WHERE UID= %s'%uid)
			
		global entryData
		entryData = cursor.fetchall()	
		
	def getOne(self, table, drop, search):
		tabs = []
		if table[3] == 'Medium':
			tab = 'pictures'
		elif table[3] == 'Release Year':
			tab = 'movies'
		elif table[3] == 'Album':
			tab = 'music'
		else:
			tab = 'games'
		comb = [tab, drop, search]
		for i in comb:
			i.replace("","'")
		
		
		cursor.execute('SELECT * FROM %s WHERE %s= %s' % (tab, drop, search))
		
		global oneData
		oneData = cursor.fetchall
		
	def selectedRB(self, table):
		test = '%s'%var.get()
		global radioSelect
		radioSelect = test
		self.getData(test, table)	
		
	def refreshEntry(self, uid, table, master):
		self.getData(uid, table)
		self.openDataEntry(uid, table, entryData)
		master.destroy()
		
	def openNextEntry(self, uid, table, master):
		nuid = int(uid) + 1
		self.getData(nuid, table)	
		ntable = table
		self.openDataEntry(nuid, ntable, entryData)
		master.destroy()		
			
	def openPrevEntry(self, uid, table, master):
		nuid = int(uid) - 1
		self.getData(nuid, table)
		ntable = table
		self.openDataEntry(nuid, ntable, entryData)
		master.destroy()

	def closeRefresh(self, table, master):
		master.destroy()
		frame2 = Frame(root)
		frame2.pack()
		
		o = displayEntries(frame2, table)

		
	def openFile(self, uid, table):
		cursor = db.cursor()
		lenTab = len(table)
		
		if lenTab > 3:
			if table[1] == 'Artist':
				tab = 'music'
			else:
				tab = 'movies'
		elif table[1] == 'Developer':
			tab = 'games'
		else:
			tab = 'pictures'
			
		cursor.execute('SELECT PATH FROM {table_name} WHERE UID= %s'.format(table_name= tab) %  uid)
		path = cursor.fetchone()
		
		path = str(path)
		path = re.sub("[(',)]", '', path)
		
		if tab == 'games':
			os.system('%s'%path)
		else:			
			op = subprocess.check_output(['xdg-open', '%s'%path])
		
#		os.system("start", '%s'%path)

			
		
class connectDB:
	
	def __init__(self):
		try:
			global db
			db = MySQLdb.connect("localhost", "****", "*****", 'mediaTool')
			global cursor
			cursor = db.cursor()
			print 'Connected!!!'
		except:
			print 'DB does not exist... yet!'
			self.createConnect
		
		
	def createDB(self):
		db = MySQLdb.connect("localhost", "****", "*****")
		
		global cursor
		cursor = db.cursor()

		cr_db = 'CREATE DATABASE mediaTool'

		change_db = 'USE mediaTool'

		pics = """CREATE TABLE pictures (
				TITLE CHAR(64) NOT NULL,
				ARTIST CHAR(64),
				MEDIUM CHAR(255),
				PATH CHAR(128),
				UID INT NOT NULL AUTO_INCREMENT primary key,
				UNIQUE(PATH)
				)"""

		movies = """CREATE TABLE movies (
				TITLE CHAR(64) NOT NULL,
				DIRECTOR CHAR(64),
				GENRE CHAR(255),
				RELEASEYEAR CHAR(32),
				PATH CHAR(128),
				UID INT NOT NULL AUTO_INCREMENT primary key,
				UNIQUE(PATH)
				)"""

		games = """CREATE TABLE games (
				TITLE CHAR(64) NOT NULL,
				DEVELOPER CHAR(64),
				GENRE CHAR(255),
				PATH CHAR(128),
				UID INT NOT NULL AUTO_INCREMENT primary key,
				UNIQUE(PATH)
				);"""

		music = """CREATE TABLE music (
				TITLE CHAR(64) NOT NULL,
				ARTIST CHAR(64),
				ALBUM CHAR(64),
				GENRE CHAR(255),
				PATH CHAR(128),
				UID INT NOT NULL AUTO_INCREMENT primary key,
				UNIQUE(PATH)
				);""" 
		
		
		cursor.execute(cr_db)
		cursor.execute(change_db)
		cursor.execute(games)
		cursor.execute(pics)
		cursor.execute(movies)
		cursor.execute(music)

		db.commit()

	
	
class updateMstrLists:
	
	def __init__(self):
		self.readDirectories()
		print 'Directories Read'
		self.differentialFile()
		print 'Diff Files Ready'
		self.insertNewData()
		print 'Data Inserted'
		
		db.commit()
		

		
		
	def readDirectories(self):
		empty = '-'
		
		picpath = '/home/******/mediaTool/images'
		movpath = '/home/******/mediaTool/movies'
		muspath = '/home/******/mediaTool/music'
		gampath = '/home/******/mediaTool/games'
		
		
		
		
		test = [picpath, movpath, muspath, gampath]
			
		for i in test:
			if i == picpath:
				dirs = os.listdir(picpath)
				imgList = open('/home/******/mediaTool/tempimglist.csv', "wb")
				for file in dirs:
					title, extension = os.path.splitext(file)
					imgList.write(title + "\t" + empty + "\t" + picpath + '/' + file + "\t" + empty + "\n")
				
			elif i == movpath:
				dirs = os.listdir(movpath)
				movList = open('/home/******/mediaTool/tempmovlist.csv', "wb")
				for file in dirs:
					title, extension = os.path.splitext(file)
					movList.write(title + "\t" + empty + "\t" + movpath + '/' + file + "\t" + empty + "\t" + empty + "\n")

			elif i == muspath:
				dirs = os.listdir(muspath)
				musList = open('/home/******/mediaTool/tempmuslist.csv', "wb")
				for file in dirs:
					title, extension = os.path.splitext(file)
					musList.write(title + "\t" + empty + "\t" + muspath + '/' + file + "\t" + empty + "\t" + empty + "\n")
					
			else:
				dirs = os.listdir(gampath)
				gamList = open('/home/******/mediaTool/tempgamlist.csv', "wb")
				for file in dirs:
					title, extension = os.path.splitext(file)
					gamList.write(title + "\t" + empty + "\t" + gampath + '/' + file + "\t" + empty + "\n")
		
		
	def differentialFile(self):
			
		test = [1, 2, 3, 4]
					
		for i in test:
			if i == test[0]:
				master_file = 'imglist.csv'
				temp_file = 'tempimglist.csv'
				diff_file = 'diffimg.csv'
			elif i == test[1]:
				master_file = 'movlist.csv'
				temp_file = 'tempmovlist.csv'
				diff_file = 'diffmov.csv'
			elif i == test[2]:
				master_file = 'muslist.csv'
				temp_file = 'tempmuslist.csv'
				diff_file = 'diffmus.csv'
			else:
				master_file = 'gamlist.csv'
				temp_file = 'tempgamlist.csv'
				diff_file = 'diffgam.csv'
				
			master_data = file(master_file).read().split('\n')
			temp_data = file(temp_file).read().split('\n')

			master_set = set(master_data)
			temp_set = set(temp_data)

			new_entries = temp_set - master_set
			new_master = master_set|new_entries


			diff = open('%s'%diff_file, 'wb')
			master = open('%s'%master_file, 'wb')
	
			for line in temp_data:
				if line in new_entries:
					diff.write(line + '\n')
				if line in new_master:
					master.write(line + '\n')
	
	def insertNewData(self):
		
		test = ['pictures', 'movies', 'music', 'games']
		
		for i in test:
			if i == test[0]:
				openFile = open('diffimg.csv', 'rb')
				reader = csv.reader(openFile, delimiter = '\t')
				for row in reader:
					if len(row) != 0:
						cursor.execute('INSERT INTO pictures(TITLE,ARTIST,PATH,MEDIUM) VALUES(%s, %s, %s, %s)', (row))
					else:
						continue
			elif i == test[1]:
				openFile = open('diffmov.csv', 'rb')
				reader = csv.reader(openFile, delimiter = '\t')
				for row in reader:
					if len(row) != 0:
						cursor.execute('INSERT INTO movies(TITLE,DIRECTOR,PATH,GENRE,RELEASEYEAR) VALUES(%s, %s, %s, %s, %s)', (row))
					else:
						continue				
			elif i == test[2]:
				openFile = open('diffmus.csv', 'rb')
				reader = csv.reader(openFile, delimiter = '\t')
				for row in reader:
					if len(row) != 0:
						cursor.execute('INSERT INTO music(TITLE,ARTIST,PATH,GENRE,ALBUM) VALUES(%s, %s, %s, %s, %s)', (row))
					else:
						continue				
			else:
				openFile = open('diffgam.csv', 'rb')
				reader = csv.reader(openFile, delimiter = '\t')
				for row in reader:
					if len(row) != 0:
						cursor.execute('INSERT INTO games(TITLE,DEVELOPER,PATH,GENRE) VALUES(%s, %s, %s, %s)', (row))
					else:
						continue			
						
		

class welcomeWindow:
	
	def __init__(self, master):
		welcomeFrame = Frame(master)
		welcomeFrame.pack()
		
		
		global tableSelect
		colNum = 0
		
		for i in range(0, 9):
			styleLabel1 = Label(welcomeFrame, text='')
			styleLabel1.grid(row = 0, column = colNum)		
			colNum = colNum + 1
		
		welcomeLabel = Label(welcomeFrame, text="Welcome to JIPtheVIP's MediaTool", font = 'Helvetica 16 bold')
		welcomeLabel.grid(row = 1, column = 1, rowspan = 2)

		colNum = 0
		rowNum = 3
		
		for i in range(0, 3):
			for i in range(0, 2):
				styleLabel2 = Label(welcomeFrame, text='')
				styleLabel2.grid(row = rowNum, column = colNum)		
				colNum = colNum + 1
			rowNum = rowNum + 1
		
		returningUser = Label(welcomeFrame, text='          If you are a returning user:', font = 'Helvetica 12')
		returningUser.grid(row = 6, column = 0, sticky = W)
		newUser = Label(welcomeFrame, text='      If you are a new user:        ', font = 'Helvetica 12')
		newUser.grid(row = 6, column = 3, sticky = E)
		style = Label(welcomeFrame, text= '')
		style.grid(row= 7, column = 0)
		newButton = Button(welcomeFrame, text = 'Click Here', command = lambda: self.scanWait(welcomeFrame))
		newButton.grid(row = 8, column = 3)
		returnButton = Button(welcomeFrame, text= 'Click Here', command = lambda: self.tableSelect(welcomeFrame))
		returnButton.grid(row = 8, column = 0)
		
		colNum = 0
		rowNum = 9
		
		for i in range(0, 3):
			for i in range(0, 2):
				styleLabel2 = Label(welcomeFrame, text='')
				styleLabel2.grid(row = rowNum, column = colNum)		
				colNum = colNum + 1
			rowNum = rowNum + 1
		
		
		
		
	def scanWait(self, master):
		rootietootie = Tk()
		message1 = Label(rootietootie, text='Please move all files you wish to add')
		message1.grid(row = 0, column = 0)
		message2 = Label(rootietootie, text='into their respective folders then click continue.')
		message2.grid(row = 1, column = 0)
		styleRow1 = Label(rootietootie, text = '')
		styleRow1.grid(row = 2, column = 0)
		message3 = Label(rootietootie, text='Example: ~/mediaTool/music')
		message3.grid(row = 3, column = 0)
		styleRow2 = Label(rootietootie, text = '')
		styleRow2.grid(row = 4, column = 0)
		continueBut = Button(rootietootie, text='Continue', command = lambda: self.updt(master, rootietootie))
		continueBut.grid(row = 5, column = 0, sticky = E)

	def updt(self, master, fr):
		u = updateMstrLists()
		fr.destroy()
		self.tableSelect(master)
		
	def tableSelect(self, master):
		master.destroy()
		frame = Frame(root)
		frame.pack()
		
		question = Label(frame, text= 'Which database would you like to access?')
		question.grid(row = 0, column = 0)
		
		
		global pictures
		global movies
		global games
		global music
		
		pictures = ['UID', 'Title', 'Artist', 'Medium']
		movies = ['UID', 'Title', 'Director', 'Release Year', 'Genre']
		games = ['UID','Title', 'Developer', 'Genre']
		music = ['UID', 'Title', 'Artist', 'Album', 'Genre']
		
		global tables
		tables = [pictures, movies, games, music]
		global var
		var = StringVar()
		
		
		for i in tables:
			if i == pictures:
				self.uidCheck = Radiobutton(frame,text= 'Pictures', variable = var, value= 'pictures', command = lambda: self.selectedRB())
				self.uidCheck.grid(row = 2, column = 0, sticky = W)
			elif i == movies:
				self.uidCheck = Radiobutton(frame, text= 'Movies', variable = var, value= 'movies', command = lambda: self.selectedRB())
				self.uidCheck.grid(row = 2, column = 1, sticky = W)
			elif i == games:
				self.uidCheck = Radiobutton(frame, text= 'Games', variable = var, value= 'games', command = lambda: self.selectedRB())
				self.uidCheck.grid(row = 3, column = 0, sticky = W)
			else:
				self.uidCheck = Radiobutton(frame, text= 'Music', variable = var, value= 'music', command = lambda: self.selectedRB())
				self.uidCheck.grid(row = 3, column = 1, sticky = W)

		tab = Button(frame, text= 'Search', command = lambda: displayEntries(frame, tableSelect))
		tab.grid(row = 4, column = 0)	
						 
			
			
	def selectedRB(self):
		val = var.get()
		global tableSelect
		if val == 'pictures':
			tableSelect = tables[0]
		elif val == 'movies':
			tableSelect = tables[1]
		elif val == 'games':
			tableSelect = tables[2]
		else:
			tableSelect = tables[3]
		
			 
						 
						 
global root						 
root = Tk()






d = connectDB()
u = updateMstrLists()
w = welcomeWindow(root)


root.mainloop()