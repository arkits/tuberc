import httplib2
import os
import webapp2
from apiclient.discovery import build
from oauth2client.contrib.appengine import OAuth2DecoratorFromClientSecrets
import json
import logging
import time
from datetime import datetime
from dateutil.parser import parse 
import pprint
import jinja2
from google.appengine.api import users
import create_feed
from utilities import users_utils
import ast
from utilities import add_channel


class Home(webapp2.RequestHandler):

    def get(self):
        
        page = self.request.get('page')
        
        show_back = False
        back_page = None 
        
        if page == '':
            page = 1
        else:
            page = int(page)        
        
        user = users.get_current_user()
        users_utils.add(user)
        
        tuberuser = users_utils.get_user(user.user_id())
        tuberuser_email = tuberuser.user_email
        tuberuser_sub_channels = tuberuser.sub_channels
        
        if len(tuberuser_sub_channels) > 2:
        
            tuberuser_sub_channels = ast.literal_eval(tuberuser_sub_channels)
        
            feed, number_of_vids = create_feed.post(tuberuser_sub_channels, page)
        
            dump = feed
            
            max_page = page * 20
            
            if max_page <= number_of_vids:
                show_next = True
                next_page = str(page + 1)
            else:
                show_next = False
                next_page = None
                
            if page > 1 :
                show_back = True
                back_page = str(page - 1)                    
            

            content = {
                'dump' : dump,
                'number_of_vids' : number_of_vids, 
                'tuberuser_email' : tuberuser_email,
                'show_next' : show_next,
                'show_back' : show_back,
                'next_page' : next_page,
                'back_page' : back_page
            }
            
            content = json.dumps(content)
            
            self.response.headers['Content-Type'] = 'application/json'   
            self.response.out.write(content)             



routes = [('/api/home', Home)]
app = webapp2.WSGIApplication(routes, debug=True)
