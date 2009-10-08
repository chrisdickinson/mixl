import re
from elements import *
from mixl_exceptions import NoSuchRule, CommandSyntaxError

MIXL_COMMAND_CHAR = '%'

def parse(contents):
    """
        parse(self, contents):
            the dumb-as-rocks parser workhorse. knows only two modes,
            "look for a rule", and "finish this rule's block".
            when in "look for a rule" mode, it will also pay attention to
            preprocessor commands.

            returns a list of rules.
    """

    file_length = len(contents)
    BLOCK_SEARCH = 0
    BLOCK_FINISH = 1
    mode = BLOCK_SEARCH
    search_start = 0
    block_start = 0
    last_char = None
    index = 0
    nodes = []

    while index < file_length:
        char = contents[index]
        if mode == BLOCK_SEARCH and last_char in ("\n",' ', "\t", None) and char == MIXL_COMMAND_CHAR:
            line_end = contents.find('\n', index+1)
            cmd = contents[index+1:line_end]
            nodes.append(MixlCommandNode(cmd))
            index += line_end - index 
            search_start = index
            continue
        elif mode == BLOCK_SEARCH:
            if char == '{':
                name = contents[search_start:index]
                block_start = index+1
                mode = BLOCK_FINISH
        elif mode == BLOCK_FINISH:
            if char == '}':
                search_start = index+1
                block = contents[block_start:index]
                nodes.append(MixlRuleNode(name, block))
                mode = BLOCK_SEARCH
        index += 1
        last_char = char
    return nodes
