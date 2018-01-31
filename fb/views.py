import logging
from django.shortcuts import render
from django.shortcuts import redirect
import csv
from django.http import HttpResponse
from fb.utils.fbmanager import FbManager
from fb.utils.igmanager import IgManager
from fb.config import saved_list
# Create your views here.

IGMANAGER = IgManager()
print(">>>>> DONR")

def fb_login(request):
    context = {}
    return render(request, 'fb/open_page.html', context)


def page_results(request):
    if request.method == 'POST':
        fb = FbManager()
        page_str = request.POST.get('page')
        page = fb.get_page(page_str)
        if page is None:
            return render(request, 'fb/page_not_found.html')

        posts = fb.get_page_posts(page)
        if posts is None or len(posts) == 0:
            return render(request, 'fb/page_not_found.html')


        # return HttpResponse(posts)

        posts2 = []
        for p in posts:
            posts2.append(fb.post_engagement(p))

        return HttpResponse(posts2)
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
            if p['sharedposts'] is not None:
                for u in p['sharedposts']:
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
        return render(request, 'fb/page_results.html', context)
    else:
        return redirect("/test_fb")


def ig_auth(request):
    if not IGMANAGER.access_token:
        IGMANAGER.set_attributes(redirect_scheme=request.scheme, redirect_host=request.META['HTTP_HOST'],
                                 redirect_path="/ig_redirect/")
        url = IGMANAGER.auth_url()
        return redirect(url)
    else:
        return render(request, 'fb/ig_on.html', {})


def ig_auth_resp(request, code=None):
    if 'code' not in request.GET:
        return HttpResponse("Une erreur est survenue. Merci de réessayer")
    else:
        print('>>>> Resp')
        code = request.GET['code']
        print(">> code=", code)
        res = IGMANAGER.set_access_token(code)
        print("Access token: ", IGMANAGER.access_token)
        # l = ig.search_user(username='fabrice zapfack')
        # l = ig.get_user_media()
        return render(request, 'fb/ig_on.html', {})

def ig_medias(request):
    username = "jackie aina"
    l = IGMANAGER.search_user(username=username)
    return HttpResponse(l)
