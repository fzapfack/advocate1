from django.shortcuts import render
from django.shortcuts import redirect
import csv
from django.http import HttpResponse
from fb.utils.fbmanager import FbManager
from fb.config import saved_list
# Create your views here.


def fb_login(request):
    # host = "https://facebook.com/v2.8"
    # client_id = "1702911896701938"
    # redirect_uri = "https://www.facebook.com/connect/login_success.html"
    # path = "/dialog/oauth"
    # params = urlencode({"client_id": client_id, "redirect_uri": redirect_uri})
    # # url = "{host}{path}?{params}".format(host=host, path=path, params=params)
    # url = "{host}{path}?{params}".format(host=host, path=path, params="client_id="+client_id+
    #                                     "&redirect_uri="+redirect_uri)

    # return HttpResponse(url)
    context = {}
    return render(request, 'open_page.html', context)


def add_user(uid, user_name, users):
    if uid not in users:
        users[uid] = {
            "name": user_name,
            "likes": [],
            "shares": [],
            "comments": [],
        }


def page_results(request):
    page = {}
    if request.method == 'POST':
        fb = FbManager()
        path = "/" + request.POST.get('page')
        params = {}
        res = fb.call_graph_api_token(path, params)
        if res is None:
            return render(request, 'page_not_found.html')
        else:
            res_url = res[0]
            res = res[1]
        page["name"] = res["name"]
        page["id"] = res["id"]
        page["url"] = "https://www.facebook.com/" + request.POST.get('page')

        path = "/" + page["id"]
        fields = ["posts"]
        params = {"fields": ','.join(fields)}
        res = fb.call_graph_api_token(path, params)
        if res is None:
            pass
        else:
            res_url = res[0]
            res = res[1]
        posts = [{"id":i["id"], "created_time":i["created_time"]} for i in res["posts"]["data"]]
        posts2 = []
        for p in posts:
            path = "/" + p["id"]
            fields = ["reactions", "comments", "sharedposts"]
            params = {"fields": ','.join(fields)}
            res = fb.call_graph_api_token(path, params)
            if res is None:
                pass
            else:
                res_url = res[0]
                res = res[1]
            a = res.get("reactions")
            if a is None:
                p["likes"] = None
            else:
                p["likes"] = [(i["id"], i["name"]) for i in a["data"]]
            a = res.get("comments")
            if a is None:
                p["comments"] = None
            else:
                p["comments"] = [(i["from"]["id"], i["from"]["name"]) for i in a["data"]]
            posts2.append(p)

        users = {}
        for p in posts2:
            if p['likes'] is not None:
                for u in p['likes']:
                    add_user(u[0], u[1], users)
                    users[u[0]]["likes"].append(p["id"])
            if p['comments'] is not None:
                for u in p['comments']:
                    add_user(u[0], u[1], users)
                    users[u[0]]["comments"].append(p["id"])

        users_list = []
        for u in users.items():
            d = {}
            d['id'] = u[0]
            d['url'] = "https://www.facebook.com/" + d['id']
            d['name'] = u[1]['name']
            d['num_likes'] = len(u[1]['likes'])
            d['num_comments'] = len(u[1]['comments'])
            users_list.append(d)

        context = {
            "page": page,
            "users_list": users_list
        }
        return render(request, 'page_results.html', context)
    else:
        return redirect("/test_fb")
