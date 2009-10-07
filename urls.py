from django.conf.urls.defaults import *
import views
urlpatterns = patterns('',
    url(r'^(?P<filename>.*)', views.mixl_css, name='mixl-css'),
)
