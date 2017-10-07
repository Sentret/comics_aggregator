from django.conf.urls import url
from django.contrib import admin
from app import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^comics/$', views.main_page),
    url(r'^$', views.main_page),
    url(r'^comics/(?P<shop>.\w*)/$', views.main_page,name='main_page'),
    
]