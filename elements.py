import re
from mixl_exceptions import *

class Rule(object):
    """
        Rule(name, block, mixins, do_output)
            the internal representation of a CSS rule
            mixins are lazily referenced, and not looked up
            until the rule is actually required to output itself
    """
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
    """
        Mixin(parser, reference_name)
            mixins search from the parser where they originated from,
            extending from that parser into children parsers.

            their reference_name references a Rule's name.
    """
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
    """
        Command(name, function, match)
            a command element takes a function of the form
            fn(<parser object>, <command string encountered>),
            which is executed when the match function returns
            True. The match function, by default, just checks that 
            the command startswith the proper string, but
            can be overridden with another function or lambda
            during initialization 
    """
    def __init__(self, name, function, match=None):
        self.name = name
        if match is not None:
            self.match = match
        self.function = function

    def match(self, x):
        return x.startswith(self.name)
