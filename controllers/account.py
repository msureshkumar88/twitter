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
            'user': user['user']
        }

        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/edit_profile.html')
        request.response.write(template.render(template_values))

    @classmethod
    def update_profile_post(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(request)

        request.request.get("first_name")
        request.request.get("last_name")
        request.request.get("dob")
        request.request.get("city")
        request.request.get("website")
        request.request.get("bio")
        data = {
            "first_name": request.request.get("first_name"),
            "last_name": request.request.get("last_name"),
            "dob": request.request.get("dob"),
            "city": request.request.get("city"),
            "website": request.request.get("website"),
            "bio": request.request.get("bio"),

        }
        AccountHelper.update_profile(data)



        msg = ""

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'msg': msg
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/edit_profile.html')
        request.response.write(template.render(data))



