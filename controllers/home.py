import webapp2
from google.appengine.api import users
import os
import logging
import template_engine

from library.user import UserLibrary


class HomePage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(self)

        template_values = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user']
        }

        template = template_engine.JINJA_ENVIRONMENT.get_template('views/home.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(self)

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/home.html')
        self.response.write(template.render(data))


app = webapp2.WSGIApplication([
    ('/', HomePage),
], debug=True)
