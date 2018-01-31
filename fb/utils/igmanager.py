import json
from urllib.request import urlopen
from urllib.parse import urlencode
import urllib.parse
from datetime import datetime
import subprocess

with open('secrets.json', 'r') as f:
    conf = json.load(f)

class IgManager:
    IG_CREDENTIALS = conf['IG_CREDENTIALS']

    def __init__(self, ):
        self.access_token = None
        self.token_created_timestamp = None
        self.user = None
        self.client_id = None
        self.client_secret = None
        self.redirect_uri = None

    def set_attributes(self, redirect_scheme=IG_CREDENTIALS['redirect_scheme'],
                       client_id=IG_CREDENTIALS['client_id'],
                       redirect_host=IG_CREDENTIALS['redirect_host'],
                       redirect_path=IG_CREDENTIALS['redirect_path'],
                       client_secret=IG_CREDENTIALS['client_secret']):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_scheme + '://' + redirect_host + redirect_path

    def set_access_token(self, code):
        cmd = "curl -F 'client_id={client_id}' \
        -F 'client_secret={client_secret}' \
        -F 'grant_type=authorization_code' \
        -F 'redirect_uri={redirect_uri}' \
        -F 'code={code}' \
        https://api.instagram.com/oauth/access_token"
        cmd = cmd.format(client_id=self.client_id,
                         client_secret=self.client_secret,
                         redirect_uri=self.redirect_uri,
                         code=code)
        try:
            out = subprocess.check_output(cmd, shell=True)
            res = json.loads(out.decode('utf-8'))
            print(res)
            self.access_token = res.get('access_token')
            ACCESS_TOKEN = res.get('access_token')
            self.token_created_timestamp = datetime.now()
            self.user = res.get('user')
            print("Access token created, ", self.access_token)
        except Exception as e:
            print(e)
            res = "Error" + str(e)
        return res

    def auth_url(self):
        url = "https://api.instagram.com/oauth/authorize/?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        url += "&scope=public_content"
        url = url.format(client_id=self.client_id, redirect_uri=self.redirect_uri)
        print(url)
        return url

    def get_all_data(self, res):
        stop = False
        data = res.get('data')
        while not stop:
            pag = res.get('pagination')
            if pag is None or len(pag)==0 or 'http' not in pag['next_url']:
                stop = True
            else:
                url = pag['next_url']
                resp = urlopen(url)
                res = json.loads(resp.read().decode("utf-8"))
                data.append(res.get('data'))
        return data

    def get_media_likes(self, media_id):
        url = "https://api.instagram.com/v1/media/{media_id}/likes?access_token={access}"
        url = url.format(media_id=media_id, access=self.access_token)
        resp = urlopen(url)
        res = json.loads(resp.read().decode("utf-8"))
        print('>>>>> like media ', media_id)
        print(res)
        data = self.get_all_data(res)
        users = []
        for i in data:
            u = {'id': i['id'],
                 'username': i['username'],
                 'type': i['type']}
            users.append(u)
        return users

    def get_media_comments(self, media_id):
        url = "https://api.instagram.com/v1/media/{media_id}/comments?access_token={access}"
        url = url.format(media_id=media_id, access=self.access_token)
        resp = urlopen(url)
        res = json.loads(resp.read().decode("utf-8"))
        print('>>>>> COmments media ', media_id)
        print(res)
        data = self.get_all_data(res)
        comments = []
        comments_uid = []
        for i in data:
            if i['id'] not in comments_uid:
                c = {'uid': i['from']['id'],
                     'username': i['from']['username'],
                     'id': i['id']}
                comments_uid.append(c['id'])
                comments.append(c)
        return comments

    def get_user_media(self, user='self'):
        url = "https://api.instagram.com/v1/users/{user_id}/media/recent/?access_token={access}"
        url = url.format(user_id=user, access=self.access_token)
        resp = urlopen(url)
        res = json.loads(resp.read().decode("utf-8"))
        return res
        # data = self.get_all_data(res)
        # medias = []
        # for i in data:
        #     m = {'id': i['id'],
        #          'date': i['created_time'],
        #          'type': i['type'],
        #          'num_likes': int(i['likes']['count']),
        #          'num_comments': int(i['comments']['count']),
        #          'likers': None,
        #          'commenters': None,
        #          }
        #     if m['num_likes'] > 0:
        #         m['likers'] = self.get_media_likes(m['id'])
        #     if m['num_comments'] > 0:
        #         m['commenters'] = self.get_media_comments(m['id'])
        #     medias.append(m)
        #     # print('adding media')
        #     # print(m)
        # return str(medias)

    def search_user(self, username='fabrice zapfack'):
        url = "https://api.instagram.com/v1/users/search?q={username}&access_token={access}"
        url = url.format(username=urllib.parse.quote_plus(username), access=self.access_token)
        print(url)
        resp = urlopen(url)
        res = json.loads(resp.read().decode("utf-8"))
        print(res)
        return str(res)


