import webapp2

import logging
from controllers.profile import ProfileController
from google.appengine.ext.webapp import blobstore_handlers
from webapp2_extras import sessions

class ProfileRequest(webapp2.RequestHandler):
    def get(self):
        path = self.request.path
        logging.info(path)
        if path in "/profile":
            ProfileController.show_profile(self)
        elif path in "/delete-tweet":
            ProfileController.delete_tweet(self)
        elif path in "/edit-tweet":
            ProfileController.update_tweet(self,"get")
        elif path in "/search-user":
            ProfileController.search_user(self)
        elif path in "/search-tweet":
            ProfileController.search_tweet(self)

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

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()


class SaveTweetRequest(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        ProfileController.save_tweet(self)

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    ('/profile', ProfileRequest),
    ('/delete-tweet', ProfileRequest),
    ('/edit-tweet', ProfileRequest),
    ('/search-user', ProfileRequest),
    ('/search-tweet', ProfileRequest),
    ('/save-tweet', SaveTweetRequest),
], debug=True, config=config)
