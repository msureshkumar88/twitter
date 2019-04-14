from google.appengine.ext import ndb


class Tweet(ndb.Model):
    text = ndb.StringProperty()
    date_added = ndb.DateTimeProperty(auto_now_add=True)
    image = ndb.BlobKeyProperty()
    user_email = ndb.StringProperty()
    user_name = ndb.StringProperty()