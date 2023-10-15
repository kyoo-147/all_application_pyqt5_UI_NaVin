from pyexpat import model
from threading import get_ident
from urllib import request
from difflib import SequenceMatcher
from PyQt5.QtWidgets import QApplication  
# from scrapper import scrap_poster
from src.scrapper import scrap_poster

import pandas as pd
import gc


movies = pd.read_csv('data/data.csv')
movies.dropna(inplace=True)
movies.imdb_id=movies.imdb_id.apply(lambda x: str(int(x)))
movies.indices = movies.indices.astype('int')

model_dict = {0:'model_1.csv',1:'model_2.csv',2:'model_3.csv',3:'model_4.csv',4:'model_5.csv',5:'model_6.csv',6:'model_7.csv',7:'model_8.csv',8:'model_9.csv'}
indices = pd.read_csv('data/model/model_metadata.csv', index_col=0,squeeze=True)
def stringParser(movie_name):
      movie_name_ = ''
      for i in movie_name:
            if i.isalpha() or i==' ':
                  movie_name_+=i
      movie_name_ = movie_name_.split()
      movie_name_ = '-'.join(movie_name_)
      return movie_name_
'''
      create table with all required constrain as per the ER diagram, insert 10 records each in 3 tables write atleast conditional updates, use select command to display data of all three tables.
'''
def searchSimilarInDB(given_movie,widget,label):
      if widget is not None:
            widget.setStyleSheet('QWidget{background-color:rgba(0,0,0,150)}')
            widget.raise_()
            label.setText('Searching for your movie in database!!')
      QApplication.processEvents()
      print('i am in DB')
      movieList = []
      for movie in movies.original_title.tolist(): 
            ratio_ =SequenceMatcher(a=given_movie.lower(),b=movie.lower()).ratio()
            if ratio_>0.5:
                  movieList.append((ratio_,tuple(movies[movies['original_title']==movie].iloc[0])[:-1]))
                  # print(tuple(movies[movies['original_title']==movie].iloc[0]))
      movieList.sort(key= lambda x:x[0],reverse=True)
      flag = False
      if widget is not None:
            label.setText('')
            widget.lower()
            widget.setStyleSheet('QWidget{background-color:rgba(0,0,0,0)}')
      return [x[1] for x in movieList[:10]]
def getPoster(movies):

      

      for i in movies:
            # print(i)
            print('calling scrapper')
            scrap_poster(i[2],i[1])

# print(searchSimilarInDB('avengers',None,None))

temp = [('The Avengers','0848228'),('Avengers: Age of Ultron','2395427'),('Avengers: Infinity War','4154756'),('Avengers: Endgame','4154796'),('Avatar','0499549'),('Inception','1375666')]
# getPoster(temp)


def check_internet_connectivity():
      import requests
      timeout = 3
      try:
            url = 'https://www.google.com'
            request = requests.get(url,timeout=timeout)
            return True
      except(requests.ConnectionError,requests.Timeout) as exception:
            return False
# print(check_internet_connectivity())

def clear_poster():
      import os
 
      dir = 'img/posters'
      for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

def fetchRecommendation(movieName):       # movieName => tuple( similarityScore-string,tuple(movieTitle,imdbId,movie-url))
      flag =None
      idx = indices[movieName[0]]
      if isinstance(idx,pd.Series):
            idx=idx[0]
      if idx in range(5000):
            flag = 0
      elif idx in range(5000,10000):
            flag = 1
      elif idx in range(10000,15000):
            flag = 2
      elif idx in range(15000,20000):
            flag = 3
      elif idx in range(20000,25000):
            flag = 4
      elif idx in range(25000,30000):
            flag = 5
      elif idx in range(30000,35000):
            flag = 6
      elif idx in range(35000,40000):
            flag = 7
      else:
            flag = 8
      model = pd.read_csv('data/model/'+model_dict[flag])
      recommed = list(enumerate(model[str(idx)]))
      movies_ = sorted(recommed,key = lambda x:x[1],reverse=True)
      l = movies_[1:11]
      recMovieIndices = [i[0] for i in l]
      
      l= tuple(movies[movies['indices'].isin(recMovieIndices)].itertuples(index=False,name=None))
      del model
      return l

gc.collect()

# fetchRecommendation(('Toy Story',123,'urls'))
