import logging
import template_engine

class AccountController:
    @classmethod
    def update_profile_get(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(request)

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

        msg = ""

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'msg': msg
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/edit_profile.html')
        request.response.write(template.render(data))



