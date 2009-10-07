class NoSuchRule(Exception):
    """
        NoSuchRule
            thrown when a Rule object contains a mixin referencing a rule name that doesn't exist.
    """
    pass

class CommandSyntaxError(Exception):
    """
        CommandSyntaxError
            thrown when a preprocessor command fails to parse, or any other generic error while
            processing a command
    """
    pass
