import httplib2
import os
import webapp2
from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.contrib.appengine import OAuth2DecoratorFromClientSecrets
import json
import logging
import time
from datetime import datetime
from dateutil.parser import parse 
from lib import feedparser

decorator = OAuth2DecoratorFromClientSecrets(os.path.join(os.path.dirname(__file__), 'tuberc.json'),  'https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/plus.login')
service = build('youtube', 'v3')



def get_user_info():
    
    request = service.channels().list(mine=True, part='snippet').execute(decorator.http())
    
    items = request.get('items')
    uid = items[0].get('id')

    snippet = items[0].get('snippet')
    title = snippet.get('title')
    description = snippet.get('description')

    thumbnails = snippet.get('thumbnails')
    high = thumbnails.get('high')
    url = high.get('url')

    self.response.write(uid + '<br>')
    self.response.write(str(title) + '<br>')
    self.response.write(str(description) + '<br>')
    self.response.write('<img src="'+ str(url) + '">')    

def get_sub_list():
    
    more = True
    nextPageToken = False    
    
    while more: 
                
        if nextPageToken:
            subs = service.subscriptions().list(pageToken = nextPageToken, maxResults=50, part='snippet', mine=True).execute(decorator.http())
        else:
            subs = service.subscriptions().list(maxResults=50, part='snippet', mine=True).execute(decorator.http())
        
        items = subs.get('items')

        for item in items:
            snippet = item.get('snippet')
            title = snippet.get('title')
            self.response.write('channel title - ' + title + ' // ')       
        
            resourceId = snippet.get('resourceId')
            channelId = resourceId.get('channelId') 
            self.response.write('channelId - ' + channelId + '<br>')                  

    
    
        nextPageToken = subs.get('nextPageToken')
    
        if nextPageToken:
            logging.debug('Recieved nextPageToken...')
            more = True
        else:
            more = False  


class MainPage(webapp2.RequestHandler):

    @decorator.oauth_aware
    def get(self):

        if decorator.has_credentials():
            
            
            self.response.headers["Content-Type"] = "text/html"
            self.response.write("<h1> I'M IN BOIS! </h1>")
        
            d = feedparser.parse('https://www.youtube.com/feeds/videos.xml?channel_id=UCxt9Pvye-9x_AIcb1UtmF1Q')
            self.response.write( '<h2> Feed Title - ' + d.feed.title + '</h2>' )  
            self.response.write(  '<h3> Feed link - ' +    d['feed']['link'] + '</h3>' )
            self.response.write(  '<h3> Number of entries - ' +    str(len(d['entries'])) + '</h3>' )
            for post in d.entries:
                post_date = parse(post.published)
                post_date = post_date.strftime('%Y-%m-%d %H:%M:%S')
                self.response.write( post.title + " --- " + post.link  + ' --- ' + str(post_date) + '<br>')
            
         
                             
        else:
            url = decorator.authorize_url()
            self.response.headers["Content-Type"] = "text/html"
            self.response.write("<h1>Sign in karle bsdk... :(</h1>")
            self.response.write("<a href=" + url +">Click here to login</a>")

routes = [('/', MainPage),  (decorator.callback_path, decorator.callback_handler())]

app = webapp2.WSGIApplication(routes, debug=True)
