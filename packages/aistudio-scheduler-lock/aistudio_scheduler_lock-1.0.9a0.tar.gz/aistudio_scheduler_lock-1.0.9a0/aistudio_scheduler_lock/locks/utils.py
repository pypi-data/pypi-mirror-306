import os
import socket
import time
import uuid


class LockUtils:
    @staticmethod
    def get_pid() -> int:
        return os.getpid()

    @staticmethod
    def get_hostname() -> str:
        return socket.gethostname()

    @staticmethod
    def get_mac_address() -> str:
        return hex(uuid.getnode())

    @classmethod
    def get_current_instance_name(cls) -> str:
        """
        Returns name of the current instance in the format: process_id:mac_id:hostname.
        In case the current instance gets the lock, this will be the lock owner name.

        With containers, chances of process id being same are quite high.
        In fact, if your program is main docker process, its process id will mostly be 1.
        Even with machines, there is a possibility, though rare, that two processes
        running on two different machines will have same process id.
        """
        return f"{cls.get_pid()}:{cls.get_mac_address()}:{cls.get_hostname()}"

    @staticmethod
    def get_epochtime_in_millis() -> int:
        MILLION = 1000000
        return int(time.time_ns() / MILLION)
