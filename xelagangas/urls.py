from django.conf.urls import include,url
from django.contrib import admin
from posts import views as post_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_views.post_list, name ="list"),
    url(r'^create/', post_views.post_create, name ="crear"),
    url(r'^(?P<id>\d+)/', post_views.post_detail, name ='detail'),
    url(r'^edit/(?P<id>\d+)/', post_views.post_update, name = 'update'),
    url(r'^delete/(?P<id>\d+)/', post_views.post_delete),
    url(r'^artista/', post_views.entrada, name="artista"),
    url(r'^signup/$', post_views.signup, name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^home/$', post_views.home, name='home'),
    url(r'^logout/$', auth_views.logout, name="logout"),
    url(r'^main/$', post_views.post_list2, name='main'),
    url(r'^main2/$', post_views.nopermiso, name='main2'),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
