from PyQt5.QtWidgets import *
from main import Ui_MainWindow
import os
import sys
from PyQt5 import QtGui
import urllib.request
from pytube import Playlist
from pafy import new


class MainApp(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.HANDEL_UI()
        self.HANDEL_BUTTON()
    
    def HANDEL_UI(self):
        self.setWindowTitle('QT Downloader')
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__),'icon.png')))
        self.setFixedSize(710,406)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)


    def HANDEL_BUTTON(self):
        self.DownloadFile.clicked.connect(self.DOWNLOAD_FILE)
        self.BrowseFile.clicked.connect(self.BROWSE_FILE)
        self.SearchVideo.clicked.connect(self.SEARCH_VIDEO)
        self.DownloadVideo.clicked.connect(self.DOWNLOAD_VIDEO)
        self.BrowseVideo.clicked.connect(self.BROWSE_FOLDER)
        self.BrowsePlaylist.clicked.connect(self.BROWSE_FOLDER_1)
        self.DownloadPlaylist.clicked.connect(self.DOWNLOAD_PLAYLIST)

        self.SearchPlaylist.clicked.connect(self.SEARCH_Playlist)
    def CLOSE_APP(self):
        if self.checkBox.isChecked() == True:
            exit()
    def SHUTDOWN_PC(self):
        if self.checkBox_2.isChecked() == True:
            os.system("shutdown /s /t 1")

    def BROWSE_FILE(self):
        path = QFileDialog.getSaveFileName(self)
        self.PathFile.setText(path[0].replace('/','\\'))
        
    def BROWSE_FOLDER(self):
        path = QFileDialog.getExistingDirectory(self,'save as')
        self.PathVideo.setText(path.replace('/','\\'))
    def BROWSE_FOLDER_1(self):
        path = QFileDialog.getExistingDirectory(self,'save as')
        self.PathPlaylist.setText(path.replace('/','\\'))

    def PROGRESS_FILE(self,size,num,total):
        QApplication.processEvents()
        percent = (size * num / total) *100
        self.ProgressFile.setValue(percent)

    def DOWNLOAD_FILE(self):
        try:
            url = self.UrlFile.text()
            path = self.PathFile.text()

            r = urllib.request.urlretrieve(url,path,self.PROGRESS_FILE)
            self.CLOSE_APP()
            self.SHUTDOWN_PC()
            QMessageBox.information(self,'success download','your file is succeccfully downloaded')
            

        except Exception:
            QMessageBox.warning(self,'failed download','your dwonload is field')

        self.UrlFile.setText('')
        self.PathFile.setText('')
        self.ProgressFile.setValue(0)    
    def SEARCH_VIDEO(self):
        url = self.UrlVideo.text()
        path = self.PathVideo.text()
        video = new(url)
        self.comboBox.addItem('mp4')
        self.comboBox.addItem('mp3')
    def PROGRESS_VIDEO(self,total,recvd,ratio,rate,eta):
            percent = recvd / total * 100
            QApplication.processEvents()
            self.ProgressVideo.setValue(percent)
    def DOWNLOAD_VIDEO(self):
        try:

            url=self.UrlVideo.text()
            path=self.PathVideo.text()
            video = new(url)
            if self.comboBox.currentIndex() == 0:
                video.getbest().download(path,callback=self.PROGRESS_VIDEO)
            elif self.comboBox.currentIndex() == 1:
                video.getbestaudio().download(path,callback=self.PROGRESS_VIDEO)
            self.CLOSE_APP()
            self.SHUTDOWN_PC()
            QMessageBox.information(self,'success download','your file is succeccfully downloaded')


        except Exception:
            QMessageBox.warning(self,'failed download','your dwonload is field')

        self.UrlVideo.setText('')
        self.PathVideo.setText('')
        self.ProgressVideo.setValue(0)
        self.comboBox.clear()
    def SEARCH_Playlist(self):
        url = self.UrlPlaylist.text()
        path = self.PathPlaylist.text()
        playlist = Playlist(url)
        videosnum= 0
        for video in playlist:
            videosnum +=1
        self.lineEdit_2.setText(str(videosnum))
        self.lineEdit.setText('0')

    def DOWNLOAD_PLAYLIST(self):
        try:
            videocurrent=0
            url= self.UrlPlaylist.text()
            path= self.PathPlaylist.text()
            playlist= Playlist(url)
            os.chdir(path)
            if not os.path.isdir(playlist.title):
                os.mkdir(playlist.title)

            os.chdir(playlist.title)
            for video in playlist.videos:
                QApplication.processEvents()
                video.streams.get_highest_resolution().download()
                videocurrent+=1
                self.lineEdit.setText(str(videocurrent))
            self.UrlPlaylist.setText('')
            self.PathPlaylist.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit.setText('')
            self.CLOSE_APP()
            self.SHUTDOWN_PC()
            QMessageBox.information(self,'success download','your file is succeccfully downloaded')

        except Exception:
            QMessageBox.warning(self,'failed download','your dwonload is field')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()