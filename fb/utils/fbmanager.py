import json
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime


class FbManager:
    FB_CREDENTIALS = {
        'graph_api_host': "https://graph.facebook.com/v2.8",
        'app_id': "1702911896701938",
        'app_secret': "27b76bb69ded0ce5873c120c2d0e0df0",

    }

    def __init__(self):
        self.access_token = None
        self.token_created_timestamp = None

    def call_graph_api(self, path, params):
        try:
            params = urlencode(params)
            url = "{host}{path}?{params}".format(host=self.FB_CREDENTIALS['graph_api_host'],
                                                 path=path, params=params)
            resp = urlopen(url)
            res = json.loads(resp.read().decode("utf-8"))
            res_url = resp.geturl()
            # print(res_url)
            # print(res)
            return res_url, res
        except Exception as e:
            print(e)
            print("url >>", url)
            return None

    def generate_token(self):
        path = "/oauth/access_token"
        params = {"client_id": self.FB_CREDENTIALS['app_id'],
                  "client_secret": self.FB_CREDENTIALS['app_secret'],
                  "grant_type": "client_credentials"}
        res = self.call_graph_api(path, params)
        self.access_token = res[1]['access_token']
        self.token_created_timestamp = datetime.now()
        return True

    def call_graph_api_token(self, path, params):
        if self.access_token is None:
            self.generate_token()
            print("New access token generated")
        try:
            params['access_token'] = self.access_token
            params = urlencode(params)
            url = "{host}{path}?{params}".format(host=self.FB_CREDENTIALS['graph_api_host'],
                                                 path=path, params=params)
            resp = urlopen(url)
            res = json.loads(resp.read().decode("utf-8"))
            res_url = resp.geturl()
            return res_url, res
        except Exception as e:
            print(e)
            print("url >>", url)
            return None
