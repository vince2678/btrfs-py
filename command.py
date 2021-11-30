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

    def extend(self, other) -> None:
        '''
        '''
        self.commands.extend(other.commands)
        self.args.extend(other.args)
        self.flags.extend(other.flags)

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
    
    def add_subcommand(self, command) -> None:
        '''
        '''
        self.subcommands[command.name] = command

    def add_flag(self, flag) -> None:
        self.flags.add(flag)

    def parse_args(self, *args) -> CommandResult:
        ''' Parse args specified, where args is an iterable, and
            return a list of CommandResult, or None if parsing failed.

            If args is not specified, sys.argv is used
        '''
        return CommandTree(self, args).parse_args()

class CommandTree:

    def __init__(self, commands, *args) -> None:
        '''
        '''
        self.commands = {c.name:c for c in commands}

        if len(args) == 0:
            import sys
            self.args = list(sys.argv[1:])
        else:
            self.args = list(args)

    def parse_args(self) -> CommandResult:
        ''' Parse args specified, where args is an iterable, and
            return a list of CommandResult.

            If args is not specified, sys.argv is used
        '''
        key = self.args
        if key in self.commands.keys():
            return self._parse_args(self.commands[key], self.args)
        
        return None

    def _parse_args(self, command, args) -> CommandResult:
        '''
        '''
        #if not command.name.startswith(args[0]):

        commands = []
        args = []
        flags = []


        i = 1
        while i < len(args):
            arg = args[i]

            # check if flag
            if arg in command.flags:
                flags.append(arg)
            # check if subcommand
            elif arg in command.subcommands:
                r = command.subcommands[arg].parse_args()

                if r:
                    commands.extend(r.commands)
                    args.extend(r.args)
                    flags.extend(r.flags)



        return CommandResult(commands, args, flags)

        ##################

        i = 1
        while i < len(args):
            arg = args[i]
            # check if any of the following args are flags
            if arg in command.flags: #TODO: Flags strictly should come before required  args
                result.flags.add(arg)
            # check if the arg is a subcommand
            elif arg in command.subcommands:
                subcommand_result = self._parse_args(command.subcommand[arg], args[1:])
                # process subcommand
                if subcommand_result:
                    result.extend(subcommand_result)
                break
            # save arg if we're expecting any
            elif command.expected_args < 0:
                result.args.extend(args[i:])
                break
            elif command.expected_args > 0:
                result.args.append(arg)
            # user did something stupid
            else: #TODO: Is this necessary/reachable?
                raise UnexpectedArgumentError("Command {} got unexpected argument {}"\
                    .format(command.name, arg))

            i = i + 1
            
        if command.expected_args < 0 and len(result.args) == 0:
            raise MissingArgumentError("Command {} expected at least 1 arg, none given"\
                .format(command.name))
        elif len(result.args) != command.expected_args:
            raise ArgumentCountError("Command {} expected {} args, {} given"\
                .format(command.name, command.expected_args, len(args) - 1))

        return result