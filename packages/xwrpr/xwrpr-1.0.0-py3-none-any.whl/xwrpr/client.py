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
import socket
import ssl
import time
import select
from pathlib import Path
import logging
import json
from threading import Lock
from typing import List, Optional
import errno
from xwrpr.utils import generate_logger


class SocketFail(Enum):
    """
    The SocketFail class is an enumeration class
    for the possible failure causes of the
    Client class.

    Attributes:
        CREATE (str): Client creation failed.
        WRAP (str): SSL wrapping failed.
        CONNECT (str): Connection failed.
        TRANSMIT (str): Message transmission failed.
    """

    CREATE = "create"
    WRAP = "wrap"
    CONNECT = "connect"
    TRANSMIT = "transmit"


class CheckMode(Enum):
    """
    The CheckMode class is an enumeration class
    for the possible check modes of the
    Client class.

    Attributes:
        BASIC (str): Basic check mode.
        READABLE (str): Readable check mode.
        WRITABLE (str): Writable check mode.
    """

    BASIC = "basic"
    READABLE = "readable"
    WRITABLE = "writable"


class SocketTask(Enum):
    """
    The SocketTask class is an enumeration class
    for the possible socket tasks of the
    Client class.

    Attributes:
        CONNECT (str): Connect task.
        SEND (str): Send task.
        RECEIVE (str): Receive task.
    """

    CONNECT = "connect"
    SEND = "send"
    RECEIVE = "receive"

class ClientError(Exception):
    """
    The ClientError class is a custom
    exception class for the Client class.
    """

    pass


