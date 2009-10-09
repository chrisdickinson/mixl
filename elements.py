import re
from mixl_exceptions import *
from utils import mixl_import

CONTEXT_MATCH = re.compile(r'(?P<context_name><[a-zA-Z0-9\-_]+>)')

class MixlNode(object):
    def __init__(self):
        pass

    def visit(self, template, state):
        return ''

class MixlRuleNode(MixlNode):
    def __str__(self):
        return "<MixlRuleNode: %s>" % self.name

    def __init__(self, name, block):
        self.name = name.strip()
        self.block = block

    def parse_block(self, template, state):
        block_statements = [line.strip() for line in self.block.split(';')]
        output = []
        def context_matcher(matchobj):
            name = matchobj.group()[1:-1]
            return state.get_value(name)

        for block_statement in block_statements:
            if len(block_statement) < 1:
                continue
            elif block_statement[0] == '+':
                try: 
                    rule = state.lookup_rule(block_statement[1:], lambda x,y: x==y)
                    output.append(rule.parse_block(template, state))
                except NoSuchRule:
                    output.append('/* ERROR: no such rule %s */' % block_statement[1:])
            elif '<' in block_statement:
                output.append(CONTEXT_MATCH.sub(context_matcher, block_statement)) 
            else:
                output.append(block_statement)
        return ';  '.join(output) + ';'

    def visit(self, template, state):
        return '%s { %s }' % (self.name, self.parse_block(template, state))

class MixlCommandNode(MixlNode):
    def __init__(self, command_string):
        self.command_string = command_string

    def visit(self, template, state):
        command = state.get_command(self.command_string)
        output = ''

        try:
            output = command(template, state, self.command_string)
        except Exception, e:
            pass
        return output

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
