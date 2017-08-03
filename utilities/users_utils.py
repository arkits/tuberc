import datetime
import webapp2
import os
import jinja2
from models.channel import Channel
from models.tuberuser import Tuberuser
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
from oauth2client.contrib.appengine import OAuth2DecoratorFromClientSecrets
from apiclient.discovery import build
import httplib2
        
def add(user):
    
    user_email = user.email()
    
    user_id = user.user_id()
    
    sub_channels = []
    
    in_the_db = check_by_user_id(user_id)
    
    if not in_the_db:
        
        tuberuser = Tuberuser()
        tuberuser.key = ndb.Key(Tuberuser, user_id)
        tuberuser.user_email = user_email
        tuberuser.user_id = user_id
        tuberuser.add_date = datetime.datetime.now()
        tuberuser.last_update_date = datetime.datetime.now()
        tuberuser.sub_channels = str(sub_channels)
        tuberuser.put()
        
        logging.info('Added to db - {}'.format(user_email))
        
    #else:
        #logging.info('I should update this user - {}'.format(user_email))
        #tuberuser = get_user(user_id)
        #refresh_sub_channels(tuberuser)


def check_by_user_id(user_id):
    
    tuberuser = get_user(user_id)
        
    if tuberuser:
        # if channel exists
        logging.info('Tuberuser already exists in db - {}'.format(user_id))
        return True
    else:
        # if channel doesn't exist
        logging.info('New Tuberuser - {}'.format(user_id))
        return False
    
def get_user(user_id):
    
    key = ndb.Key(Tuberuser, user_id)
    tuberuser = key.get()
    return tuberuser


def refresh_sub_channels(tuberuser):
    
    decorator = OAuth2DecoratorFromClientSecrets(os.path.join(os.path.dirname(__file__), 'tuberc.json'),  'https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/plus.login')
    service = build('youtube', 'v3')    
    
    if decorator.has_credentials():
        
        logging.info('Refreshing sub channels... {}'.format(tuberuser.user_email))   
        
        more = True
        nextPageToken = False    
    
        subs_channel_id = []
    
        while more: 
    
            if nextPageToken:
                subs = service.subscriptions().list(pageToken = nextPageToken, maxResults=50, part='snippet', mine=True).execute(decorator.http())
            else:
                subs = service.subscriptions().list(maxResults=50, part='snippet', mine=True).execute(decorator.http())
    
            items = subs.get('items')
    
            for item in items:
                snippet = item.get('snippet')        
                resourceId = snippet.get('resourceId')
                channelId = resourceId.get('channelId') 
                logging.info('channelId - {}'.format(channelId)) 
                subs_channel_id.append(channelId)
    
            nextPageToken = subs.get('nextPageToken')
    
            if nextPageToken:
                logging.info('Recieved nextPageToken...')
                more = True
            else:
                more = False      
            
        print subs_channel_id
        
    else:
        print 'pls authorizeeee'
            