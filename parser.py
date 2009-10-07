import re
from elements import *
from commands import MIXL_DEFAULT_COMMANDS
from mixl_exceptions import NoSuchRule

MIXL_COMMAND_CHAR = '%'
MIXIN_MATCH = re.compile(r'\+(?P<mixin_name>.*);')
CONTEXT_MATCH = re.compile(r'(?P<context_name><[a-zA-Z0-9\-_]+>)')

class ParserReference(object):
    is_silent = False
    filename = None
    parser_object = None

    def __init__(self, filename, silent):
        self.is_silent = silent
        self.filename = filename

    def load_parser_object(self, parent_parser):
        from utils import mixl_import
        parser_object = mixl_import(self.filename, parent_parser.paths, commands=parent_parser.commands, context=parent_parser.context)
        return parser_object

    def find_rule(self, name, parent_parser):
        if self.parser_object is None:
            self.parser_object = self.load_parser_object(parent_parser)
        return self.parser_object.find_rule(name)

    def output(self, parent_parser):
        if self.parser_object is None:
            self.parser_object = self.load_parser_object(parent_parser)
        return self.parser_object.output()

class Parser(object):
    paths = ['./']
    def __init__(self, string, context={}, paths=[], commands=MIXL_DEFAULT_COMMANDS):
        if paths is not None:
            self.paths = paths
        self.context = context
        self.commands = commands
        self.parser_refs = []
        self.rules = self.parse(string)

    def register_parser(self, parser_filename, silent):
        self.parser_refs.append(ParserReference(parser_filename, silent))

    def find_rule(self, name):
        for rule in self.rules:
            if rule.name == name:
                return rule
        parser_refs = getattr(self, 'parser_refs', [])
        for ref in parser_refs:
            try:
                rule = ref.find_rule(name,self)
                return rule
            except IOError:
                pass
            except NoSuchRule:
                pass
        raise NoSuchRule

    def process_command(self, command):
        for registered_command in self.commands:
            if registered_command.match(command):
                registered_command.function(self, command)

    def parse_block(self, for_block):
        lines = for_block.split("\n")
        lines_out = []
        mixins = []
        for line in lines:
            mixin_match = MIXIN_MATCH.search(line)
            if mixin_match:
                mixins.append(Mixin(self, mixin_match.groupdict()['mixin_name']))
            else:
                lines_out.append(line)
        def context_matcher(matchobj):
            name = matchobj.group()[1:-1]
            if name in self.context.keys():
                return self.context[name]
            return ''
        context_processed_lines = []
        for line in lines_out:
            context_processed_lines.append(CONTEXT_MATCH.sub(context_matcher, line))
        return ' '.join(context_processed_lines), mixins 

    def parse(self, contents):
        file_length = len(contents)
        i = 0
        BLOCK_SEARCH = 0
        BLOCK_FINISH = 1
        mode = BLOCK_SEARCH

        search_start = 0
        block_start = 0
        name = ""

        rules = [] 
        last_char = None
        while i < file_length:
            char = contents[i]
            if mode == BLOCK_SEARCH and last_char in ("\n", None) and char == MIXL_COMMAND_CHAR:
                line_end = contents.find('\n', i+1)
                cmd = contents[i+1:line_end]
                self.process_command(cmd)
                i += line_end - i
                search_start = i
                continue
            elif mode == BLOCK_SEARCH:
                if char == '{':
                    name = contents[search_start:i]
                    block_start = i+1
                    mode = BLOCK_FINISH
            elif mode == BLOCK_FINISH:
                if char == '}':
                    search_start = i+1
                    block = contents[block_start:i]
                    block, mixins = self.parse_block(block)
                    rules.append(Rule(name, block, mixins))
                    mode = BLOCK_SEARCH
            i += 1
            last_char = char
        return rules

    def output(self):
        output = ''
        parser_refs = getattr(self, 'parser_refs', [])
        for ref in parser_refs:
            if ref.is_silent == False:
                output += ref.output(self)
        return output + ''.join([rule.output() for rule in self.rules])