class Client():
    """
    The Client class provides a simple interface for creating and managing a TCP/IP
    socket connection to a server. It supports both blocking and non-blocking
    modes, as well as SSL encryption. The class also provides methods for
    sending and receiving messages in JSON format over the socket connection.
    The class is designed to be thread-safe and supports the use of a lock for
    thread safety.

    Attributes:
        __socket_lock (threading.Lock): A lock for thread safety.
        __logger (logging.Logger): The logger instance to use for logging.
        _host (str): The host address to connect to.
        _port (int): The port number to connect to.
        _encrypted (bool): Indicates whether the connection should be encrypted.
        _timeout (float): The timeout value for the connection.
        _min_request_interval (float): The interval between requests in seconds.
        _max_retries (int): The maximum number of consecutive failed requests before giving up.
        _bytes_out (int): The maximum number of bytes to send in each request.
        _bytes_in (int): The maximum number of bytes to receive in each response.
        _decoder (json.JSONDecoder): The JSON decoder instance.
        _durable_json_buffer (str): The durable JSON buffer, used to accumulate partial JSON messages.
        _addresses (dict): A dictionary of available addresses for the socket connection.
        _socket (socket.socket): The socket connection instance.
        _address_key (str): The address key for the current address.
        
    Methods:
        _get_addresses: Gets the available addresses for the socket connection.
        check: Check the socket for readability, writability, or errors.
        create: Creates a socket connection thread safely.
        _create_sub: Submethod for creating a socket.
        _check_blocking: Check if the socket is in blocking mode.
        _handle_blocking_error: Handles a BlockingIOError that can occur comunicating with the socket.
        _handle_ssl_error: Handles an SSL error that can occur comunicating with the socket.
        _handle_socket_error: Handles a socket error that can occur comunicating with the socket.
        open: Opens a connection to the server.
        send: Sends a message over the socket connection.
        receive: Receives a message from the socket.
        close: Closes the connection and releases the socket thread safely.
        _close_sub: Submethod for closing the connection and releasing the socket.

    Properties:
        timeout: The timeout value for the connection.
        min_request_interval: The interval between requests in seconds.
        max_retries: The maximum number of consecutive failed requests before giving up.
        bytes_out: The maximum number of bytes to send in each request.
        bytes_in: The maximum number of bytes to receive in each response.
    """

    def __init__(
        self,
        
        host: str,
        port: int,
        
        encrypted: bool,
        timeout: Optional[float] = None,
        min_request_interval: float = 0.5,
        max_retries: int = 10,
        bytes_out: int = 1024,
        bytes_in: int = 1024,
        
        logger: Optional[logging.Logger] = None
    ) -> None:
        """
        Initializes a new instance of the Client class.

        Args:
            host (str): The host address to connect to.
            port (int): The port number to connect to.
            encrypted (bool): Indicates whether the connection should be ssl encrypted.
            timeout (float, optional): The timeout value for connection in seconds. Defaults to None.
            min_request_interval (float, optional): The minimum interval between requests in seconds. Defaults to 0.5.
            max_retries (int, optional): The maximum number of consecutive failed requests before giving up. Defaults to 10.
            bytes_out (int, optional): The maximum number of bytes to send in each request. Defaults to 1024.
            bytes_in (int, optional): The maximum number of bytes to receive in each response. Defaults to 1024.
            logger (logging.Logger, optional): The logger instance to use for logging. Defaults to None.
        """

        # Lock for thread safety of the socket
        self.__socket_lock = Lock()

        # Thread safety necessary
        # The initialization of the class has to be finished
        # before the class can be used
        with self.__socket_lock:
            if logger:
                # Generates a child logger of the provided logger
                self.__logger = logger.getChild('Clt')
            else:
                # In case no logger is provided, generate a new one
                self.__logger = generate_logger(name = 'Client', path = Path.cwd() / "logs")

            self.__logger.debug("Initializing Client ..")
            
            # Initialize the class attributes
            self._host = host
            self._port = port
            self._encrypted = encrypted

            if timeout and timeout < 0:
                self.__logger.error("The timeout argument must be greater than or equal to zero")
                raise ValueError("The timeout argument must be greater than or equal to zero")
            self._timeout = timeout

            if min_request_interval < 0:
                self.__logger.error("The min_request_interval argument must be greater than or equal to zero")
                raise ValueError("The min_request_interval argument must be greater than or equal to zero")
            self._min_request_interval = min_request_interval

            if max_retries < 0:
                self.__logger.error("The max_retries argument must be greater than or equal to zero")
                raise ValueError("The max_retries argument must be greater than or equal to zero")
            self._max_retries = max_retries

            if bytes_out < 1:
                self.__logger.error("The bytes_out argument must be greater than zero")
                raise ValueError("The bytes_out argument must be greater than zero")
            self._bytes_out = bytes_out

            if bytes_in < 1:
                self.__logger.error("The bytes_in argument must be greater than zero")
                raise ValueError("The bytes_in argument must be greater than zero")
            self._bytes_in = bytes_in

            # Initialize the JSON decoder
            self._decoder = json.JSONDecoder()
            # Initialize the durable JSON buffer
            self._durable_json_buffer = ''

            # A dictionary of available addresses for the socket connection.
            self._addresses = {}
            # Initialize the socket class attribute
            self._socket = None
            # Initialize the address key for the current address
            self._address_key = None

            # Get the available addresses for the socket connection
            self._get_addresses()
            # Create the socket
            self.create(lock = False) # Lock is managed by the calling method

            self.__logger.debug("Client initialized")

    def _get_addresses(self) -> None:
        """
        Gets the available addresses for the socket connection.

        Raises:
            ValueError: If no available addresses are found.
            ValueError: If no suitable addresses are found.
        """

        try:
            # Get all available addresses for the host and port
            avl_addresses = socket.getaddrinfo(
                host = self._host,
                port = self._port,
                family = socket.AF_UNSPEC,
                type = socket.SOCK_STREAM,
                proto = socket.IPPROTO_TCP
            )
        except socket.error as e:
            self.__logger.error(f"Failed to query address info: {e}")
            raise
        
        # Check if there are any available addresses
        num_addresses = len(avl_addresses)
        if num_addresses == 0:
            self.__logger.error("No available addresses found")
            raise ValueError("No available addresses found")
        self.__logger.debug(f"{num_addresses} addresses found")
        
        for address in avl_addresses:
            # Extract the address info         
            family, socktype, proto, cname, sockaddr = address
            flowinfo, scopeid = None, None

            if family == socket.AF_INET:
                # IPv4 sockedadress consists of (ip, port)
                ip_address, port = sockaddr
            elif family == socket.AF_INET6:
                # IPv6 sockedadress consists of (ip, port, flowinfo, scopeid)
                ip_address, port, flowinfo, scopeid = sockaddr 
            else:
                # Skip other address families
                # Only TCP/IP is supported
                continue

            # Log the suitable address
            self.__logger.debug("Suitable address:")
            self.__logger.debug(
                "\nFamily: %s\nSocket Type: %s\nProtocol: %s\nCanonical Name: %s\nIP-address: %s\nPort: %s",
                family, socktype, proto, cname, ip_address, port
            )
            if family == socket.AF_INET6:
                self.__logger.debug("Flow Info: %s\nScope ID: %s", flowinfo, scopeid)

            # Create a unique key for the address
            address_key = f"{family}__{socktype}__{proto}"
            # Store the address info and status
            self._addresses[address_key] = {
                'last_fail': None,
                'family': family,
                'socktype': socktype,
                'proto': proto,
                'sockaddr': sockaddr
            }

        # Check the number of suitable addresses
        num_addresses = len(self._addresses)
        if num_addresses == 0:
            self.__logger.error("No suitable addresses found")
            raise ValueError("No suitable addresses found")
        self.__logger.debug(f"{num_addresses} suitable addresses found")

    def check(
        self,
        mode: CheckMode = CheckMode.BASIC,
        timeout: Optional[float] = None
    ) -> None:
        """
        Check the socket for readability, writability, or errors without making a request to the server.

        Args:
            mode (CheckMode, optional): The mode of the socket check. Can be one of BASIC, READABLE, or WRITABLE. Defaults to BASIC.
            timeout (float, optional): The timeout value for the check in seconds. Defaults is the timeout value of the connection.

        Raises:
            socket.error: If there is an error with the socket in BASIC mode.
            TimeoutError: If the socket does not become ready (readable or writable) within the specified timeout.
        """

        # If no timeout is specified, use the timeout value of the connection
        if timeout is None:
            timeout = self._timeout

        # Define the socket lists based on the requested mode
        to_read = [self._socket] if mode in (CheckMode.READABLE, CheckMode.BASIC) else []
        to_write = [self._socket] if mode in (CheckMode.WRITABLE, CheckMode.BASIC) else []
        errored = [self._socket]

        # Check the socket for readability, writability, or errors
        readable, writable, errored = select.select(to_read, to_write, errored, timeout)

        # Check if the socket timed out
        if not readable and not writable and not errored:
            self.__logger.error("Socket did not respond within the timeout period")
            raise TimeoutError("Socket did not respond within the specified timeout")

        # Check for errors in BASIC mode
        if mode == CheckMode.BASIC and self._socket in errored:
            self.__logger.error("Socket error after check")
            raise socket.error("Socket error after check")
        
        # Check for readability if READABLE mode is specified
        if mode == CheckMode.READABLE and self._socket not in readable:
            self.__logger.error("Socket is not readable within the specified time")
            raise TimeoutError("Socket is not readable within the specified time")
        
         # Check for writability if WRITABLE mode is specified
        if mode == CheckMode.WRITABLE and self._socket not in writable:
            self.__logger.error("Socket is not writable within the specified time")
            raise TimeoutError("Socket is not writable within the specified time")
        
    def create(self, excluded_fails: List[SocketFail] = [], lock: bool = True) -> None:
        """
        Creates a socket

        Args:
            excluded_fails (List[SocketFail], optional): A list of failure causes to exclude from retrying. Defaults to [].
            lock (bool, optional): Indicates whether to use the lock for thread safety. Defaults to True.
        """

        # Thread safety necessary
        # Socket can just be created once
        if lock:
            # Lock is not managed by the calling method
            with self.__socket_lock:
                self._create_sub(excluded_fails = excluded_fails)
        else:
            # Lock is managed by the calling method
            self._create_sub(excluded_fails = excluded_fails)

    def _create_sub(self, excluded_fails: List[SocketFail] = []) -> None:
        """
        Submethod for creating a socket.

        Args:
            excluded_fails (List[SocketFail], optional): A list of failure causes to exclude from retrying. Defaults to [].

        Raises:
            ClientError: If all attempts to create the socket fail.
        """

        self.__logger.info("Creating socket ...")

        # Check for existing socket
        if isinstance(self._socket, socket.socket) and self._socket.fileno() != -1:
            self.__logger.warning("Socket already exists")
            # Close the existing socket
            self.close(lock = False) # Lock is managed by the calling method

        # Loop all suitable addresses until a socket is created
        # or all addresses are tried or an error occurs
        for address_key, address in self._addresses.items():
            # Check if the andress has unallowed fails
            if address['last_fail'] in excluded_fails:
                self.__logger.debug(f"Excluded address {address}")
                continue

            self.__logger.debug(f"Trying address {address_key} ...")
            try:
                # Create the socket
                self._socket = socket.socket(
                    family = address['family'],
                    type = address['socktype'],
                    proto = address['proto'],
                )
            except socket.error as e:
                self.__logger.error(f"Failed to create socket: {e}")
                # Log the failure cause
                self._addresses[address_key]['last_fail'] = SocketFail.CREATE
                # Close the socket if it is not stable
                self.close(lock = False) # Lock is managed by the calling method
                # Try the next address
                continue
            self.__logger.info("Socket created")

            # Set the socket blocking mode
            # Setting the blocking mode before SSL wrapping ensures that the socket behaves
            # consistently during the entire SSL handshake and subsequent operations.
            if self._timeout is None:
                # Fully blocking mode (wait indefinitely)
                self._socket.setblocking(True)
                self.__logger.debug("Setting socket to fully blocking mode without timeout")
            elif self._timeout > 0:
                # Blocking with a timeout, which still makes getblocking() return True
                self._socket.settimeout(self._timeout)
                self.__logger.debug("Setting blocking mode with a timeout of: %s seconds", self._timeout)
            else:
                # Fully non-blocking mode (returns immediately)
                self._socket.setblocking(False)
                self.__logger.debug("Setting socket to fully non-blocking mode")

            # Wrap the socket with SSL encryption
            # Wraping before connection avoids exposure of sensitive data 
            # during the connection process
            if self._encrypted:
                try:
                    self.__logger.info("Wrapping socket with SSL ...")
                    # Create a default SSL context
                    context = ssl.create_default_context()
                    # Wrap the socket with SSL encryption
                    self._socket = context.wrap_socket(
                        sock = self._socket,
                        server_hostname = self._host
                    )
                except ssl.SSLError as e:
                    self.__logger.error(f"Failed to wrap socket: {e}")
                    # Log the failure cause
                    self._addresses[address_key]['last_fail'] = SocketFail.WRAP
                    # Close the socket if it is not stable
                    self.close(lock = False) # Lock is managed by the calling method
                    # Try the next address
                    continue
                self.__logger.info("Socket wrapped")

            # Socket successfully created
            # Store the address key
            self._address_key = address_key
            return

        # If all attempts to create the socket failed raise an exception
        self.__logger.error("All attempts to create socket failed")
        raise ClientError("All attempts to create socket failed")
    
    def _check_blocking(self) -> bool:
        """
        Check if the socket is in blocking mode.

        Returns:
            bool: True if the socket is in blocking mode, False otherwise.

        Raises:
            ClientError: If the socket is not created yet.
        """

        try:
            # Check if the socket is in blocking mode
            blocking = self._socket.getblocking()
        except AttributeError as e:
            # If the socket is not created yet
            self.__logger.error(f"Socket not yet created: {e}")
            raise ClientError("Socket not yet created") from e

        return blocking
    
    def _handle_blocking_error(self, error: BlockingIOError, task: SocketTask, blocking: bool) -> None:
        """
        Handles a BlockingIOError that can occur while communicating with the socket.

        Args:
            error (BlockingIOError): The blocking error instance.
            task (SocketTask): The task of the socket operation. Can be one of 'CONNECT', 'SEND', or 'RECEIVE'.
            blocking (bool): Indicates whether the socket is in blocking mode.

        Raises:
            ClientError: Unexpected BlockingIOError.
            TimeoutError: If the socket does not become ready within the specified timeout.
        """

        if blocking:
            # If socket is in blocking mode, raise an exception
            self.__logger.error(f"Unexpected BlockingIOError in blocking socket mode: {error}")
            raise ClientError("Unexpected BlockingIOError in blocking socket mode") from error
        
        if task in {SocketTask.CONNECT, SocketTask.SEND} and error.errno == errno.EINPROGRESS:
            # In non-blocking mode, the socket may not be ready yet, so check 
            self.__logger.debug("BlockingIOError: Non-blocking connection in progress, awaiting readiness...")
        elif task in {SocketTask.CONNECT, SocketTask.SEND} and error.errno == errno.EALREADY:
            # Operation already in progress, allow another attempt to complete
            self.__logger.debug("BlockingIOError: Operation already in progress, retrying...")
        elif task in {SocketTask.SEND, SocketTask.RECEIVE} and error.errno in {errno.EAGAIN, errno.EWOULDBLOCK}:
            # For non blocking sockets with a timeout equal to zero, the operation would not raise a
            # socket.timeot exception but these BlockingIOErrors. So to get the same behavior as for
            # sockets with a timeout greater than zero, the method jus passes
            self.__logger.debug("BlockingIOError: Operation would block, passing ...")
        else:
            # Unexpected BlockingIOError in non-blocking mode
            self.__logger.error(f"Unexpected BlockingIOError in non blocking socket mode: {error}")
            raise ClientError("Unexpected BlockingIOError in non blocking socket mode") from error
        
    def _handle_ssl_error(self, error: ssl.SSLError, task: SocketTask, blocking: bool) -> None:
        """
        Handles an SSL error that can occur while communicating with the socket.

        Args:
            error (ssl.SSLError): The SSL error instance.
            task (SocketTask): The task of the socket operation. Can be one of 'CONNECT', 'SEND', or 'RECEIVE'.
            blocking (bool): Indicates whether the socket is in blocking mode.

        Raises:
            ClientError: Unexpected SSL error.
            TimeoutError: If the socket does not become ready within the specified timeout.
        """

        if blocking:
            # If socket is in blocking mode, raise an exception
            self.__logger.error(f"Unexpected SSL error in blocking socket mode: {error}")
            raise ClientError("Unexpected SSL error in blocking socket mode") from error
        
        if task in {SocketTask.CONNECT, SocketTask.SEND} and error.errno == ssl.SSL_ERROR_WANT_WRITE:
            # Socket was in waiting state, try again
            self.__logger.debug("SSL write operation would block, awaiting writability...")
            # Wait until the socket is ready or TimeoutError is raised
            try:
                self.check(mode = CheckMode.WRITABLE)
            except TimeoutError as error:
                self.__logger.error(f"SSL write operation timed out while awaiting writability: {error}")
                raise TimeoutError("SSL write operation timed out while awaiting writability") from error
        elif task == SocketTask.RECEIVE and error.errno == ssl.SSL_ERROR_WANT_READ:
            # Socket was in waiting state, try again
            self.__logger.debug("SSL read operation would block, awaiting readability...")
            # Wait until the socket is ready or TimeoutError is raised
            try:
                self.check(mode = CheckMode.READABLE)
            except TimeoutError as error:
                self.__logger.error(f"SSL read operation timed out while awaiting readability: {error}")
                raise TimeoutError("SSL read operation timed out while awaiting readability") from error
        else:
            # Unexpected SSL error in non-blocking mode
            self.__logger.error(f"Unexpected SSL error in non blocking socket mode: {error}")
            raise ClientError("Unexpected SSL error in non blocking socket mode") from error
        
    def _handle_socket_error(self, error: socket.error, task: SocketTask, blocking: bool) -> None:
        """
        Handles a general socket error that can occur while communicating with the socket.

        Args:
            error (socket.error): The socket error instance.
            task (SocketTask): The task of the socket operation. Can be one of 'CONNECT', 'SEND', or 'RECEIVE'.
            blocking (bool): Indicates whether the socket is in blocking mode.

        Raises:
            ClientError: Unexpected socket error.
            TimeoutError: If the socket does not become ready within the specified timeout.
        """

        if blocking:
            # If socket is in blocking mode, raise an exception
            self.__logger.error(f"Unexpected socket error in blocking socket mode: {error}")
            raise ClientError("Unexpected socket error in blocking socket mode") from error

        if task in {SocketTask.CONNECT, SocketTask.SEND} and error.errno == errno.EINPROGRESS:
            # In non-blocking mode, the socket may not be ready yet, so check
            self.__logger.debug("SocketError: Non-blocking connection in progress, awaiting writability...")
        elif task == SocketTask.CONNECT and error.errno == errno.EISCONN:
            self.__logger.debug("SocketError: Socket is already connected.")
            # Connection is considered successful, no further action needed
        elif task in {SocketTask.CONNECT, SocketTask.SEND} and error.errno == errno.EALREADY:
            # Operation already in progress, allow another attempt to complete
            self.__logger.debug("SocketError: Operation already in progress, retrying...")
        else:
            # Unexpected socket error in non-blocking mode
            self.__logger.error(f"Unexpected socket error in non blocking socket mode: {error}")
            raise ClientError("Unexpected socket error in non blocking socket mode") from error

    def open(self, recreate: bool = True) -> None:
        """
        Opens a connection to the server.

        Args:
            recreate (bool, optional): Indicates whether to recreate the socket if the connection fails. Defaults to True.

        Raises:
            Exception: If there is an error opening the connection.
        """

        # Thread safety necessary
        # Socket can just be connected once
        with self.__socket_lock:
            self.__logger.info("Opening connection ...")

            # Check if the socket is in blocking mode
            blocking = self._check_blocking()

            # Loop until the connection is established
            # or an error occurs
            connection_attempts = 0
            while True:
                try:
                    try:
                        try:
                            # Request limitation to the server
                            time.sleep(self._min_request_interval)
                            # Ceck if socket is already connected
                            if self._socket.getpeername():
                                # Return if the socket is already connected
                                self.__logger.info("Connection opened")
                                break
                        except socket.error:
                            # Pass if the socket is not connected
                            pass

                        try:
                            # Connect to the server
                            self._socket.connect(self._addresses[self._address_key]['sockaddr'])
                            # Exit loop if connection was successful
                            self.__logger.info("Connection opened")
                            break
                        except socket.timeout:
                            # If the connection times out, try again
                            # Can just happen in non-blocking mode
                            self.__logger.debug("Socket connection timed out")
                        except BlockingIOError as e:
                            # Handle the blocking error
                            self._handle_blocking_error(error = e, task = SocketTask.CONNECT, blocking = blocking)
                        except ssl.SSLError as e:
                            # Handle the SSL error
                            self._handle_ssl_error(error = e, task = SocketTask.CONNECT, blocking = blocking)
                        except socket.error as e:
                            # Handle the socket error
                            self._handle_socket_error(error = e, task = SocketTask.CONNECT, blocking = blocking)
                    except (ClientError, TimeoutError) as e:
                        # Decide about a new connection attempt
                        if connection_attempts <= self._max_retries:
                            self.__logger.debug("Retrying connection ...")
                            connection_attempts += 1
                            self.__logger.debug(f"Attempt {connection_attempts} of {self._max_retries + 1}")
                        else:
                            self.__logger.error(f"Max fails reached. Unable to connect to server: {e}")
                            raise
                except Exception as e:
                    # In case of too many fails or unexpected error
                    self.__logger.error(f"Error opening connection: {e}")
                    # Log the failure cause
                    self._addresses[self._address_key]['last_fail'] = SocketFail.CONNECT

                    # Close the connection if it is not stable
                    self.close(lock = False) # Lock is managed by the calling method
                    if recreate:
                        # Try to create a new socket
                        self.__logger.info("Attempting to recreate socket ...")
                        # Excludtion of the fails guarantees that not the same address is tried again
                        self.create(
                            excluded_fails = [SocketFail.CREATE, SocketFail.WRAP, SocketFail.CONNECT],
                            lock = False # Lock is managed by the calling method
                        )
                    else:
                        self.__logger.debug("Recreation of socket disabled")
                        raise

    def send(self, msg: str) -> None:
        """
        Sends a message over the socket connection.

        Args:
            msg (str): The message to send.

        Raises:
            Exception: If there is an error sending the message
        """

        # Thread safety necessary
        # To limit the requests to the server
        with self.__socket_lock:
            self.__logger.info("Sending message ...")

            # Check if the socket is in blocking mode
            blocking = self._check_blocking()

            try:
                # Convert the message to a json string
                msg =  json.dumps(msg)
                # Encode the json string as UTF-8
                msg = msg.encode("utf-8")
            except json.JSONDecodeError as e:
                self.__logger.error(f"Error dumping message to json: {e}")
                raise
            except UnicodeEncodeError as e:
                self.__logger.error(f"Error encoding message to utf-8: {e}")
                raise

            # Initialize the message length variables
            sent_msg_length = 0
            msg_length = len(msg)

            # Loop until the entire message is sent
            # Or an error occurs
            send_attempts = 0
            while sent_msg_length < msg_length:
                # Calculate the package size
                # for the next sending attempt
                package_size = min(self._bytes_out, msg_length - sent_msg_length)
                try:
                    try:
                        try:
                            # Request limitation to the server
                            time.sleep(self._min_request_interval)
                            # Attempt to send the message chunk
                            sent_msg_length += self._socket.send(msg[sent_msg_length:sent_msg_length + package_size])
                            self.__logger.debug(f"Sent message chunk of size {package_size} bytes")
                        except socket.timeout:
                            # If the connection times out, try again
                            # Can just happen in non-blocking mode
                            self.__logger.debug("Socket connection timed out")
                        except BlockingIOError as e:
                            # Handle the blocking error
                            self._handle_blocking_error(error = e, task = SocketTask.SEND, blocking = blocking)
                        except ssl.SSLError as e:
                            # Handle the SSL error
                            self._handle_ssl_error(error = e, task = SocketTask.SEND, blocking = blocking)
                        except socket.error as e:
                            # Handle the socket error
                            self._handle_socket_error(error = e, task = SocketTask.SEND, blocking = blocking)
                    except (ClientError, TimeoutError) as e:
                        # Decide about a new sending attempt
                        if send_attempts <= self._max_retries:
                            self.__logger.debug("Retry sending ...")
                            send_attempts += 1
                            self.__logger.debug(f"Attempt {send_attempts} of {self._max_retries+1}")
                        else:
                            self.__logger.error(f"Max fails reached. Unable to reach server: {e}")
                            raise
                except Exception as e:
                    # In case of too many fails or unexpected error
                    self.__logger.error(f"Error sending message: {e}")
                    # Log the failure cause
                    self._addresses[self._address_key]['last_fail'] = SocketFail.TRANSMIT
                    raise
                        
            self.__logger.info("Message sent")

    def receive(self) -> List[str]:
        """
        Receives a message from the socket.

        Returns:
            List[str]: The received messages as a list of strings.

        Raises:
            Exception: If there is an error receiving the message.
            ValueError: If no message is received in blocking mode.
            Exception: If there is an error accumulating the message.
        """

        # Thread safety necessary
        # Socket can just handle one request at a time
        with self.__socket_lock:
            self.__logger.info("Receiving message ...")

            # Check if the socket is in blocking mode
            blocking = self._check_blocking()

            # Initialize the buffer
            bit_buffer = b''
            temporary_json_buffer = self._durable_json_buffer # Hand over the data to the temporary buffer
            full_msg = ''
            msg_list = []
            
            # Loop until the entire message is received
            # Or an error occurs
            receive_attempts = 0
            while True:
                try:
                    try:
                        try:
                            # Receive the message chunk
                            msg_chunk = self._socket.recv(self._bytes_in)
                            self.__logger.debug(f"Received message chunk of size {len(msg_chunk)} bytes")
                        except socket.timeout:
                            # If the connection times out, stop receiving
                            # Can just happen in non-blocking mode
                            self.__logger.debug("Socket connection timed out")
                            break
                        except BlockingIOError as e:
                            # Handle the blocking error
                            self._handle_blocking_error(error = e, task = SocketTask.RECEIVE, blocking = blocking)
                            break
                        except ssl.SSLError as e:
                            # Handle the SSL error
                            self._handle_ssl_error(error = e, task = SocketTask.RECEIVE, blocking = blocking)
                            break
                        except socket.error as e:
                            # Handle the socket error
                            self._handle_socket_error(error = e, task = SocketTask.RECEIVE, blocking = blocking)
                            break
                    except (ClientError, TimeoutError) as e:
                        # Decide about a new receiving attempt
                        if receive_attempts <= self._max_retries:
                            self.__logger.debug("Retry receiving ...")
                            receive_attempts += 1
                            self.__logger.debug(f"Attempt {receive_attempts} of {self._max_retries+1}")
                            continue
                        else:
                            self.__logger.error(f"Max fails reached. Unable to reach server: {e}")
                            raise
                except Exception as e:
                    # In case of too many fails or unexpected error
                    self.__logger.error(f"Error receiving message: {e}")
                    # Log the failure cause
                    self._addresses[self._address_key]['last_fail'] = SocketFail.TRANSMIT
                    raise
                    
                # Check if the message is empty
                if not msg_chunk:
                        self.__logger.error("Socket connection broken. May use a bigger socket-timeout.")
                        raise ValueError("Socket connection broken. May use a bigger socket-timeout.")
                                        
                # Append the received chunk to the buffer
                bit_buffer += msg_chunk

                try:
                    # Try decoding the buffer as UTF-8
                    msg = bit_buffer.decode("utf-8")
                    self.__logger.debug(f"Received complete message of size {len(msg)} bytes")
                    # Clear the buffer after successful decoding
                    bit_buffer = b''
                except UnicodeDecodeError:
                    # If the buffer does not contain a complete message yet, we will continue receiving
                    self.__logger.debug("Partial message received, waiting for more data")
                    continue

                try:
                    # Remove any leading whitespace from the temporary buffer
                    # In case the buffer already contains a partial message
                    if temporary_json_buffer and temporary_json_buffer[0] in ' \n\t':
                        self.__logger.debug("Removing leading whitespace")
                        temporary_json_buffer = temporary_json_buffer.lstrip()
                except Exception as e:
                    self.__logger.error(f"Error accumulating message: {e}")
                    raise Exception("Error accumulating message") from e
                
                # Accumulate the received data into the buffer
                temporary_json_buffer += msg

                # Decode all complete JSON messages from the buffer
                while True:
                    try:
                        # Decode the buffer as JSON
                        full_msg, pos = self._decoder.raw_decode(temporary_json_buffer)
                        self.__logger.debug("Decoded message: " + str(full_msg)[:100] + ('...' if len(str(full_msg)) > 100 else ''))
                        # Append the full message to the list
                        msg_list.append(full_msg)

                        # Update the buffer to only keep the undecoded data
                        temporary_json_buffer = temporary_json_buffer[pos:].strip()
                        # Exit the loop if the entire buffer was decoded
                        if not temporary_json_buffer:
                            break
                    except json.JSONDecodeError:
                        # The JsonDecodeError indicates that the json_buffer does not contain a complete JSON message yet
                        self.__logger.debug("Incomplete JSON, left in buffer")
                        break

                # If at least one complete message was received, break
                if len(msg_list) > 0:
                    # If there is remaining data, store it in the durable buffer
                    if temporary_json_buffer:
                        self._durable_json_buffer = temporary_json_buffer[pos:].strip()
                        self.__logger.debug(f"Partial message stored in durable buffer length: {len(self._durable_json_buffer)}")
                    break

                self.__logger.debug("Incomplete JSON, awaiting more data")
        
            self.__logger.info("Message received")

            # Return the list of received messages
            return msg_list

    def __del__(self) -> None:
        """
        Destructor method that is called when the Client object is about to be destroyed.
        It ensures that any open connections are closed properly and any resources
        are released.

        Raises:
            None
        """

        try:
            self.close()
        except Exception as e:
            # For graceful closing no raise of exception is not allowed
            pass

    def close(self, lock: bool = True) -> None:
        """
        Closes the connection and releases the socket.

        Args:
            lock (bool, optional): Indicates whether to use the lock for thread safety. Defaults to True.
        """

        # Thread safety necessary
        # Socket can just be closed once
        if lock:
            # Lock is not managed by the calling method
            with self.__socket_lock:
                self._close_sub()
        else:
            # Lock is managed by the calling method
            self._close_sub()

    def _close_sub(self) -> None:
        """
        Submethod for closing the connection and releasing the socket.

        Raises:
            None
        """

        # Check if the socket is in a basic state
        if self._socket.fileno() == -1:
            self.__logger.warning("Connection and socket already closed.")
            return

        try:
            # Shut down the connection
            self.__logger.info("Closing connection ...")
            self._socket.shutdown(socket.SHUT_RDWR)
            self.__logger.info("Connection shut down successfully.")
        except OSError as e:
            # Handle the error if the socket is already disconnected
            if e.errno == errno.ENOTCONN:
                self.__logger.info("Socket already disconnected")
            else:
                self.__logger.error(f"Error shutting down socket: {e}")
        finally:
            try:
                # Close the socket
                self.__logger.info("Closing socket ...")
                self._socket.close()
                self.__logger.info("Socket closed.")
            except OSError as e:
                self.__logger.error(f"Error closing socket: {e}")
            # Flush the durable JSON buffer
            self.__logger.info("Flushing durable JSON buffer ...")
            self._durable_json_buffer = ''
            
    @property
    def timeout(self) -> Optional[float]:
        return self._timeout
    
    @timeout.setter
    def timeout(self, value: Optional[float] = None) -> None:
        # Check if the timeout value is valid
        if value and value < 0:
            self.__logger.error("The timeout argument must be greater than or equal to zero")
            raise ValueError("The timeout argument must be greater than or equal to zero")

        if self._timeout != None and value != None and self._timeout != value:
            # Non blocking mode hasnt changed
            # Just set the new timeout value
            self._timeout = value
            self._socket.settimeout(self._timeout)
        elif self._encrypted and self._timeout == None and value != None or self._timeout != None and value == None:
            # If the blocking mode has changed, and the socket is ssl wrapped
            # the socket has to be reconnected for a correct wrapping behavior
            connected = False
            try:
                # Ceck if socket is already connected
                if self._socket.getpeername():
                    connected = True
            except AttributeError:
                # Pass if the socket is not created yet
                pass
            except socket.error:
                # Pass if the socket is not connected
                pass

            # Set the new timeout value
            self._timeout = value
            # Recreate the socket with the new timeout value
            self.create()
            if connected:
                # If the socket was connected, open the connection again
                self.open()

    @property
    def min_request_interval(self) -> float:
        return self._min_request_interval

    @min_request_interval.setter
    def min_request_interval(self, value: float) -> None:
        # Check if the interval value is valid
        if value < 0:
            raise ValueError("Interval must be greater than or equal to zero")
        # Set the new interval value
        self._min_request_interval = value

    @property
    def max_retries(self) -> int:
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value: int) -> None:
        # Check if the max retries value is valid
        if value < 0:
            raise ValueError("Max fails must be greater than or equal to zero")
        # Set the new max retries value
        self._max_retries = value

    @property
    def bytes_out(self) -> int:
        return self._bytes_out

    @bytes_out.setter
    def bytes_out(self, value: int) -> None:
        # Check if the bytes out value is valid
        if value < 1:
            raise ValueError("Bytes out must be greater than or equal to one")
        # Set the new bytes out value
        self._bytes_out = value

    @property
    def bytes_in(self) -> int:
        return self._bytes_in

    @bytes_in.setter
    def bytes_in(self, value: int) -> None:
        # Check if the bytes in value
        if value < 1:
            raise ValueError("Bytes in must be greater than or equal to one")
        # Set the new bytes in value
        self._bytes_in = value