import httplib2
import os
import webapp2
from apiclient.discovery import build
from oauth2client.contrib.appengine import OAuth2DecoratorFromClientSecrets
import json
import logging
import jinja2
from google.appengine.api import users
from utilities import users_utils
from utilities import add_channel
import datetime

decorator = OAuth2DecoratorFromClientSecrets(os.path.join(os.path.dirname(__file__), 'tuberc.json'),  'https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/plus.login')
service = build('youtube', 'v3')

# Set jinja Environment
template_env= jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))



def get_sub_list():
    
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
    
    return subs_channel_id


class refreshSubs(webapp2.RequestHandler):

    @decorator.oauth_aware
    def get(self):

        if decorator.has_credentials():
            
            user = users.get_current_user()
            
            try:
                subs_channel_list = get_sub_list()
                tuberuser = users_utils.get_user(user.user_id())
                tuberuser.sub_channels = str(subs_channel_list)
                tuberuser.last_update_date = datetime.datetime.now()
                tuberuser.put()
                
                add_channel.add_channel_list(subs_channel_list)
                self.redirect("/main")                
            except:
                # Get URL
                url = decorator.authorize_url()
                self.redirect(url)   

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

routes = [('/refresh_subs', refreshSubs),  (decorator.callback_path, decorator.callback_handler())]
app = webapp2.WSGIApplication(routes, debug=True)
