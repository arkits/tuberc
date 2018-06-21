from app import app, db
from app.models import User, Channel 
import ast
import json

def build_feed(sub_chans):

    list_of_subs = ast.literal_eval(sub_chans)
    
    feed = []

    for sub in list_of_subs:
        q = Channel.query.filter_by(yt_id=sub).first()
        if q is not None:
            all_videos = ast.literal_eval(q.videos)
            for videos in all_videos:
                feed.append(videos['title'])

    return feed