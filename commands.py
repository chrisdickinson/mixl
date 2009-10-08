import re
from utils import mixl_import
from elements import Command, Rule
from mixl_exceptions import CommandSyntaxError
 
MIXL_IMPORT_REGEX = re.compile('import "(?P<filename>.+?)"( (?P<silently>silently)?)?')
MIXL_DEFINE_REGEX = re.compile('define (?P<variable_name>[\w\-]+)\s*:(?P<value>.*)')
MIXL_SYNTH_RULES_REGEX = re.compile('synth-rules (?P<class_name>.+) with \{(?P<block>.+)\} for (?P<variable_name>\w+) in \[(?P<variable_list>.*)\]')
def mixl_command_import(_p, command, state):
    """
        in mixl:
            %import "example.css"
            OR
            %import "example.css" silently
        register a new css file with the current parser,
        also let it know whether or not you want to 
        import it silently
    """
    match = MIXL_IMPORT_REGEX.match(command)
    if match is not None:
        from parser import Parser
        matches = match.groupdict()
        filename = matches['filename']
        silently = matches['silently'] is not None
        _p.register_parser(filename, silently)
    else:
        raise CommandSyntaxError()

def mixl_define(parser, command, state):
    """
        in mixl:
            %define variable:value
            and to use it:
            h1 { color:<variable>; }

        contributes to the parser's context member variable.
    """
    match = MIXL_DEFINE_REGEX.match(command)
    if match is not None:
        matches = match.groupdict()
        var_name = matches['variable_name']
        value = matches['value']
        parser.context.update({var_name:value})    
    else:
        raise CommandSyntaxError()


def mixl_synth_rules(parser, command, state):
    match = MIXL_SYNTH_RULES_REGEX.match(command)
    if match is not None:
        rules = []
        matches = match.groupdict()
        class_name_base = matches['class_name']
        block = matches['block']
        variable_name = matches['variable_name']
        variable_list = matches['variable_list'].split(' ')
        old_variable_value = None
        if variable_name in parser.context.keys():
            old_variable_value = parser.context[variable_name]

        i = 0
        new_rules = []
        for variable in variable_list:
            if variable not in parser.context.keys():
                continue
            parser.context[variable_name] = parser.context[variable]
            new_block, mixins = parser.parse_block(block)
            rule_name = "%s%d" % (class_name_base, i)
            new_rule = Rule(rule_name, new_block, mixins, not getattr(parser, 'is_silent', True))
            new_rules.append(new_rule)
            i += 1
        state.rules += new_rules
        if old_variable_value is not None:
            parser.context[variable_name] = old_variable_value

MIXL_DEFAULT_COMMANDS = [
    Command('import', mixl_command_import),
    Command('define', mixl_define),
    Command('synth-rules', mixl_synth_rules),
]

