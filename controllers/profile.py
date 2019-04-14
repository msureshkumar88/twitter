import logging
import template_engine
from library.user import UserLibrary
from library.account import AccountHelper
from google.appengine.api import search
from google.appengine.ext import blobstore
from google.appengine.api import images


class ProfileController:
    @classmethod
    def show_profile(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_logged_user()
        if not user.user_name:
            request.redirect('/')
        other_user = AccountHelper.in_other_profile(request.request.params)
        logging.info(other_user)
        data = ProfileController.get_profile_template_data(request)
        data['upload_url'] = blobstore.create_upload_url('/save-tweet')
        data['save_result'] = request.session.get('save_result')

        if "save_result" in request.session:
            del request.session['save_result']

        if 'user' in request.request.params:
            if not other_user:
                return request.redirect('/profile')

        if other_user and user.user_name == other_user.user_name:
            return request.redirect('/profile')
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/profile.html')
        request.response.write(template.render(data))

    @classmethod
    def save_tweet(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(request)

        tweet = request.request.get("tweet")
        result = AccountHelper.save_tweet(request)
        request.session['save_result'] = result
        tweets = AccountHelper.get_tweets_by_user(request.request.params)
        msg = ""
        data = ProfileController.get_profile_template_data(request)
        data['msg'] = msg
        data['tweets'] = tweets
        data['result'] = result
        request.redirect('/profile')
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/profile.html')
        request.response.write(template.render(data))

    @classmethod
    def update_tweet(cls, request, type):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(request)
        id = request.request.params["id"]
        text = request.request.get("tweet")
        tweet = AccountHelper.get_tweet_by_id(id)
        if type == "post":
            AccountHelper.update_tweet(id, text)

        msg = ""
        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'msg': msg,
            'tweet': tweet,
            'id': id
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/edit_tweet.html')
        request.response.write(template.render(data))

    @classmethod
    def delete_tweet(cls, request):
        # request.response.headers['Content-Type'] = 'text/html'
        logging.info(request.request.params["id"])
        AccountHelper.delete_tweet(request.request.params["id"])
        request.redirect("/profile?delete_success=delete_success")
        return

    @classmethod
    def search_tweet(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(request)

        data = ProfileController.get_profile_template_data(request)
        data["search_tweet"] = True
        result = AccountHelper.search_tweet(request.request.params)
        # logging.info(result)
        # message = ""
        # if not result:
        #     message = "No tweets found"
        # data['message'] = message
        data["result"] = result

        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/profile.html')
        request.response.write(template.render(data))

    @classmethod
    def search_user(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(request)

        msg = ""
        data = ProfileController.get_profile_template_data(request)
        data["search_user"] = True
        result = AccountHelper.search_by_username(request.request.params)
        data['result'] = result

        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/profile.html')
        request.response.write(template.render(data))

    @classmethod
    def update_following_status(cls, request):
        request.response.headers['Content-Type'] = 'text/html'

        other_user = AccountHelper.in_other_profile(request.request.params)
        AccountHelper.change_following_status(request.request.get("btn_text"), other_user.user_name)

        data = ProfileController.get_profile_template_data(request)

        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/profile.html')
        request.response.write(template.render(data))

    @classmethod
    def get_profile_template_data(cls, request):
        user = UserLibrary.get_user(request)
        tweets = AccountHelper.get_tweets_by_user(request.request.params)
        other_user = AccountHelper.in_other_profile(request.request.params)
        follow_text = ""
        if other_user:
            AccountHelper.get_follow_status(other_user.user_name)
            follow_text = AccountHelper.get_following_text(other_user.user_name)
        template_values = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'tweets': tweets,
            'other_user': other_user,
            'profile_data': AccountHelper.get_profile_data(request.request.params),
            'follow_text': follow_text,
            'images': images
        }
        return template_values
