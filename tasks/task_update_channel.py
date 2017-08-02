import datetime
import webapp2
import os
import re
from google.appengine.api import taskqueue
import jinja2
from models.channel import Channel
from google.appengine.ext import ndb
import logging



class taskUpdateChannel(webapp2.RequestHandler):


    def post(self):

        # Is triggered by a CRON job. Send a POST to EnqueueTaskHandler to the directory update task. 
        # Returns: response (response.status): A value of 204 to indicate success


        logging.info('Yolo from task_update_channel!')




app = webapp2.WSGIApplication([
    ('/task_update_channel', taskUpdateChannel),
], debug=True)



