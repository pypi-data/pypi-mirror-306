#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###########################################################################
#
#    xwrpr - A wrapper for the API of XTB (https://www.xtb.com)
#
#    Copyright (C) 2024  Philipp Craighero
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###########################################################################

from typing import Optional
import logging
from pathlib import Path
import re
import threading
import datetime
import tzlocal
from dateutil.relativedelta import relativedelta # Necessary for timedeltas > 1 month


def generate_logger(
    name: str,
    stream_level: Optional[str] = None,
    file_level: Optional[str] = None,
    path: Optional[Path] = None
) -> logging.Logger:
    """
    Generate a logger with the specified name and configuration.

    Args:
        name (str): The name of the logger.
        stream_level (str, optional): The log level for the console output. Defaults to None.
        file_level (str, optional): The log level for the file output. Defaults to None.
        path (str, optional): The path to the directory where the log file will be saved. Defaults to None.

    Returns:
        logging.Logger: The configured logger instance.

    Raises:
        ValueError: If the provided log level is invalid.
    """

    # Create a logger with the specified name
    logger = logging.getLogger(name)

    # In case a logger with the same name is already created, return it
    if logger.hasHandlers():
        return logger

    # Define the log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Set the logger level to DEBUG
    logger.setLevel(logging.DEBUG)

    # Create a stream handler for the console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(_validate_level(stream_level, default = "warning"))
    logger.addHandler(stream_handler)

    if path is not None:
        try:
            # Checks if the path exists, if not, creates it
            path.mkdir(parents = True)
        except FileExistsError:
            pass
        except Exception as e:
            raise ValueError(f"Could not create the directory {path}. Error: {e}")

        # Create a file handler for the log file
        log_file_path = path / f"{name}.log"
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(_validate_level(file_level, default = "debug"))
        logger.addHandler(file_handler)

    return logger

def _validate_level(
    level: Optional[str] = None,
    default: str = "debug"
    ) -> int:
    """
    Validates the logging level and returns the corresponding logging level constant.

    Args:
        level (str, optional): The desired logging level. Defaults to None.
        default (str, optional): The default logging level. Defaults to "debug".

    Returns:
        int: The logging level constant.

    Raises:
        ValueError: If the provided level or default level is invalid.
    """

    # Define the mapping of logging levels
    levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    level = level.lower() if level else default.lower()

    if level not in levels:
        raise ValueError(f"Invalid logger level: {level}")

    return levels[level]

class CustomThread(threading.Thread):
    """
    A custom thread class that extends the functionality of the threading.Thread class.
    Necessary to read the custom attributes passed to the constructor.

    Attributes:
        target (callable): The callable object to be invoked by the thread's run() method.
        args (tuple): The arguments to be passed to the target callable.
        daemon (bool): A flag indicating whether the thread should be a daemon thread.
        kwargs (dict): The keyword arguments to be passed to the target callable.

    Properties:
        target (callable): The callable object to be invoked by the thread's run() method.
        args (tuple): The arguments to be passed to the target callable.
        daemon (bool): A flag indicating whether the thread should be a daemon thread.
        kwargs (dict): The keyword arguments to be passed to the target callable.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a new instance of the class.

        Args:
            args: The positional arguments to be passed to the threading.Thread class.
            kwargs: The keyword arguments to be passed to the threading.Thread class.
        """

        # Extract the custom attributes
        # Necessary to rename the attributes to avoid conflicts with the threading.Thread class
        self._custom_target = kwargs.get('target', None)
        self._custom_args = kwargs.get('args', ())
        self._custom_daemon = kwargs.get('daemon', True)
        self._custom_kwargs = kwargs.get('kwargs', {})

        # Create a new instance of the threading.Thread class
        super().__init__(
            target = self._custom_target,
            args = self._custom_args,
            daemon = self._custom_daemon,
            kwargs = self._custom_kwargs
        )

    @property
    def target(self) -> callable:
        return self._custom_target

    @property
    def args(self) -> tuple:
        return self._custom_args
    
    @property
    def daemon(self) -> bool:
        return self._custom_daemon

    @property
    def kwargs(self) -> dict:
        return self._custom_kwargs

def pretty(command: str) -> str:
    """
    Returns a pretty version of the given command by inserting a space before each capital letter.

    Args:
        command (str): The command to make pretty.

    Returns:
        str: The pretty version of the command.
    """

    if command.startswith("get"):
        # Trim the command to remove the "get" prefix
        trimmed_command = command[3:]
    elif command.startswith("trade"):
        # Trim the command to remove the "trade" prefix
        trimmed_command = command[5:]
    else:
        # Use the command as is
        trimmed_command = command
        
    return re.sub(r'([A-Z])', r'{}\1'.format(' '), trimmed_command)[1:]

def calculate_timesteps(start: datetime, end: datetime, period: str = 'minutes') -> float:
    """
    Calculate the time difference between two datetime objects.

    Parameters:
        start (datetime): The starting datetime object.
        end (datetime): The ending datetime object.
        period (str, optional): The unit of time to calculate the difference in. Defaults to 'minutes'.

        Supported units for "period":
            - 'minutes'
            - 'hours'
            - 'days'
            - 'weeks'
            - 'months'

    Returns:
        float: The difference between the two datetime objects in the specified unit.

    Raises:
        ValueError: If an unsupported unit is provided.
    """
    
    # Calculate the difference
    delta = end - start

    # Return the difference in the desired unit
    if period == 'minutes':
        steps = delta.total_seconds() / 60
    elif period == 'hours':
        steps = delta.total_seconds() / 3600
    elif period == 'days':
        steps = delta.days
    elif period == 'weeks':
        steps = delta.days / 7
    elif period == 'months':
        rd = relativedelta(end, start) # Use relativedelta to calculate the number of months
        steps = rd.years * 12 + rd.months
    else:
        raise ValueError("Unsupported unit. Please choose from 'minutes', 'hours', 'days', 'weeks', or 'months'.")
    
    return steps

def datetime_to_unixtime(dt: datetime.datetime) -> int:
    """
    Convert a datetime object into a Unix timestamp (milliseconds since 01.01.1970, 00:00 UTC).
    In case the datetime object is naive, it is assumed to be in the local timezone.
    
    Args:
        dt (datetime): The datetime object to convert.
    
    Returns:
        float: The timestamp in milliseconds.
    """

    # Check if the datetime object is naive
    if dt.tzinfo is None:
        # Get the local timezone
        local_timezone = tzlocal.get_localzone()
        # Convert the naive datetime to the local timezone
        dt = dt.replace(tzinfo = local_timezone)

    # Ensure the datetime is in UTC
    dt_utc = dt.astimezone(datetime.timezone.utc)

    # Get the Unix timestamp in seconds and convert to milliseconds
    return int(dt_utc.timestamp() * 1000)

def local_to_utc(dt_local: datetime.datetime) -> datetime.datetime:
    """
    Converts a datetime object from the local timezone to UTC.
    In case the datetime object is naive, it is assumed to be in the local timezone.

    Args:
        dt_local (datetime): A datetime object in the local timezone.

    Returns:
        datetime: A datetime object in UTC.
    """

    # Check if the datetime object is naive
    if dt_local.tzinfo is None:
        # Get the local timezone
        local_timezone = tzlocal.get_localzone()
        # Convert the naive datetime to the local timezone
        dt_local = dt_local.replace(tzinfo = local_timezone)
    
    # Convert to UTC
    return dt_local.astimezone(datetime.timezone.utc)