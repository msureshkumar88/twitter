import webapp2

import logging
from controllers.profile import ProfileController

class ProfileRequest(webapp2.RequestHandler):
    def get(self):
        path = self.request.path
        logging.info(path)
        if path == "/profile":
            ProfileController.show_profile(self)
        elif path in "/delete-tweet":
            ProfileController.delete_tweet(self)
        elif path in "/edit-tweet":
            ProfileController.update_tweet(self,"get")

    def post(self):
        form_name = self.request.get('form')
        if form_name == "save_tweet":
            ProfileController.save_tweet(self)
        elif form_name == "update_tweet":
            ProfileController.update_tweet(self, "post")
        elif form_name == "search_tweet":
            ProfileController.search_tweet(self)
        elif form_name == "search_user":
            ProfileController.search_user(self)
        elif form_name == "update_following_status":
            ProfileController.update_following_status(self)



app = webapp2.WSGIApplication([
    ('/profile', ProfileRequest),
    ('/delete-tweet', ProfileRequest),
    ('/edit-tweet', ProfileRequest)
], debug=True)
