import json
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime
import csv


class FbManager:
    FB_CREDENTIALS = {
        'graph_api_host': "https://graph.facebook.com/v2.8",
        'app_id': "1702911896701938",
        'app_secret': "27b76bb69ded0ce5873c120c2d0e0df0",
    }

    def __init__(self):
        self.access_token = None
        self.token_created_timestamp = None
        self.users = {}

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

    def get_page(self, page_str):
        path = "/" + page_str
        params = {}
        res = self.call_graph_api_token(path, params)
        if res is None:
            return res
        else:
            res_url = res[0]
            res = res[1]
        page = {}
        page["name"] = res["name"]
        page["id"] = res["id"]
        page["url"] = "https://www.facebook.com/" + page["name"]
        return page

    def complete_pagination(self, field, res):
        if field not in res:
            print(field, "not present")
            return res
        else:
            stop = False
            url = res[field]['paging'].get('next')
            while not stop:
                if url is None:
                    stop = True
                else:
                    print('paging')
                    resp = urlopen(url)
                    res2 = json.loads(resp.read().decode("utf-8"))
                    data = res2.get('data')
                    if data is None or len(data) == 0:
                        stop = True
                    else:
                        res[field]['data'].extend(data)
                        url = res2['paging'].get('next')
            return res

    def paging_post(self, res):
        for field in ['reactions', 'comments']:
        # for field in ['reactions', 'comments', 'sharedposts']:
            res = self.complete_pagination(field, res)

        return res

    def get_page_posts(self, page):
        path = "/" + page["id"]
        fields = ["posts"]
        params = {"fields": ','.join(fields)}
        res = self.call_graph_api_token(path, params)
        if res is None:
            pass
        else:
            res_url = res[0]
            res = res[1]
        res = self.complete_pagination('posts', res)
        posts = [{"id": i["id"], "created_time": i["created_time"]} for i in res["posts"]["data"]]
        return posts

    def post_engagement(self, p):
        path = "/" + p["id"]
        # fields = ["reactions", "comments", "sharedposts"]
        fields = ["reactions", "comments"]
        params = {"fields": ','.join(fields)}
        res = self.call_graph_api_token(path, params)
        if res is None:
            print('error')
        else:
            res_url = res[0]
            res = res[1]
        # Complete pagination
        res = self.paging_post(res)
        if res is None:
            print("error in extracting post ", p[id])
            p["reactions"] = None
            p["comments"] = None
            p["sharedposts"] = None
            p['num_reactions'] = 0
            p['num_comments'] = 0
            p['num_sharedposts'] = len(p["sharedposts"])
        else:
            a = res.get("reactions")
            # TO-DO check reaction type
            if a is None:
                p["reactions"] = None
                p['num_reactions'] = 0
            else:
                p["reactions"] = [(i["id"], i["name"]) for i in a["data"]]
                p['num_reactions'] = len(p["reactions"])
            a = res.get("comments")
            if a is None:
                p["comments"] = None
                p['num_comments'] = 0
            else:
                p["comments"] = [(i["from"]["id"], i["from"]["name"]) for i in a["data"]]
                p['num_comments'] = len(p["comments"])

            # for sharredpost, get lists of id and send an api call to fecth user
            # we need user_post rigths to collect shared posts
            # a = res.get("sharedposts")
            # if a is None:
            #     p["sharedposts"] = None
            #     p['num_sharedposts'] = 0
            # else:
            #     p["sharedposts"] = [(i["id"], 0) for i in a["data"]]
            #     p['num_sharedposts'] = len(p["sharedposts"])


            # p2 = {'id':p['id'], 'num_reactions':p['num_reactions'], 'num_sharedposts':p['num_sharedposts']}
        return p

    def add_user(self, uid, user_name):
        if uid not in self.users:
            self.users[uid] = {
                "name": user_name,
                "likes": [],
                "shares": [],
                "comments": [],
            }

    def extract_users(self, posts):
        posts2 = []
        for p in posts:
            posts2.append(self.post_engagement(p))

        for p in posts2:
            if p['reactions'] is not None:
                for u in p['reactions']:
                    self.add_user(u[0], u[1])
                    self.users[u[0]]["likes"].append(p["id"])
            if p['comments'] is not None:
                for u in p['comments']:
                    self.add_user(u[0], u[1])
                    self.users[u[0]]["comments"].append(p["id"])

        users_list = []
        for u in self.users.items():
            d = {}
            d['id'] = u[0]
            d['url'] = "https://www.facebook.com/" + d['id']
            d['name'] = u[1]['name']
            d['num_likes'] = len(u[1]['likes'])
            d['num_comments'] = len(u[1]['comments'])
            users_list.append(d)
        return users_list

    def remove_user(self, uid):
        res = self.users.pop(uid, None)
        if res is None:
            print("User do not exist")
        else:
            print("removed user")
            print(res)
        return True

    def users_to_csv(self, filename=None, fields=None):
        if filename is None:
            filename = "out.csv"
        users_list = []
        for u in self.users.items():
            d = {}
            if 'uid' in fields:
                d['uid'] = u[0]
            if 'name' in fields:
                res = u[1]['name'].split()
                if len(res)>1:
                    d['name1'] = res[0]
                    d['name2'] = " ".join(res[1:])
            if fields is None:
                d['uid'] = u[0]
                d['url'] = "https://www.facebook.com/" + d['uid']
                res = u[1]['name'].split()
                if len(res) > 1:
                    d['name1'] = res[0]
                    d['name2'] = " ".join(res[1:])
                d['num_likes'] = len(u[1]['likes'])
                d['num_comments'] = len(u[1]['comments'])

            d['email'] = "".join(u[1]['name'].split()) + "@facebook.com"
            d['country'] = "FR"
            d['zip'] = "75000"

            users_list.append(d)

        with open(filename, 'w') as f:
            w = csv.DictWriter(f, users_list[0].keys())
            w.writeheader()
            for u in users_list:
                w.writerow(u)

        print(len(users_list), "users exported to file ", filename)
        return True


def analyze_page(page_str, to_csv=False, filename=None, fields=None):
    fb = FbManager()
    page = fb.get_page(page_str)
    if page is None:
        print("No page found")
    posts = fb.get_page_posts(page)
    if posts is None or len(posts) == 0:
        print("No post found")
    users_list = fb.extract_users(posts)
    fb.remove_user(page['id'])

    if to_csv:
        _ = fb.users_to_csv(filename=filename, fields=fields)

    return users_list


