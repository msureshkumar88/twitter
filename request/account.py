import webapp2

import logging
from controllers.account import AccountController

class AccountRequest(webapp2.RequestHandler):
    def get(self):
        path = self.request.path
        if path == "/edit-profile":
            AccountController.update_profile_get(self)

    def post(self):
        path = self.request.path
        if path == "/edit-profile":
            AccountController.update_profile_post(self)


app = webapp2.WSGIApplication([
    ('/edit-profile', AccountRequest),
], debug=True)
