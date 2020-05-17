from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from ui import *
import os
import datetime
import sip
import zipfile
class GUIForm(Ui_MainWindow):
	def __init__(self,window):
		self.setupUi(window)
		self.NewList.setColumnWidth(0,400)
		self.ExtractList.setColumnWidth(0,250)
		self.FileInfoList.setColumnWidth(0,250)
		self.window = window
		self.FileCount=0
		self.AddFileBtn.clicked.connect(self.addFileToList)
		self.RemoveFileBtn.clicked.connect(self.removeFileFromList)
		self.ClearListBtn.clicked.connect(self.clearList)
		self.CreateZipBtn.clicked.connect(self.createZip)
		self.NewSelectDestBtn.clicked.connect(self.NewSelectDest)
		self.ExtractSelectBtn.clicked.connect(self.ExtSelectFile)
		self.ExtractDestBtn.clicked.connect(self.ExtSelectDest)
		self.ExtractBtn.clicked.connect(self.Extract)
		self.FileSelectBtn.clicked.connect(self.SelectFile)
	def addFileToList(self,window):
		fpath = QFileDialog.getOpenFileNames(self.window,'Add file','',"All files (*.*)")
		files= fpath[0]
		try:
			for file in files:
				item = QTreeWidgetItem(self.NewList,self.getFileData(file))
				self.FileCount+=1
		except:
			QMessageBox.warning(self.window,'Error!','Something went wrong!')
	def getFileData(self,fpath):
		lst=[]
		lst.append(fpath)
		time = datetime.datetime.fromtimestamp(os.path.getmtime(fpath))
		time = "{}/{}/{}".format(time.day,time.month,time.year)
		lst.append(time)
		fsize = str(os.path.getsize(fpath))
		fsize+=' Bytes'
		lst.append(fsize)
		return lst
	def removeFileFromList(self):
		try:
			x = self.NewList.selectedItems()
			sip.delete(x[0])
			self.FileCount-=1
		except:
			QMessageBox.warning(self.window,'Error!','Select a file from the list!')
	def clearList(self):
		self.NewList.clear()
	def NewSelectDest(self):
		fname = QFileDialog.getSaveFileName(self.window,'Select destination','','Zip file(*.zip)')
		fname = fname[0]
		self.DestinationInput.setText(fname)
	def createZip(self):
		items=[]
		files=[]
		try:
			root = self.NewList.invisibleRootItem()
			for i in range(self.FileCount):
				items.append(root.child(i))
			for i in items:
				files.append(i.text(0))
			destination = self.DestinationInput.text()
			if(destination!=''): 
				zip = zipfile.ZipFile(destination,'a')
				for file in files:
					destinationABS = os.path.basename(file)
					zip.write(file,destinationABS)
			else:
				self.NewSelectDest()
		except Exception as error:
			QMessageBox.warning(self.window,'Error!','Something went wrong!')
	def ExtSelectFile(self):
		try:
			fname = QFileDialog.getOpenFileName(self.window,'Open a Zip','','Zip files (*.zip)')
			fname = fname[0]
			self.ExtractFileInput.setText(fname)
			zip = zipfile.ZipFile(fname,'r',allowZip64=True)
			FilesInZip = zip.infolist()
			FileList = []
			for file in FilesInZip:
				z=[]
				z.append(file.filename)
				date = file.date_time
				date = '{}/{}/{}'.format(date[2],date[1],date[0])
				z.append(date)
				z.append(str(file.file_size)+' Bytes')
				FileList.append(z)
			self.ExtractList.clear()
			for fileInfo in FileList:
				item = QTreeWidgetItem(self.ExtractList,fileInfo)
		except Exception as error:
			QMessageBox.warning(self.window,'Error!','Something went wrong!')
	def ExtSelectDest(self):
		try:
			fname = QFileDialog.getExistingDirectory(self.window,'Select destination','')
			self.ExtractDestInput.setText(fname)
		except:
			QMessageBox.warning(self.window,'Error!','Something went wrong!')
	def Extract(self):
		src = self.ExtractFileInput.text()
		dest = self.ExtractDestInput.text()
		if(src==''):
			self.ExtSelectFile()
		if(dest==''):
			self.ExtSelectDest()
		try:
			zip = zipfile.ZipFile(dest,'r',allowZip64=True)
			zip.extractall(path=dest)
		except Exception as error:
			print(error)
	def SelectFile(self):
		try:
			fname = QFileDialog.getOpenFileName(self.window,'Open a Zip','','Zip files (*.zip)')
			fname = fname[0]
			self.FileInfoInput.setText(fname)
			zip = zipfile.ZipFile(fname,'r',allowZip64=True)
			FilesInZip = zip.infolist()
			FileList = []
			for file in FilesInZip:
				z=[]
				z.append(file.filename)
				date = file.date_time
				date = '{}/{}/{}'.format(date[2],date[1],date[0])
				z.append(date)
				z.append(str(file.file_size)+' Bytes')
				FileList.append(z)
			self.ExtractList.clear()
			for fileInfo in FileList:
				item = QTreeWidgetItem(self.FileInfoList,fileInfo)
		except Exception as error:
			QMessageBox.warning(self.window,'Error!','Something went wrong!')		



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GUIForm(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

