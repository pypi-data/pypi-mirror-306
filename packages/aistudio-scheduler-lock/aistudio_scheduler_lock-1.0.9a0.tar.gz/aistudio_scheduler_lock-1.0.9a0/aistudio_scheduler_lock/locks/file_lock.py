import logging
import os
import sys

from .base_lock import DistributedLock
from .utils import LockUtils

logger = logging.getLogger(__name__)


class FCNTLFileLock(DistributedLock):
    """
    FCNTLFileLock uses Python fcntl module which internally uses system calls like
    'fcntl', 'flock' etc. These system calls are available on most flavours of Linux.
    fcntl: It is used to manipulate file descriptors. Performs operations such as
           duplicating file descriptors, advisory locking, file status flags etc.
           Source: https://man7.org/linux/man-pages/man2/fcntl.2.html
    flock: It is used to apply or remove an advisory lock on an open file.
           Source: https://manpages.debian.org/bullseye/manpages-dev/flock.2.en.html
    ---------------------------- Note on Azure Files -------------------------------
    In Azure, you mount 'Azure File' on Linux VMs which can be used by applications
    directly running on VMs or containers(pods) which run on these VMs. An 'Azure File'
    can be mounted using either SMB protocol or NFS protocol. With the former, fcntl.flock()
    running on more than one machine on the same file will succeed and this NO longer is
    the distributed lock. fcntl.flock() works in the expected way with SMB mounted
    Azure file as long as all the processes are running on the same machine.
    For distributed lock to work with 'Azure File', it has to be mounted with NFS and for
    that to happen, (1) 'Premium' storage account has to be created with 'File shares:' as
    the value for 'Premium account type'. (2) Azure file share you create inside this
    storage account needs to be created with 'NFS' protocol. Without the former, you don't get
    a choice to select the protocol and Azure will create file share with 'SMB' protocol.
    """

    # Even if lock is acquired by another process, can_execute_task method
    # of the base class just returns True, but try_acquire_lock fails.

    def __init__(self, lock_file: str):

        # You can't do this at the top of the file. Reason is, even if
        # FCNTLFileLock never gets instantiated, moment file_lock gets
        # imported in another file, code at the top will execute and
        # program will quit if 'fcntl' module in not found which would
        # be the case on Windows. FCNTLFileLock class gets instantiated
        # only when SCHEDULER_LOCK_TYPE is 'File'.
        # Other option will be to conditionally import file_lock module
        # based on value of SCHEDULER_LOCK_TYPE which is not so nice.
        # Also, since 'fcntl' module is now present at the instance level,
        # we access it in all subsequent methods using 'self.fcntl'.
        try:
            import fcntl

            logger.debug("Module %s imported successfully!", fcntl.__name__)
        except ModuleNotFoundError as e:
            logger.error(f"ModuleNotFoundError: {e}")
            logger.error("SCHEDULER_LOCK_TYPE=File will NOT work on Windows.")
            sys.exit(1)

        self.fcntl = fcntl
        self.lock_file = lock_file
        self.lock_file_fd = None

    def try_acquire_lock(self) -> True:
        fd = None
        try:
            f_exists = os.path.exists(self.lock_file)
            open_mode = os.O_RDWR if f_exists else os.O_RDWR | os.O_CREAT
            fd = os.open(self.lock_file, open_mode, 0o600)

            # LOCK_EX: Place an exclusive lock. Only one process may hold an
            # exclusive lock for a given file at a given time.
            # LOCK_NB: A call to flock() may block if an incompatible lock is
            # held by another process. To make a nonblocking request, include LOCK_NB.
            # Source: https://manpages.debian.org/bullseye/manpages-dev/flock.2.en.html

            self.fcntl.flock(fd, self.fcntl.LOCK_EX | self.fcntl.LOCK_NB)
            owner = LockUtils.get_current_instance_name()
            logger.debug(f"{owner} owns lock on file {self.lock_file}")
            owner_bytes = bytes(owner + "\n", "utf-8")
            os.write(fd, owner_bytes)
            os.truncate(fd, len(owner_bytes))
            self.lock_file_fd = fd
        except (IOError, OSError) as e:
            logger.debug(e)
            if fd is not None:
                logger.debug(f"Lock not obtained, closing {fd}, pid: {os.getpid()}")
                os.close(fd)
            return False
        return True

    # This method actually never gets called.
    # Lock is released only when lock owner dies, shuts down etc.
    # Also, following code is most probably buggy
    def release(self) -> None:

        if not self.lock_file_fd:
            f_exists = os.path.exists(self.lock_file)
            open_mode = os.O_RDWR if f_exists else os.O_RDWR | os.O_CREAT
            fd = os.open(self.lock_file, open_mode, 0o600)
        else:
            fd = self.lock_file_fd
        # Do not remove the lockfile:
        #
        #   https://github.com/benediktschmitt/py-filelock/issues/31
        #   https://stackoverflow.com/questions/17708885/flock-removing-locked-file-without-race-condition
        self.fcntl.flock(fd, self.fcntl.LOCK_UN | self.fcntl.LOCK_NB)
        os.close(fd)

    def renew_lease(self) -> bool:
        # We can possibly use the concept of lease here, by maintaining the
        # validity of the lock in the file. But for now, we don't.
        # We just return true if the lock file is present, else false.
        return bool(os.path.exists(self.lock_file))

    def get_current_owner(self) -> str:
        if os.path.exists(self.lock_file):
            with open(self.lock_file) as f:
                return f.read().strip()
        else:
            return "Lock file does not exist. Unable to fetch lock owner."
