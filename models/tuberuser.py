# -*- coding: UTF-8 -*-

# Module:     User

# Synopsis:   This module describes and sets behavior for the User objects.


from google.appengine.ext import ndb


class Tuberuser(ndb.Model):

    # General Info
    user_id = ndb.StringProperty()
    user_email = ndb.StringProperty()
    last_request_date = ndb.DateTimeProperty(auto_now_add=True)
    add_date = ndb.DateTimeProperty(auto_now_add=True)
    # Channels
    sub_channels = ndb.TextProperty()    
    
    @classmethod
    def query_all(cls):

        query_result = cls.query().order(-cls.last_request_date)

        return query_result

    @classmethod
    def delete_all(cls):

        ndb.delete_multi(
            cls.query().fetch(keys_only=True)
        )

