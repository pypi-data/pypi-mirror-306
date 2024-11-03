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

from enum import Enum
import logging
import configparser
from pathlib import Path
from typing import Union, List, Optional
import time
from threading import Lock
from queue import Queue, Full, Empty
from statistics import mean
from xwrpr.client import Client
from xwrpr.utils import pretty, generate_logger, CustomThread
from xwrpr.account import get_userId, get_password, set_path


# Read the configuration file
config = configparser.ConfigParser()
config_path = Path(__file__).parent.absolute()/'api.ini'
config.read(config_path)

HOST = config.get('SOCKET', 'HOST')
PORT_DEMO = config.getint('SOCKET', 'PORT_DEMO')
PORT_DEMO_STREAM = config.getint('SOCKET', 'PORT_DEMO_STREAM')
PORT_REAL = config.getint('SOCKET', 'PORT_REAL')
PORT_REAL_STREAM = config.getint('SOCKET', 'PORT_REAL_STREAM')
THREAD_TICKER = float(config.getint('HANDLER', 'THREAD_TICKER')/1000)
MIN_FLAWLESS_INTERVAL = float(config.getint('HANDLER', 'MIN_FLAWLESS_INTERVAL')/1000)
SLIDING_MEAN_WINDOW = config.getint('HANDLER', 'SLIDING_MEAN_WINDOW')
QUEUE_LEVEL_THRESHOLD = float(config.getint('HANDLER', 'QUEUE_LEVEL_THRESHOLD')/100)


