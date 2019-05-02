import webapp2
from google.appengine.api import users
import os
import logging
import template_engine

from library.user import UserLibrary


class HomeController(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(self)
        logging.info(user['user'])
        if user['user'] and user['user'].user_name:
            self.redirect('/profile')

        template_values = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'result': {}
        }

        template = template_engine.JINJA_ENVIRONMENT.get_template('views/home.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(self)

        userName = self.request.get("username")

        result = UserLibrary.update_username(self)

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'result': result
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/home.html')
        self.response.write(template.render(data))


app = webapp2.WSGIApplication([
    ('/', HomeController),
], debug=True)
