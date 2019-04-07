from google.appengine.api import users
from google.appengine.ext import ndb
from models.user import User

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
            url = users.create_logout_url(request.request.uri)
            url_string = 'Logout'
            myuser_key = ndb.Key('User', user.email())
            myuser = myuser_key.get()
            user_key = user.user_id()
            if myuser == None:
                myuser = User(id=user.email(), email=user.email())
                myuser.put()
        else:
            url = users.create_login_url(request.request.uri)
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
