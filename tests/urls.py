from django.conf.urls import patterns, url

def view():
    pass

urlpatterns = patterns('',
    url(r'^.*/$', view)
)
