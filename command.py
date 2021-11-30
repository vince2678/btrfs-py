class ArgumentError(Exception):
    pass

class UnexpectedArgumentError(ArgumentError):
    pass

class MissingArgumentError(ArgumentError):
    pass

class CommandResult:
    def __init__(self) -> None:
        '''
        '''
        self.commands = []
        self.args = []
        self.flags = []

    def extend(self, other) -> None:
        '''
        '''
        self.commands.extend(other.commands)
        self.args.extend(other.args)
        self.flags.extend(other.flags)

class Command:

    def __init__(self, name, expected_args = 0, flags = [], subcommands = []) -> None:
        ''' Initialise a Command with name, accepting expected_args as the count
            of positional arguments, and taking flags, with subcommands.

            If expected_args is < 0, accept at least 1 arg
        '''

        if expected_args != 0 and len(subcommands) > 0:
            raise ValueError("Expected args and subcommands are mutually exclusive")

        self.name = name
        self.expected_args = expected_args
        self.flags = flags
        self.subcommands = {v.name:v for v in subcommands}
    
    def add_subcommand(self, command) -> None:
        '''
        '''
        self.subcommands[command.name] = command

    def add_flag(self, flag) -> None:
        self.flags.add(flag)

    def parse_args(self, args) -> CommandResult:
        ''' Parse args specified, where args is an iterable, and
            return a list of CommandResult, or None if parsing failed.

            If args is not specified, sys.argv is used
        '''
        if len(args) == 0:
            import sys
            c_args = list(sys.argv[1:])
        else:
            c_args = list(args)

        if self.name != c_args[0]:
            return None 

        result = CommandResult()
        result.commands.append(self.name)

        i = 1
        while i < len(c_args):
            arg = c_args[i]

            # check if arg is a flag.
            # we should allow flags for the parent cmd to come
            # before subcommands, and not the other way round
            if arg in self.flags:
                result.flags.append(arg)
            # check if subcommand
            elif self.expected_args == 0 and arg in self.subcommands:

                # if we got any args in the result, we should throw an exception
                if len(result.args) != 0:
                    raise UnexpectedArgumentError("Unexpected argument(s) {}"\
                        .format(', '.join(result.args)))

                # if we got a value then we've finished processing
                r = self.subcommands[arg].parse_args(c_args[i:])
                result.extend(r)
                return result

            #  check if we got an unexpected # of args
            elif self.expected_args >= 0 and len(result.args) + 1 > self.expected_args:
                raise UnexpectedArgumentError("Command {} got unexpected argument {}"\
                    .format(self.name, arg))
            else:
                result.args.append(arg)

            i = i + 1

        if self.expected_args < 0 and len(result.args) == 0:
            raise MissingArgumentError("Command {} expected at least 1 arg, none given"\
                .format(self.name))
        elif len(result.args) < self.expected_args:
            raise MissingArgumentError("Command {} expected {} args, {} given"\
                .format(self.name, self.expected_args, len(result.args)))

        return result