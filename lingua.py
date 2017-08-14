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
from collections import defaultdict
from operator import itemgetter
import json
from rake_nltk import Rake

        
def topics(subs_channel_list):
    
    
    channel_key_list = []
    
    categories_dict = dict()
           
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
                    
                video_category = str(video['category'])
                
                video_author = str(video['author'])
                
                

                if video_category in categories_dict:
                    
                    if video_author not in categories_dict[video_category]:
                        
                        if len(categories_dict[video_category]) >= 7:
                            
                            pass
                        
                        else:                        
                        
                            categories_dict[video_category].append(video_author)
                    
                else:
                    # create a new array in this slot
                    categories_dict[video_category] = [video_author]
                    
            
    
    return categories_dict