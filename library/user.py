from google.appengine.api import users
from google.appengine.ext import ndb
from models.user import User
import re
from datetime import datetime

import logging

class UserLibrary:
    @classmethod
    def get_user(cls, request):

        user = users.get_current_user()
        url = ''
        url_string = ''
        myuser = None
        user_key = ""
        if user:
            url = users.create_logout_url("/")
            url_string = 'Logout'
            myuser_key = ndb.Key('User', user.email())
            myuser = myuser_key.get()
            user_key = user.user_id()
            if myuser == None:
                myuser = User(id=user.email(), email=user.email())
                myuser.put()
        else:
            url = users.create_login_url("/")
            url_string = 'Login'

        data = {
            'url': url,
            'url_string': url_string,
            'user': myuser,
            'user_id':user_key
        }
        return data

    @classmethod
    def get_current_user(cls):
        return users.get_current_user()

    @classmethod
    def get_logged_user(cls):
        user = users.get_current_user()
        user_key = ndb.Key('User', user.email())
        return user_key.get()

    @classmethod
    def validate_username(cls, word):
        word = word.strip()
        return re.search('^[a-zA-Z0-9]+$', word)

    @classmethod
    def update_username(cls, req):
        msg = ""
        user_name = req.request.get("username")
        first_name = req.request.get("first_name")
        last_name = req.request.get("last_name")
        bio = req.request.get("bio")

        if not UserLibrary.validate_username(user_name):
            return {"status": False, "message":"Username can only be alphabetic and numeric"}

        if len(bio) > 280:
            return {"status": False, "message": "Only 280 characters allowed"}

        query = User.query(User.user_name == user_name)
        username_exist = query.fetch()

        if username_exist:
            return {"status": False, "message": "Username already taken"}

        if not msg:
            user_key = ndb.Key('User', UserLibrary.get_current_user().email())
            user = user_key.get()
            user.user_name = user_name
            user.first_name = first_name
            user.last_name = last_name
            user.bio = bio
            user.put()
            return {"status": True, "message": "Profile updated successfully"}
        return msg

    @classmethod
    def get_user_by_username(cls, username):
        user = User.query(User.user_name == username).fetch()
        if user:
            return user[0]
        return None

    @classmethod
    def format_time(cls, time):
        datetime_object = time.strftime('%Y-%m-%d %H:%M:%S')
        return datetime_object
