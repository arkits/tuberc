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


class ChannelUpdateException(Exception):
    pass


class taskUpdateChannel(webapp2.RequestHandler):

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
                
                # Update channel name and link
                channel.channel_name = d.feed.title
                channel.channel_link = d.feed.link
                
                videos = []
                
                # Loop through all videos/posts
                for post in d.entries:

                    video = {}
                    
                    video['title'] = post.title
                    video['link'] = post.link
                    video['author'] = d.feed.title
                    
                    post_date = parse(post.published)
                    post_date = post_date.strftime('%Y-%m-%d %H:%M:%S')
                    video['post_date'] = post_date
                
                    videos.append(video)
            
                # Convert list to string for ds save    
                channel.videos = str(videos)
                
                # Update last_update_date
                last_update_date = datetime.now()
                channel.last_update_date = last_update_date 
                
                # Commit to ds
                channel.put()
                
            except Exception as e:
                logging.exception('Exception caught - {}'.format(e))  
                raise ChannelUpdateException('Called exception during video update')

             


app = webapp2.WSGIApplication([
    ('/task_update_channel', taskUpdateChannel),
], debug=True)



