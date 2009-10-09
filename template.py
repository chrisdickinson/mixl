from elements import MixlRuleNode
from mixl_exceptions import NoSuchRule, CommandSyntaxError 
from commands import MIXL_DEFAULT_COMMANDS
from utils import mixl_import

class MixlRenderState(object):
    context = {}
    commands = []
    visited_nodes = {} 

    def __init__(self, context, commands):
        self.context = context
        self.commands = commands

    def visit(self, template, node):
        if node not in self.visited_nodes.keys():
            self.visited_nodes[node] = node.visit(template, self)
        return self.visited_nodes[node]

    def get_value(self, var):
        if var in self.context.keys():
            return self.context[var]
        return ''

    def define(self, var, value):
        self.context.update({var:value})

    def get_command(self, command):
        """
            process_command(self, <command string>):
                attempt to find a Command object that
                will respond to this command string.
        """
        for registered_command in self.commands:
            if registered_command.match(command):
                return registered_command.function
        raise CommandSyntaxError

    def lookup_rule(self, rule_name, match_function):
        for node in self.visited_nodes.keys():
            if isinstance(node, MixlRuleNode) and match_function(node.name, rule_name):
                return node
        raise NoSuchRule

class MixlTemplate(object):
    def __init__(self, nodes, paths):
        self.nodes = nodes 
        self.references = []
        self.paths = paths

    def register_reference(self, reference_name):
        self.references.append(reference_name)

    def lookup_rule(self, rule_name, state=None, match_function=None):
        match_function = lambda x,y:x==y
        for node in self.nodes:
            if isinstance(node, MixlRuleNode) and match_function(node.name, rule_name):
                return (node, self)
        for reference in self.references:
            try:
                reference_template = mixl_import(reference, self.paths)
                (rule, template) = reference_template.lookup_rule(rule_name, match_function)
                return (rule, template)
            except IOError:
                pass
            except NoSuchRule:
                pass
        raise NoSuchRule

    def visit(self, state):
        len_start = len(self.nodes)
        output = []
        for node in self.nodes:
            output.append(state.visit(self, node))
        return output

    def output(self, context, commands=MIXL_DEFAULT_COMMANDS):
        state = MixlRenderState(context, commands)
        output = self.visit(state)
        return '\n'.join(output)
