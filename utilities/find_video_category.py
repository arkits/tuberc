import bs4 as bs
import html
from urllib2 import urlopen

source = urlopen('https://www.youtube.com/watch?v=eMtHmKO8GsA').read()

soup = bs.BeautifulSoup(source,"html.parser")

video_elements = soup.find_all(attrs={"class": "g-hovercard yt-uix-sessionlink spf-link "})

for element in video_elements:
    classes = element
    link = classes.string
    print link

