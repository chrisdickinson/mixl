import re
from utils import mixl_import
from elements import Command
from mixl_exceptions import CommandSyntaxError
 
MIXL_IMPORT_REGEX = re.compile('import "(?P<filename>.+?)"( (?P<silently>silently)?)?')
MIXL_DEFINE_REGEX = re.compile('define (?P<variable_name>\w+)\s*:(?P<value>.*)')

def mixl_command_import(_p, command):
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

def mixl_define(parser, command):
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

MIXL_DEFAULT_COMMANDS = [
    Command('import', mixl_command_import),
    Command('define', mixl_define),
]