class Status(Enum):
    """
    Enum class for the status of the handler.

    Attributes:
        ACTIVE: The handler is active.
        INACTIVE: The handler is inactive.
        SUSPENDED: The handler is suspended.
        FAILED: The handler failed.
        DELETED: The handler is deleted.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    FAILED = "failed"
    DELETED = "deleted"


class _GeneralHandler(Client):
    """
    Handles general requests to and from the XTB trading platform.

    Attributes:
        _logger (logging.Logger): The logger instance.
        _ping (dict): A dictionary to store ping related information.
        _client_lock (Lock): A lock for acessing the client.

    Methods:
        _send_request: Sends a request to the server.
        _receive_response: Receives a response from the server.
        _thread_monitor: Monitors a thread and handles reactivation if necessary.
        _start_ping: Starts the ping process.
        _send_ping: Sends ping requests to the server.
        _stop_ping: Stops the ping process.
    """

    def __init__(
            self,

            host: str,
            port: int,

            max_send_data: int,
            max_received_data: int,
            max_retries: int,
            min_request_interval: float,
            socket_timeout: Optional[float] = None,

            logger: Optional[logging.Logger] = None
        ) -> None:
        """
        Initializes a new instance of the GeneralHandler class.

        Args:
            host (str): The host address.
            port (int): The port number.
            max_send_data (int): Max size of data sent to server at once [bytes].
            max_received_data (int): Max size of data received from server at once [bytes].
            max_retries (int): Max retries for request to server [-].
            min_request_interval (float): Min allowed interval for server requests [s].
            socket_timeout (float, optional): The timeout for blocking socket connection [s]. Defaults to None.
            logger (logging.Logger, optional): The logger object. Defaults to None.
        """

        if logger:
            # Use the provided logger
            self._logger = logger
        else:
            # In case no logger is provided, generate a new one
            self._logger = generate_logger(name = 'GeneralHandler', path = Path.cwd() / "logs")

        self._logger.debug("Initializing GeneralHandler ...")

        # Initialize the Client instance
        try:
            super().__init__(
                host = host,
                port = port, 

                encrypted = True,
                timeout = socket_timeout,
                min_request_interval = min_request_interval,
                max_retries = max_retries,
                bytes_out = max_send_data,
                bytes_in = max_received_data,

                logger = self._logger
            )
        except Exception as e:
            # Catch errors that occur when initializing the Client,
            # reconnect or healthcheck will do the rest
            self._logger.error(f"Failed to initialize Client: {e}")

        # Initialize the ping dictionary
        self._ping = dict()
        # Initialize the client lock
        self._client_lock = Lock()

        self._logger.debug("GeneralHandler initialized")
    
    def _send_request(
        self,
        command: str,
        ssid: Optional[str] = None,
        arguments: Optional[dict] = None,
        tag: Optional[str] = None
        ) -> None:
        """
        Sends a request to the server.

        Args:
            command (str): The command to send.
            ssid (str, optional): The stream session ID. Defaults to None.
            arguments (dict, optional): Additional arguments for the request. Defaults to None.
            tag (str, optional): A custom tag for the request. Defaults to None.
        """

        self._logger.info("Sending request ...")

        # Every request must at least contain the command
        request = {'command': command}

        # Add the stream session ID, arguments, and custom tag to the request
        if ssid is not None:
            # For stream commands the stream session ID is required
            request['streamSessionId'] = ssid
        if arguments is not None:
            # Some commands require additional arguments
            request.update(arguments)
        if tag is not None:
            # Tags ar always optional and can be used for debugging
            # The response will contain the same tag
            request['customTag'] = tag

        # Send the request to the server
        self.send(request)

        # For the login command, the user ID and password are masked
        if command == 'login':
            request['arguments']['userId'] = '*****'
            request['arguments']['password'] = '*****'

        self._logger.debug(f"Request sent: {request}")

    def _receive_response(self, stream: bool = False) -> Union[List[dict], dict]:
        """
        Receives a response from the server.

        Args:
            stream (bool, optional): A flag indicating whether the response is for a stream request. Defaults to False.

        Returns:
            Union[List[dict], dict]: The response from the server.

        Raises:
            ValueError: If the response is empty or not a dictionary.
            ValueError: If the response is corrupted.
            ValueError: If the request failed.
        """

        self._logger.info("Receiving response ...")

        # Receive the response from the server
        response_list = self.receive()
        self._logger.debug("Received %s responses", len(response_list))

        if stream:
            return response_list
        else:
            # Message analysis must stay in GeneralHandler for ping handling
            # Data connection need exatly one response
            if response_list == []:
                self._logger.error("Empty response")
                raise ValueError("Empty response")
            elif len(response_list) > 1:
                self._logger.error("Multiple responses received")
                raise ValueError("Multiple responses received")
            
            # Retrieve the response from the list
            response = response_list[0]

            # Non stream responses have the flag "status"
            if 'status' not in response:
                self._logger.error("Response corrupted")
                raise ValueError("Response corrupted")

            # If the status is False, the response contains an error code and description
            if not response['status']:
                self._logger.error("Request failed. Error code: " + str(response['errorCode']) + ", Error description: " + response['errorDescr'])
                raise ValueError("Request failed. Error code: " + str(response['errorCode']) + ", Error description: " + response['errorDescr'])

            return response
    
    def _thread_monitor(
        self,
        name: str,
        thread_data: dict,
        handler: Union['_DataHandler', '_StreamHandler'],
        reactivate: bool = False
    ) -> None:
        """
        Monitors the specified thread and handles reactivation if necessary.

        Args:
            name (str): The name of the thread being monitored.
            thread_data (dict): A dictionary containing information about the thread.
            handler (_DataHandler or _StreamHandler): The handler instance.
            reactivate (bool, optional): A flag indicating whether the thread should be reactivated. Defaults to False.
        """

        self._logger.info(f"Monitoring thread for {name} ...")

        last_reactivation = time.time()

        # Loop until the run flag is set to False
        # or an error occurs
        while thread_data['run']:
            # If the thread is still running, continue monitoring
            if thread_data['thread'].is_alive():
                # Use Thread ticker to limit the loop interval
                time.sleep(THREAD_TICKER)
                continue

            # Check if the thread should still be running
            if not thread_data['run']:
                break

            self._logger.error(f"Thread for {name} died")

            # Check if the reactivation interval is too short
            if time.time() - last_reactivation < MIN_FLAWLESS_INTERVAL:
                self._logger.info(f"Reactivation intervals for {name} too short")
                # Set the status to failed
                # Reactivation method or healthcheck will do the rest
                handler.status = Status.FAILED
                break

            # Check if the thread shall be reactivated
            if reactivate:
                handler._reactivate()

            self._logger.info(f"Restarting thread for {name} ...")

            # Create a new thread with the parameters of the dead thread
            dead_thread = thread_data['thread']
            thread_data['thread'] = CustomThread(
                target = dead_thread.target,
                args = dead_thread.args,
                daemon = dead_thread.daemon,
                kwargs = dead_thread.kwargs
            )
            thread_data['thread'].start()

            # Update the last reactivation time
            last_reactivation = time.time()

            self._logger.info(f"Thread for {name} restarted")

        self._logger.info(f"Monitoring for thread {name} stopped")

    def _start_ping(
        self,
        handler: Union['_DataHandler', '_StreamHandler']
    ) -> None:
        """
        Starts the ping functionality.

        Args:
            handler (_DataHandler or _StreamHandler): The handler instance.
        """

        self._logger.info("Starting ping ...")

        # Set the run flag for the ping on true
        self._ping['run'] = True
        # Create a new thread for the ping
        self._ping['thread'] = CustomThread(
            target = self._send_ping,
            args = (handler, self._ping, ),
            daemon = True
        )
        self._ping['thread'].start()

        self._logger.info("Ping started")

        self._logger.info("Starting ping monitor ...")

        # Create the thread monitor for the ping thread
        monitor_thread = CustomThread(
            target = self._thread_monitor,
            args = ('Ping', self._ping, handler, True, ),
            daemon = True)
        # Start the thread monitor
        monitor_thread.start()

        self._logger.info("Ping monitor started")

    def _send_ping(
        self,
        handler: Union['_DataHandler', '_StreamHandler'],
        thread_data: dict
        ) -> None:
        """
        Sends ping requests to the server.

        Args:
            handler (_DataHandler or _StreamHandler): The handler instance.
            thread_data (dict): A dictionary containing information about the thread.
        """

        # sends ping all 9 minutes
        # Ping should be sent at least every 10 minutes
        ping_interval = 60*9
        # Initially send ping to keep connection open
        elapsed_time = ping_interval

        self._logger.info("Start sending ping ...")

        # Loop until the run flag is set to False
        while thread_data['run']:
            # Start the timer
            start_time = time.time()

            # Check if the ping timer has reached the interval
            if elapsed_time >= ping_interval:
                # thanks to th with statement the ping could fail to keep is sheduled interval
                # but thats not important because this is just the maximal needed interval and
                # a function that locks the ping_key also initiates a reset to the server
                with self._client_lock:
                    # dynamic allocation of ssid for StreamHandler
                    # ssid could change during the ping process
                    if isinstance(handler, _StreamHandler):
                        ssid = handler._dh.ssid
                    else:
                        ssid = None

                    # Stream handler have to send their ssid with every request to the host
                    self._send_request(command = 'ping', ssid = ssid)
                    if not ssid:
                        # None stream pings receive a response
                        self._receive_response()

                    # reset the ping timer
                    elapsed_time = 0

            # Use Thread ticker to limit the loop interval
            time.sleep(THREAD_TICKER)

            # Calculate the elapsed time
            elapsed_time += time.time() - start_time

        self._logger.info("Ping stopped")

    def _stop_ping(self) -> None:
        """
        Stops the ping process.
        """

        self._logger.info("Stopping ping ...")

        # Check if ping was ever created
        if not self._ping:
            self._logger.warning("Ping never started")
            return

        # Check if the ping is intended to run 
        if not self._ping['run']:
            self._logger.warning("Ping already stopped")
        else:
            self._ping['run'] = False

            # Wait for the ping thread to stop
            self._ping['thread'].join(timeout = THREAD_TICKER*5)


class _DataHandler(_GeneralHandler):
    """
    Handles data requests to and from the XTB trading platform.

    Attributes:
        __status (Status): The status of the handler.
        __lock (Lock): The lock for essential handler operations.
        _logger (logging.Logger): The logger instance used for logging.
        _username (str): The username for the XTB trading platform.
        _password (str): The password for the XTB trading platform.
        _stream_handler (list): A list of attached stream handlers.
        _ssid (str): The stream session ID received from the server.

    Methods:
        _delete: Deletes the DataHandler.
        _login: Logs in to the XTB trading platform.
        _logout: Logs out the user from the XTB trading platform.
        _get_data: Retrieves data for the specified command.
        _retrieve_data: Retrieves data from the server.
        _reactivate: Reactivates the DataHandler.
        _attach_stream_handler: Attaches a stream handler to the DataHandler.
        _detach_stream_handler: Detaches a stream handler from the DataHandler.
        _close_stream_handlers: Closes the stream handlers.
        _inform_stream_handlers: Informs the stream handlers about the updated data handler.

    Properties:
        stream_handler: The stream handlers attached to the DataHandler.
        handler_lock: The lock for essential handler operations.
        status: The status of the DataHandler.
        ssid: The stream session ID.
    """

    def __init__(
        self,
        demo: bool,

        username: str,
        password: str,

        max_send_data: int,
        max_received_data: int,
        max_retries: int,
        min_request_interval: float,

        logger: Optional[logging.Logger] = None
    ) -> None:
        """
        Initializes a new instance of the DataHandler class.

        Args:
            demo (bool): Specifies whether the DataHandler is for demo or real trading.
            username (str): The username for the XTB trading platform.
            password (str): The password for the XTB trading platform.
            max_send_data (int):  Max size of data sent to server at once [bytes].
            max_received_data (int): Max size of data received from server at once [bytes].
            max_retries (int): Max retries for request to server [-].
            min_request_interval (float): Min allowed interval for server requests [s].
            logger (logging.Logger, optional): The logger object to use for logging. If not provided, a new logger will be generated.
        """

        # The status of the handler is initially inactive
        # because not jet ready for usage   
        self.__status = Status.INACTIVE

        # The lock for essential handler operations
        self.__lock = Lock()

        # Thread safety necessary
        # The initialization of the class has to be finished
        # before the class can be used
        with self.__lock:
            if logger:
                # Use the provided logger
                self._logger = logger
            else:
                # In case no logger is provided, generate a new one
                self._logger = generate_logger(name = 'DataHandler', path = Path.cwd() / "logs")

            self._logger.debug("Initializing DataHandler ...")

            # The username and password for the XTB trading platform
            self._username = username
            self._password = password

            # Initialize the GeneralHandler instance
            super().__init__(
                host = HOST,
                port = PORT_DEMO if demo else PORT_REAL,

                max_send_data = max_send_data,
                max_received_data = max_received_data,
                max_retries = max_retries,
                min_request_interval = min_request_interval,

                logger = self._logger
            )
            
            # Stream handlers that are attached to the DataHandler
            self._stream_handler: List['_StreamHandler'] = []
            # Stream session ID is necessary for stream requests
            # It is provided from the server after login
            self._ssid = None

            # Log in to the XTB trading platform
            self._login()
            # Starts ping to keep connection open
            self._start_ping(handler = self)

            self._logger.debug("DataHandler initialized")
        
    def __del__(self) -> None:
        """
        Destructor method that is called when the DataHandler object is about to be destroyed.
        It ensures that any open connections are closed properly and any resources
        are released.

        Raises:
            None
        """

        try:
            self._delete()
        except Exception as e:
            # For graceful closing no raise of exception is not allowed
            pass
    
    def _delete(self) -> None:
        """
        Deletes the DataHandler.

        Raises:
            None
        """

        # In case a other essential operation is in progress
        with self.__lock:
            # Check if the DataHandler is already deleted
            if self.__status == Status.DELETED:
                self._logger.debug("DataHandler already deleted")
                # For graceful deletion a raise of exception is not allowed
                return
            
            self._logger.info("Deleting DataHandler ...")

            try:
                # Close the stream handlers and stop the ping process
                self._close_stream_handlers()
                self._stop_ping()
                # Log out from the XTB trading platform
                self._logout()
            except Exception as e:
                # For graceful closing no raise of exception is not allowed
                self._logger.error(f"Failed to delete DataHandler: {e}")
            finally:
                # Set Status to deleted
                self.__status = Status.DELETED
                
            self._logger.info("DataHandler deleted")
            
    def _login(self) -> None:
        """
        Logs in to the XTB trading platform.

        Raises:
            None
        """

        self._logger.info("Logging in ...")

        try:
            # Open the connection to the server
            self.open()
        except Exception as e:
            # Catch errors that occur when opening the connection,
            # reconnect or healthcheck will do the rest
            self._logger.error(f"Failed to open connection: {e}")

        # Locks out the ping process
        # To avoid conflicts with the login process
        # Could happen if relogin of running handler is necessary
        with self._client_lock:
            # Send the login request to the server
            # No reactivation if request fails because the login method
            # is part of the reactivation method
            try:
                self._send_request(
                    command = 'login',
                    arguments = {
                        'arguments': {
                            'userId': self._username,
                            'password': self._password
                        }
                    }
                )
                # Receive the response from the server
                response = self._receive_response()
            except Exception as e:
                self._logger.error(f"Failed to log in: {e}")
                # Set the status to failed
                # Reactivation method or healthcheck will do the rest
                self.__status = Status.FAILED
                return

        self._logger.info("Log in successfully")
        self._ssid = response['streamSessionId']

        # DataHandler is now ready for usage
        self.__status = Status.ACTIVE
                            
    def _logout(self) -> None:
        """
        Logs out from the XTB trading platform.

        Raises:
            None
        """

        if not self._ssid:
            # Only Logged in clients have a stream session ID
            self._logger.warning("Already logged out")
        
        # Locks out the ping process
        # To avoid conflicts with the login process
        with self._client_lock:
            try:
                self._logger.info("Logging out ...")
                # Send the logout request to the server
                # Server sends no response for logout request
                # No reactivation if request fails because the login method
                # is part of the reactivation method
                self._send_request(command = 'logout')
                self._logger.info("Logged out successfully")
            except Exception as e:
                # For graceful logout no raise of exception is not allowed
                self._logger.error(f"Could not log out: {e}")
            finally:
                # Close the socket
                self.close()
                # Delete the stream session ID 
                self._ssid = None
                # DataHandler no longer ready for usage
                self.__status = Status.INACTIVE

    def _get_data(self, command: str, **kwargs) -> dict:
        """
        Retrieves data for the specified command.

        Args:
            command (str): The command to retrieve data.
            **kwargs: Additional keyword arguments for the command.

        Returns:
            The retrieved data if successful.
        """

        # Checks if the DataHandler is logged in
        if not self._ssid:
            self._logger.error("Got no StreamSessionId from Server")
            raise ValueError("Got no StreamSessionId from Server")
        
        # Try to retrieve the data twice
        # This enables a automatic reactivation if the first attempt fails
        for tries in range(2):
            try:
                # Retrieve the data for the specified command
                return  self._retrieve_data(command, **kwargs)
            except Exception as e:
                self._logger.error(f"Failed to retrieve data: {e}")
                if tries == 0:
                    # Reactivate the DataHandler if the first attempt fails
                    self._logger.info("Try a reactivation ...")
                    self._reactivate()
                else:
                    # If the data could not be retrieved, raise an error
                    raise

    def _retrieve_data(self, command: str, **kwargs) -> dict:
        """
        Retrieves data from the server.

        Args:
            command (str): The command to retrieve data for.
            **kwargs: Additional keyword arguments to be passed to the command.

        Returns:
            The retrieved data as a dictionary.
        """

        # Locks out the ping process
        # To avoid conflicts with the login process
        with self._client_lock:
            self._logger.info("Getting data for " + pretty(command) + " ...")

            # Send the request to the server
            self._send_request(
                command = command,
                arguments = {'arguments': kwargs} if bool(kwargs) else None)
                
            # Receive the response from the server
            response = self._receive_response()
            
            # Response must contain 'returnData' key
            # rest of message check was done in GeneralHandler
            if 'returnData' not in response:
                self._logger.error("No data in response")
                raise ValueError("No data in response")
                
            # Log the successful retrieval of data in pretty format
            self._logger.info("Data for "+pretty(command) +" received")

            # Return the data
            return response['returnData']
 
    def _reactivate(self) -> None:
        """
        Reactivates the DataHandler.

        This method is used to establish a new connection to the server in case the current connection is lost.

        Raises:
            None
        """

        # In case a other essential operation is in progress
        if self.__lock.acquire(blocking = False):
            # Only DataHandler in active status can be reactivated
            if self.__status == Status.ACTIVE:
                try:
                    self._logger.info("Checking connection ...")
                    # Check the Socket
                    self.check()
                    self._logger.info("Connection is active")
                    # The DataHandlerr seems to be active
                    self.__status = Status.ACTIVE
                except Exception as e:
                    try:
                        # Set the status to suspended
                        self.__status = Status.SUSPENDED
                        self._logger.info("Reactivating ...")
                        # Create a new socket
                        self.create()
                        # Relogin to the server
                        self._login() # Sets the status automatically to active
                        self._logger.info("Reactivation successful")
                        # Inform the stream handlers about the updated ssid
                        self._inform_stream_handlers()
                    except Exception as e:
                        self._logger.error(f"Failed to reactivate: {e}")
                        # Reactivation failed
                        # Healthcheck will do the rest
                        self.__status = Status.FAILED
            
            # Release the handler lock
            self.__lock.release()
        else:
            self._logger.warning("Reactivation not possible. Other essential operation in progress")

    def _attach_stream_handler(self, handler: '_StreamHandler') -> None:
        """
        Attach a StreamHandler to the DataHandler.

        Args:
            handler (_StreamHandler): The stream handler to attach.
        """

        self._logger.info("Attaching StreamHandler ...")

        # Check if the StreamHandler is already attached
        if handler not in self._stream_handler:
            # Append the StreamHandler to the list of attached stream handlers
            self._stream_handler.append(handler)
            self._logger.info("StreamHandler attached")
        else:
            self._logger.warning("StreamHandler already attached")

    def _detach_stream_handler(self, handler: '_StreamHandler') -> None:
        """
        Detaches a StreamHandler from the DataHandler.

        Args:
            handler (_StreamHandler): The stream handler to detach.
        """

        self._logger.info("Detaching StreamHandler ...")

        # Check if the StreamHandler is attached
        if handler in self._stream_handler:
            # Remove the StreamHandler from the list of attached stream handlers
            self._stream_handler.remove(handler)
            self._logger.info("StreamHandler detached")
        else:
            self._logger.warning("StreamHandler not found")

    def _close_stream_handlers(self) -> None:
        """
        Closes the stream handlers.
        """

        self._logger.info("Closing StreamHandlers ...")

        if not self._stream_handler:
            # Check if there are any stream handlers to close
            self._logger.info("No StreamHandlers to close")
        else:
            # Delete all connected stream handlers
            # Detaching is only executed by StreamHandler itself
            for handler in list(self._stream_handler): # Dynamic change of dictionary 
                handler._delete()

    def _inform_stream_handlers(self) -> None:
        """
        Informs the stream handlers about the updated datahandler
        """

        self._logger.info("Informing StreamHandlers ...")

        # Inform the stream handlers about the updated data handler
        for handler in list(self._stream_handler): # Dynamic change of dictionary 
            handler.dh = self

    @property
    def stream_handler(self) -> List['_StreamHandler']:
        return self._stream_handler
    
    @property
    def handler_lock(self) -> Lock:
        return self.__lock
    
    @property
    def status(self) -> Status:
        return self.__status
    
    @status.setter
    def status(self, value: Status) -> None:
        self._logger.debug(f"Status externally set to {value}")
        self.__status = value
    
    @property
    def ssid(self) -> str:
        return self._ssid


class _StreamHandler(_GeneralHandler):
    """
    Handles stream requests to and from the XTB trading platform.

    Attributes:
        __status (Status): The status of the stream handler.
        __lock (Lock): The lock for essential handler operations.
        _logger (logging.Logger): The logger object used for logging.
        _dh (_DataHandler): The data handler object.
        _max_queue_elements (int): The maximum number of elements in the queue.
        _stream (dict): The stream dictionary.
        _stream_tasks (dict): The dictionary of stream tasks.
        _stop_lock (Lock): The lock for stopping the stream.
        _halt (bool): A flag to halt the stream.
        _max_queue_levels (list): The list of the last max queue levels.
        _sm_max_queue_level (float): The sliding mean of the max queue levels.

    Subclasses:
        exchange: A class to store the exchange information for the stream tasks.

    Methods:
        _delete: Deletes the StreamHandler.
        _stream_data: Starts streaming data from the server.
        _start_stream: Starts the stream for the specified command.
        _export_stream: Exports the stream data.
        _calculate_sm_max_queue_level: Calculates the sliding mean of the max queue levels.
        _receive_stream: Receives the stream data.
        _stop_stream: Stops the stream.
        _stop_task: Stops the stream task.
        _reactivate: Reactivates the StreamHandler.
        _transplant_stream_task: Transplants the stream tasks from another StreamHandler.

    Properties:
        dh: The data handler object.
        status: The status of the stream handler.
        stream_tasks: The stream tasks.
        sm_max_queue_level: The sliding mean of the max queue levels.
    """

    def __init__(
        self,

        data_handler: _DataHandler,
        demo: bool,

        max_send_data: int,
        max_received_data: int,
        max_retries: int,
        min_request_interval: float,
        socket_timeout: float,
        max_queue_elements: int,

        logger: Optional[logging.Logger] = None
        ) -> None:
        """
        Initializes a new instance of the StreamHandler class.

        Args:
            data_handler (_DataHandler): The data handler object.
            demo (bool): A boolean indicating whether the handler is for demo or real trading.
            max_send_data (int): Max size of data sent to server at once [bytes].
            max_received_data (int): Max size of data received from server at once [bytes].
            max_retries (int): Max retries for request to server [-].
            min_request_interval (float): Min allowed interval for server requests [s].
            socket_timeout (float): The timeout for blocking socket connection [s].
            max_queue_elements (int): The max number of elements in the stream queue [-].
            logger (logging.Logger, optional): The logger object to use for logging. Defaults to None.
        """

        # The status of the handler is initially inactive
        # because not jet ready for usage   
        self.__status = Status.INACTIVE

        # The lock for essential handler operations
        self.__lock = Lock()

        # Thread safety necessary
        # The initialization of the class has to be finished
        # before the class can be used
        with self.__lock:
            if logger:
                # Use the provided logger
                self._logger = logger
            else:
                # In case no logger is provided, generate a new one
                self._logger = generate_logger(name = 'StreamHandler', path = Path.cwd() / "logs")

            self._logger.debug("Initializing StreamHandler ...")

            # Initialize the GeneralHandler instance
            super().__init__(
                host = HOST,
                port = PORT_DEMO_STREAM if demo else PORT_REAL_STREAM,

                max_send_data = max_send_data,
                max_received_data = max_received_data,
                max_retries = max_retries,
                min_request_interval = min_request_interval,
                socket_timeout= socket_timeout,

                logger = self._logger
            )

            # Attach the StreamHandler to the DataHandler
            self._dh = data_handler
            self._dh._attach_stream_handler(handler = self)

            # Set the maximum number of elements in the queue
            self._max_queue_elements = max_queue_elements
            # The dictionary for the thread control of the stream
            self._stream = dict()
            # Stream tasks are stored in a dictionary
            self._stream_tasks = dict()
            # Lock for stopping a stream task
            self._stop_lock = Lock()
            # A Flag to halt the stream
            self._halt = False

            # The list of the last max queue levels
            self._max_queue_levels = []
            # The sliding mean of the max queue levels
            self._sm_max_queue_level = 0

            try:
                # Open connection to the server
                self.open()
            except Exception as e:
                self._logger.error(f"Failed to open connection: {e}")
                # Set the status to failed
                # Reactivation method or healthcheck will do the rest
                self.__status = Status.FAILED
                return

            # Send KeepAlive to keep connection open
            # First command must beb sent 1 second after connection is opened
            # Otherwise the server will close the connection
            self._stream_data(command = 'getKeepAlive')
            # Start ping to keep connection open
            self._start_ping(handler = self)
            
            # StreamHandler need no login
            # so the status is active right after the connection is open
            self.__status = Status.ACTIVE
            
            self._logger.debug("StreamHandler initialized")

    def __del__(self) -> None:
        """
        Destructor method that is called when the StreamHandler object is about to be destroyed.
        It ensures that any open connections are closed properly and any resources
        are released.

        Raises:
            None
        """
        
        try:
            self._delete()
        except Exception as e:
            # For graceful closing no raise of exception is not allowed
            pass
            
    def _delete(self) -> None:
        """
        Deletes the StreamHandler.

        Raises:
            None
        """

        # In case a other essential operation is in progress
        with self.__lock:
            # Check if the StreamHandler is already deleted
            if self.__status == Status.DELETED:
                self._logger.debug("StreamHandler already deleted")
                # For graceful deletion a raise of exception is not allowed
                return
            
            self._logger.info("Deleting StreamHandler ...")

            try:
                # Stop the stream and ping processes
                self._stop_stream()
                self._stop_ping()
                # Detach the StreamHandler from the DataHandler
                self._dh._detach_stream_handler(handler = self)
            except Exception as e:
                # For graceful closing no raise of exception is not allowed
                self._logger.error(f"Failed to delete StreamHandler: {e}")
            finally:
                # Close the connection to the server
                self.close()
                # Set Status to deleted
                self.__status= Status.DELETED
            
                self._logger.info("StreamHandler deleted")

    class exchange:
        """
        A class to store the exchange information for the stream tasks.

        Attributes:
            _sh (_StreamHandler): The stream handler object.
            _queue (Queue): The queue for the stream task.

        Methods:
            _update: Updates the stream handler object.
            _put: Puts data into the queue for the stream task.
            get: Gets data from the queue for the stream task.
            stop: Stops the stream task.
        """

        def __init__(self, sh: '_StreamHandler', task: str) -> None:
            """
            Initializes a new instance of the _exchange class.

            Args:
                sh (_StreamHandler): The stream handler object.
                task (str): The stream task.
            """

            self._sh  = sh
            self._task = task

            self._queue = Queue(maxsize = self._sh._max_queue_elements)

        def __del__(self) -> None:
            """
            Destructor method that is called when the StreamHandler object is about to be destroyed.
            It ensures that any open connections are closed properly and any resources
            are released.

            Raises:
                None
            """
            
            try:
                if self._sh.__status != Status.DELETED:
                    self.stop()
            except Exception as e:
                # For graceful closing no raise of exception is not allowed
                pass

        def _update(self, sh: '_StreamHandler') -> None:
            """
            Updates the stream handler object.

            Args:
                sh (_StreamHandler): The stream handler object.
            """

            self._sh = sh

        def _put(self, data: dict) -> None:
            """
            Puts data into the queue for the stream task.

            Args:
                data (dict): The data to put into the queue.

            Raises:
                Full: If the queue is full.
            """

            self._queue.put(data, block = False)
            
        def get(self, timeout: Optional[float] = None) -> dict:
            """
            Gets data from the queue for the stream task.

            Args:
                timeout (float): The timeout for getting data from the queue

            Returns:
                dict: The data from the queue for the stream task.
            """

            # Set the block flag for the queue
            block = False if timeout == 0 else True

            try:
                return self._queue.get(timeout = timeout, block = block)
            except Empty:
                self._sh._logger.warning("Queue is empty")
        
        def stop(self) -> None:
            """
            Stops the stream task.
            """

            self._sh._stop_task(task = self._task)

    def _stream_data(
        self,
        command: str,
        exchange: Optional['exchange'] = None,
        **kwargs
        ) -> Optional['exchange']:
        """
        Start streaming data from the server.

        Args:
            command (str): The command to start streaming data.
            exchange (_StreamHandler.exchange, optional): The exchange object for the stream task. Defaults to None.
            **kwargs: Additional keyword arguments for the command.

        Returns:
            Optional[_StreamHandler.exchange]: The exchange object for the stream

        Raises:
            ValueError: If the DataHandler has no StreamSessionId from the server.
        """
        
        # Check if DataHandler can provide a ssid
        if not self._dh.ssid:
            self._logger.error("DataHandler got no StreamSessionId from Server")
            raise ValueError("DataHandler got no StreamSessionId from Server")
        
        # Check if the specific stream is already open
        task = command
        if 'symbol' in kwargs:
            task += "_" + str(kwargs['symbol'])
        if task in self._stream_tasks:
            self._logger.warning("Stream for data already open")
            return

        # Start the stream for the specified command
        self._start_stream(command, **kwargs)
        
        # Initiate the stream thread for the handler
        if not self._stream:
            # Set the run flag for the stream on true
            self._stream['run'] = True
            # Create a new thread for the stream
            self._stream['thread'] = CustomThread(
                target = self._export_stream,
                daemon = True
            )
            # Start the stream thread
            self._stream['thread'].start()

            # Create the thread monitor for the stream thread
            monitor_thread = CustomThread(
                target = self._thread_monitor,
                args = ('Stream', self._stream, self, ),
                daemon = True
            )
            # Start the thread monitor
            monitor_thread.start()

        # Register the stream task
        self._stream_tasks[task] = {
            'command': command,
            'arguments': kwargs
        }

        self._logger.info("Stream started for " + pretty(command))

        # The data from the KeepAlive command is unnecessary
        if command != 'getKeepAlive':
            if exchange:
                # In case a exchange object is provided
                # the StreamHandler attribute of the exchange object has to be updated
                task_exchange = exchange
                task_exchange._update(sh = self)
            else:
                # Create a new exchange object for the stream task
                task_exchange = self.exchange(sh=self, task=task)

            # Store the exchange object in the stream tasks dictionary
            self._stream_tasks[task]['exchange'] = task_exchange
            # Store the queue level in the stream tasks dictionary
            self._stream_tasks[task]['queue_level'] = 0

            # Return the exchange object
            return task_exchange

    def _start_stream(self, command: str, **kwargs) -> None:
        """
        Starts a stream for the given command.

        Args:
            command (str): The command to start the stream for.
            **kwargs: Additional keyword arguments to be passed as arguments for the stream.
        """

        # Locks out the ping process
        # To avoid conflicts with the stream request
        with self._client_lock:
            self._logger.info("Starting stream for " + pretty(command) + " ...")

            # Dynamic allocation of ssid for StreamHandler
            # ssid could change during DataHandler is open
            self._ssid = self._dh.ssid

            # Try to start the stream twice
            # This enables a automatic reactivation if the first attempt fails
            for tries in range(2):
                try:
                    # Send the request for the stream to the server
                    self._send_request(
                        command = command,
                        ssid = self._ssid,
                        arguments = kwargs if bool(kwargs) else None
                    )
                    # Stream started successfully
                    break
                except Exception as e:
                    self._logger.error(f"Failed to start stream: {e}")
                    if tries == 0:
                        # Reactivateif the first attempt fails
                        self._logger.info("Try a reactivation ...")
                        self._reactivate()
                    else:
                        # If the stream could not be started, raise an error
                        raise
 
    def _export_stream(self) -> None:
        """
        Exports the stream data to the exchange.
        """

        # Translates the "receive" command to the "send" command
        translate = {
            'balance': 'getBalance',
            'candle': 'getCandles',
            'keepAlive': 'getKeepAlive',
            'news': 'getNews',
            'profit': 'getProfits',
            'tickPrices': 'getTickPrices',
            'trade' : 'getTrades',
            'tradeStatus': 'getTradeStatus',
            }

        # Loop until the run flag is set to False
        while self._stream['run']:
            if self._halt:
                continue

            self._logger.info("Streaming data ...")

            # Get the stream data from the server
            response_list = self._receive_stream()

            # Check if the response list is empty
            if response_list == []:
                continue

            # Reset the maximum queue level
            max_queue_level = 0

            # Loop through the response list
            for response in response_list:
                # Response must contain 'command' key with command
                if 'command' not in response:
                    self._logger.error("No command in response")
                    raise ValueError("No command in response")

                # Response must contain 'data' key with data
                if 'data' not in response:
                    self._logger.error("No data in response")
                    raise ValueError("No data in response")
            
                # KeepAlive stream is not necessary for the exchange
                if response['command'] == 'keepAlive':
                    continue

                # Check if the response is for a stream task
                task = translate[response['command']]
                if task in ['getCandles', 'getTickPrices']:
                    task += "_" + str(response['data']['symbol'])
                if task not in self._stream_tasks:
                    self._logger.warning("Stream task not found")
                    continue
                    # No raise of exception because even if task is stopped
                    # there could still be a rest of data to be received
                    
                self._logger.info("Data received for " + task)

                # Check the queue level of the stream task
                self._stream_tasks[task]['queue_level'] = self._stream_tasks[task]['exchange']._queue.qsize()/self._max_queue_elements
                # Check the maximum queue level of all updated tasks
                # Has to be done before the filling of the queue to give user a chance to process the data in the queue
                max_queue_level = max(max_queue_level, self._stream_tasks[task]['queue_level'])

                try:
                    # Put the data into the queue for the exchange
                    self._stream_tasks[task]['exchange']._put(response['data'])
                except Full:
                    self._logger.error("Queue overflow. Incoming messages not processed fast enough")
                    # Stop the stream task not possible because this method is within the stream thread
                    # The healthcheck method of the Handlermanager will stop the stream task
                    self._stream['run'] = False
                    break

            # Calculate the sliding mean of the maximum queue level
            self._calculate_sm_max_queue_level(max_queue_level)

        self._logger.info("All streams stopped")

    def _calculate_sm_max_queue_level(self, max_queue_level: float) -> None:
        """
        Calculates the sliding mean of the maximum queue level.

        Args:
            max_queue_level (float): The maximum queue level.
        """

        # Append the maximum queue level to the list
        self._max_queue_levels.append(max_queue_level)

        # Keep the list of the last maximum queue levels within the sliding mean window
        if len(self._max_queue_levels) > SLIDING_MEAN_WINDOW:
            self._max_queue_levels.pop(0)

        # Calculate the sliding mean of the maximum queue level
        self._sm_max_queue_level = mean(self._max_queue_levels)

    def _receive_stream(self) -> dict:
        """
        Receives the stream data from the server.

        Returns:
            The stream data as a dictionary.
        """

        self._logger.info("Getting stream data ...")

        # Locks out the ping process
        # To avoid conflicts with the receive process
        with self._client_lock:
            # Try to get the stream data twice
            # This enables a automatic reactivation if the first attempt fails
            for tries in range(2):
                try:
                    # Receive the response from the server
                    response_list = self._receive_response(stream = True)
                    # Stream data received successfully
                    break
                except Exception as e:
                    self._logger.error(f"Failed to stream data: {e}")
                    if tries == 0:
                        # Reactivateif the first attempt fails
                        self._logger.info("Try a reactivation ...")
                        self._reactivate()
                    else:
                        # If the stream data could not be received, raise an error
                        raise

        self._logger.info("Stream data received")

        # Return the stream data
        return response_list
         
    def _stop_stream(self) -> None:
        """
        Stops the stream and ends all associated tasks.
        """

        self._logger.info("Stopping all streams ...")

        # Check if the stream was ever created
        if not self._stream:
            self._logger.warning("Stream never started")
            return
        
        # Check if the stream is intended to run
        if not self._stream['run']:
            self._logger.warning("Stream already ended")
        else:
            self._stream['run'] = False

            # Wait for the stream thread to stop
            self._stream['thread'].join(timeout = THREAD_TICKER*5)

        # Stop all stream tasks
        for task in list(self._stream_tasks): # Dynamic change of dictionary 
            self._stop_task(task = task)
            
        self._logger.info("All streams stopped")

    def _stop_task(self, task: str, kill: bool = True) -> None:
        """
        Stops a stream task at the specified index.

        Args:
            task (str): The key of the stream task.
            kill (bool, optional): A boolean indicating whether to kill the stream task. Defaults to True.

        Raises:
            KeyError: If the stream task is not found.
        """

        # Necessary if task is stopped by user(thread) and handler(delete) at the same time
        with self._stop_lock:
            # Raise an error if the stream task is not found
            if task not in self._stream_tasks:
                self._logger.error(f"Stream task {task} not found")
                raise KeyError(f"Stream task {task} not found")

            command = self._stream_tasks[task]['command']
            arguments = self._stream_tasks[task]['arguments']

            self._logger.info("Stopping stream for " + pretty(command) + " ...")

            # Locks out the ping process
            # To avoid conflicts with the stop request
            with self._client_lock:
                # Send the stop request to the server
                self._send_request(
                    command = 'stop' + command[3:], # Remove get from the command
                    arguments = {'symbol': arguments['symbol']} if 'symbol' in arguments else None
                )

            if kill:
                # Deregister the stream task
                del self._stream_tasks[task]

            self._logger.info("Stream stopped for " + pretty(command))

    def _reactivate(self) -> None:
        """
        Reactivates the StreamHandler to the DataHandler.
        """

        # At first check if the DataHandler is still active
        # because the StreamHandler dependends on the DataHandler
        self._dh._reactivate()

        # In case a other essential operation is in progress
        if self.__lock.acquire(blocking = False):
            # Only StreamHandler with active status can be reactivated
            if self.__status == Status.ACTIVE:
                try:
                    self._logger.info("Checking connection ...")
                    # Check the StreamHandler Socket
                    self.check()
                    self._logger.info("Connection is active")
                except Exception:
                    # Classmethods are to nested for a intern reactivation
                    # Setting Status on failed and wait for the healthcheck of the Handlermanager
                    # to reactivate the Streams in an other StreamHandler
                    self.__status = Status.FAILED

            # Release the handler lock
            self.__lock.release()
        else:
            self._logger.warning("Reactivation not possible. Other essential operation in progress")
    
    def _transplant_stream_task(self, task_args: dict) -> None:
        """
        Transplants the stream tasks from another StreamHandler.

        Args:
            task_args (dict): The arguments for the stream tasks
        """

        # In case a other essential operation is in progress
        with self.__lock:
            self._logger.info("Transplanting stream tasks ...")
            # Sets status of the StreamHandler to suspended during the transplant
            self.__status = Status.SUSPENDED

            # Extract the necessary information from the task
            command = task_args['command']
            arguments = task_args['arguments']
            exchange = task_args['exchange']

            # Start the stream for the specified command
            self._stream_data(
                command = command,
                exchange = exchange,
                **arguments
            )

            self._logger.info("Stream tasks transplanted")

        # Sets status of the StreamHandler back to active after the transplant
        self.__status = Status.ACTIVE

    @property
    def dh(self) -> _DataHandler:
        return self._dh

    @dh.setter
    def dh(self, value: _DataHandler) -> None:
        
        # In case a other essential operation is in progress
        with self.__lock:
            # Shut down the StreamHandler
            self._logger.info("Shutting down StreamHandler ...")
            self.__status = Status.SUSPENDED
            self._stop_ping()

            self._logger.info("Stopping all streams ...")
            self._halt = True
            for task in list(self._stream_tasks): # Dynamic change of dictionary 
                self._stop_task(task = task, kill = False)
            self._logger.info("All streams stopped")

            self.close()
            self._dh._detach_stream_handler(handler = self)

            # Change the DataHandler
            self._logger.info("Changing DataHandler")
            self._dh = value

            # Boot up the StreamHandler
            self._dh._attach_stream_handler(handler = self)
            self.create()
            self.open()
            
            self._logger.info("Restarting all streams ...")
            for task in list(self._stream_tasks): # Dynamic change of dictionary 
                command = self._stream_tasks[task]['command']
                kwargs = self._stream_tasks[task]['arguments']
                self._start_stream(command, **kwargs)
                self._halt = False # Restart Stream right after the first task is restarted
            self._logger.info("All streams restarted")

            self._start_ping(handler = self)
            self.__status = Status.ACTIVE
            
            self._logger.info("StreamHandler reinitiated")
    
    @property
    def status(self) -> Status:
        return self.__status
    
    @status.setter
    def status(self, value: Status) -> None:
        self._logger.debug(f"Status externally set to {value}")
        self.__status = value

    @property
    def stream_tasks(self) -> dict:
        return self._stream_tasks
    
    @property
    def sm_max_queue_level(self) -> float:
        return self._sm_max_queue_level


class HandlerManager():
    """
    Manages the handlers for the XTB trading platform.

    Attributes:
        __status (Status): The status of the handler manager.
        __lock (Lock): The lock for essential handler operations.
        _logger (logging.Logger): The logger object used for logging.
        _demo (bool): A boolean indicating whether the handlers are for demo or real trading.
        _username (str): The username for the XTB trading platform.
        _password (str): The password for the XTB trading platform.
        _max_connections (int): Max allowed data and stream connections to server [-].
        _max_send_data (int): Max size of data sent to server at once [bytes].
        _max_received_data (int): Max size of data received from server at once [bytes].
        _max_retries (int): Max retries for request to server [-].
        _min_request_interval (float): Min allowed interval for server requests [s].
        _socket_timeout (float): The timeout for blocking stream socket connection [s].
        _max_queue_elements (int): The max number of elements in the stream queue [-].
        _dynamic_shifting (bool): Flag to allow dynamic shifting of streaming tasks.
        _handler_register (dict): The dictionary of registered handlers.
        _find_available_stream_handler (StreamHandler): Finds an available StreamHandler with capacity to accept additional tasks.
        _healthcheck_thread (CustomThread): The handler management thread.

    Methods:
        _delete: Deletes the HandlerManager instance.
        _delete_handler: Deletes a specific handler and deregisters it.
        _avlb_DataHandler: Gets an available data handler.
        _avlb_StreamHandler: Gets an available stream handler.
        _get_connection_number: Gets the number of active connections.
        _generate_DataHandler: Generates a new data handler.
        _generate_StreamHandler: Generates a new stream handler.
        _provide_DataHandler: Provides a data handler.
        _provide_StreamHandler: Provides a stream handler.
        _get_data: Retrieves data from the server.
        _stream_data: Starts streaming data from the server.
        _healthcheck: Checks the health of the handlers.
    """
        
    def __init__(
        self,
        
        max_connections: int,
        max_send_data: int,
        max_received_data: int,
        max_retries: int,
        min_request_interval: float,
        socket_timeout: float,
        max_queue_elements: int,
        dynamic_shifting: bool,

        demo: bool,

        username: Optional[str] = None,
        password: Optional[str] = None,
        path: Optional[str] = None,

        logger: Optional[logging.Logger] = None
        ) -> None:
        """
        Initializes a new instance of the HandlerManager class.

        Args:
            max_connections (int): Max allowed data and stream connections to server [-].
            max_send_data (int): Max size of data sent to server at once [bytes].
            max_received_data (int): Max size of data received from server at once [bytes].
            max_retries (int): Max retries for request to server [-].
            min_request_interval (float): Min allowed interval for server requests [s].
            socket_timeout (float): The timeout for blocking stream socket connection [s].
            max_queue_elements (int): The max number of elements in the stream queue [-].
            dynamic_shifting (bool): Flag to allow dynamic shifting of streaming tasks.
            demo (bool, optional): Specifies whether the handlers are for demo purposes.
            username (str, optional): The username for the XTB trading platform. Defaults to None.
            password (str, optional): The password for the XTB trading platform. Defaults to None.
            path (str, optional): The path to the XTB API credentials file. Defaults to None.
            logger (logging.Logger, optional): The logger instance to use for logging. Defaults to None.
        """

        # The status of the handler is initially inactive
        # because not jet ready for usage   
        self.__status = Status.INACTIVE

        # The lock for essential manager operations
        self.__lock = Lock()

        # Thread safety necessary
        # The initialization of the class has to be finished
        # before the class can be used
        with self.__lock:
            if logger:
                # Use the provided logger
                self._logger = logger
            else:
                # In case no logger is provided, generate a new one
                self._logger = generate_logger(name = 'HandlerManager', path = Path.cwd() / "logs")

            self._logger.debug("Initializing HandlerManager ...")

            self._demo = demo

            # Check if username and password are provided
            if username and password:
                # Set the username and password
                self._logger.debug("Using provided username and password")
                self._username = username
                self._password = password
            else:
                # Sets the path to the credentials file
                if path:
                    self._logger.debug("Using provided path to credentials file")
                    set_path(path = path)

                # Get the username and password from the config file
                self._logger.debug("Getting username and password from config file")
                self._username = get_userId(self._demo)
                self._password = get_password()

            self._max_connections = max_connections
            self._max_send_data = max_send_data
            self._max_received_data = max_received_data
            self._max_retries = max_retries
            self._min_request_interval = min_request_interval
            self._socket_timeout = socket_timeout
            self._max_queue_elements = max_queue_elements
            self._dynamic_shifting = dynamic_shifting

            # Initialize the handlers dictionary
            self._handler_register = {'data': {}, 'stream': {}}

            # The HandlerManager is automatically active after initialization
            self.__status = Status.ACTIVE

            # Start the handler management thread
            self._healthcheck_thread = CustomThread(
                target = self._healthcheck,
                daemon = True
            )
            self._healthcheck_thread.start()

            self._logger.debug("HandlerManager initialized")

    def __del__(self) -> None:
        """
        Destructor method that is called when the HandlerManager object is about to be destroyed.
        It ensures that any open connections are closed properly and any resources
        are released.

        Raises:
            None
        """

        try:
            self._delete()
        except Exception as e:
            # For graceful closing no raise of exception is not allowed
            pass

    def _delete(self) -> None:
        """
        Deletes the HandlerManager instance and all associated handlers.
        """

        # In case a other essential operation is in progress
        with self.__lock:
            # Check if the HandlerManager is already deleted
            if self.__status == Status.DELETED:
                self._logger.debug("HandlerManager already deleted")
                # For graceful deletion a raise of exception is not allowed
                return
            
            self._logger.info("Deleting HandlerManager ...")
            
            for handler in list(self._handler_register['data']): # Dynamic change of dictionary 
                # Delete all data handlers
                # The DataHandler wil send a delete command to every attached StreamHandler
                if handler.status != Status.DELETED:
                    self._delete_handler(handler)

            # Set the deleted flag to True
            self.__status = Status.DELETED

            # Wait for the handler management thread to stop
            self._healthcheck_thread.join(timeout = THREAD_TICKER*5)

            self._logger.info("HandlerManager deleted")
    
    def _delete_handler(self, handler: Union[_DataHandler, _StreamHandler]) -> None:
        """
        Deletes a specific handler and deregisters it from the HandlerManager.

        Args:
            handler (Union[_DataHandler, _StreamHandler]): The handler to delete.
        """

        if isinstance(handler, _DataHandler):
            self._logger.info("Deregister DataHandler "+self._handler_register['data'][handler]['name'])
            del self._handler_register['data'][handler]
        elif isinstance(handler, _StreamHandler):
            self._logger.info("Deregister StreamHandler "+self._handler_register['stream'][handler]['name'])
            del self._handler_register['stream'][handler]

        # Delete the handler
        handler._delete()

    def _avlb_DataHandler(self) -> _DataHandler:
        """
        Gets an available data handler.

        Returns:
            _DataHandler: An available DataHandler if found.
        """

        for handler in self._handler_register['data']:
            # Check if the handler is active
            if handler.status == Status.ACTIVE:
                return handler
    
    def _avlb_StreamHandler(self) -> _StreamHandler:
        """
        Gets an available stream handler.

        Returns:
            _StreamHandler: An available StreamHandler if found.
        """

        for handler in self._handler_register['stream']:
            # Check if the handler is active
            # and the queue level is below the threshold
            if handler.status == Status.ACTIVE:
                if handler.sm_max_queue_level > QUEUE_LEVEL_THRESHOLD:
                    self._logger.info("StreamHandler "+self._handler_register['stream'][handler]['name']+" rejected for queue level over threshold")
                    continue
                return handler

    def _get_connection_number(self) -> int:
        """
        Gets the number of active connections.

        Returns:
            int: The number of active connections.
        """

        return len(self._handler_register['data']) + len(self._handler_register['stream'])

    def _generate_DataHandler(self) -> _DataHandler:
        """
        Generates a new data handler.

        Returns:
            _DataHandler: A new DataHandler.

        Raises:
            RuntimeError: If the maximum number of connections is reached.
            RuntimeError: If the DataHandler is not ready for usage.
        """

        self._logger.info("Generating DataHandler ...")

        if self._get_connection_number() >= self._max_connections:
            self._logger.error("Maximum number of connections reached")
            raise RuntimeError("Maximum number of connections reached")

        # Index the new DataHandler
        index = len(self._handler_register['data'])
        name = 'DH_' + str(index)
        dh_logger = self._logger.getChild(name)

        # Create the new DataHandler
        dh = _DataHandler(
            demo = self._demo,

            username = self._username,
            password = self._password,

            max_send_data = self._max_send_data,
            max_received_data = self._max_received_data,
            max_retries = self._max_retries,
            min_request_interval = self._min_request_interval,

            logger = dh_logger
        )

        # Check if the initialization of the DataHandler was successful
        if dh.status != Status.ACTIVE:
            self._logger.error("DataHandler not ready for usage")
            raise RuntimeError("DataHandler not ready for usage")

        # Register the new DataHandler
        self._handler_register['data'][dh] = {'name': name}

        self._logger.info("DataHandler generated")

        return dh

    def _generate_StreamHandler(self) -> _StreamHandler:
        """
        Generates a new stream handler.

        Returns:
            _StreamHandler: A new StreamHandler.

        Raises:
            RuntimeError: If the maximum number of connections is reached.
            RuntimeError: If the StreamHandler is not ready for usage.
        """

        self._logger.info("Generating StreamHandler ...")

        if self._get_connection_number() >= self._max_connections:
            self._logger.error("Maximum number of connections reached")
            raise RuntimeError("Maximum number of connections reached")

        # Index the new StreamHandler
        index = len(self._handler_register['stream'])
        name = 'SH_' + str(index)
        sh_logger = self._logger.getChild(name)

        # Create the new StreamHandler
        dh = self._provide_DataHandler()
        sh = _StreamHandler(
            data_handler = dh,
            demo = self._demo,

            max_send_data = self._max_send_data,
            max_received_data = self._max_received_data,
            max_retries = self._max_retries,
            min_request_interval = self._min_request_interval,
            socket_timeout = self._socket_timeout,
            max_queue_elements = self._max_queue_elements,

            logger = sh_logger
        )

        # Check if the initialization of the StreamHandler was successful
        if sh.status != Status.ACTIVE:
            self._logger.error("StreamHandler not ready for usage")
            raise RuntimeError("StreamHandler not ready for usage")

        # Register the new StreamHandler
        self._handler_register['stream'][sh] = {'name': name}

        self._logger.info("StreamHandler generated")

        return sh

    def _provide_DataHandler(self) -> _DataHandler:
        """
        Provides an available data handler.

        Returns:
            _DataHandler: An DataHandler if found, otherwise a new DataHandler.
        """

        # Check if an available data handler is available
        handler = self._avlb_DataHandler()

        # If no available data handler is found, generate a new one
        if not handler:
            self._logger.info("No DataHandler available")
            try:
                handler = self._generate_DataHandler()
            except RuntimeError as e:
                self._logger.error(f"Failed to generate DataHandler: {e}")
                raise

        return handler

    def _provide_StreamHandler(self) -> _StreamHandler:
        """
        Provides an available stream handler.

        Returns:
            _StreamHandler: An available stream handler if found, otherwise a new stream handler.
        """

        # Check if an available stream handler is available
        handler = self._avlb_StreamHandler()

        # If no available stream handler is found, generate a new one
        if not handler:
            self._logger.info("No StreamHandler available")
            try:
                handler = self._generate_StreamHandler()
            except RuntimeError as e:
                self._logger.error(f"Failed to generate StreamHandler: {e}")
                raise

        return handler
    
    def _get_data(
        self,
        command: str,
        **kwargs
        ) -> dict:
        """
        Retrieves data from the server.

        Args:
            command (str): The command to get data.
            **kwargs: Additional keyword arguments for the command.

        Returns:
            dict: The data from the server.
        """

        # Provide a new DataHandler that is ready for usage
        try:
            dh = self._provide_DataHandler()
        except RuntimeError as e:
            self._logger.error(f"Failed to provide DataHandler: {e}")
            # For graceful behaviour, only log the error and return
            return

        # Get the data from the server
        data = dh._get_data(command = command, **kwargs)

        return data

    def _stream_data(
        self,
        command: str,
        **kwargs
        ) -> _StreamHandler.exchange:
        """
        Starts streaming data from the server.

        Args:
            command (str): The command to start streaming data.
            **kwargs: Additional keyword arguments for the command.

        Returns:
            _StreamHandler.exchange: The exchange object for the stream task.
        """

        # Provide a new StreamHandler that is ready for usage
        try:
            sh = self._provide_StreamHandler()
        except RuntimeError as e:
            self._logger.error(f"Failed to provide StreamHandler: {e}")
            # For graceful behaviour, only log the error and return
            return

        # Start the stream for the specified command
        return sh._stream_data(command = command, **kwargs)
    
    def _find_available_stream_handler(self, exclude_handler=None) -> _StreamHandler:
        """
        Finds an available StreamHandler with capacity to accept additional tasks.

        Args:
            exclude_handler (_StreamHandler, optional): The StreamHandler to exclude from the search. Defaults to None.

        Returns:
            _StreamHandler: An available StreamHandler if found, otherwise None.
        """

        # Check for available StreamHandler with capacity to accept additional tasks
        for sh in self._handler_register['stream']:
            if sh != exclude_handler and sh.sm_max_queue_level <= QUEUE_LEVEL_THRESHOLD:
                return sh
            
    def _healthcheck(self) -> None:
        """
        Manages the handlers in case of failure and overflow.
        """

        # Initialize the probation tasks dictionary
        probation_tasks = {}
        # Initialize the probation term
        probation_term = 60

        while self.__status == Status.ACTIVE:
            for handler in list(self._handler_register['data']): # Dynamic change of dictionary 
                # Check if the handler is failed
                if handler.status == Status.FAILED:
                    # Check for connected stream handlers
                    self._logger.error(f"DataHandler {self._handler_register['data'][handler]['name']} failed")
                    if len(handler.stream_handler) > 0:
                        # Provide a new DataHandler that is ready for usage
                        try:
                            dh_new = self._provide_DataHandler()
                        except RuntimeError as e:
                            continue
                        self._logger.info(f"DataHandler {self._handler_register['data'][handler]['name']} replaced by DataHandler {self._handler_register['data'][dh_new]['name']}")
                        # Assign the new DataHandler to the connected stream handlers
                        for sh in list(handler.stream_handler): # Dynamic change of dictionary 
                            sh.dh = dh_new
                    else:
                        self._logger.error("No DataHandler available")
                    # Eventually delete the handler
                    self._delete_handler(handler = handler)

            for handler in list(self._handler_register['stream']): # Dynamic change of dictionary 
                # Check if the handler is failed
                if handler.status == Status.FAILED:
                    self._logger.error(f"StreamHandler {self._handler_register['stream'][handler]['name']} failed")
                    # Check for open stream tasks
                    if len(handler.stream_tasks) > 0:
                        # Provide a new StreamHandler that is ready for usage
                        try:
                            sh_new = self._provide_StreamHandler()
                        except RuntimeError as e:
                            continue
                        self._logger.info(f"StreamHandler {self._handler_register['stream'][handler]['name']} replaced by StreamHandler {self._handler_register['stream'][sh_new]['name']}")
                        # Assign the new StreamHandler to the stream tasks
                        for task , task_args in list(handler.stream_tasks.items()): # Dynamic change of dictionary 
                            if task_args['command'] == 'getKeepAlive':
                                # KeepAlive stream is not necessary for the exchange
                                # As it is automatically sent by the StreamHandler
                                continue
                            try:
                                self._logger.info(f"Transplanting stream task {task} to StreamHandler {self._handler_register['stream'][sh_new]['name']}")
                                sh_new._transplant_stream_task(task_args)
                            except Exception as e:
                                self._logger.error(f"Failed to transplant stream task: {e}")
                                raise
                    # Eventually delete the handler
                    self._delete_handler(handler = handler)

            # Start the dynamic shifting of streaming tasks
            if self._dynamic_shifting:
                # Check for queue overflow
                for handler in list(self._handler_register['stream']): # Dynamic change of dictionary
                    # Reset the shift tasks list
                    shift_tasks = []
                    # Check for tasks reaching threshold 80% of max queue level
                    if handler.sm_max_queue_level > QUEUE_LEVEL_THRESHOLD:
                        self._logger.warning(f"Task(s) in StreamHandler {self._handler_register['stream'][handler]['name']} reached {QUEUE_LEVEL_THRESHOLD}% of queue level threshold")
                        # Find tasks to shift
                        for task, task_args in list(handler.stream_tasks.items()):
                            if task_args['queue_level'] > QUEUE_LEVEL_THRESHOLD:
                                # Check if task is on probation
                                if task in probation_tasks.get(self._handler_register['stream'][handler]['name'], {}):
                                    # Check if task is still on probation
                                    if time.time() - probation_tasks[self._handler_register['stream'][handler]['name']][task] < probation_term:
                                        self._logger.warning(f"Stream task {task} still on probation")
                                        continue
                                self._logger.warning(f"Stream task {task} reached {QUEUE_LEVEL_THRESHOLD}% queue level threshold")
                                shift_tasks.append(task)

                    # Attempt to shift tasks to available StreamHandlers
                    for task in shift_tasks:
                        # Find an available StreamHandler to shift the task to
                        target_sh = self._find_available_stream_handler(exclude_handler=handler)
                        # If no available StreamHandler is found, provide a new one
                        if not target_sh:
                            try:
                                target_sh = self._provide_StreamHandler()
                            except RuntimeError as e:
                                continue
                            self._logger.info(f"Created new StreamHandler {self._handler_register['stream'][target_sh]['name']} for task shifting")

                        # Shift the task to the new or available StreamHandler
                        task_args = handler.stream_tasks[task]
                        try:
                            self._logger.info(f"Transplanting stream task {task} to StreamHandler {self._handler_register['stream'][sh_new]['name']}")
                            target_sh._transplant_stream_task(task_args)
                        except Exception as e:
                            self._logger.error(f"Failed to transplant stream task: {e}")
                            raise
                        # Stop the task in the old StreamHandler
                        handler._stop_task(task = task)
                        # Add the shifted task to the excep
                        probation_tasks[self._handler_register['stream'][sh_new]['name']][task] = time.time()

                # Clean up probation tasks that are not active
                for sh_name, tasks in list(probation_tasks.items()):
                    for task, timestamp in list(tasks.items()):
                        # Check if task is still in probation
                        if time.time() - timestamp > probation_term:
                            self._logger.info(f"Stream task {task} of StreamHandler {sh_name} removed from probation")
                            del probation_tasks[sh_name][task]
                    # Clean up handler entry if no more tasks are on probation
                    if not probation_tasks[sh_name]:
                        del probation_tasks[sh_name]

            # Use Thread ticker to limit the loop interval
            time.sleep(THREAD_TICKER)