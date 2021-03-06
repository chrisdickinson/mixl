# Create your views here.
from django.conf import settings
from utils import mixl_import
from django.http import HttpResponse, Http404
from django.conf import settings

def mixl_css(request, filename):
    """
        mixl_css view
            - THIS SHOULD NOT BE USED IN PRODUCTION, just for development

            attempts to locate a css file along the MIXL_PATHS and then
            parses and returns the content

            in production, please use the management commands to compile
            your mixl css files into your MEDIA_ROOT.
    """
    paths = getattr(settings, 'MIXL_PATHS', ['./'])
    #try:
    context = {
        'MEDIA_URL':settings.MEDIA_URL
    }
    template = mixl_import(filename, paths, context=context)
    output = template.output(context)
    #if output is None:
    #    raise Http404
    #except IOError:
    #    raise Http404
    return HttpResponse(content=output, mimetype='text/css', status=200)
