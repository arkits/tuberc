import datetime
import webapp2
import os
import re
from google.appengine.api import taskqueue
import jinja2
from models.channel import Channel
from google.appengine.ext import ndb
import logging

        
    
class EnqueueTaskHandler(webapp2.RequestHandler):
    
    def post(self, channel_id):
        
        task_response = taskqueue.add(
            queue_name='update-channel',
            url='/task_update_channel',
            params={
            'channel_id':channel_id
            })
        
        return task_response


class updateAllChannels(webapp2.RequestHandler):

    def get(self):
           
        all_channels = Channel.query_all()
        
        for channel in all_channels:
            
            channel_id = channel.channel_id
            logging.info('Queing task a channel update task from updateAllChannels - {}'.format(channel_id))
            handler = EnqueueTaskHandler()
            task_response = handler.post(channel_id)

app = webapp2.WSGIApplication([
    ('/update_all_channels', updateAllChannels),
], debug=True)

        
    
        