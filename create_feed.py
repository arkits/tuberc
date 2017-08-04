import datetime
import webapp2
import os
import re
from google.appengine.api import taskqueue
import jinja2
from models.channel import Channel
from google.appengine.ext import ndb
import logging
import pprint
import ast
from operator import itemgetter


def post(subs_channel_list):
    
    subs_videos = []
    
    channel_key_list = []
           
    for channel_id in subs_channel_list:
        
        key = ndb.Key(Channel, channel_id)
        
        logging.debug('Adding channel_id to list {}'.format(channel_id))
        
        channel_key_list.append(key)
    
    channels = ndb.get_multi(channel_key_list)
        
    for channel in channels:    
        
        if channel:
        
            videos_list = channel.videos
            
            lit_eval = ast.literal_eval(videos_list)
            
            for video in lit_eval:
                
                subs_videos.append(video)
                
                
    ordered_subs_video = sorted(subs_videos, key=itemgetter('post_date') , reverse=True) 
    
    small_list = ordered_subs_video[:20]
    
    dump = small_list
     
    logging.debug('Returning feed - {}'.format(channel_id))
    
    return dump
    
        
    
        