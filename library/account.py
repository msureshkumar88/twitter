import logging
import re
from library.user import UserLibrary
from models.tweet import Tweet
from models.user import User
from google.appengine.ext import ndb
import datetime
import time
from google.appengine.api import search
from google.appengine.api import images
from google.appengine.ext import blobstore
class AccountHelper:
    @classmethod
    def update_profile(cls, request_data):
        first_name = request_data["first_name"]
        last_name = request_data["last_name"]
        dob = request_data["dob"]
        if dob:
            dob = datetime.datetime.strptime(request_data["dob"], '%Y-%m-%d')
        else:
            dob = None
        city = request_data["city"]
        website = request_data["website"]
        bio = request_data["bio"]

        user_key = ndb.Key('User', UserLibrary.get_current_user().email())
        user = user_key.get()
        user.first_name = first_name
        user.last_name = last_name
        user.dob = dob
        user.city = city
        user.website = website
        user.bio = bio
        user.put()

    @classmethod
    def get_profile(cls):
        user_key = ndb.Key('User', UserLibrary.get_current_user().email())
        return user_key.get()

    @classmethod
    def validate_tweet(cls):
        pass

    @classmethod
    def save_tweet(cls, request):
        text = request.request.get("tweet")
        file = request.get_uploads()
        if len(text) == 0:
            return {"status": False, "message": "Tweet field cannot be empty"}
        if len(text)> 280:
            return {"status":False,"message":"Tweet field character limit exceeded, only 280 allowed"}

        upload = None
        if file:
            upload = file[0].key()
            info = blobstore.BlobReader(upload)
            if info.blob_info.content_type not in ['image/jpeg','image/png']:
                blobstore.delete(upload)
                return {"status": True, "message": "Only png PNG and JPEG can be uploaded"}

        user = UserLibrary.get_logged_user()
        tweet = Tweet(id=AccountHelper.get_tweet_key(), text=text, user_email=user.email, user_name = user.user_name, image=upload)
        tweet.put()

        user_key = ndb.Key('User', user.email)
        user_record = user_key.get()
        user_record.tweet_count = user_record.tweet_count + 1
        user_record.put()

        d = search.Document(
            doc_id=AccountHelper.get_tweet_key(),
            fields=[search.TextField(name='tweet', value=text),
                    search.TextField(name='user_name', value=user.user_name)],
            language='en')

        add_result = search.Index(name='tweet').put(d)
        return {"status": True, "message": "Tweet saved successfully"}

    @classmethod
    def get_tweet_key(cls):
        ts = time.time()
        user = UserLibrary.get_logged_user()
        return user.email + '/' + str(int(ts))

    @classmethod
    def get_tweet_key_by_id(cls, id):
        user = UserLibrary.get_logged_user()
        return user.email + '/' + str(id)

    @classmethod
    def get_tweets_by_user(cls, params=None):
        user = None
        tweet = []
        if 'user' in params:
            user = AccountHelper.in_other_profile(params)
            tweet = Tweet.query(Tweet.user_email == user.email).order(-Tweet.date_added).fetch(50)
        else:
            user = UserLibrary.get_logged_user()
            user.following.append(user.user_name)
            tweet = Tweet.query(Tweet.user_name.IN(user.following)).order(-Tweet.date_added).fetch(50)
        return tweet

    @classmethod
    def delete_tweet(cls, id):
        user = UserLibrary.get_logged_user()
        key = ndb.Key('Tweet', AccountHelper.get_tweet_key_by_id(id))
        tweet = key.get()
        if tweet:
            blobstore.delete(tweet.image)
            key.delete()

            user_key = ndb.Key('User', user.email)
            user_record = user_key.get()
            user_record.tweet_count = user_record.tweet_count - 1
            user_record.put()
            return True
        return False

    @classmethod
    def get_tweet_by_id(cls, id):
        key = ndb.Key('Tweet', AccountHelper.get_tweet_key_by_id(id))
        tweet = key.get()
        if tweet:
            return tweet
        return None

    @classmethod
    def update_tweet(cls, id, text):
        key = ndb.Key('Tweet', AccountHelper.get_tweet_key_by_id(id))
        tweet = key.get()
        if tweet:
            tweet.text = text
            tweet.put()
            return True
        return False

    @classmethod
    def in_other_profile(cls, params):
        if 'user' in params:
            user = UserLibrary.get_user_by_username(params["user"])
            if user:
                return user
        return None

    @classmethod
    def get_profile_data(cls, params=None):
        user = UserLibrary.get_logged_user()
        if 'user' in params:
            user = UserLibrary.get_user_by_username(params["user"])
        return user

    @classmethod
    def get_follow_status(cls, username):
        user = UserLibrary.get_logged_user()
        result = User.query(User.user_name == user.user_name, User.following == username).fetch()
        if result:
            return True
        return False

    @classmethod
    def get_following_text(cls, username):
        text = "Follow"
        if AccountHelper.get_follow_status(username):
            text = "Unfollow"
        return text

    @classmethod
    def change_following_status(cls,status,user):
        if status == "Follow":
            current_user = UserLibrary.get_logged_user()
            current_user.following_count = current_user.following_count + 1
            current_user.following.append(user)
            current_user.put()

            following_user = UserLibrary.get_user_by_username(user)
            following_user.follows_count = following_user.follows_count + 1
            following_user.follows.append(current_user.user_name)
            following_user.put()
        else:
            current_user = UserLibrary.get_logged_user()
            current_user.following_count = current_user.following_count - 1
            current_user.following.remove(user)
            current_user.put()

            following_user = UserLibrary.get_user_by_username(user)
            following_user.follows_count = following_user.follows_count - 1
            following_user.follows.remove(current_user.user_name)
            following_user.put()

    @classmethod
    def search_by_username(cls, params):

        if params and "username" in params:
            if len(params['username'])==0:
                return {"status": False, "message":"Please enter search value", "data" : None}
            user = User.query(User.user_name == params['username']).fetch()
            if user:
                return {"status": True, "message":"", "data" : user[0]}
            return {"status": False, "message": "User not found", "data": None}

    @classmethod
    def search_tweet(cls, params):
        if params and "text" in params:
            index = search.Index('tweet')
            text = params['text'].lower().rstrip()
            if len(text) == 0:
                return []
            search_query = search.Query(query_string=text)
            search_results = index.search(search_query)
            tweets = []
            for doc in search_results:
                tweets.append(AccountHelper.get_tweet_by_id(doc.doc_id))

            return tweets

    @classmethod
    def get_tweet_by_id(cls, id):
        key = ndb.Key('Tweet', id)
        return key.get()



