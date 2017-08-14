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

decorator = OAuth2DecoratorFromClientSecrets(os.path.join(os.path.dirname(__file__), 'tuberc.json'),  'https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/plus.login')
service = build('youtube', 'v3')

# Set jinja Environmen
template_env= jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))


def pretty_date(data):
    
    time = parse(data)
    
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"


template_env.filters['pretty_date'] = pretty_date
    

class MainPage(webapp2.RequestHandler):

    @decorator.oauth_aware
    def get(self):

        if decorator.has_credentials():
            
            page = self.request.get('page')
            
            show_back = False
            back_page = None 
            
            if page == '':
                page = 1
            else:
                page = int(page)
                
            start = time.time()

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
                    
                
            
                template = template_env.get_template('/www/main.html')

                content = {
                    'dump' : dump,
                    'number_of_vids' : number_of_vids, 
                    'tuberuser_email' : tuberuser_email,
                    'show_next' : show_next,
                    'show_back' : show_back,
                    'next_page' : next_page,
                    'back_page' : back_page
                }
            
                self.response.out.write(template.render(content)) 
                
            else:
                
                template = template_env.get_template('/www/no_subs.html')
                self.response.out.write(template.render())
            
            elapsed_time = (time.time() - start)
            logging.info('Elapsed Time - {}'.format(elapsed_time))

        else:
            
            # Get URL
            url = decorator.authorize_url()
            
            # Set the template
            template = template_env.get_template('/www/login.html')
            
            # Setup Content
            content = {
                'url':url
                }
            
            # Render
            self.response.out.write(template.render(content)) 

routes = [('/main', MainPage),  (decorator.callback_path, decorator.callback_handler())]

app = webapp2.WSGIApplication(routes, debug=True)
