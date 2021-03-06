import logging
import template_engine
from library.user import UserLibrary
from library.account import AccountHelper

class SearchController:
    @classmethod
    def search_user(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(request)
        logging.info(user['user'])
        template_values = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user']
        }

        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/search_user.html')
        request.response.write(template.render(template_values))

    @classmethod
    def search_tweet(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(request)

        msg = ""

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'msg': msg
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/search_tweet.html')
        request.response.write(template.render(data))



