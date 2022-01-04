#!/bin/bash
SNAPSHOT_CMD="python3 /home/vincent/GitHub/btrfs-py/btrfs-util.py snapshot create --recursive"
SNAPSHOT_ROOT="/btrfsroot"

SOURCE_SNAPSHOT="debian-bullseye"
TARGET_SNAPSHOT="snapshots/debian-bullseye_`date +%d-%m-%Y_%H-%M`"

${SNAPSHOT_CMD} ${SNAPSHOT_ROOT}/${SOURCE_SNAPSHOT} ${SNAPSHOT_ROOT}/${TARGET_SNAPSHOT}
