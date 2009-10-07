from django.test import TestCase
from parser import Parser, ParserReference
from elements import *
from exceptions import *

class ParserTests(TestCase):
    def test_unclosed_brace(self):
        unclosed_brace_end = "a { color:red; } b {background:red;"
        parser = Parser(unclosed_brace_end)
        self.assertEqual(parser.output(), "a {  color:red; }\n")
        unclosed_brace_begin = "} a { color:red; }"

        parser = Parser(unclosed_brace_begin)
        self.assertEqual(parser.output(), "} a {  color:red; }\n")

    def test_variable_insertion(self):
        variable_insertion = "a {color:<var>;}"
        variable_insertion_no_result = "a {color:<undefined_var>;}"
        variable_insertion_outside_of_block = "<var> a {color:#FF0000;}"
        variable_dict = {
            'var':'#FFF',
        }
        parser_tests = [
            (Parser(variable_insertion, context=variable_dict),                                 "a {  color:#FFF; }\n"),
            (Parser(variable_insertion_no_result, context=variable_dict),                       "a {  color:; }\n"),
            (Parser(variable_insertion_outside_of_block, context=variable_dict),                "<var> a {  color:#FF0000; }\n"),
        ]

        for parser, result in parser_tests:
            self.assertEqual(parser.output(), result)

    def test_command_execution(self):
        output_value = False
        def cmd(parser, command):
            output_value = True
        commands = (Command('flag', cmd), )
        test_command_executes = """
            %flag
            a { color:red; }
        """
        test_command_fails = """
            %does_not_exist
            a { color:red; }
        """
        parser = Parser(test_command_executes, commands=commands)
        result = "a {  color:red; }\n"
        self.assertEqual(parser.output(), result)
        self.assertRaises(CommandSyntaxError, Parser, string=test_command_fails, commands=commands)

    def test_lookup_rules(self):
        rule_parse = ".rule { color:red; }"
        parser = Parser(rule_parse)
        rule = parser.find_rule('.rule')
        self.assertEqual(rule.block, "color:red;")
        self.assertEqual(rule.name, ".rule")
        self.assertRaises(NoSuchRule, parser.find_rule, '.does-not-exist')
        parser_ref = ParserReference('fake-file.css', silent=False)
        parser_ref.parser_object = Parser(".subparser-rule { color:red; }")
        parser.parser_refs = [parser_ref,]
        rule = parser.find_rule('.subparser-rule')
        self.assertEqual(rule.block, 'color:red;')
        self.assertEqual(rule.name, '.subparser-rule')

    def test_empty_string(self):
        empty_string = ""
        parser = Parser(empty_string)
        self.assertEqual(parser.output(), "")
