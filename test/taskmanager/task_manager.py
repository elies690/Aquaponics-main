from logging import FATAL, fatal, raiseExceptions
import re
from typing import Type
#from typing_extensions import TypeAlias
import schedule
import time
from enum import Enum
import logging


_stop = False


class TimeOrder(Enum):
    """Time Order enum
    """
    SECOND = 1
    MINUTE = 2
    HOUR = 3
    DAY = 4


class Task(object):
    """Task object

    Args:
        name (str): The task name.
        delay (int): The task frequency.
        action (callable): The task action to be executed.
        delay_time_order (TimeOrder): The task frequency order.
        tags (*str): The tags to apply to the task.
    """

    def __init__(self, name: str, action: callable, delay: int, delay_time_order: TimeOrder, *tags) -> None:
        super().__init__()
        if name is None:
            raise TypeError(name)
        if delay <= 0:
            raise TypeError(delay)
        if not isinstance(delay_time_order, TimeOrder):
            raise TypeError(delay_time_order)

        self._name = name
        self._delay = delay
        self._delay_time_order = delay_time_order
        self._tags = tags
        self._isEnabled = False
        self._action = action
        return

    @property
    def Action(self):
        return self._action

    @property
    def Name(self):
        return self._name

    @property
    def Delay(self):
        return self._delay

    @property
    def DelayTimeOrder(self):
        return self._delay_time_order

    @property
    def Tags(self):
        return self._tags

    @property
    def IsEnabled(self):
        """Specifies if the task is enabled or disabled
        """
        return self._isEnabled

    @IsEnabled.setter
    def IsEnabled(self, value: bool):
        """Enables or disables the task.

        Args:
            value (bool): True enables it, False diables it.
        """
        self._isEnabled = value
        return


def stop():
    _stop = True

def schedule_task(task: Task):
    """Schedules a task

    Args:
        task (Task): the task to be scheduled.
        time_settings (data_class): the settings to figure out how to schedule the task, could contain value and type (minutes, hours, normalized day in calendar)
    """
    if task.DelayTimeOrder == TimeOrder.SECOND:
        schedule.every(task.Delay).seconds.do(task.Action).tag(task.Tags)
    if task.DelayTimeOrder == TimeOrder.MINUTE:
        schedule.every(task.Delay).minutes.do(task.Action).tag(task.Tags)
    if task.DelayTimeOrder == TimeOrder.HOUR:
        schedule.every(task.Delay).hours.do(task.Action).tag(task.Tags)
    if task.DelayTimeOrder == TimeOrder.DAY:
        schedule.every(task.Delay).days.do(task.Action).tag(task.Tags)
    
    return


def clear_tasks(tag):
    print('cancelling...')
    schedule.clear(tag)
    return


def _ini_run():
    logging.debug("Task scheduler started.")
    pass


async def run():
    """run an async method that keeps checking the schedule
    """
    _ini_run()

    schedule.run_pending()
    time.sleep(1)
    logging.debug("Task Scheduler stopped.")
    return


def dispose():
    """Clean up here if needed
    """
    Stop = False
    logging.debug("Task Scheduler disposed.")
    return
