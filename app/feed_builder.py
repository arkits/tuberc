from app import app, db
from app.models import User, Channel 
import ast
import json

def build_feed(sub_chans):

    feed = []

    if sub_chans is not None:

        list_of_subs = ast.literal_eval(sub_chans)

        for sub in list_of_subs:
            q = Channel.query.filter_by(yt_id=sub).first()
            if hasattr(q, 'videos'):
                try:
                    all_videos = ast.literal_eval(q.videos)
                    for videos in all_videos:
                        feed.append(videos['title'])
                except ValueError:
                    print("ValueError Caught at feed_builder.py")

        feed = feed[:10]

    return feed