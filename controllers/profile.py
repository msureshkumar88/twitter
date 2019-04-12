import logging
import template_engine
from library.user import UserLibrary
from library.account import AccountHelper


class ProfileController:
    @classmethod
    def show_profile(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_logged_user()
        other_user = AccountHelper.in_other_profile(request.request.params)
        if other_user and user.user_name == other_user.user_name:
            return request.redirect('/profile')
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/profile.html')
        request.response.write(template.render(ProfileController.get_profile_template_data(request)))

    @classmethod
    def save_tweet(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(request)
        tweet = request.request.get("tweet")
        logging.info(tweet)
        AccountHelper.save_tweet(tweet)
        tweets = AccountHelper.get_tweets_by_user(request.request.params)
        msg = ""
        data = ProfileController.get_profile_template_data(request)
        data['msg'] = msg
        data['tweets'] = tweets

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

        msg = ""
        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'msg': msg
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/twitter/profile.html')
        request.response.write(template.render(data))

    @classmethod
    def search_user(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserLibrary.get_user(request)

        msg = ""
        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'msg': msg
        }
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
            'follow_text': follow_text
        }
        return template_values
