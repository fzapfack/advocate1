from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin
import hello.views
from listener.views import add_tweet_view
from listener.views import get_name
import predictor.views
from listener.regbackend import MyRegistrationView
from fb.views import fb_login
from fb.views import page_results


admin.autodiscover()
# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='home'),
    url(r'^test_fb/$', fb_login, name='Insert a page'),
    url(r'^test_fb_results/$', page_results, name='Page results'),
    url(r'^test/(?P<id>\w+)/$', predictor.views.test, name='test_page'),
    url(r'^start_listening', add_tweet_view, name='start_listening'),
    url(r'^labeling', get_name, name='labeling'),
    url(r'^accounts/register/$', MyRegistrationView.as_view(),
            name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
