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
    
    video_title_str = ''
    
    
           
    for channel_id in subs_channel_list:
        key = ndb.Key(Channel, channel_id)
        channel_key_list.append(key)
    
    channels = ndb.get_multi(channel_key_list)
        
    for channel in channels:    
        if channel:
            videos_list = channel.videos
            lit_eval = ast.literal_eval(videos_list)
            for video in lit_eval:
                
                video_title = str(video['title'].encode('utf-8').strip())
                
                
                video_title_str = video_title_str + " " + video_title
    
    r = Rake()
    
    r.extract_keywords_from_text(video_title_str)
    
    dump = r.get_ranked_phrases()
                
    return dump