import httplib2
import os
import webapp2
import jinja2
from datetime import datetime
from dateutil.parser import parse 
from apiclient.discovery import build
from oauth2client.contrib.appengine import OAuth2DecoratorFromClientSecrets
from google.appengine.api import users
from utilities import users_utils
import logging
import time
import create_feed
import ast
import urllib

decorator = OAuth2DecoratorFromClientSecrets(os.path.join(os.path.dirname(__file__), 'tuberc.json'),  'https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/plus.login')
service = build('youtube', 'v3')

# Set jinja Environment
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))


def urlsafe(data):
    safe = urllib.quote_plus(data)
    return safe
    
    
template_env.filters['urlsafe'] = urlsafe


class CategoryList(webapp2.RequestHandler):

    @decorator.oauth_aware
    def get(self):

        if decorator.has_credentials():      
            
            start = time.time()
            
            user = users.get_current_user()
            users_utils.add(user)
            
            tuberuser = users_utils.get_user(user.user_id())
            tuberuser_email = tuberuser.user_email
            tuberuser_sub_channels = tuberuser.sub_channels
            
            if len(tuberuser_sub_channels) > 2:
                
                tuberuser_sub_channels = ast.literal_eval(tuberuser_sub_channels)
            
                dump = create_feed.user_categories_list(tuberuser_sub_channels)

                template = template_env.get_template('/www/category_list.html')

                content = {
                    'dump' : dump,
                    'tuberuser_email' : tuberuser_email,
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

routes = [('/category_list', CategoryList),  (decorator.callback_path, decorator.callback_handler())]

app = webapp2.WSGIApplication(routes, debug=True)