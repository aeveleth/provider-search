from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('providers.views',
        url(r'^search/$', 'search'),
)
