from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

import hello.views
from listener.views import add_tweet_view
from listener.views import get_name


# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='home'),
    url(r'^map', hello.views.map, name='maps'),
    # url(r'^db', hello.views.db, name='db'),
    url(r'^start_listening', add_tweet_view, name='start_listening'),
    url(r'^labeling', get_name, name='labeling'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
