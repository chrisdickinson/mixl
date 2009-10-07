from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option
from testmixl.mixl.utils import mixl_import
from django.core.management.color import supports_color
import os

if supports_color():
    from django.utils.termcolors import *
else:
    def colorize(*args, **kwargs):
        return args[0]


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--src', '-s', dest='source',
            help='Process .css files in [src] MIXL_PATH directory'),
        make_option('--dest', '-o', dest='output',
            help='Set the destination of the mixl output'),
    )
    help = 'Compiles .css files in your mixl paths to their destination (defaults to MEDIA_DIR)'

    def read_directory(self, arg, dirname, names):
        target_dir = dirname.replace(self.source[0], self.output) 
        print target_dir
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        for name in names:
            full_name = os.path.join(target_dir, name)
            full_target = os.path.join(self.output, full_name)
            location = os.path.join(self.source, full_name)
            if not os.path.isdir(location) and os.path.exists(location) and full_name[-3:] == 'css':
                try:
                    print 'attempting to compile <%s> -> <%s>...' % (full_name, full_target),
                    parser = mixl_import(full_name, paths=self.source)
                    file = open(full_target, 'w')
                    file.write(parser.output())
                    file.close()
                    print colorize('\t\t\tsuccess!', fg='green')
                except IOError:
                    print colorize('\t\t\tfailure!', fg='red')

    def handle(self, source=None, output=None, **kwargs):
        available_directories = getattr(settings, 'MIXL_PATHS', None)
        if output is None:
            output = getattr(settings, 'MEDIA_ROOT', None)
        if available_directories is None and source is None:
            raise CommandError("You must have MIXL_PATHS defined in your settings.py file (or supply one with -s <dir>).")
        if output is None:
            raise CommandError("You must have MEDIA_ROOT defined your settings.py file (or supply a destination directory with -o <dir>).")
        if source is None:
            source = (available_directories[0], )           # just process the first in the list 
        else:
            source = (source, )
 
        self.output = output
        self.source = source
        os.path.walk(source[0], self.read_directory, None)
