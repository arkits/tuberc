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


def post(subs_channel_list, page):
    
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
    
    if page > 1:
        min_page = (page - 1) * 20
    else:
        min_page = 0
        
    max_page  = page * 20
    
    small_list = ordered_subs_video[min_page:max_page]
    
    number_of_vids = len(ordered_subs_video)
    
    dump = small_list
     
    logging.debug('Returning feed - {}'.format(channel_id))
    
    return dump, number_of_vids
    
        
def feed_cat(subs_channel_list, category, page):
    
    category = category.lower()
    
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
                
                if category == video['category'].lower():
                    
                    subs_videos.append(video)
                
    ordered_subs_video = sorted(subs_videos, key=itemgetter('post_date') , reverse=True) 
    
    if page > 1:
        min_page = (page - 1) * 20
    else:
        min_page = 0
        
    max_page  = page * 20
    
    small_list = ordered_subs_video[min_page:max_page]
    
    number_of_vids = len(ordered_subs_video)
    
    dump = small_list
     
    logging.debug('Returning feed - {}'.format(channel_id))
    
    return dump, number_of_vids 
        
def user_categories_list(subs_channel_list):
    
    user_categories_list = []
    
    description_list = []
    
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
                    
                video_category = str(video['category'])
                
                if video_category not in user_categories_list:
                
                    user_categories_list.append(video_category)
                    
                    index = user_categories_list.index(video_category)
                    
                    try:
                        description_list[index] = description_list[index] + ", " + video['author']
                    except:
                        description_list.append(video['author'])
                    

    dump = user_categories_list
    
    return user_categories_list,  description_list