from abc import ABC, abstractmethod


class DistributedLock(ABC):
    def can_execute_task(self) -> bool:
        # This method is not strictly needed if try_acquire_lock function
        # is implemented correctly. It is used only in certain cases, for e.g.
        # in DatabaseLock and DatabaseAdvisoryLock to check for lock ownership.
        return True

    @abstractmethod
    def try_acquire_lock(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def renew_lease(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_current_owner(self) -> str:
        raise NotImplementedError()
