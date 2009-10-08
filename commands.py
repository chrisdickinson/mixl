import re
from utils import mixl_import
from elements import Command, MixlRuleNode
from mixl_exceptions import CommandSyntaxError
 
MIXL_IMPORT_REGEX = re.compile('import "(?P<filename>.+?)"( (?P<silently>silently)?)?')
MIXL_DEFINE_REGEX = re.compile('define (?P<variable_name>[\w\-]+)\s*:(?P<value>.*)')
MIXL_SYNTH_RULES_REGEX = re.compile('synth-rules (?P<class_name>.+) with \{(?P<block>.+)\} for (?P<variable_name>\w+) in \[(?P<variable_list>.*)\]')
def mixl_command_import(template, state, command):
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
    output = ''
    if match is not None:
        matches = match.groupdict()
        filename = matches['filename']
        silently = matches['silently'] is not None
        template.register_reference(filename)
        reference_template = mixl_import(filename, template.paths)
        results = reference_template.visit(state)
        if not silently:
            output = '\n'.join(results)
    else:
        raise CommandSyntaxError()
    return output

def mixl_define(template, state, command):
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
        state.context.update({var_name:value})    
    else:
        raise CommandSyntaxError()
    return ''

def mixl_synth_rules(template, state, command):
    match = MIXL_SYNTH_RULES_REGEX.match(command)
    if match is not None:
        matches = match.groupdict()
        class_name_base = matches['class_name']
        block = matches['block']
        variable_name = matches['variable_name']
        variable_list = matches['variable_list'].strip().split(' ')
        old_variable_value = None

        if variable_name in state.context.keys():
            old_variable_value = state.context[variable_name]

        for variable in variable_list:
            if variable not in state.context.keys():
                continue
            state.context[variable_name] = state.context[variable]
            rule_name = "%s%s" % (class_name_base, variable)
            new_rule = MixlRuleNode(rule_name, block)
            new_rule.block = new_rule.parse_block(template, state)
            state.visit(template, new_rule)
        if old_variable_value is not None:
            state.context[variable_name] = old_variable_value
    return ''

MIXL_DEFAULT_COMMANDS = [
    Command('import', mixl_command_import),
    Command('define', mixl_define),
    Command('synth-rules', mixl_synth_rules),
]

