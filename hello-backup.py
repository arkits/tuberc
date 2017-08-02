import httplib2
import os
import webapp2
from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.contrib.appengine import OAuth2DecoratorFromClientSecrets
import json
import logging
import time
from datetime import datetime
from dateutil.parser import parse 
from lib import feedparser
import pprint
from operator import itemgetter
import jinja2

decorator = OAuth2DecoratorFromClientSecrets(os.path.join(os.path.dirname(__file__), 'tuberc.json'),  'https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/plus.login')
service = build('youtube', 'v3')

# Set jinja Environment
template_env= jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))


def get_user_info():
    
    request = service.channels().list(mine=True, part='snippet').execute(decorator.http())
    
    items = request.get('items')
    uid = items[0].get('id')

    snippet = items[0].get('snippet')
    title = snippet.get('title')
    description = snippet.get('description')

    thumbnails = snippet.get('thumbnails')
    high = thumbnails.get('high')
    url = high.get('url')

    self.response.write(uid + '<br>')
    self.response.write(str(title) + '<br>')
    self.response.write(str(description) + '<br>')
    self.response.write('<img src="'+ str(url) + '">')    

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

def get_feed(channel_id):
       
    feedurl = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + str(channel_id)
    try:
        d = feedparser.parse(feedurl)
    except Exception as e:
        logging.info('exception caught {}'.format(e))
    

