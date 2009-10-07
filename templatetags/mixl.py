import os
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
register = template.Library()

class MixlIncludeNode(template.Node):
    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        return super(MixlIncludeNode, self).__init__(*args, **kwargs)

    def render(self, context):
        if settings.DEBUG:
            return reverse('mixl-css', kwargs={'filename':self.filename})
        else:
            path = ''
            if 'MEDIA_URL' in context.keys():
                path = context['MEDIA_URL']
            return os.path.join(path, self.filename)
            

def mixl_include(parser, token):
    items = token.contents.split(' ')
    filename = items[1][1:-1]
    return MixlIncludeNode(filename)


register.tag('mixl_include', mixl_include)
