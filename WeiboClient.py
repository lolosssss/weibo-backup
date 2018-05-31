# -*- coding: utf-8 -*-

import time
import requests
import os
from io import open

class WeiboClient(object):

    def __init__(self, app_key, app_secret, redirect_uri):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.access_token = None

    def get_authorize_url(self, redirect_uri=None):
        return "https://api.weibo.com/oauth2/authorize?response_type=code&client_id=%s&redirect_uri=%s" % (self.client_id, requests.utils.requote_uri(redirect_uri))

    def __parse_access_token(self, r):
        current = int(time.time())
        expires = r.expires_in + current
        access_token = r.access_token
        uid = r.uid
        return { access_token: access_token, expires: expires, uid: uid}

    def request_access_token(self, code):
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        resp = requests.post("https://api.weibo.com/oauth2/access_token", params= params)
        return resp.access_token

    def set_access_token(self, access_token):
        self.access_token = access_token

    def request_user_timeline(self, uid, access_token, count=20, page=1):
        """
        Get specified user's latest posts list. BUT, this API can only get 5 posts.
        Args:
            uid(string): specified user's unique ID
            access_token(string): access_token required by OAuth2
            count(number): query number of posts, miximum is 100
            page(number): query page of result
        Returns:
            None
        """
        params = {
            "access_token": access_token,
            "uid": uid,
            "count": count,
            "page": page
        }
        resp = requests.get("https://api.weibo.com/statuses/user_timeline.json", params=params)
        return resp.json()

    def request_home_timeline(self, access_token, count=20, page=1, trim_user=1):
        """
        Get authorized users' posts.
        Args:
            access_token(string): access_token required by OAuth2
            count(number):
            page(number):
            trim_user(number): return 0 - complete user field, 1 - only user_id
        Returns:
            JSON formatted response, including ads? FUCK WEIBO.
            Users' posts in 'statuses'
        """
        params = {
            "access_token": access_token,
            "count": count,
            "page": page,
            "trim_user": trim_user
        }
        resp = requests.get("https://api.weibo.com/statuses/home_timeline.json", params=params)
        return resp.json()

    def request_user_info(self, uid, access_token):
        """
        Get specified user's information.
        Args:
            uid(string): user's unique ID
            access_token(string): access_token asked by OAuth2
        Returns:
            JSON formatted user's information.
            Refer to http://open.weibo.com/wiki/2/users/show
        """
        params = {
            "access_token": access_token,
            "uid": uid
        }
        resp = requests.get("https://api.weibo.com/2/users/show.json", params=params)
        return resp.json()

    def request_user_counts(self, uids, access_token):
        """
        Get specified users' counts, including count of fans, posts, etc.
        Args:
            uids(string): mutiple user's unique ID, separated with ',', number
                of uid limited to 100.
            access_token(string): access_token asked by OAuth2
        Returns:
            JSON Array.
            example:
            [{
                "id": "1404376560",
                "followers_count": "1369",
                "friends_count": "526",
                "statuses_count": "2908"
            }, ...]
        """
        params = {
            "access_token": access_token,
            "uids": uids
        }
        resp = requests.get("https://api.weibo.com/2/users/counts.json", params=params)
        return resp.json()

    def request_image(self, img_url, file_path='.'):
        """
        Get the image from specified URL.
        Args:
            img_url(string): specified image url
            file_path(string): path to save image, default is current directory
        Returns:
            bool - save image successfully or not
        """
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = img_url.split('/')[-1]
        i = requests.get(img_url)
        if i.status_code == requests.codes['ok']:
            with open(file_path + '/' + file_name, 'wb') as file:
                file.write(i.content)
            return True
        else:
            return False