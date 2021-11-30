import unittest
from command import *
#from .. import command_tree as c_tree

class TestCases(unittest.TestCase):

    def test_conflicting_args(self) -> None:
        '''
        '''

        subcommands = []
        subcommands.append(Command("delete", -1, flags = ["--recursive", "-R"]))
        subcommands.append(Command("create", 2, ["-r", "-R", "--recursive", "--read-only"]))

        with self.assertRaises(ValueError):
            Command("snapshot", 3, subcommands=subcommands)

    def test_argument_errors(self) -> None:
        '''
        '''

        subcommands = []
        subcommands.append(Command("delete", -1, flags = ["--recursive", "-R"]))
        subcommands.append(Command("create", 2, ["-r", "-R", "--recursive", "--read-only"]))

        parent_command = Command("snapshot", subcommands=subcommands)
        # snapshot create [-R|--recursive]|[-r|--read-only] [source] [dest]

        with self.assertRaises(MissingArgumentError):
            parent_command.parse_args("snapshot", "create")

        with self.assertRaises(MissingArgumentError):
            parent_command.parse_args("snapshot", "create", "-R")

        with self.assertRaises(MissingArgumentError):
            parent_command.parse_args("snapshot", "create", "-R", "/")

        with self.assertRaises(ArgumentCountError):
            parent_command.parse_args("snapshot", "create", "/source", "/target", "/target")

        with self.assertRaises(MissingArgumentError):
            parent_command.parse_args("snapshot", "delete", "-R")

        with self.assertRaises(MissingArgumentError):
            parent_command.parse_args("snapshot", "delete")

    def test_command_result(self) -> None:
        '''
        '''
        subcommands = []
        subcommands.append(Command("delete", -1, flags = ["--recursive", "-R"]))
        subcommands.append(Command("create", 2, ["-r", "-R", "--recursive", "--read-only"]))

        parent_command = Command("snapshot", subcommands=subcommands)

        parsed = parent_command.parse_args("snapshot", "create", "-R", "/source", "/target")

        self.assertEqual(len(parsed.args), 2)
        self.assertEqual(parsed.args[0], "/source")
        self.assertEqual(parsed.args[1], "/target")
        self.assertEqual(parsed.)

        parsed = parent_command.parse_args("snapshot", "create", "/source", "/target")
        parsed = parent_command.parse_args("snapshot", "delete", "/snapshot")
        parsed = parent_command.parse_args("snapshot", "delete", "-R", "/snapshot")
        parsed = parent_command.parse_args("snapshot", "delete", "-R", "/snapshot1", "/snapshot2")

if __name__ == "__main__":
    unittest.main()