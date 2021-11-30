import sys
from command import *
import btrfsutil

def usage():
    print("usage: {} ...".format(sys.argv[0]))
    exit(1)

def is_subvolume(path) -> bool:
    ''' Check whether path is a subvolume
    '''
    return btrfsutil.is_subvolume(path)

def create_snapshot(source, dest, recursive = False, read_only = False) -> None:
    ''' Create a new snapshot
    '''
    btrfsutil.create_snapshot(source, dest, recursive, read_only)

def delete_subvolume(path, recursive = False) -> None:
    ''' Delete a subvol or snapshot
    '''
    btrfsutil.delete_subvolume(path, recursive)

def is_subvolume_read_only(path) -> bool:
    ''' Check if subvolume is read only
    '''
    return btrfsutil.get_subvolume_read_only(path)

def set_subvolume_read_only(path, read_only = True) -> bool:
    ''' Set the subvolume read_only (or not) and return
        True if operation is completed successfully
    '''
    btrfsutil.set_subvolume_read_only(path, read_only)
    return is_subvolume_read_only(path) == read_only

def subvolume_path(path) -> str:
    ''' Get the path of a subvol relative to the fs root
    '''
    return btrfsutil.subvolume_info(path)

def start_sync(path) -> int:
    ''' Start a sync on a btrfs fs and return the transaction id
    '''
    return btrfsutil.start_sync(path)

def sync(path) -> None:
    ''' Sync a specific btrfs fs
    '''
    btrfsutil.sync(path)

def wait_sync(path, transaction_id = 0) -> None:
    ''' Wait for a transaction to sync
    '''
    btrfsutil.wait_sync(path, transaction_id)

#commands = []
#commands.append(command_tree.Command("snapshot", 2)))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()

    subcommands = []
    subcommands.append(Command("delete", -1, flags = ["--recursive", "-R"]))
    subcommands.append(Command("create", 2, ["-r", "-R", "--recursive", "--read-only"]))

    parent_command = Command("snapshot", subcommands=subcommands)

    result = parent_command.parse_args()
    if not result:
        usage()

    read_only = False
    recursive = False

    if '-R' in result.flags or '--recursive' in result.flags:
        recursive = True
        read_only = False
    elif '-r' in result.flags or '--readonly' in result.flags:
        read_only = True
        recursive = False

    if result.commands[1] == "create":
        source = result.args[0]
        dest = result.args[1]

        if not is_subvolume(source):
            print("{} is not a subvolume".format(source))
            exit(1)

        create_snapshot(source, dest, recursive=recursive, read_only=read_only)
    elif result.commands[1] == "delete":
        ret = 0
        for path in result.args:
            if is_subvolume(path):
                delete_subvolume(path, recursive=recursive)
            else:
                print("{} is not a subvolume".format(path))
                ret = 1

        exit(ret)