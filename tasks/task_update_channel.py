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
        
        channel_id = self.request.get('channel_id')

        logging.info('Yolo from task_update_channel - {}'.format(channel_id))


app = webapp2.WSGIApplication([
    ('/task_update_channel', taskUpdateChannel),
], debug=True)



