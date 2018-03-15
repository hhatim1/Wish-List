from django.conf.urls import url
from . import views
#from django import models
#####################################
urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^logout$', views.logout, name = "logout"),
    url(r'^create_item$', views.create_item, name='create_item'),
    url(r'^leave/(?P<item_id>\d+)', views.leave, name="leave"),
    url(r'^join/(?P<item_id>\d+)', views.join, name="leave"),
    url(r'^info/(?P<item_id>\d+)', views.info, name="leave")
    
]