import logging
import re
from library.user import UserLibrary
from models.tweet import Tweet
from google.appengine.ext import ndb
import datetime
import time


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
    def save_tweet(cls, text):
        user = UserLibrary.get_logged_user()
        tweet = Tweet(id=AccountHelper.get_tweet_key(), text=text, user_email=user.email)
        tweet.put()

        user_key = ndb.Key('User', user.email)
        user_record = user_key.get()
        user_record.tweet_count = user_record.tweet_count + 1
        user_record.put()

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
        if params:
            user = AccountHelper.in_other_profile(params)
        else:
            user = UserLibrary.get_logged_user()
        return Tweet.query(Tweet.user_email == user.email).fetch()

    @classmethod
    def delete_tweet(cls, id):
        user = UserLibrary.get_logged_user()
        key = ndb.Key('Tweet', AccountHelper.get_tweet_key_by_id(id))
        tweet = key.get()
        if tweet:
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




