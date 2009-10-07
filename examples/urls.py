from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^css/', include('mixl.urls')), 
    (r'^', include('test_app.urls')),
)
