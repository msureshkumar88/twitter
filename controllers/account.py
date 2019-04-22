import logging
import template_engine
from library.user import UserLibrary
from library.account import AccountHelper

class AccountController:
    @classmethod
    def update_profile_get(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(request)
        logging.info(user['user'])
        template_values = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'profile_data': AccountHelper.get_profile_data(request.request.params)
        }

        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/edit_profile.html')
        request.response.write(template.render(template_values))

    @classmethod
    def update_profile_post(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(request)

        inputs = {
            "first_name": request.request.get("first_name"),
            "last_name": request.request.get("last_name"),
            "bio": request.request.get("bio"),

        }
        result = AccountHelper.update_profile(inputs)

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'profile_data': AccountHelper.get_profile_data(request.request.params),
            'result': result,
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/edit_profile.html')
        request.response.write(template.render(data))



