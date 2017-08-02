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
           
    for channel_id in subs_channel_list:
        
        logging.info('Aggregating channel {}'.format(channel_id))
        
        key = ndb.Key(Channel, channel_id)
        channel = key.get()        
        
        videos_list = channel.videos
        
        lit_eval = ast.literal_eval(videos_list)
        
        for video in lit_eval:
            
            subs_videos.append(video)
            
        
    ordered_subs_video = sorted(subs_videos, key=itemgetter('post_date') , reverse=True) 
    
    dump = ordered_subs_video
    dump = pprint.pformat(dump, indent=4)    
    
    return dump
    
        
    
        