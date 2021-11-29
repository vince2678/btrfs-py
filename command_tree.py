class Command:
    def __init__(self, name, expected_args = 0, flags = [], subcommands = [], help = "") -> None:

        if expected_args > 0 and len(subcommands) > 0:
            raise Exception("Expected args and subcommands are mutually exclusive")

        self.name = name
        self.expected_args = set(expected_args)
        self.flags = flags
        self.subcommands = {v.name:v for v in subcommands}
        #self.subcommands = subcommands
        self.help = help

    def height(self) -> int:
        ''' Return the max height of the graph
        '''
        return 1 + max([c.height() for c in self.subcommands])
    
    def add_subcommand(self, command) -> None:
        '''
        '''
        self.subcommands[command.name] = command
    
    def add_flag(self, flag) -> None:
        self.flags.add(flag)

class CommandResult:
    def __init__(self, name, args = [], flags = dict(), subcommand_results = []) -> None:
        self.name = name
        self.args = args
        self.flags = set(flags)
        self.subcommand_results = {v.name:v for v in subcommand_results}
        #self.subcommand_results = subcommand_results

class CommandTree:

    def __init__(self, commands, args = None) -> None:

        self.commands = commands

        if args == None:
            import sys
            self.args = list(sys.argv[1:])
        else:
            self.args = list(args)

    def parse_args(self) -> list:
        '''
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
            if arg in command.flags:
                res.flags.add(arg)
            # check if the arg is a subcommand
            elif arg in command.subcommands:
                subcommand_result = self._parse_args(command.subcommand[arg], args[1:])
                # process subcommand
                if subcommand_result:
                    res.subcommand_results[subcommand_result.name] = subcommand_result
                break
            # save arg if we're expecting any
            elif command.expected_args > 0:
                res.args.append(arg)
            # user did something stupid
            else:
                raise Exception("Command {} got unexpected argument {}"\
                    .format(command.name, arg))

            i = i + 1
            
        if len(res.args) != command.expected_args:
            raise Exception("Command {} expected {} args, {} given"\
                .format(command.name, command.expected_args, len(args) - 1))

        return res
