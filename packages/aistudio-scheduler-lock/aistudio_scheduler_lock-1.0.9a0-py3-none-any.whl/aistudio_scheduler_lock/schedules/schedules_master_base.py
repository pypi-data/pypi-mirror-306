from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, TypedDict, Union


class IntervalTriggerParams(TypedDict):
    days: int
    hours: int
    minutes: int
    seconds: int
    timezone: str
    start_date: datetime
    end_date: datetime


class CronTriggerParams(TypedDict):
    year: str
    month: str
    day: str
    week: str
    day_of_week: str
    hour: str
    minute: str
    second: str
    timezone: str
    start_date: datetime
    end_date: datetime


class DateTriggerParams(TypedDict):
    run_date: datetime
    timezone: str


class ScheduleDict(TypedDict):
    func: callable
    trigger: str
    trigger_params: Union[IntervalTriggerParams, CronTriggerParams, DateTriggerParams]
    name: str
    is_enabled: bool
    max_instances: int


class SchedulesDict(TypedDict):
    global_schedules: list[ScheduleDict]
    local_schedules: list[ScheduleDict]


class SchedulesMasterBase(ABC):
    @abstractmethod
    def get_all(self) -> SchedulesDict:
        """Method to fetch all schedules and pass it to this scheduler lock instance.
        It is mandatory to implement this wherever we use this library.
        """
        raise NotImplementedError()

    @staticmethod
    def to_reload_schedules(last_updated_on: Optional[int]) -> bool:
        """Override this to implement custom logic to decide whether schedules are to be reloaded

        Args:
            last_updated_on (Optional[int]):
                Timestamp when schedules were last loaded on this scheduler lock instance

        Returns:
            bool: Whether to reload schedules or not
        """
        return False
