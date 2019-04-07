from google.appengine.ext import ndb


class User(ndb.Model):
    email = ndb.StringProperty()
    user_name = ndb.StringProperty()
    following = ndb.StringProperty(repeated=True)
    follows = ndb.StringProperty(repeated=True)
    following_count = ndb.IntegerProperty(default=0)
    follows_count = ndb.IntegerProperty(default=0)
    joined = ndb.DateTimeProperty(auto_now_add=True)
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    dob = ndb.DateProperty()
    city = ndb.StringProperty()
    website = ndb.StringProperty()
    bio = ndb.StringProperty()
    tweet_count = ndb.IntegerProperty()
    profile_image = ndb.IntegerProperty()