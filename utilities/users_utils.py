import datetime
import webapp2
import os
import jinja2
from models.channel import Channel
from models.tuberuser import Tuberuser
from google.appengine.ext import ndb
from google.appengine.api import users
import logging

        
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
        
    else:
        logging.info('I should update this user - {}'.format(user_email))


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

        
        
    
        