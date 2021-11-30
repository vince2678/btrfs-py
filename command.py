class ArgumentError(Exception):
    pass

class UnexpectedArgumentError(ArgumentError):
    pass

class MissingArgumentError(ArgumentError):
    pass

class ArgumentCountError(ArgumentError):
    pass

class CommandResult:
    def __init__(self, commands, args = [], flags = []) -> None:
        '''
        '''
        self.commands = commands
        self.args = args
        self.flags = flags

#class Flag:
#    def __init__(self, flag, *aliases) -> None:
#        ''' Initialise a flag, and any aliases
#        '''

class Command:

    def __init__(self, name, expected_args = 0, flags = [], subcommands = [], help = "") -> None:
        ''' Initialise a Command with name, accepting expected_args as the count
            of positional arguments, and taking flags, with subcommands.

            If expected_args is < 0, accept at least 1 arg
        '''

        if expected_args > 0 and len(subcommands) > 0:
            raise ValueError("Expected args and subcommands are mutually exclusive")

        self.name = name
        self.expected_args = expected_args
        self.flags = flags
        self.subcommands = {v.name:v for v in subcommands}
        #self.subcommands = subcommands
        self.help = help

    def height(self) -> int:
        ''' Return the max height of the graph
        >>> c = Command("test")
        >>> c.height()
        1
        >>> c.add_subcommand(Command("new"))
        >>> c.height()
        2
        '''
        maxHeight = 0

        for c in self.subcommands.values():
            h = c.height()

            if maxHeight < h:
                maxHeight = h

        return 1 + maxHeight
    
    def add_subcommand(self, command) -> None:
        '''
        '''
        self.subcommands[command.name] = command

    def add_flag(self, flag) -> None:
        self.flags.add(flag)

    def parse_args(self, *args) -> CommandResult:
        ''' Parse args specified, where args is an iterable, and
            return a list of CommandResult.

            If args is not specified, sys.argv is used
        '''
        return CommandTree(self, args).parse_args()

class CommandTree:

    def __init__(self, commands, *args) -> None:

        self.commands = commands

        if len(args) == 0:
            import sys
            self.args = list(sys.argv[1:])
        else:
            self.args = list(args)

    def parse_args(self) -> list:
        ''' Parse args specified, where args is an iterable, and
            return a list of CommandResult.

            If args is not specified, sys.argv is used
        '''
        ret = []

        for command in self.commands:
            result = self._parse_args(command, self.args)
            if result:
                ret.append(result)

#        return [self._parse_args(c, self.args) for c in self.commands]
        return ret

    def _parse_args(self, command, args) -> CommandResult:
        '''
        '''

        #if not command.name.startswith(args[0]):
        if command.name != args[0]:
            return None

        res = CommandResult(command.name)

        i = 1
        while i < len(args):
            arg = args[i]
            # check if any of the following args are flags
            if arg in command.flags: #TODO: Flags strictly should come before required  args
                res.flags.add(arg)
            # check if the arg is a subcommand
            elif arg in command.subcommands:
                subcommand_result = self._parse_args(command.subcommand[arg], args[1:])
                # process subcommand
                if subcommand_result:
                    res.subcommand_results[subcommand_result.name] = subcommand_result
                break
            # save arg if we're expecting any
            elif command.expected_args < 0:
                res.args.extend(args[i:])
                break
            elif command.expected_args > 0:
                res.args.append(arg)
            # user did something stupid
            else: #TODO: Is this necessary/reachable?
                raise UnexpectedArgumentError("Command {} got unexpected argument {}"\
                    .format(command.name, arg))

            i = i + 1
            
        if command.expected_args < 0 and len(res.args) == 0:
            raise MissingArgumentError("Command {} expected at least 1 arg, none given"\
                .format(command.name))
        elif len(res.args) != command.expected_args:
            raise ArgumentCountError("Command {} expected {} args, {} given"\
                .format(command.name, command.expected_args, len(args) - 1))

        return res