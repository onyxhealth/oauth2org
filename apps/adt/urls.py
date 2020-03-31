from django.conf.urls import url
from django.contrib import admin
from .views import post_adt_feed

admin.autodiscover()

urlpatterns = [

    url(r'api/post-adt$', post_adt_feed, name='post_adt_feed'),
]
