
import requests 
from bs4 import BeautifulSoup 
import os.path
def getdata(url): 
    r = requests.get(url) 
    return r.text 


def scrap_poster(movie_name_,id):
      if os.path.exists('img/posters/'+movie_name_+".png"):
            return True
      print('call picked')
      url = "https://www.cinematerial.com/movies/"
      htmldata = getdata(url+movie_name_+'-i'+id) 
      soup = BeautifulSoup(htmldata, 'html.parser') 
      counter =0
      done = False
      print('URL:',url+movie_name_+'-i'+id)
      for item in soup.find_all('img')[:5]:
            start = item['src'].find('https')
            if start!= -1:
                  url = item['src'][start:]
                  response = requests.get(url)

                  file = open('img/posters/'+movie_name_+".png", "wb")
                  file.write(response.content)
                  file.close()
                  done=True
            if done:
                  print('call processed completely! Poster of movie',movie_name_,'is available')
                  break
      return done

# scrap_poster('Avengers: Endgame','123798')