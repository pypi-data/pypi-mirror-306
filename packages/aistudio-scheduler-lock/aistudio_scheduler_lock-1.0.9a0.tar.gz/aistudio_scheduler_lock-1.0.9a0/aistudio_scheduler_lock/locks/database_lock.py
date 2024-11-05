import logging
import os

from django.db import IntegrityError

from .base_lock import DistributedLock
from .utils import LockUtils

logger = logging.getLogger(__name__)


class DatabaseLock(DistributedLock):
    def __init__(self, name, lease_time, record_id):
        self.lock_name = name
        self.lock_owner = LockUtils.get_current_instance_name()
        # Time in milliseconds
        self.lease_time = lease_time * 1000
        self.record_id = record_id
        self.fencing_token_id = -1

    def can_execute_task(self) -> bool:
        """
        Returns True if process lock owner name and the one in the database
        is the same, returns False otherwise. We implement this function to
        handle possible concurrency issues - refer to the comment in models.py
        for details.
        """
        from aistudio_scheduler_lock.models import SchedulerLock

        try:
            SchedulerLock.objects.get(lock_id=self.record_id, owner=self.lock_owner)
            return True
        except Exception as e:
            logger.error(
                f"Process: {os.getpid()} {self.lock_owner} is not lock owner, but still trying "
                f"to execute a scheduled job, error: {e}"
            )
            return False

    def _get_valid_until(self) -> int:
        return LockUtils.get_epochtime_in_millis() + self.lease_time

    def _acquire_lock(self) -> bool:
        return self._do_acquire_lock()

    def _do_acquire_lock(self) -> bool:
        from aistudio_scheduler_lock.models import SchedulerLock

        try:
            sl = SchedulerLock(
                lock_id=self.record_id,
                name=self.lock_name,
                owner=self.lock_owner,
                valid_until=self._get_valid_until(),
            )
            sl.save()
            self.fencing_token_id = sl.fencing_token_id
            logger.debug(
                f"lock acquired by {self.lock_owner}, "
                f"fencing_token_id: {sl.fencing_token_id}"
            )
            return True
        except IntegrityError as e:
            logger.debug(
                f"Error when {self.lock_owner} tried to acquire the lock, lock already "
                f"held by someone else: {e}"
            )
            return False
        except Exception as e:
            logger.error(f"Error when {self.lock_owner} tried to acquire the lock: {e}")
            return False

    # When one tries to acquire the lock, there are 3 possibilities
    # 1. There is no row in the lock table; you can try to insert the row in the lock
    #    table. If insert succeeds, you have the lock.
    # 2. There is already a row in the lock table and lock lease is valid, i.e.
    #    valid_until > epoch_time_in_milliseconds. In this case, don't try to
    #    acquire the lock. Typically, if you own the lock, you woudln't be calling
    #    this method.
    # 3. There is already a row in the lock table but lock lease has expired.
    #    Delete the row and try to insert a new one. If insert succeeds, you have the lock.
    def try_acquire_lock(self) -> bool:
        from aistudio_scheduler_lock.models import SchedulerLock

        try:
            record = SchedulerLock.objects.get(lock_id=self.record_id)
            if record.valid_until < LockUtils.get_epochtime_in_millis():
                record.delete()
                if self._acquire_lock():
                    return True
            else:
                logger.debug(
                    f"valid lock held by, OWNER: {record.owner}, EXPIRY: {record.valid_until}"
                )
                return False
        except Exception as e:
            logger.error(f"Error when {self.lock_owner} tried to query lock: {e}")
            if self._acquire_lock():
                return True
        return False

    def renew_lease(self) -> bool:
        return self._do_renew_lease()

    def _do_renew_lease(self) -> bool:
        from aistudio_scheduler_lock.models import SchedulerLock

        # renew lease ONLY if you are the owner of the lock
        try:
            record = SchedulerLock.objects.get(
                lock_id=self.record_id, owner=self.lock_owner
            )
            record.valid_until = self._get_valid_until()
            record.save()
            self.fencing_token_id = record.fencing_token_id
            return True
        except Exception as e:
            logger.error(
                f"Trying to renew a lock which does not exist {os.getpid()}, Error: {e}"
            )
            return False

    def get_current_owner(self) -> str:
        from aistudio_scheduler_lock.models import SchedulerLock

        try:
            return SchedulerLock.objects.get().owner
        except Exception as exc:
            logger.exception(exc)
            return "Exception occured. Unable to fetch lock owner."
