from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
def home(request):
    template = get_template('home.html')
    return render_to_response('home.html', {}, context_instance=RequestContext(request))
