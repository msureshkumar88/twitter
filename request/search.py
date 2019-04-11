import webapp2

import logging
from controllers.search import SearchController


class SearchRequest(webapp2.RequestHandler):
    def get(self):
        path = self.request.path
        if path == "/search_user":
            SearchController.search_user(self)
        elif path == "/search_tweet":
            SearchController.search_tweet(self)


app = webapp2.WSGIApplication([
    ('/search_user', SearchRequest),
    ('/search_tweet', SearchRequest)
], debug=True)
