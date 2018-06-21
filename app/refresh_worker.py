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