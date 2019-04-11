import webapp2

import logging
from controllers.profile import ProfileController

class ProfileRequest(webapp2.RequestHandler):
    def get(self):
        path = self.request.path
        if path == "/profile":
            AccountController.update_profile_get(self)

    def post(self):
        form_name = self.request.get('form')
        if form_name == "save_tweet":
            ProfileController.save_tweet(self)
        elif form_name == "update_tweet":
            ProfileController.update_tweet(self)
        elif form_name == "delete_tweet":
            ProfileController.delete_tweet(self)
        elif form_name == "search_tweet":
            ProfileController.search_tweet(self)
        elif form_name == "search_user":
            ProfileController.search_user(self)
        elif form_name == "update_following_status":
            ProfileController.update_following_status(self)



app = webapp2.WSGIApplication([
    ('/profile', ProfileRequest),
], debug=True)
