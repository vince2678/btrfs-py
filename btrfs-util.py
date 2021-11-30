import sys
import command
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

    pass