# -*- coding: UTF-8 -*-
# Module:     Channel
# Synopsis:   This module describes and sets behavior for the Channel object.


from google.appengine.ext import ndb


class Channel(ndb.Model):
    
    # Decriptive Info
    channel_id = ndb.StringProperty()
    channel_name = ndb.StringProperty()
    channel_link = ndb.StringProperty()
    
    # Housekeeping Info
    last_update_date = ndb.DateTimeProperty(auto_now_add=True)
    
    # Videos
    videos = ndb.TextProperty()
