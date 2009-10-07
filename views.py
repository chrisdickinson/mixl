# Create your views here.
from parser import Parser
from django.conf import settings
from utils import mixl_import
from django.http import HttpResponse, Http404

def mixl_css(request, filename):
    paths = getattr(settings, 'MIXL_PATHS', ['./'])

    try:
        parser = mixl_import(filename, paths)
        output = parser.output()
        if output is None:
            raise Http404
    except IOError:
        raise Http404
    return HttpResponse(content=output, mimetype='text/css', status=200)
