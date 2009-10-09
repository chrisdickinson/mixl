from django.test import TestCase
from elements import *
from mixl_exceptions import *
from commands import *
from template import *
from parser import *

class ParserTests(TestCase):
    def test_unclosed_brace(self):
        unclosed_brace_end = "a { color:red; } b {background:red;"
        unclosed_brace_begin = "} a { color:red; }"

        end_results = parse(unclosed_brace_end)
        begin_results = parse(unclosed_brace_begin)
        
        self.assertEqual(len(end_results), 1)
        self.assertEqual(len(begin_results), 1)
        self.assertTrue(isinstance(end_results[0], MixlRuleNode))
        self.assertTrue(isinstance(begin_results[0], MixlRuleNode))
        self.assertEqual(getattr(begin_results[0], 'name', None), '} a')
        self.assertEqual(getattr(end_results[0], 'name', None), 'a')

    def test_create_nodes(self):
        node_test = """
            %cmd_node
            rule_node { }
        """
        results = parse(node_test)
        self.assertEqual(len(results), 2)
        self.assertTrue(isinstance(results[0], MixlCommandNode))
        self.assertEqual(getattr(results[0], 'command_string', None), 'cmd_node')
        self.assertTrue(isinstance(results[1], MixlRuleNode))
        self.assertEqual(getattr(results[1], 'name', None), 'rule_node')
        self.assertEqual(getattr(results[1], 'block', None), ' ')

class TemplateStateTests(TestCase):
    def test_get_command(self):
        pass

    def test_visit_node(self):
        pass

    def test_lookup_rule(self):
        pass

class TemplateTests(TestCase):
    pass

class CommandTests(TestCase):
    def test_command_import(self):
        bad_command = 'import gary busey poorly'
        good_command = 'import "test.css"'
        good_command_silently = 'import "test.css" silently'
        good_command_no_file = 'import "dne.css"'
        
        expected_triggers = {
            'register_reference': [],
            'visit': [],
        }

        class MockTemplate(MixlTemplate):
            def register_reference(self, filename):
                expected_triggers['register_reference'].append(True)
                return super(MockTemplate, self).register_reference(state)
            def visit(self, state):
                expected_triggers['visit'].append(True)
                return super(MockTemplate, self).visit(state)
        def mock_mixl_import_good(filename, paths):
            return MockTemplate([MixlRuleNode('a', 'background: red;'),], paths)
        template = MockTemplate([], [])
        state = MixlRenderState({}, MIXL_DEFAULT_COMMANDS) 

        self.assertRaises(CommandSyntaxError, mixl_command_import, template=template, state=state, command=bad_command)
        good_results = mixl_command_import(template, state, good_command, mock_mixl_import_good)
        good_results_silently = mixl_command_import(template, state, good_command_silently, mock_mixl_import_good)
        self.assertRaises(IOError, mixl_command_import, template,state,good_command_no_file)
        self.assertEqual(len(expected_triggers['register_reference']), 3)
        self.assertEqual(len(expected_triggers['visit']), 2)
        self.assertEqual(good_results, 'a { background: red; }')
        self.assertEqual(good_results_silently, '')

    def test_command_define(self):
        bad_command = 'define asdf'
        good_command = 'define asdf:asdf'
        expected_triggers = {
            'define':[],
        }
        class MockTemplateState(MixlRenderState):
            def define(self, var, value):
                expected_triggers['define'].append(True)
                return super(MockTemplateState, self).define(var, value)
        template = MixlTemplate([], [])
        self.assertRaises(CommandSyntaxError, mixl_define, template, MockTemplateState({}, MIXL_DEFAULT_COMMANDS), bad_command)
        mock_state = MockTemplateState({}, MIXL_DEFAULT_COMMANDS)
        mixl_define(template, mock_state, good_command)
        self.assertEqual(len(expected_triggers['define']), 1)
        self.assertEqual(mock_state.get_value('asdf'), 'asdf')
        self.assertEqual(mock_state.get_value('dne'), '')

    def test_command_synth_rules(self):
        pass

class RenderStateTests(TestCase):
    def test_get_command(self):
        expected_triggers = {
            'cmd_matcher':[],
        }
        def simple_cmd(template, state, command):
            return ''
        def cmd_matcher(test):
            expected_triggers['cmd_matcher'].append(True)
            return test.startswith('complex') 
        cmd = Command('simple', simple_cmd)
        complex_cmd = Command('complex_match', simple_cmd, cmd_matcher)
        state = MixlRenderState({}, [cmd, complex_cmd])
        self.assertEqual(state.get_command('simple'), simple_cmd)
        self.assertRaises(CommandSyntaxError, state.get_command, 'sim')
        self.assertEqual(state.get_command('complex'), simple_cmd)
        self.assertEqual(len(expected_triggers['cmd_matcher']), 2) 

    def test_lookup_rule(self):
        expected_triggers = {
            'match_function':[],
        }
        def match_function(lhs, rhs):
            expected_triggers['match_function'] = True
            return lhs == rhs 

        rule_list = [
            MixlRuleNode('name1', 'block1'),
            MixlRuleNode('name2', 'block2'),
        ]

        state = MixlRenderState({}, [])
        template = MixlTemplate(rule_list, [])
        template.visit(state)

        default_match = lambda x,y: x==y
        self.assertEqual(state.lookup_rule('name1', default_match), rule_list[0])
        self.assertEqual(state.lookup_rule('name2', default_match), rule_list[1])
        self.assertEqual(state.lookup_rule('name2', match_function), rule_list[1])
        self.assertEqual(expected_triggers['match_function'], True)
        self.assertRaises(NoSuchRule, state.lookup_rule, 'name3', default_match)
