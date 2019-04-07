from google.appengine.ext import ndb


class Tweet(ndb.Model):
    text = ndb.StringProperty()
    date_added = ndb.DateTimeProperty(auto_now_add=True)
    profile_image = ndb.StringProperty()