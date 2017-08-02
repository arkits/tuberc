import datetime
import webapp2
import os
import jinja2
from models.channel import Channel
from google.appengine.ext import ndb
import logging

        
def add(channel_id):
    
    # Set last_update_date to now
    last_update_date = datetime.datetime.now()
    
    # Build channel object
    channel = Channel()
    channel.key = ndb.Key(Channel, channel_id)
    
    channel.channel_id = channel_id
    channel.channel_name = 'Channel Name'
    channel.channel_link = 'https://www.youtube.com/'
    channel.last_update_date = last_update_date   
    
    # Put in db
    channel.put()
    
def add_channel_list(channel_list):
    
    for channel_id in channel_list:
        
        # Check if channel exists in db with key
        key = ndb.Key(Channel, channel_id)
        channel = key.get()
        
        if channel:
            # if channel exists
            logging.info('Channel already exists in db - {}'.format(channel_id))
        else:
            # if channel doesn't exist
            logging.info('Adding Channel - {}'.format(channel_id))
            add(channel_id)

        
        
    
        