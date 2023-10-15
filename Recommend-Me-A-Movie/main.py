import sys
from time import sleep
from turtle import title

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QStackedWidget,QDialog,QApplication,QLabel,QGraphicsDropShadowEffect,QGraphicsBlurEffect,QMessageBox
from PyQt5.QtGui import QPixmap,QColor
from PyQt5 import QtGui
# from PyQt5.QtGui import 

from src.utility import *

movieData = (('The Avengers','0.3','The-Avengers'),'7.5','Bhai dekhle please dekhle main keh raha hu achi hai dekh le \n Kya matlab hero alom ka fan hai')

class mainWin(QDialog):
      
      internetConnectivity          = check_internet_connectivity()
      relatedMovies                 = [] # [('The Avengers','1848228'),('Avengers: Age of Ultron','2395427'),('Avengers: Infinity War','4154756'),('Avengers: Endgame','4154796'),('Avatar','1499549'),('Inception','1375666')]
      relatedMoviesPoster           = []
      recommended_movies            = []
      title_blocks                  = []
      related_moviePostersLabels    = []
      related_indexer               = 0;
      recommeder_indexer            = 0;

      prev_selected                 = None
      selectedMovieIndex            = None 
      def __init__(self):
            super(mainWin,self).__init__()
            loadUi('main.ui',self)
            self.setFixedHeight(931)
            self.setFixedWidth(1141)
            
            blur = QGraphicsBlurEffect()
            blur2 = QGraphicsBlurEffect()
            blur3 = QGraphicsBlurEffect()
            blur4 = QGraphicsBlurEffect()
            shadow = QGraphicsDropShadowEffect()
            shadow2 = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow2.setBlurRadius(30)
            color = QColor()
            color.fromRgb(255,255,255)
            # blur.set
            self.shadow1.setGraphicsEffect(blur)
            self.shadow2.setGraphicsEffect(blur2)
            self.shadow3.setGraphicsEffect(blur3)
            self.related_movies.setGraphicsEffect(blur4)
            # self.next.setGraphicsEffect(shadow)
            self.Title.setGraphicsEffect(shadow)
            self.recommended_moviesWidget.setGraphicsEffect(shadow2)
            self.search.clicked.connect(self.searchInDB)
            self.next.clicked.  connect(self.simNext)
            self.prev.clicked.  connect(self.simPrev)
            self.rec_next.clicked.connect(self.recNext)
            self.rec_prev.clicked.connect(self.recPrev)
            self.help.clicked.  connect(self.help_)
            
            self.next.setStyleSheet('QPushButton{background-color: #545454;}')
            self.prev.setStyleSheet('QPushButton{background-color: #545454;}')
            
            self.next.        setEnabled(False)
            self.prev.        setEnabled(False)
            self.moviePoster1.setEnabled(False)
            self.moviePoster2.setEnabled(False)
            self.moviePoster3.setEnabled(False)
            self.moviePoster4.setEnabled(False)
            self.moviePoster5.setEnabled(False)
            self.rec_prev    .setEnabled(False)
            self.rec_next    .setEnabled(False)

            self.moviePoster1.mousePressEvent =self.poster1
            self.moviePoster2.mousePressEvent =self.poster2
            self.moviePoster3.mousePressEvent =self.poster3
            self.moviePoster4.mousePressEvent =self.poster4
            self.moviePoster5.mousePressEvent =self.poster5
            self.internetConnection.mousePressEvent = self.refereshInternet

            self.loading.lower()

            if self.internetConnectivity:
                  pixi = QPixmap('img/wifi.png')
                  pixi.scaledToWidth(40)
                  self.internetConnection.setPixmap(pixi)
            else:
                  pixi = QPixmap('img/no-wifi.png')
                  pixi.scaledToWidth(40)
                  self.internetConnection.setPixmap(pixi)
                  # self.internetConnection.setStyleSheet('QLabel{background-color:gray;}')

            self.title_blocks.              extend([self.movie1,self.movie2,self.movie3,self.movie4,self.movie5])
            self.related_moviePostersLabels.extend([self.moviePoster1,self.moviePoster2,self.moviePoster3,self.moviePoster4,self.moviePoster5])
      
      def refereshInternet(self,event):
            self.internetConnectivity= check_internet_connectivity()
            print(self.internetConnectivity)
            if self.internetConnectivity:
                  pixi = QPixmap('img/wifi.png')
                  pixi.scaledToWidth(40)
                  self.internetConnection.setPixmap(pixi)
            else:
                  print('executing else:')
                  pixi = QPixmap('img/no-wifi.png')
                  pixi.scaledToWidth(40)
      def poster1(self,event):
            if self.prev_selected is not None:
                  self.related_moviePostersLabels[self.prev_selected].setStyleSheet('QLabel{border:None};')
            self.prev_selected = 0
            self.selectedMovieIndex = 0 +self.related_indexer
            self.related_moviePostersLabels[0].setStyleSheet('QLabel{border: 10 solid #2ce2cd;border-radius:3px}')
            self.getRecommendation()
            self.showRecommended()

            print('selectedIndexer:',self.selectedMovieIndex)
            print('movie selected:',self.relatedMovies[self.selectedMovieIndex])
      def poster2(self,event):
            if self.prev_selected is not None:
                  self.related_moviePostersLabels[self.prev_selected].setStyleSheet('QLabel{border:None};')
            self.prev_selected = 1
            self.selectedMovieIndex = 1 +self.related_indexer
            self.related_moviePostersLabels[1].setStyleSheet('QLabel{border: 10 solid #2ce2cd;border-radius:3px}')
            print('selectedIndexer:',self.selectedMovieIndex)
            print('movie selected:',self.relatedMovies[self.selectedMovieIndex])
            self.getRecommendation()
            self.showRecommended()

            
      def poster3(self,event):
            if self.prev_selected is not None:
                  self.related_moviePostersLabels[self.prev_selected].setStyleSheet('QLabel{border:None};')
            self.prev_selected = 2
            self.selectedMovieIndex = 2 +self.related_indexer
            
            self.related_moviePostersLabels[2].setStyleSheet('QLabel{border: 10 solid #2ce2cd;border-radius:3px}')
            print('selectedIndexer:',self.selectedMovieIndex)
            self.getRecommendation()
            print('movie selected:',self.relatedMovies[self.selectedMovieIndex])
            self.showRecommended()
            
      def poster4(      self,event):
            if self.prev_selected is not None:
                  self.related_moviePostersLabels[self.prev_selected].setStyleSheet('QLabel{border:None};')
            self.prev_selected = 3
            self.selectedMovieIndex = 3 +self.related_indexer
            self.related_moviePostersLabels[3].setStyleSheet('QLabel{border: 10 solid #2ce2cd;border-radius:3px}')
            print('selectedIndexer:',self.selectedMovieIndex)

            print('movie selected:',self.relatedMovies[self.selectedMovieIndex])
            self.getRecommendation()
            self.showRecommended()
            
      def poster5(self,event):
            if self.prev_selected is not None:
                  self.related_moviePostersLabels[self.prev_selected].setStyleSheet('QLabel{border:None};')
            self.prev_selected = 4
            self.selectedMovieIndex = 4 +self.related_indexer
            self.related_moviePostersLabels[4].setStyleSheet('QLabel{border: 10 solid #2ce2cd;border-radius:3px}')
            print('selectedIndexer:',self.selectedMovieIndex)
            print('movie selected:',self.relatedMovies[self.selectedMovieIndex])
            self.getRecommendation()
            self.showRecommended()
            
      def searchInDB(self):
            movieToSearch      = self.searchBar.text()
            if not self.internetConnectivity:
                  noInternet = QMessageBox()
                  noInternet.setWindowTitle('No Internet')
                  noInternet.setText('Check Your internet connection\nEihter no internet connection detected or weak internet\n Press internet icon to refresh')
                  noInternet.show()
                  noInternet.exec()
            else:
                  if movieToSearch == 'Search Here':
                        noMovieGiven = QMessageBox()
                        noMovieGiven.setWindowTitle('No movie provided')
                        noMovieGiven.setText('Please proivde a movie name to search.')
                        noMovieGiven.show()
                        noMovieGiven.exec()
                  else:
                        self.showSim(movie = movieToSearch)
                        self.switchPosters(True)

                        self.next.setEnabled(True)
                        self.next.setStyleSheet('''
                                                      
                                                
QPushButton#next{
border:None;
background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.898, y2:0.977, stop:0.211454 rgba(4, 21, 132, 255), stop:1 rgba(5, 182, 191, 255));
border-top-left-radius:15px;
border-bottom-left-radius:15px;
}

QPushButton#next:hover{
	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.898, y2:0.977, stop:0.211454 rgba(5, 182, 191, 255), stop:1 rgba(4, 21, 132, 255));
}
'''
                                                )
      def simNext(self):
            limit          =5
            self.enablePrev()
            self.enableNext()
            if self.prev_selected is not None:
                  self.related_moviePostersLabels[self.prev_selected].setStyleSheet('QLabel{border:None};')
            print(self.related_indexer)
            if self.related_indexer<limit:
                  self.related_indexer    +=1
                  for i in range(5):
                              self.title_blocks[i].setStyleSheet("QLabel{background-color:None;color:'black'; }")
                              self.title_blocks[i].setText(self.relatedMovies[i+self.related_indexer][0])
                              pixi = QPixmap('img/posters/'+self.relatedMovies[i+self.related_indexer][2]+'.png')
                              if pixi.isNull():
                                    pixi = QPixmap('img/null/null.jpg')
                              pixi = pixi.scaledToWidth(141)
                              pixi = pixi.scaledToWidth(141)
                              self.related_moviePostersLabels[i].setPixmap(pixi)
            else:
                  self.next.setEnabled(False)
                  self.next.setStyleSheet('QPushButton{background-color: qlineargradient(spread:pad, x1:0, y1:0.00531818, x2:1, y2:1, stop:0 rgba(58, 58, 58, 255), stop:1 rgba(212, 212, 212, 255));}')

                        

      def simPrev(self):

            self.enableNext()
            self.enablePrev()
            if self.prev_selected is not None:
                  self.related_moviePostersLabels[self.prev_selected].setStyleSheet('QLabel{border:None};')
            limit =0
            print(self.related_indexer)
            if self.related_indexer>limit:
                  self.related_indexer-=1
                  for i in range(5):
                              self.title_blocks[i].setStyleSheet("QLabel{background-color:None;color:'black'; }")
                              self.title_blocks[i].setText(self.relatedMovies[i+self.related_indexer][0])
                              pixi = QPixmap('img/posters/'+self.relatedMovies[i+self.related_indexer][2] +'.png')
                              if pixi.isNull():
                                    pixi = QPixmap('img/null/null.jpg')
                              pixi = pixi.scaledToWidth(141)
                              self.related_moviePostersLabels[i].setPixmap(pixi)
                              pixi = pixi.scaledToWidth(141)
                              self.related_moviePostersLabels[i].setPixmap(pixi)
            else:
                  self.prev.setEnabled(False)
                  self.prev.setStyleSheet('QPushButton{background-color: qlineargradient(spread:pad, x1:0, y1:0.00531818, x2:1, y2:1, stop:0 rgba(58, 58, 58, 255), stop:1 rgba(212, 212, 212, 255));}')

      def help_(self):
            HELP = QMessageBox(self)
            HELP.setWindowTitle('Help')
            HELP.setText('''
This application recommends you a movie based upon the story,cast,reviews.. based upon the movie you choose.

Search:
      search your movie in our data by using search bar and search button.


Select:
      Select the movie from the movie shown below by clicking on the image shown.

Enjoy:
      Review 10 best matches
            ''')
            HELP.show()
            button = HELP.exec()
      def showSim(self,movie):
            self.relatedMovies = searchSimilarInDB(movie,widget= self.loading,label=self.label)
            print(self.relatedMovies)
            self.relatedMoviesPoster = getPoster(self.relatedMovies)

            for i in range(5):
                        self.title_blocks[i].setStyleSheet('QLabel{background-color:None;color:"black";font: 57 11pt "Noto Sans"; }')
                        self.title_blocks[i].setText(self.relatedMovies[i][0])
                        pixi = QPixmap('img/posters/'+self.relatedMovies[i][2] +'.png')
                        if pixi.isNull():
                              pixi = QPixmap('img/null/null.jpg')
                        pixi = pixi.scaledToWidth(141)
                        self.related_moviePostersLabels[i].setPixmap(pixi)
      def enablePrev(self):
            if self.related_indexer>=0:
                  self.prev.setEnabled(True)
                  self.prev.setStyleSheet('''
                                                
                                          QPushButton#prev{
                                          border:None;
                                          background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.898, y2:0.977, stop:0.211454 rgba(4, 21, 132, 255), stop:1 rgba(5, 182, 191, 255));
                                          border-top-right-radius:15px;
                                          border-bottom-right-radius:15px;
                                          }

                                          QPushButton#prev:hover{
                                                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.898, y2:0.977, stop:0.211454 rgba(5, 182, 191, 255), stop:1 rgba(4, 21, 132, 255));
                                          }'''
                                          )
      def enableNext(self):
            if self.related_indexer<=5:
                  self.next.setEnabled(True)
                  self.next.setStyleSheet('''
                                          QPushButton#next{
                                          border:None;
                                          background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.898, y2:0.977, stop:0.211454 rgba(4, 21, 132, 255), stop:1 rgba(5, 182, 191, 255));
                                          border-top-left-radius:15px;
                                          border-bottom-left-radius:15px;
                                          }

                                          QPushButton#next:hover{
                                                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.898, y2:0.977, stop:0.211454 rgba(5, 182, 191, 255), stop:1 rgba(4, 21, 132, 255));
                                          }'''
                                          )
      def switchPosters(self,flag:bool):
            self.moviePoster1.setEnabled(flag)
            self.moviePoster2.setEnabled(flag)
            self.moviePoster3.setEnabled(flag)
            self.moviePoster4.setEnabled(flag)
            self.moviePoster5.setEnabled(flag)


      def showRecommended(self):
            import os
            self.loading.raise_()
            self.loading.setStyleSheet('QWidget{background-color:rgba(0,0,0,150)}')
            self.label.setText('Loading')
            QApplication.processEvents()
            print('img/posters/'+self.recommended_movies[self.recommeder_indexer][2]+'.png')
            Path = 'img/posters/'+self.recommended_movies[self.recommeder_indexer][2]+'.png'
            if not os.path.exists(Path):
                  getPoster([self.recommended_movies[self.recommeder_indexer]])
            pixi = QPixmap(Path)
            self.moviePoster.setPixmap(pixi)
            self.movieTitle.setStyleSheet('''QLabel{background-color:None;
                                             color: white;
                                             font-size:25pt;}''')
            self.movieTitle.setText(self.recommended_movies[self.recommeder_indexer][0])
            self.movieTitle.adjustSize()
            self.movieRating.setStyleSheet('''QLabel{background-color:None;
                                                color: white;font-size:12;}''')
            self.movieRating.setText('Rating:   '+str(self.recommended_movies[self.recommeder_indexer][-1])+'/10')
            self.movieDesc.setText(self.recommended_movies[self.recommeder_indexer][4])
            self.movieDesc.setStyleSheet('QLabel{background-color:None;color: white;font: 25 12pt "Noto Sans"; }')
            # self.movieDesc.adjustSize()
            self.loading.setStyleSheet('QWidget{background-color:rgba(0,0,0,0)}')
            self.label.setText('')
            self.loading.lower()

      def getRecommendation(self):
            self.rec_prev.setEnabled(True)
            self.rec_next.setEnabled(True)
            self.loading.raise_()
            self.loading.setStyleSheet('QWidget{background-color:rgba(0,0,0,150)}')
            self.label.setText('Bot is watching movies to recommend you some')
            QApplication.processEvents()
            self.recommended_movies = fetchRecommendation(self.relatedMovies[self.related_indexer])
            self.loading.setStyleSheet('QWidget{background-color:rgba(0,0,0,0)}')
            self.label.setText('')
            self.loading.lower()
      def recNext(self):
            if self.recommeder_indexer>5:
                  self.rec_next.setEnabled(False)
            else:
                  self.recommeder_indexer+=1
                  self.showRecommended()
            pass
      def recPrev(self):
            if self.recommeder_indexer<1:
                  self.rec_prev.setEnabled(False)
            else:
                  self.recommeder_indexer-=1
                  self.showRecommended()
            pass
if __name__ == '__main__':
      app = QApplication(sys.argv)
      app.setApplicationDisplayName('Recommend me a movie!!')
      ui = mainWin()
      main = QStackedWidget()
      main.addWidget(ui)
      main.show()
      app.exec_()
      clear_poster()
      sys.exit()