import re
from mixl_exceptions import *

class Rule(object):
    def __init__(self, name, block, mixins, do_output=True):
        self.name = name.strip()
        self.block = block.strip()
        self.mixins = mixins
        self.do_output = do_output

    def output(self):
        if self.do_output:
            return "%s { %s %s }\n" % (self.name, ' '.join([mixin.output() for mixin in self.mixins]), self.block)
        return '' 

class Mixin(object):
    def __init__(self, parser, reference_name):
        self.reference_name = reference_name
        self.parser = parser

    def output(self):
        try:
            rule = self.parser.find_rule(self.reference_name)
            return rule.block
        except NoSuchRule:
            return '/* unknown mixin %s */' % self.reference_name

class Command(object):
    def __init__(self, name, function, match=None):
        self.name = name
        if match is not None:
            self.match = match
        self.function = function

    def match(self, x):
        return x.startswith(self.name)
