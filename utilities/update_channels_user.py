import datetime
import webapp2
import os
import re
from google.appengine.api import taskqueue
import jinja2
from models.channel import Channel
from google.appengine.ext import ndb
import logging
from google.appengine.api import users
from utilities import users_utils
import ast
        
    
class EnqueueTaskHandler(webapp2.RequestHandler):
    
    def post(self, channel_id):
        
        task_response = taskqueue.add(
            queue_name='update-channel',
            url='/task_update_channel',
            params={
            'channel_id':channel_id
            })
        
        return task_response


class updateChannels(webapp2.RequestHandler):

    def get(self):
        
        user = users.get_current_user()
        tuberuser = users_utils.get_user(user.user_id())
        tuberuser_sub_channels = tuberuser.sub_channels
        
        if len(tuberuser_sub_channels) > 2:
        
            tuberuser_sub_channels = ast.literal_eval(tuberuser_sub_channels)        
        
            for channel_id in tuberuser_sub_channels:
                
                logging.info('Queing task a channel update task from updateChannels - {}'.format(channel_id))
                handler = EnqueueTaskHandler()
                task_response = handler.post(channel_id)
                
        self.redirect("/main") 

app = webapp2.WSGIApplication([
    ('/update_channels', updateChannels),
], debug=True)

        
    
        