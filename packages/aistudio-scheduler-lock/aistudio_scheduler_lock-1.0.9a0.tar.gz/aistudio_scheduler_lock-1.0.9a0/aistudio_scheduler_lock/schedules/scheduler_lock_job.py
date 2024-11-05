import importlib
import logging
import os
import time
from datetime import datetime
from typing import Callable, Type

from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig, apps
from django.conf import settings

from aistudio_scheduler_lock.locks.database_advisory_lock import DatabaseAdvisoryLock
from aistudio_scheduler_lock.locks.database_lock import DatabaseLock
from aistudio_scheduler_lock.locks.file_lock import FCNTLFileLock

from .enums import ScheduleType
from .schedules_master_base import ScheduleDict, SchedulesMasterBase

logger = logging.getLogger(__name__)


class SchedulerLockJob:
    # Am I owner of the lock
    lock_owner = False
    lock = None
    if settings.SCHEDULER_LOCK_TYPE == "Database":
        lock = DatabaseLock(
            settings.SCHEDULER_LOCK_NAME,
            settings.SCHEDULER_LOCK_LEASE_TIME,
            settings.SCHEDULER_LOCK_RECORD_ID,
        )
    elif settings.SCHEDULER_LOCK_TYPE == "Database_Advisory":
        lock = DatabaseAdvisoryLock(
            settings.SCHEDULER_LOCK_NAME,
            settings.SCHEDULER_LOCK_LEASE_TIME,
            settings.SCHEDULER_LOCK_RECORD_ID,
        )
    elif settings.SCHEDULER_LOCK_TYPE == "File":
        lock = FCNTLFileLock(
            os.path.join(settings.LOCK_FILE_BASE_PATH, "aistudio.lock")
        )
    else:
        raise Exception(
            f"Scheduler lock type {settings.SCHEDULER_LOCK_TYPE} not supported."
        )

    jobs = {"global_schedules": [], "local_schedules": []}

    # Time when schedules were last newly loaded/reloaded in this instance
    last_updated_on = None

    @staticmethod
    def get_schedules_master() -> Type[SchedulesMasterBase]:
        schedules_class_str = settings.SCHEDULES_MASTER_CLASS
        schedules_class_listified = schedules_class_str.split(".")
        module_name = ".".join(schedules_class_listified[:-1])
        class_name = schedules_class_listified[-1]

        module = importlib.import_module(module_name)

        return getattr(module, class_name)

    @staticmethod
    def add_schedule(scheduler_lock_app: AppConfig, schedule_dict: ScheduleDict) -> Job:
        schedule = scheduler_lock_app.scheduler.add_job(
            name=schedule_dict["name"],
            func=schedule_dict["func"],
            trigger=schedule_dict["trigger"],
            max_instances=schedule_dict["max_instances"],
            **schedule_dict["trigger_params"],
        )
        logger.debug(
            f"added job: process {os.getpid()}, added jobid: {schedule.id}, job name: {schedule.name}"
        )
        return schedule

    @staticmethod
    def remove_schedule(scheduler_lock_app: AppConfig, schedule: Job) -> None:
        try:
            scheduler_lock_app.scheduler.remove_job(schedule.id)
        except Exception as e:
            logger.error(
                f"Error removing job: process {os.getpid()}, jobid: {schedule.id}, job name: {schedule.name}"
            )
            logger.exception(e)
        else:
            logger.debug(
                f"removed job: process {os.getpid()}, removed jobid: {schedule.id}, job name: {schedule.name}"
            )

    @classmethod
    def add_all_schedules(
        cls, scheduler_lock_app: AppConfig, SchedulesMaster: Type[SchedulesMasterBase]
    ) -> None:
        if cls.lock_owner:
            cls.add_schedules(
                scheduler_lock_app, SchedulesMaster, schedule_type=ScheduleType.GLOBAL
            )

        cls.add_schedules(
            scheduler_lock_app, SchedulesMaster, schedule_type=ScheduleType.LOCAL
        )

    @classmethod
    def add_schedules(
        cls,
        scheduler_lock_app: AppConfig,
        SchedulesMaster: Type[SchedulesMasterBase],
        schedule_type: ScheduleType,
    ) -> None:
        schedules_from_master = SchedulesMaster.get_all()

        logger.debug(f"Process {os.getpid()} is adding {schedule_type.value} schedules")
        for schedule in schedules_from_master[f"{schedule_type.value}_schedules"]:
            job = cls.add_schedule(scheduler_lock_app, schedule)
            cls.jobs[f"{schedule_type.value}_schedules"].append(job)

    @classmethod
    def reload_all_schedules(
        cls,
        scheduler_lock_app: AppConfig,
        SchedulesMaster: Type[SchedulesMasterBase],
    ) -> None:
        logger.debug(
            f"------------ Process {os.getpid()} is reloading schedules ---------------"
        )

        for j in cls.jobs["global_schedules"] + cls.jobs["local_schedules"]:
            cls.remove_schedule(scheduler_lock_app, j)

        cls.jobs["global_schedules"] = []
        cls.jobs["local_schedules"] = []

        cls.add_all_schedules(scheduler_lock_app, SchedulesMaster)

        logger.debug(
            f"------------ Process {os.getpid()} has reloaded all schedules ---------------"
        )

    @classmethod
    def scheduler_lock(cls) -> None:
        """
        This is the schedule which checks whether the current instance holds
        the lock. If no other instance holds the lock, it acquires it and
        adds the global schedules to the instance's scheduler
        (scheduler_lock_app.scheduler). Local schedules, however, are added
        to the instance regardless of whether it holds the lock or not.
        The interval it runs after is set in the SCHEDULER_LOCK_JOB_INTERVAL
        setting.
        """

        logger.debug(
            f"running scheduler_lock job, pid: {os.getpid()}, time: {time.asctime()}"
        )

        scheduler_lock_app = apps.get_app_config("aistudio_scheduler_lock")
        SchedulesMaster = cls.get_schedules_master()

        if cls.lock_owner:
            logger.debug(f"I {os.getpid()} am already a lock owner!")

            if not cls.lock.renew_lease():
                # if lock owner loses the lease, it is no longer the lock owner
                # and has to stop executing global schedules
                logger.debug(f"Sadly, I {os.getpid()} have lost the lease.")

                for j in cls.jobs["global_schedules"]:
                    cls.remove_schedule(scheduler_lock_app, j)

                cls.lock_owner = False
                cls.jobs["global_schedules"] = []

        if not cls.lock_owner and cls.lock.try_acquire_lock():
            # if any instance newly acquires the lock, mark it as lock owner and add the global schedules
            logger.debug(f"VOILA I {os.getpid()} am the lock owner VOILA")
            cls.lock_owner = True
            cls.add_schedules(
                scheduler_lock_app,
                SchedulesMaster,
                schedule_type=ScheduleType.GLOBAL,
            )

        if not cls.last_updated_on:
            # Add local schedules when newly initiated
            cls.add_schedules(
                scheduler_lock_app, SchedulesMaster, schedule_type=ScheduleType.LOCAL
            )
            # Typically, last_updated_on will be None on newly initiated instances.
            # By this point, both global and local schedules have been loaded,
            # so it is safe to update it with the current time.
            cls.last_updated_on = time.time()

        if SchedulesMaster.to_reload_schedules(cls.last_updated_on):
            # If schedules have to be reloaded, reload all schedules (both global and local)
            # and update the value of last_updated_on with the current value
            cls.reload_all_schedules(scheduler_lock_app, SchedulesMaster)
            cls.last_updated_on = time.time()

        logger.debug("Following jobs will be run by pid %s: %s,", os.getpid(), cls.jobs)

    @classmethod
    def can_execute_task(cls) -> bool:
        return cls.lock.can_execute_task()

    @classmethod
    def get_current_lock_owner(cls) -> str:
        return cls.lock.get_current_owner()

    @staticmethod
    def _get_next_n_run_times(n: int, job: Job):
        run_times = []

        for i in range(n):
            if i == 0:
                next_run_time = job.next_run_time
            else:
                next_run_time = job.trigger.get_next_fire_time(
                    run_times[-1], run_times[-1]
                )

            if not next_run_time:
                break

            run_times.append(next_run_time)

        return run_times

    @classmethod
    def get_next_n_run_times(
        cls,
        n: int,
        func: Callable,
        trigger: str,
        max_instances: int,
        trigger_params: dict,
    ) -> datetime:
        temp_scheduler = BackgroundScheduler()

        j = temp_scheduler.add_job(
            func=func, trigger=trigger, max_instances=max_instances, **trigger_params
        )
        temp_scheduler.start(paused=True)

        return cls._get_next_n_run_times(n, j)
