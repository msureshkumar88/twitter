import logging
import re
from library.user import UserLibrary
from google.appengine.ext import ndb
import datetime

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
