import urllib.request
from bs4 import BeautifulSoup
import re
import requests
import json

from . import settings

API_KEY = settings.API_KEY
LYRICS_URL = settings.LYRICS_URL


def find_lyrics(artist, song_title):
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    url = LYRICS_URL + song_title + '&q_artist=' + artist + '&apikey=' + API_KEY
    content = json.loads(requests.get(url).text[9:-2])['message']['body']['lyrics']['lyrics_body']

    return content


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
