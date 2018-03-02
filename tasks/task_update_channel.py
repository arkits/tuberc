from datetime import datetime
from dateutil.parser import parse 
import webapp2
import os
import re
from google.appengine.api import taskqueue
import jinja2
from models.channel import Channel
from google.appengine.ext import ndb
import logging
from lib import feedparser
from operator import itemgetter
import json
import bs4 as bs
import html
from urllib2 import urlopen
import settings 


class ChannelUpdateException(Exception):
    pass


class taskUpdateChannel(webapp2.RequestHandler):
    
    def getCategory(self, link, author):
        
        source = urlopen(link).read()
        
        soup = bs.BeautifulSoup(source,"html.parser")
        
        category = "Uncategorized"
        
        genre = soup.find("meta", {"itemprop":"genre"})
        
        if genre is not None:
            
            if genre['content'] is not None:
                
                category = genre['content']
                
        return category
    
    
    def getDisplayPicture(self, channelid):
        
        api_key = settings.YOUTUBE_WEBDATA_API_KEY
        
        url_part_a = 'https://www.googleapis.com/youtube/v3/channels?part=snippet&id='
        
        url_part_b = '&fields=items%2Fsnippet%2Fthumbnails&key='
        
        link = url_part_a + channelid + url_part_b + api_key
        
        response = urlopen(link)
        
        data = json.load(response)  
        
        item = data.get('items')
        
        snippet = item[0].get('snippet')
        
        thumbnails = snippet.get('thumbnails')
        
        #high = thumbnails.get('high')
        
        default = thumbnails.get('default')
        
        url = default.get('url')        
    
        return url    
    

    def post(self):
        
        # Request Channel ID
        channel_id = self.request.get('channel_id')
        
        logging.info('Yolo from task_update_channel - {}'.format(channel_id))
        
        # Key channel from the ds 
        key = ndb.Key(Channel, channel_id)
        channel = key.get()
    
        if channel:   
            
            # If channel exists 
            logging.info('Found channel in the ds - {}'.format(channel_id))
            
            # Setup feedurl
            feedurl = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + str(channel_id)
            logging.debug('feedurl - {}'.format(feedurl)) 
        
            try:
                
                # Parse RSS Feed
                d = feedparser.parse(feedurl)
                
                logging.info('Getting RSS feed - {}'.format(channel_id))
                
                if 'title' in d.feed:
                
                    # Update channel name and link
                    channel.channel_name = d.feed.title
                    channel.channel_link = d.feed.link
                    
                    url = self.getDisplayPicture(channel_id)
                    channel.display_picture = url
                    
                    videos = []
                    
                    # Loop through all videos/posts
                    for post in d.entries:
    
                        video = {}
                        
                        video['title'] = post.title
                        video['link'] = post.link
                        video['author'] = d.feed.title
                        video['videoid'] = post.yt_videoid
                        
                        category = self.getCategory(video['link'], video['author'])
                        
                        video['category'] = category
                        
                        try:
                            thumbnail =  post.media_thumbnail[0]
                            video['thumbnail'] = thumbnail['url']                        
                        except:
                            video['thumbnail'] = '/img/nahin.jpeg' 
                            
                        post_date = parse(post.published)
                        post_date = post_date.strftime('%Y-%m-%d %H:%M:%S')
                        video['post_date'] = post_date
                        
                        video['author_avatar'] = url
                    
                        videos.append(video)
                
                    # Convert list to string for ds save    
                    channel.videos = str(videos)
                    
                    # Update last_update_date
                    last_update_date = datetime.now()
                    channel.last_update_date = last_update_date 
                    
                    # Commit to ds
                    channel.put()
                    
                    logging.info('Channel update complete! {}'.format(channel_id))
                
            except Exception as e:
                logging.exception('Exception caught - {}'.format(e))  
                raise ChannelUpdateException('Called exception during video update')

             


app = webapp2.WSGIApplication([
    ('/task_update_channel', taskUpdateChannel),
], debug=True)



