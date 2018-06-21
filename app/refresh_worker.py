import ast
from app import app, db
from app.models import User, Channel 
import threading
import time
import feedparser
from dateutil.parser import parse 

def refresh(sub_chans):

    start = time.time()

    list_of_subs = ast.literal_eval(sub_chans)

    for sub in list_of_subs:
        q = Channel.query.filter_by(yt_id=sub).first()
        if q is None:
            c = Channel(
                yt_id = sub
            )
            db.session.add(c)
            db.session.commit()
        else:
            print ("I got it!")
    
    pf = PullFeeds(list_of_subs)
    pf.startThreadingFeeds()
            
    print ("Elapsed Time: %s" % (time.time() - start))


class PullFeeds:
    def __init__(self, channel_ids):
        # channel_ids = [u'UCJ0-OtVpF0wOKEqT2Z1HEtA', u'UC4rqhyiTs7XyuODcECvuiiQ', u'UC5I2hjZYiW9gZPVkvzM8_Cw', u'UCBa659QWEk1AI4Tg--mrJ2A', u'UCDWIvJwLJsE4LG1Atne2blQ', u'UCK9_x1DImhU-eolIay5rb2Q', u'UCmeds0MLhjfkjD_5acPnFlQ', u'UClcE-kVhqyiHCcjYwcpfj9w', u'UCgc4xqIMDoiP4KOTFS21TJA', u'UCtM5z2gkrGRuWd0JQMx76qA', u'UCLx053rWZxCiYWsBETgdKrQ', u'UCciKycgzURdymx-GRSY2_dA', u'UC4USoIAL9qcsx5nCZV_QRnA', u'UCsvn_Po0SmunchJYOWpOxMg', u'UCxt9Pvye-9x_AIcb1UtmF1Q', u'UCmYBTQilY7p8EQ9IsyA3oLw', u'UCWCw2Sd7RlYJ2yuNVHDWNOA', u'UCq6VFHwMzcMXbuKyG7SQYIg', u'UCPhVxopWpXWy-qHMXRVPLEQ', u'UCJHA_jMfCvEnv-3kRjTCQXw', u'UCV5vRGJYbGN6TL8245QeHOg', u'UCSOpcUkE-is7u7c4AkLgqTw', u'UC4w1YQAJMWOz4qtxinq55LQ', u'UCWqr2tH3dPshNhPjV5h1xRw', u'UCqg5FCR7NrpvlBWMXdt-5Vg', u'UCywBfpGBYhsczNuyyh6Cf6w', u'UCyWDmyZRjrGHeKF-ofFsT5Q', u'UCxzC4EngIsMrPmbm6Nxvb-A', u'UCB2527zGV3A0Km_quJiUaeQ', u'UC9PBzalIcEQCsiIkq36PyUA', u'UCTzLRZUgelatKZ4nyIKcAbg', u'UCddiUEpeqJcYeBxX1IVBKvQ', u'UCYo4DGKIw8UmIQXbTuP3JsQ', u'UC9-y-6csu5WGm29I7JiwpnA', u'UCmu9PVIZBk-ZCi-Sk2F2utA', u'UC3KEoMzNz8eYnwBC34RaKCQ', u'UCyU5wkjgQYGRB0hIHMwm2Sg', u'UCBJycsmduvYEL83R_U4JriQ', u'UCvWWf-LYjaujE50iYai8WgQ' ]

        feedurls = []
        for channel_id in channel_ids:
            feedurls.append("https://www.youtube.com/feeds/videos.xml?channel_id=" + str(channel_id))
        self.data = feedurls

    def startThreadingFeeds(self):
        threads = []
        for url in self.data:
             t = RssParser(url)
             threads.append(t)
        for thread in threads:
             thread.start()
        for thread in threads:
             thread.join()

class RssParser(threading.Thread):
     def __init__(self, url):
         threading.Thread.__init__(self)
         self.url = url

     def run(self):
         d = feedparser.parse(self.url)
         if 'title' in d.feed:
            channel_name = d.feed.title
            channel_id = d.feed.yt_channelid
            videos = []
            for post in d.entries:
                video = {}
                video['title'] = post.title
                video['link'] = post.link
                video['author'] = d.feed.title
                video['videoid'] = post.yt_videoid
                post_date = parse(post.published)
                post_date = post_date.strftime('%Y-%m-%d %H:%M:%S')
                video['post_date'] = post_date
                videos.append(video)
            
            c = Channel.query.filter_by(yt_id=channel_id).first()
            c.name = channel_name
            c.videos = str(videos)
            db.session.add(c)
            db.session.commit()

            print ("Done! " + channel_name + "\n")