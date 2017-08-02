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
    
    @classmethod
    def query_all(cls):
        
        """
        Queries the Channel Datastore table and returns a list of all the users.

        Args:
            cls (Channel):          Class that will be queried.

        Returns:
            query_result (list):    List of the Channel found.
        """
        
        query_result = cls.query().order(-cls.last_update_date)

        return query_result    