class MainPage(webapp2.RequestHandler):

    @decorator.oauth_aware
    def get(self):

        if decorator.has_credentials():
            
            start = time.time()
           
            #subs_channel_id = get_sub_list()
            
            #subs_channel_id = ["UCxt9Pvye-9x_AIcb1UtmF1Q", "UCdJdEguB1F1CiYe7OEi3SBg", "UCWCw2Sd7RlYJ2yuNVHDWNOA", "UCZDA1kA3y3EIg25BpcHSpwQ", "UCVYamHliCI9rw1tHR1xbkfw", "UC29ju8bIPH5as8OGnQzwJyA", "UCmeds0MLhjfkjD_5acPnFlQ", "UCq6VFHwMzcMXbuKyG7SQYIg", "UCTzLRZUgelatKZ4nyIKcAbg", "UC5I2hjZYiW9gZPVkvzM8_Cw", "UC9PBzalIcEQCsiIkq36PyUA", "UCqg5FCR7NrpvlBWMXdt-5Vg", "UCgc4xqIMDoiP4KOTFS21TJA", "UCSOpcUkE-is7u7c4AkLgqTw", "UCyU5wkjgQYGRB0hIHMwm2Sg", "UCWqr2tH3dPshNhPjV5h1xRw", "UCLx053rWZxCiYWsBETgdKrQ", "UCy1Ms_5qBTawC-k7PVjHXKQ", "UCBE-FO9JUOghSysV9gjTeHw", "UCEOQ9pSmMEIqfhtCDa2JORw", "UCT3dQ11QZIymHGK-HW--4AQ", "UCO_vmeInQm5Z6dEZ6R5Kk0A", "UC1JTQBa5QxZCpXrFSkMxmPw", "UCsvn_Po0SmunchJYOWpOxMg", "UCGzyw0aUIbRPfHR0ThS1nNw", "UCRFJKGSEkgfIyOLYLthuUvQ", "UCL5RKbiAPqSC_mUIjCpx3xg", "UCciKycgzURdymx-GRSY2_dA", "UC1_-cyLlwnmTAesbMgruDpQ", "UCyWDmyZRjrGHeKF-ofFsT5Q", "UCK9_x1DImhU-eolIay5rb2Q", "UCEKJKJ3FO-9SFv5x5BzyxhQ", "UCYZtp0YIxYOipX15v_h_jnA", "UCmWRcMQyU-mGL1VRo2J3FuQ", "UCddiUEpeqJcYeBxX1IVBKvQ", "UC4USoIAL9qcsx5nCZV_QRnA", "UCBJycsmduvYEL83R_U4JriQ", "UC3tNpTOHsTnkmbwztCs30sA", "UC0a8nteER_pU4Aj6hmEyJAQ", "UCDMnCGlkv4gyFGZo_ZT3atg", "UCUQo7nzH1sXVpzL92VesANw", "UCW6J17hZ_Vgr6cQgd_kHt5A", "UCZU9T1ceaOgwfLRq7OKFU4Q", "UCjscRSFwAXMnV7YN3vAR2Gw", "UCI4I6ldZ0jWe7vXpUVeVcpg", "UCftcLVz-jtPXoH3cWUUDwYw", "UCywBfpGBYhsczNuyyh6Cf6w", "UC70UzaroFf5GcyecHOGw-tw", "UC69aRMKDNmaruRhBQ-_wyqw", "UCkK9UDm_ZNrq_rIXCz3xCGA", "UCWEHue8kksIaktO8KTTN_zg", "UCOmcA3f_RrH6b9NmcNa4tdg", "UCUqZE3MpxMYKrfgvZ2qzsOw", "UCR0AnNR7sViH3TWMJl5jyxw", "UCYLS9TSah19IsB8yyUpiDzg", "UC9-EE_9NTDDW0lHad0YOlzQ", "UCYo4DGKIw8UmIQXbTuP3JsQ", "UChDt9wwsqoUkwJasyThkltA", "UC-kFCSJLpxuJdgMnQz8Dvrg", "UCPq2ETz4aAGo2Z-8JisDPIA", "UCo1pShh6dtg-T_ZZkgi_JDQ", "UCbR6jJpva9VIIAHTse4C3hw", "UC7dLvCYNwhYe-l__yczFp1Q", "UC3KEoMzNz8eYnwBC34RaKCQ", "UCI8iQa1hv7oV_Z8D35vVuSg", "UCK8sQmJBp8GCxrOtXWBpyEA", "UC5EGDYNWY93RTbg1jM4AqrQ", "UCzuKOJtTTVCxWgi1SM8Kg6g", "UCAL3JXZSzSm8AlZyD3nQdBA", "UCqbkm47qBxDj-P3lI9voIAw", "UCmxCoyvGU3IndS7bm9oH3Vg", "UCV5vRGJYbGN6TL8245QeHOg", "UCk1SpWNzOs4MYmr0uICEntg", "UCmu9PVIZBk-ZCi-Sk2F2utA", "UCTpiViBtYwttoTgFcq7J_Gw", "UC4w1YQAJMWOz4qtxinq55LQ", "UCiDJtJKMICpb9B1qf7qjEOA", "UCWk67Dk9uuQ7Ciyofn3hFIA", "UC6LGwT2pquVsUqlB_0IODwA", "UCJHA_jMfCvEnv-3kRjTCQXw", "UC1iLiyUKILlwgEXpdX3iN3A", "UCObgw7K0mzkxaNroxQpKSDg", "UCcck1Zdvdt5aML_O32Y_Adg", "UCPKbW1excf-E7Tmwom1AgkQ", "UC_ufxdQbKBrrMOiZ4LzrUyA", "UCVHFbqXqoYvEWM1Ddxl0QDg", "UCoDcFZ5KZ0KwBC_omalJuiA", "UCjYO25ZVJT523TD1iYHzcbw", "UCMyAVYPgP_179gj9OIJZd4A", "UCoWQja39K17_g8IimjThyLw", "UCustbySVJGb659WDpdkeATg", "UCtT2VnurQKOAA0I1EKKHSPA", "UCL8ZULXASCc1I_oaOT0NaOQ", "UCCDU1fsmgvWljcW2aodfJsA", "UCMuAor3dRed_IyrkKGzQ69Q", "UCsgv2QHkT2ljEixyulzOnUQ", "UCrI6_31b1OHRE62BHTMYN0Q", "UCTGBHncizmXKmgvwwLh8UlQ", "UCI-J59FK1a_ZKG0zNdz4vwg", "UCf4AIjSwE-E2TggCPdm-z-A", "UC9M7-jzdU8CVrQo1JwmIdWA", "UCNJcSUSzUeFm8W9P7UUlSeQ", "UCOWcZ6Wicl-1N34H0zZe38w", "UCxzC4EngIsMrPmbm6Nxvb-A", "UCqyKIlKKfFGy6AraaqAGlHA", "UCwwByLVM8DlwWQjA0zqeLYA", "UCqZ0rqkoUeYlcxlUyqSgpdg", "UCKqBXgfVRwWSDwUH_0hA2RA", "UCE1jXbVAGJQEORz9nZqb5bQ", "UCIiSwcm9xiFb3Y4wjzR41eQ", "UCjlLpF_NT7hoNYANSYRW1bQ", "UCipr-y52SQGyMX-CQ2xk3jA", "UC23BTpUPTQDkLsq6cvQBxHg", "UCYYwbzPf-IbhXf8p3MuQUVA", "UCFHMw64uu66VKPXq5gh29IQ", "UCPze-Hckg3ayKQHZS706R0A", "UCJyiQDkCGBSJYZQ-OAjLteA", "UCpdrY4TWv2GhlCNjiATkugg", "UCdVrPfq-B9N5v01axUoDfLA", "UCPtEVCTHvPxE8i8cIirX94g", "UCUjlPym2cxucUVPdE8kYOOg", "UCtjAhxsnkqA5O49D2mIwh3w", "UCB2527zGV3A0Km_quJiUaeQ", "UCJbPGzawDH1njbqV-D5HqKw", "UC7-930jaPqjKMJBTZyZLhpg", "UCfWjSnAyN6Ju8wyJdycfNKw", "UCsZ15lJ_N_hOhCrxteBZd6w", "UCVHdvAX5-R8y5l9xp6nroBQ", "UCNQ04hTmvzi3gsx0fF4b2cg", "UCijqQw0K-5ldR0MSGLUPdCQ", "UCMpqW1IPGv0g6rydrFQhMCA", "UCjKIPQOlTASJrIWQ9H-i5mA", "UCwRXb5dUK4cvsHbx-rGzSgw", "UCLxT-YVIAR4F3dRHped9Dkg", "UCVL4dCfdQyTlCBQPsS8l9Wg", "UChTNW5PPFuhNeieGJAvLKpA", "UCTcraSQKl7F8GFiLydv6eDg", "UC7V6hW6xqPAiUfataAZZtWA", "UC1Un5592U9mFx5n6j2HyXow", "UCoVwq0vh-XD8RrEyDZ0KeJw", "UC3XTzVzaHQEd30rQbuvCtTQ", "UCQD3awTLw9i8Xzh85FKsuJA", "UCYbK_tjZ2OrIZFBvU6CCMiA", "UCMeZ9Zwz5tWw9_kaZzzjZ5w", "UCB4dWKbwgl3U3ohBmrT7k3w", "UCg44zX42-GjMr5XqyK3RmsQ", "UC0fDG3byEcMtbOqPMymDNbw", "UCjF6nB_yMSZfG_vY06cVkrQ", "UCxqyBoACUss6OxFdmFvxcXQ", "UCDxRn03fR0V8M7lms_YYXOQ", "UCUnjDt3PO4OTCwQFW3N4aIQ", "UCj22tfcQrWG7EMEKS0qLeEg", "UCKbM0nOIaBgT9r0EKByiH9w", "UCQkd05iAYed2-LOmhjzDG6g", "UCYu0one5cfSaSEeviSVDjJw", "UCQlC9iwSZ2a0-96RLleG_xg", "UC1RNLY3PApEmNBpy9oCz9Dg", "UC7eHZXheF8nVOfwB2PEslMw", "UCT6LaAC9VckZYJUzutUW3PQ", "UC0GpFqMHMKQKntY6KP_BHEg", "UCneuxGi0TQd66n1ZenHp7Yw", "UCvHzs2C_iK8VLV41JgQPyug", "UCqSHAXN5sqtyE93A-w-8Ddw", "UCekQr9znsk2vWxBo3YiLq2w", "UC_c1gdsojLxBGkgzS0NsvUw", "UCocfdCiKujljqcGC-STMsCQ", "UCLXBISkERJy5VuZmRGOiv5Q", "UChORY56LMMETTuGjXaJXvLg", "UCir4goG7LBQCh5rc3frkHuA", "UCvWWf-LYjaujE50iYai8WgQ", "UCEPTp5WMAzjh9mOrKUwRLmQ", "UCd6EFsVsqGhASiz6g1KifUQ", "UCpFcHE36IoySjYj1Rytxyog", "UCS5tt2z_DFvG7-39J3aE-bQ", "UCoeAaUE-_t89BHuXjnfwykw", "UCNu61DlWxat2deDH3c0Y2nw", "UC6lUqvh42Oc3XL19Edgd9QA", "UCwHrYi0GL6dmYaRB0StEbEA", "UC7oE82gmo-TwM5WiDzIuhhQ", "UC9-y-6csu5WGm29I7JiwpnA", "UCeR0n8d3ShTn_yrMhpwyE1Q", "UCFfCqe7b9YiDk2ZiAG8UIGA", "UCDd17vMimN72DFOFR4jFCQw", "UCnIQPPwWpO_EFEqLny6TFTw", "UC_IH3nyZEJgzaXbXa6kSCdQ", "UCAwv_EtbjgwQwezrS4z9WMQ", "UCmNzgJJjGo5mleo62q8daJA", "UCzybXLxv08IApdjdN0mJhEg", "UCwK6hu9UL4R0HvxdT8JV4XQ", "UCDtH9xTCEPzpR_FJiuZ-hFQ", "UC8Wh7qpPGJm3K1eZ6DHjpKA", "UCfeeUuW7edMxF3M_cyxGT8Q", "UCIquhTRs7QJrzCfiAMwfV8w", "UCsJBJmhRP-GxuGsePpnNtIw", "UCgG3Nvp86j1WaHaLwjoVJZg", "UCqKDAO0u1vSUFc_QIQ1H-9Q", "UCZxOEoO7GKlAqRJJl3bGxag", "UCpjEsqMfepOyAkyPi_t_hgg", "UCVSOQB85UweMsgCa8BOh0IQ", "UCT31um1Ic8KweVWEMBC1K7A", "UC8N4qh2WGAN6kc75rUmY_Tw", "UCUv0uGHoWT7IIHi4NljKDYg", "UCyF-6wI0EoKAe7nZqlIOrOA", "UC6VcWc1rAoWdBCM0JxrRQ3A", "UCg0FSqPeiGD_lIiPaaAehQg", "UCEv-b-LezyQ6QZ8brh4QZQg", "UCrsECiuZUe7HObWu7UF--5A"]
            
            subs_channel_id = ["UCxt9Pvye-9x_AIcb1UtmF1Q", "UCdJdEguB1F1CiYe7OEi3SBg", "UCWCw2Sd7RlYJ2yuNVHDWNOA", "UCZDA1kA3y3EIg25BpcHSpwQ"]
            
            subs_videos = []
                       
            for channel_id in subs_channel_id:
                
                feedurl = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + str(channel_id)
                
                logging.info('feedurl - {}'.format(feedurl)) 
                
                try:
                    d = feedparser.parse(feedurl)
                    
                    for post in d.entries:

                        video = {}
                        
                        video['title'] = post.title
                        video['link'] = post.link
                        video['author'] = d.feed.title
                        
                        post_date = parse(post.published)
                        post_date = post_date.strftime('%Y-%m-%d %H:%M:%S')
                        video['post_date'] = post_date
                        
                        subs_videos.append(video)

                except Exception as e:
                    logging.info('exception caught {}'.format(e))
                    
            
            
            ordered_subs_video = sorted(subs_videos, key=itemgetter('post_date') , reverse=True) 
            
            dump = ordered_subs_video
            dump = pprint.pformat(dump, indent=4)
        
        
        
            template = template_env.get_template('/www/index.html')
            
            content = {
            'dump':dump
            }
            
            self.response.out.write(template.render(content)) 
            
            print "Elapsed Time: %s" % (time.time() - start)
            
    
                             
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

routes = [('/', MainPage),  (decorator.callback_path, decorator.callback_handler())]

app = webapp2.WSGIApplication(routes, debug=True)
