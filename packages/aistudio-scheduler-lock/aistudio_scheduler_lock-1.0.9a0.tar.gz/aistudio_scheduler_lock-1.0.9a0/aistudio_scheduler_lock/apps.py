import sys
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig
from django.conf import settings

from .schedules.scheduler_lock_job import SchedulerLockJob


class SchedulerLockConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"
    name = "aistudio_scheduler_lock"

    def ready(self):
        # Possibly with k8s, we might just run ONE pod running the scheduled jobs. If k8s
        # makes sure, at-least and at-most ONE such pod is running, we don't need to worry
        #  about making sure, scheduled jobs run only from one AIStudio instance.
        # In a way, there will be ONE microservice running just the scheduled jobs.

        run_schedules = settings.RUN_SCHEDULES
        if (
            "manage.py" in sys.argv or "manage.pyc" in sys.argv
        ) and "runserver" not in sys.argv:
            run_schedules = False

        if run_schedules:
            self.scheduler = BackgroundScheduler()
            # Minimum difference between job interval and lock lease time
            diff = 5
            interval = settings.SCHEDULER_LOCK_JOB_INTERVAL
            lease_time = settings.SCHEDULER_LOCK_LEASE_TIME
            if lease_time < interval:
                raise Exception(
                    f"Lock lease duration '{lease_time}' cannot be lesser than "
                    f"scheduler lock job interval '{interval}'."
                )
            if lease_time - interval < diff:
                raise Exception(
                    f"Difference in Lock lease duration '{lease_time}' and "
                    f"scheduler lock job interval '{interval}' should be at-least {diff}."
                )

            self.scheduler.add_job(
                SchedulerLockJob.scheduler_lock,
                "interval",
                seconds=interval,
                next_run_time=datetime.now(),
                name="scheduler_lock_job",
            )

            self.scheduler.start()
