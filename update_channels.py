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
    
    def post(self):

        # Receives a POST from DirectoryUpdateStarter class.
        # Adds a task to the taskqueue begin the directory update process. Triggers /directory_update
        # Returns a task_response (json):
                
        # Create a task to initiate the directory_update
        
        task_response = taskqueue.add(
            queue_name='update-channel',
            url='/task_update_channel',
            params={})
        
        return task_response


class updateAllChannels(webapp2.RequestHandler):

    
    def get(self):
        
        # Is triggered by a CRON job. Send a POST to EnqueueTaskHandler to the directory update task. 
        # Returns: response (response.status): A value of 204 to indicate success
           
        
        logging.info('Queing task a channel update task from updateAllChannels')
        
        handler = EnqueueTaskHandler()
        task_response = handler.post()
        

app = webapp2.WSGIApplication([
    ('/update_all_channels', updateAllChannels),
], debug=True)

        
    
        