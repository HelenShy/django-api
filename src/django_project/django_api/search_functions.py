import urllib.request
from bs4 import BeautifulSoup
import re
import requests


def find_lyrics(artist, song_title):
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"

    content = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(content, 'html.parser')
    lyrics = str(soup)
    # lyrics lies between up_partition and down_partition
    up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
    down_partition = '<!-- MxM banner -->'
    lyrics = lyrics.split(up_partition)[1]
    lyrics = lyrics.split(down_partition)[0]
    lyrics = lyrics.replace('<br>','').replace('</br>','').replace('</div>','').strip()

    return lyrics


def find_video_url(artist, song_title):
    search_text = artist.replace(' ', '+') + song_title.replace(' ', '+')
    video_search = requests.get('https://www.youtube.com/results?search_query=' + search_text)
    page = video_search.text
    soup=BeautifulSoup(page,'html.parser')
    res=soup.find_all('a', attrs={'class':'yt-uix-tile-link'}) #{'class':'yt-simple-endpoint'}
    url_list = []
    for l in res:
        url_list.append(l.get("href"))
    if len(url_list) >1:
        return "https://www.youtube.com/" + url_list[0]
    else:
        return 'Video was not found'
