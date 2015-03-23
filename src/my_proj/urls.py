from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import profiles.urls
import accounts.urls
from . import views
from profiles.models import *

urlpatterns = patterns(
    '',
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^about/$', views.AboutPage.as_view(), name='about'),
    url(r'^', include(accounts.urls, namespace='accounts')),
    url(r'^users/', include(profiles.urls, namespace='profiles')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^create/', views.StartUpCreate.as_view(success_url="/"), name='create'),
    url(r'^browse/', views.BrowsePage.as_view(), name='browse'),
    url(r'^category/(?P<category_id>\d+)?/?$', views.CategoryListView.as_view(), name='category'),
    url(r'^tag/(?P<slug>[-\w]+)/$', views.TagIndexView.as_view(), name='tags'),
    url(r'^my_startups/', views.UserListings.as_view(), name='my_startups'),
    url(r'^detail/(?P<pk>\d+)?/?$', views.StartUpDetail.as_view()),
    url(r'^edit_startup/(?P<pk>\d+)?/?$', views.UpdateStartup.as_view()),
    url(r'^delete_startup/(?P<pk>\d+)?/?$', views.DeleteStartup.as_view()),
    url(r'^like_startup/(?P<startup_id>\d+)?/?$', views.like_startup, name='like_startup'),
    url(r'^dislike_startup/(?P<startup_id>\d+)?/?$', views.dislike_startup, name='dislike_startup'),
    url(r'^json_list/(?P<k>[0-9]+)/(?P<date1>\d{4}-\d{2}-\d{2})/(?P<date2>\d{4}-\d{2}-\d{2})/$', views.json_list),
)

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
