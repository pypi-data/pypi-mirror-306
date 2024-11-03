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
from threading import Lock
import logging
from pathlib import Path
import configparser
from typing import Union, List, Optional, Dict
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta # Necessary for timedeltas > 1 month
from xwrpr.handler import HandlerManager,  _StreamHandler
from xwrpr.utils import generate_logger, calculate_timesteps, datetime_to_unixtime


# Read the configuration file
config = configparser.ConfigParser()
config_path = Path(__file__).parent.absolute()/'api.ini'
config.read(config_path)

MAX_CONNECTIONS = config.getint('CONNECTION', 'MAX_CONNECTIONS')
MAX_SEND_DATA = config.getint('CONNECTION', 'MAX_SEND_DATA')
MAX_RECEIVED_DATA = config.getint('CONNECTION', 'MAX_RECEIVED_DATA')
MAX_RETRIES = config.getint('CONNECTION', 'MAX_RETRIES')
MIN_REQUEST_INTERVAL = float(config.getint('CONNECTION', 'MIN_REQUEST_INTERVAL')/1000)
SOCKET_TIMEOUT = float(config.getint('CONNECTION', 'SOCKET_TIMEOUT')/1000)
MAX_QUEUE_ELEMENTS = config.getint('CONNECTION', 'MAX_QUEUE_ELEMENTS')
DYNAMIC_SHIFTING = config.getboolean('CONNECTION', 'DYNAMIC_SHIFTING')


class Status(Enum):
    """
    Enum class for the status of the wrapper.

    Attributes:
        INACTIVE: The handler is inactive.
        ACTIVE: The handler is active.
        DELETED: The handler is deleted.
    """

    INACTIVE = "inactive"
    ACTIVE = "active"
    DELETED = "deleted"


class Wrapper(HandlerManager):
    """
    Wrapper class for XTB API.

    Attributes:
        __status (Status): The status of the wrapper.
        __lock (Lock): The lock for essential wrapper operations.
        _logger (logging.Logger): The logger object to use for logging.

    Methods:
        delete: Deletes the Wrapper.
        _open_stream_channel: Opens a channel for the streaming of data.
        streamBalance: Allows to get actual account indicators values in real-time.
        streamCandles: Subscribes for and unsubscribes from API chart candles.
        streamNews: Subscribes for and unsubscribes from news.
        streamProfits: Subscribes for and unsubscribes from profits.
        streamTickPrices: Establishes subscription for quotations.
        streamTrades: Establishes subscription for user trade status data.
        streamTradeStatus: Allows to get status for sent trade requests in real-time.
        _open_data_channel: Opens a data channel and retrieves data.
        getAllSymbols: Returns array of all symbols available for the user.
        getCalendar: Returns calendar with market events.
        getChartLastRequest: Returns chart info, from start date to the current time.
        getChartRangeRequest: Returns chart info with data between given start and end dates.
        getCommissionDef: Returns calculation of commission and rate of exchange for a given symbol and volume.
        getCurrentUserData: Returns information about account currency, and account leverage.
        getIbsHistory: Returns IBs data from the given time range. (deprecated)
        getMarginLevel: Returns various account indicators.
        getMarginTrade: Returns expected margin for given instrument and volume.
        getNews: Returns news from trading server which were sent within specified period of time.
        getProfitCalculation: Calculates estimated profit for given deal data.
        getServerTime: Returns current time on trading server.
        getStepRules: Returns a list of step rules for DMAs.
        getSymbol: Returns information about symbol available for the user.
        getTickPrices: Returns array of current quotations for given symbols.
        getTradeRecords: Returns array of trades listed in orders argument.
        getTrades: Returns array of trades for the user.
        getTradesHistory: Returns array of trades history for the user.
        getTradingHours: Returns quotes and trading times.
        getVersion: Returns the current API version.
        tradeTransaction: Starts trade transaction.
        tradeTransactionStatus: Returns current transaction status.
    """

    def __init__(
        self,
        
        demo: bool = True,

        username: Optional[str] = None,
        password: Optional[str] = None,
        path: Optional[str] = None,

        max_connections: int = MAX_CONNECTIONS,
        max_send_data: int = MAX_SEND_DATA,
        max_received_data: int = MAX_RECEIVED_DATA,
        max_retries: int = MAX_RETRIES,
        min_request_interval: float = MIN_REQUEST_INTERVAL,
        socket_timeout: float = SOCKET_TIMEOUT,
        max_queue_elements: int = MAX_QUEUE_ELEMENTS,
        dynamic_shifting: bool = DYNAMIC_SHIFTING,

        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Initializes a new instance of the Wrapper class.

        Args:
            demo (bool): A boolean indicating whether the handler is for demo or real trading.
            username (str, optional): The username for the XTB API. Defaults to None.
            password (str, optional): The password for the XTB API. Defaults to None.
            path (str, optional): The path to the XTB API credentials file. Defaults to None.
            max_connections (int): Max allowed data and stream connections to server [-]. Default and upper limit is 50
            max_send_data (int): Max size of data sent to server at once [bytes]. Default and upper limit is 960
            max_received_data (int): Max size of data received from server at once [bytes]. Default is 4096
            max_retries (int): Max retries for request to server [-]. Default is 5         
            min_request_interval (float): Min allowed interval for server requests [s]. Default and lower limit is 0.205 
            socket_timeout (float): The timeout for blocking stream socket connection [s]. Default is 0.1
            max_queue_elements (int): The max number of elements in the stream queue [-]. Default is 1000
            dynamic_shifting (bool): Flag to allow dynamic shifting of streaming tasks. Default is True
            logger (logging.Logger, optional): The logger object to use for logging. Defaults to None.
        """

        # The status of the wrapper is initially inactive
        # because not jet ready for usage   
        self.__status = Status.INACTIVE

        # The lock for essential wrapper operations
        self.__lock = Lock()

        # Thread safety necessary
        # The initialization of the class has to be finished
        # before the class can be used
        with self.__lock:
            if logger:
                # Generates a child logger of the provided logger
                self._logger = logger.getChild('Wrp')
            else:
                # In case no logger is provided, generate a new one
                self._logger = generate_logger(name = 'Wrp', path = Path.cwd() / "logs")

            self._logger.debug("Initializing wrapper ...")

            # Check the input parameters
            if max_connections > MAX_CONNECTIONS:
                max_connections = MAX_CONNECTIONS
                self._logger.warning("Max connections must be less than " + str(MAX_CONNECTIONS) + ". Setting max connections to " + str(MAX_CONNECTIONS))

            if max_connections < 1:
                max_connections = 1
                self._logger.warning("Max connections must be at least 1. Setting max connections to 1")

            if max_send_data > MAX_SEND_DATA:
                max_send_data = MAX_SEND_DATA
                self._logger.warning("Max send data must be less than " + str(MAX_SEND_DATA) + ". Setting max send data to " + str(MAX_SEND_DATA))

            if max_send_data < 1:
                max_send_data = 1
                self._logger.warning("Max send data must be at least 1. Setting max send data to 1")

            if max_received_data < 1:
                max_received_data = 1
                self._logger.warning("Max received data must be at least 1. Setting max received data to 1")

            if max_retries < 0:
                max_retries = 0
                self._logger.warning("Max retries must be at least 0. Setting max retries to 0")

            if min_request_interval < MIN_REQUEST_INTERVAL:
                min_request_interval = MIN_REQUEST_INTERVAL
                self._logger.warning("Min request interval must be greater than " + str(MIN_REQUEST_INTERVAL) + ". Setting min request interval to " + str(MIN_REQUEST_INTERVAL))

            if socket_timeout < SOCKET_TIMEOUT:
                socket_timeout = SOCKET_TIMEOUT
                self._logger.warning("Socket timeout must be at least " + str(SOCKET_TIMEOUT) + ". Setting socket timeout to " + str(SOCKET_TIMEOUT))
            
            if max_queue_elements < 1:
                max_queue_elements = 1
                self._logger.warning("Max queue elements must be at least 1. Setting max queue elements to 1")

            # Initialize the HandlerManager
            super().__init__(
                max_connections = max_connections,
                max_send_data = max_send_data,
                max_received_data = max_received_data,
                max_retries = max_retries,
                min_request_interval = min_request_interval,
                socket_timeout = socket_timeout,
                max_queue_elements = max_queue_elements,
                dynamic_shifting = dynamic_shifting,

                demo = demo,
                
                username = username,
                password = password,
                path = path,

                logger = self._logger
            )

            # Set the status to active
            self.__status = Status.ACTIVE

            self._logger.debug("Wrapper initialized")

    def __del__(self) -> None:
        """
        Destructor method that is called when the Wrapper object is about to be destroyed.
        It ensures that any open connections are closed properly and any resources
        are released.

        Raises:
            None
        """

        try:
            self.delete()
        except Exception as e:
            # For graceful closing no raise of exception is not allowed
            pass

    def delete(self) -> None:
        """
        Deletes the Wrapper.

        Raises:
            None
        """

        # In case a other essential operation is in progress
        with self.__lock:
            # Check if the wrapper is already deleted
            if self.__status == Status.DELETED:
                self._logger.debug("Wrapper already deleted.")
                # For graceful deletion a raise of exception is not allowed
                return

            try:
                self._logger.info("Deleting wrapper ...")
                # Calling the delete method of the HandlerManager
                super()._delete()
                self._logger.info("Wrapper deleted.")
            except Exception as e:
                self._logger.error(f"Exception in delete: {e}")
            finally:
                # Set the status to deleted
                self.__status = Status.DELETED

    def _open_stream_channel(self, **kwargs) -> _StreamHandler.exchange:
        """
        Opens a channel for the strreaming of data.

        Args:
            **kwargs: Additional keyword arguments to be passed to the `streamData` method.

        Returns:
            StreamHandler.exchange: The exchange object for handling the stream.
        """
        
        # Call the streamData method of the HandlerManager
        # and store the returned dictionary in the exchange dictionary
        exchange = self._stream_data(**kwargs)

        # Return the exchange dictionary
        return exchange

    
    def streamBalance(self) -> _StreamHandler.exchange:
        """
        Allows to get actual account indicators values in real-time, as soon as they are available in the system.

        Returns:
            StreamHandler.exchange: The exchange object for handling the stream.
            - Use exchange.get() to get the latest stream data entry as a dictionary.
            - Use exchange.stop() to stop the stream.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                balance	            float	    balance in account currency
                credit	            float	    credit in account currency
                equity	            float	    sum of balance and all profits in account currency
                margin	            float	    margin requirements
                marginFree	        float	    free margin
                marginLevel	        float	    margin level percentage
        """

        return self._open_stream_channel(command = "getBalance")

    def streamCandles(self, symbol: str) -> _StreamHandler.exchange:
        """
        Subscribes for and unsubscribes from API chart candles. The interval of every candle is 1 minute.
        A new candle arrives every minute

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            symbol              string	    no          The symbol for which to retrieve the candle data.

        Returns:
            StreamHandler.exchange: The exchange object for handling the stream.
            - Use exchange.get() to get the latest stream data entry as a dictionary.
            - Use exchange.stop() to stop the stream.

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                close	            float	    Close price in base currency
                ctm	                timestamp	Candle  start time in CET time zone (Central European Time)
                ctmString	        string	    String representation of the ctm field
                high	            float	    Highest value in the given period in base currency
                low	                float	    Lowest  value in the given period in base currency
                open	            float	    Open price in base currency
                quoteId	            integer     Source of price
                symbol	            string	    Symbol
                vol	                float	    Volume in lots

            Possible values of "quoteId" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                fixed	            1	        fixed
                float	            2	        float
                depth	            3	        depth
                cross	            4	        cross
        """

        return self._open_stream_channel(command = "getCandles", symbol = symbol)
    
    def streamNews(self) -> _StreamHandler.exchange:
        """
        Subscribes for and unsubscribes from news.

        Returns:
            StreamHandler.exchange: The exchange object for handling the stream.
            - Use exchange.get() to get the latest stream data entry as a dictionary.
            - Use exchange.stop() to stop the stream.

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                body	            string	    Body
                key	                string	    News key
                time	            timestamp   Time
                title	            string	    News title
        """

        return self._open_stream_channel(command = "getNews")

    def streamProfits(self) -> _StreamHandler.exchange:
        """
        Subscribes for and unsubscribes from profits.

        Returns:
            StreamHandler.exchange: The exchange object for handling the stream.
            - Use exchange.get() to get the latest stream data entry as a dictionary.
            - Use exchange.stop() to stop the stream.

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                order	            integer 	Order number
                order2	            integer     Transaction ID
                position	        integer     Position number
                profit	            float	    Profit in account currency
        """

        return self._open_stream_channel(command = "getProfits")

    def streamTickPrices(
        self,
        symbol: str,
        min_arrival_time: Optional[int] = None,
        max_level: Optional[int] = None
        ) -> _StreamHandler.exchange:
        """
        Establishes subscription for quotations and allows to obtain the relevant information in real-time,
        as soon as it is available in the system.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            symbol              string	    no          The symbol for which to retrieve the tick prices.
            min_arrival_time    integer     yes         The minimal interval in milliseconds between any two consecutive updates  
            max_level           integer     yes         The maximum level of the tick prices

            min_arrival_time: If this field is not present, or it is set to 0 (zero), ticks - if available - are sent to the
                            client with interval equal to 200 milliseconds. In order to obtain ticks as frequently as
                            server allows you, set it to 1 (one).
            
            max_level: The maximum level of the tick prices. If this field is not specified, the subscription is active for all
                      levels that are managed in the system.

        Returns:
            StreamHandler.exchange: The exchange object for handling the stream.
            - Use exchange.get() to get the latest stream data entry as a dictionary.
            - Use exchange.stop() to stop the stream.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                ask	                float	    Ask price in base currency
                askVolume	        integer     Number of available lots to buy at given price or null if not applicable
                bid	                float	    Bid price in base currency
                bidVolume	        integer 	Number of available lots to buy at given price or null if not applicable
                high	            float	    The highest price of the day in base currency
                level	            integer 	Price level
                low	                float	    The lowest price of the day in base currency
                quoteId	            integer     Source of price, detailed description below
                spreadRaw	        float	    The difference between raw ask and bid prices
                spreadTable	        float	    Spread representation
                symbol	            string	    Symbol
                timestamp	        timestamp   Timestamp

            Possible values of "quoteId" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                fixed	            1	        fixed
                float	            2	        float
                depth	            3	        depth
                cross	            4	        cross
        """

        if min_arrival_time is not None and min_arrival_time < 0:
            min_arrival_time = 1
            self._logger.warning("minArrivalTime must greater than 0. Setting minArrivalTime to 1")
        
        if max_level is not None and max_level < 1:
            max_level = 1
            self._logger.warning("maxLevel must be at least 1. Setting maxLevel to 1")

        return self._open_stream_channel(command = "getTickPrices", symbol = symbol, minArrivalTime = min_arrival_time, maxLevel = max_level)

    def streamTrades(self) -> _StreamHandler.exchange:
        """
        Establishes subscription for user trade status data and allows to obtain the relevant information in real-time, as soon as
        it is available in the system.

        New data is sent by streaming socket only in several cases:
            - Opening the trade
            - Closing the trade
            - Modification of trade parameters
            - Explicit trade update done by server system to synchronize data.

        Returns:
            StreamHandler.exchange: The exchange object for handling the stream.
            - Use exchange.get() to get the latest stream data entry as a dictionary.
            - Use exchange.stop() to stop the stream.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                close_price	        float	    Close price in base currency
                close_time	        timestamp   Null if order is not closed
                closed	            boolean	    Closed
                cmd	                integer     Operation code
                comment	            string	    Comment
                commission	        float	    Commission in account currency, null if not applicable
                customComment	    string	    The value the customer may provide in order to retrieve it later.
                digits	            integer     Number of decimal places
                expiration	        timestamp	Null if order is not closed
                margin_rate	        float	    Margin rate
                offset	            integer     Trailing offset
                open_price	        float	    Open price in base currency
                open_time	        timestamp	Open time
                order	            integer 	Order number for opened transaction
                order2	            integer     Transaction id
                position	        integer     Position number (if type is 0 and 2) or transaction parameter (if type is 1)
                profit	            float	    null unless the trade is closed (type = 2) or opened (type = 0)
                sl	                float	    Zero if stop loss is not set (in base currency)
                state	            string	    Trade state, should be used for detecting pending order's cancellation
                storage	            float	    Storage
                symbol	            string	    Symbol
                tp	                float	    Zero if take profit is not set (in base currency)
                type	            integer     type
                volume	            float	    Volume in lots

            Possible values of "cmd" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                BUY	                0	        buy
                SELL	            1	        sell
                BUY_LIMIT	        2	        buy limit
                SELL_LIMIT	        3	        sell limit
                BUY_STOP	        4	        buy stop
                SELL_STOP	        5	        sell stop
                BALANCE	            6	        Read only
                CREDIT	            7	        Read only

            Possible values of "comment" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                STOP_LOSS	        [S/L]       the trade was closed by stop loss
                TAKE_PROFIT	        [T/P]       the trade was closed by take profit
                STOP_OUT	        [S/O margin level% equity / margin (currency)] the trade was closed because of Stop Out
                If the comment remained unchanged from that of opened order, then the order was closed by user

            Possible values of "state" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                MODIFIED	        "Modified"  modified
                DELETED	            "Deleted"   deleted

            Possible values of "type" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                OPEN	            0	        order open, used for opening orders
                PENDING	            1	        order pending, only used in the "streamTrades"  command
                CLOSE	            2	        order close
                MODIFY	            3	        order modify, only used in the "tradeTransaction"  command
                DELETE	            4	        order delete, only used in the "tradeTransaction"  command
        """

        return self._open_stream_channel(command = "getTrades")
    
    def streamTradeStatus(self) -> _StreamHandler.exchange:
        """
        Allows to get status for sent trade requests in real-time, as soon as it is available in the system.

        Returns:
            StreamHandler.exchange: The exchange object for handling the stream.
            - Use exchange.get() to get the latest stream data entry as a dictionary.
            - Use exchange.stop() to stop the stream.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                customComment	    string	    The value the customer may provide in order to retrieve it later.
                message	            string	    Can be null
                order	            integer     Unique order number
                price	            float	    Price in base currency
                requestStatus	    integer     Request status code, described below

            Possible values of "requestStatus" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                ERROR	            0	        error
                PENDING	            1	        pending
                ACCEPTED	        3	        The transaction has been executed successfully
                REJECTED	        4	        The transaction has been rejected
        """

        return self._open_stream_channel(command = "getTradeStatus")

    def _open_data_channel(self, **kwargs) -> Union[List[dict], dict]:
        """
        Opens a data channel and retrieves data.

        Args:
            **kwargs: Additional keyword arguments to be passed to the `getData` method.

        Returns:
            Union[List[dict], dict]: A list of dictionaries containing the data or a dictionary with the data.
            
        Raises:
            None
        """

        return self._get_data(**kwargs)
        
    def getAllSymbols(self) -> List[dict]:
        """
        Returns array of all symbols available for the user.

        Returns:
            A list of dictionaries containing the symbol data.

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                ask	                float	    Ask price in base currency
                bid	                float	    Bid price in base currency
                categoryName	    string	    Category name
                contractSize	    integer     Size of 1 lot
                currency	        string	    Currency
                currencyPair	    boolean	    Indicates whether the symbol represents a currency pair
                currencyProfit	    string	    The currency of calculated profit
                description	        string	    Description
                expiration	        timestamp   Null if not applicable
                groupName	        string	    Symbol group name
                high	            float	    The highest price of the day in base currency
                initialMargin	    integer    	Initial margin for 1 lot order, used for profit/margin calculation
                instantMaxVolume    integer	    Maximum instant volume multiplied by 100 (in lots)
                leverage	        float	    Symbol leverage
                longOnly	        boolean	    Long only
                lotMax	            float	    Maximum size of trade
                lotMin	            float	    Minimum size of trade
                lotStep	            float	    A value of minimum step by which the size of trade can be changed (within "lotMin" - "lotMax" range)
                low	                float	    The lowest price of the day in base currency
                marginHedged	    integer	    Used for profit calculation
                marginHedgedStrong  boolean	    For margin calculation
                marginMaintenance   integer	    For margin calculation, null if not applicable
                marginMode	        integer	    For margin calculation
                percentage	        float	    Percentage
                pipsPrecision	    integer	    Number of symbol's pip decimal places
                precision	        integer	    Number of symbol's price decimal places
                profitMode	        integer	    For profit calculation
                quoteId     	    integer	    Source of price
                shortSelling	    boolean	    Indicates whether short selling is allowed on the instrument
                spreadRaw	        float	    The difference between raw ask and bid prices
                spreadTable	        float	    Spread representation
                starting	        timestamp	Null if not applicable
                stepRuleId	        integer	    Appropriate step rule ID from "getStepRules" command response
                stopsLevel	        integer	    Minimal distance (in pips) from the current price where the stopLoss/takeProfit can be set
                swap_rollover3days  integer	    Time when additional swap is accounted for weekend
                swapEnable	        boolean	    Indicates whether swap value is added to position on end of day
                swapLong	        float	    Swap value for long positions in pips
                swapShort	        float	    Swap value for short positions in pips
                swapType	        integer	    Type of swap calculated
                symbol	            string	    Symbol name
                tickSize	        float	    Smallest possible price change, used for profit/margin calculation, null if not applicable
                tickValue	        float	    Value of smallest possible price change (in base currency), used for profit/margin calculation, null if not applicable
                time	            timestamp	Ask & bid tick time
                timeString	        string	    Time in String
                trailingEnabled	    boolean 	Indicates whether trailing stop (offset) is applicable to the instrument.
                type	            integer	    Instrument class number

            Possible values of "quoteId" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                fixed	            1	        fixed
                float	            2	        float
                depth	            3	        depth
                cross	            4	        cross

            Possible values of "marginMode" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                Forex	            101	        Forex
                CFD leveraged	    102	        CFD leveraged
                CFD	                103	        CFD

            Possible values of "profitMode" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                FOREX	            5	        FOREX
                CFD	                6	        CFD
        """

        return self._open_data_channel(command = "getAllSymbols")
    
    def getCalendar(self) -> List[dict]:
        """
        Returns calendar with market events.

        Returns:
            A list of dictionaries containing the calendar data.

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                country	            string	    Two letter country code
                current	            string	    Market value (current), empty before time of release of this value (time from "time" record)
                forecast	        string	    Forecasted value
                impact	            string	    Impact on market
                period	            string	    Information period
                previous	        string	    Value from previous information release
                time	            timestamp	Time, when the information will be released (in this time empty "current" value should be changed with exact released value)
                title           	String	    Name of the indicator for which values will be released

            Possible values of "impact" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                low	                1	        low
                medium	            2	        medium
                high	            3	        high
        """

        return self._open_data_channel(command = "getCalendar")
    
    def getChartLastRequest(self, symbol: str, period: str, start: Optional[datetime] = None) -> Dict[int, List[dict]]:
        """
        Returns chart info, from start date to the current time.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            symbol              string	    no          The symbol for which to retrieve the chart data.
            period              string	    no          Must be one of: "M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN1".
            start               datetime	yes         Start of chart block (rounded down to the nearest interval and excluding)
                                                        Default: 0001-01-01 00:00:00

            Limitations: there are limitations in charts data availability. Detailed ranges for charts data, what can be accessed
            with specific period, are as follows:

            PERIOD_M1 --- <0-1) month, i.e. one month time
            PERIOD_M30 --- <1-7) month, six months time
            PERIOD_H4 --- <7-13) month, six months time
            PERIOD_D1 --- 13 month, and earlier on
            
        Returns:
            Dictionary: A Dictionary with the chart data.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                digits	            integer	    Number of decimal places
                rateInfos	        list        List of dictionaries containing the candle data 

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                close	            float	    Value of close price (shift from open price)
                ctm	                timestamp	Candle start time in CET / CEST time zone (see Daylight Saving Time, DST)
                ctmString	        string	    String representation of the 'ctm' field
                high	            float   	Highest value in the given period (shift from open price)
                low	                float	    Lowest value in the given period (shift from open price)
                open            	float	    Open price (in base currency * 10 to the power of digits)
                vol	                float	    Volume in lots

                Price values must be divided by 10 to the power of digits in order to obtain exact prices.

                If the chosen period is greater than 1 minute, the last candle returned by the API can change until the end
                of the period. The candle is being automatically updated every minute.

        Raises:
            ValueError: If the period is invalid.
            ValueError: If the start time is greater than the current time.
        """

        # Dictionary for transforming periods to seconds
        periods = {'M1':1, 'M5':5, 'M15':15, 'M30':30, 'H1':60, 'H4':240, 'D1':1440, 'W1':10080, 'MN1':43200}    

        # Check if the period is valid
        if period not in periods:
            self._logger.error("Invalid period. Choose from: "+", ".join(periods.keys()))
            raise ValueError("Invalid period. Choose from: "+", ".join(periods.keys()))
        
        # Get the current time
        now = datetime.now()
        # Convert the current time to unix time
        now_ux = datetime_to_unixtime(now)

        # Set the limit time based on the period
        if periods[period] >= 1140:
            limit = datetime(1900, 1, 1)
        elif periods[period] >= 240:
            limit = now - relativedelta(years = 13)
        elif periods[period] >= 30:
            limit = now - relativedelta(months = 7)
        else:
            limit = now - relativedelta(months = 1)
        limit_ux = datetime_to_unixtime(limit)
        
        # Convert the start time to unix time
        if not start:
            # If no start time is given, set it to the minimum time 0001-01-01 00:00:00
            start_ux = datetime_to_unixtime(datetime.min)
        else:
            start_ux = datetime_to_unixtime(start)

        # Check if the start time is in the past
        if start_ux> now_ux:
            self._logger.error("Start time is greater than current time.")
            raise ValueError("Start time is greater than current time.")

        # Check if the start time is too far in the past
        if start_ux < limit_ux:
            start_ux = limit_ux
            self._logger.warning("Start time is too far in the past for selected period "+period+". Setting start time to "+str(limit))

        return self._open_data_channel(
            command = "getChartLastRequest",
            info = dict(
                period = periods[period],
                start = start_ux,
                symbol = symbol
            )
        )

    def getChartRangeRequest(self, symbol: str, period: str, start: Optional[datetime] = None, end: Optional[datetime] = None, ticks: int = 0) -> Dict[int, List[dict]]:
        """
        Returns chart info with data between given start and end dates.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            symbol              string	    no          The symbol for which to retrieve the chart data.
            period              string	    no          Must be one of: "M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN1".
            start               datetime	yes         Start of chart block (rounded down to the nearest interval and excluding)
                                                        Default: 0001-01-01 00:00:00
            end                 datetime	yes         End of chart block (rounded down to the nearest interval and excluding)
                                                        Default: current time
            ticks               integer     yes         The number of ticks to retrieve. If set to 0, the start and end times are used.
                                                        Default: 0

            If ticks >0 (e.g. N) then API returns N candles from time start.
            If ticks <0 then API returns N candles to time start.
            It is possible for API to return fewer chart candles than set in tick field.

            Limitations: there are limitations in charts data availability. Detailed ranges for charts data, what can be accessed
            with specific period, are as follows:

            PERIOD_M1 --- <0-1) month, i.e. one month time
            PERIOD_M30 --- <1-7) month, six months time
            PERIOD_H4 --- <7-13) month, six months time
            PERIOD_D1 --- 13 month, and earlier on

        Returns:
            Dictionary: A Dictionary with the chart data.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                digits	            integer	    Number of decimal places
                rateInfos	        list        List of dictionaries containing the candle data 

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                close	            float	    Value of close price (shift from open price)
                ctm	                timestamp	Candle start time in CET / CEST time zone (see Daylight Saving Time, DST)
                ctmString	        string	    String representation of the 'ctm' field
                high	            float   	Highest value in the given period (shift from open price)
                low	                float	    Lowest value in the given period (shift from open price)
                open            	float	    Open price (in base currency * 10 to the power of digits)
                vol	                float	    Volume in lots
            
                Price values must be divided by 10 to the power of digits in order to obtain exact prices.

        Raises:
            ValueError: If the period is invalid.
            ValueError: If the start time is greater than the current time.
            ValueError: If the end time is greater than the current time.
            ValueError: If the start time is greater or equal to the end time.
        """

        # Dictionary for transforming periods to seconds
        periods = {'M1':1, 'M5':5, 'M15':15, 'M30':30, 'H1':60, 'H4':240, 'D1':1440, 'W1':10080, 'MN1':43200}    

        if period not in periods:
            self._logger.error("Invalid period. Choose from: "+", ".join(periods.keys()))
            raise ValueError("Invalid period. Choose from: "+", ".join(periods.keys()))
        
        # Get the current time
        now = datetime.now()
        # Convert the current time to unix time
        now_ux = datetime_to_unixtime(now)

        # Set the limit time based on the period
        if periods[period] >= 1140:
            limit = datetime(1900, 1, 1)
        elif periods[period] >= 240:
            limit  =now - relativedelta(years = 13)
        elif periods[period] >= 30:
            limit = now - relativedelta(months = 7)
        else:
            limit = now - relativedelta(months = 1)
        limit_ux = datetime_to_unixtime(limit)

        # Convert the start time to unix time
        if not start:
            # If no start time is given, set it to the minimum time 0001-01-01 00:00:00
            start_ux = datetime_to_unixtime(datetime.min)
        else:
            start_ux = datetime_to_unixtime(start)

        # Check if the start time is in the past
        if start_ux> now_ux:
            self._logger.error("Start time is greater than current time.")
            raise ValueError("Start time is greater than current time.")

        # Check if the start time is too far in the past
        if start_ux < limit_ux:
            start_ux = limit_ux
            self._logger.warning("Start time is too far in the past for selected period "+period+". Setting start time to "+str(limit))

        if ticks == 0:
            # Convert the end time to unix time
            if not end:
                # If no end time is given, set it to the current time
                end_ux = now_ux
            else:
                end_ux = datetime_to_unixtime(end)
            
            # Check if the end time is in the future
            if end_ux > now_ux:
                self._logger.error("End time is greater than current time.")
                raise ValueError("End time is greater than current time.")

            # Check if the start time is greater or equal to the end time
            if start_ux >= end_ux:
                self._logger.error("Start time is greater or equal than end time.")
                raise ValueError("Start time is greater or equal than end time.")
        else:
            # In case ticks parameter is set, end time is ignored
            self._logger.info("Ticks parameter is set. Ignoring end time.")

            reference = start

            if ticks < 0:
                # If ticks is negative, the limit time lies in the past
                if period in ["M1", "M5", "M15", "M30"]:
                    delta = calculate_timesteps(limit,reference, period = 'minutes')
                elif period in ["H1", "H4"]:
                    delta = calculate_timesteps(limit,reference, period = 'hours')
                elif period == "D1":
                    delta = calculate_timesteps(limit,reference, period = 'days')
                elif period == "W1":
                    delta = calculate_timesteps(limit,reference, period = 'weeks')
                else:
                    delta = calculate_timesteps(limit,reference,period = 'months')

                # Check if the ticks reach too far in the past
                if delta < abs(ticks):
                    ticks = delta*(-1)
                    self._logger.warning("Ticks reach too far in the past for selected period "+period+". Setting tick to "+str(delta))
                    
            else:
                # If ticks is positive, the limit time lies in the future
                if period in ["M1", "M5", "M15", "M30"]:
                    delta = calculate_timesteps(reference, now, period = 'minutes')
                elif period in ["H1", "H4"]:
                    delta = calculate_timesteps(reference, now, period = 'hours')
                elif period == "D1":
                    delta = calculate_timesteps(reference, now, period = 'days')
                elif period == "W1":
                    delta = calculate_timesteps(reference, now, period = 'weeks')
                else:
                    delta = calculate_timesteps(reference, now, period = 'months')
                
                # Check if the ticks reach too far in the future
                if delta < ticks:
                    ticks = delta
                    self._logger.warning("Ticks reach too far in the future for selected period "+period+". Setting tick time to "+str(delta))

        return self._open_data_channel(
            command = "getChartRangeRequest",
            info = dict(
                end = end_ux,
                period = periods[period],
                start = start_ux,
                symbol = symbol,
                ticks = ticks
            )
        )

    def getCommissionDef(self, symbol: str, volume: float) -> dict:
        """
        Returns calculation of commission and rate of exchange. The value is calculated as expected value, and therefore might not be perfectly accurate.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            symbol              string	    no          The symbol for which to retrieve the commission definition.
            volume              float	    no          The volume for which to retrieve the commission definition.

        Returns:
            Dictionary: A Dictionary with the commission definition.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------    
                commission	        float	    calculated commission in account currency, could be null if not applicable
                rateOfExchange	    float	    rate of exchange between account currency and instrument base currency, could be null if not applicable
        
        Raises:
            ValueError: If the volume is less than or equal to 0.
        """

        # Check if the volume is less than or equal to 0
        if volume <= 0:
            self._logger.error("Volume must be greater than 0.")
            raise ValueError("Volume must be greater than 0.")

        return self._open_data_channel(command = "getCommissionDef", symbol = symbol, volume = volume)
    
    def getCurrentUserData(self) -> dict:
        """
        Returns information about account currency, and account leverage.

        Returns:
            Dictionary: A Dictionary containing the account information.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------   
                companyUnit	        integer	    Unit the account is assigned to.
                currency	        string	    account currency
                group	            string	    group
                ibAccount	        boolean	    Indicates whether this account is an IB account.
                leverage	        integer	    This field should not be used. It is inactive and its value is always 1.
                leverageMultiplier	float	    The factor used for margin calculations. The actual value of leverage can be calculated by dividing this value by 100.
                spreadType	        string	    spreadType, null if not applicable
                trailingStop	    boolean	    Indicates whether this account is enabled to use trailing stop   
        """

        return self._open_data_channel(command = "getCurrentUserData")
    
    def getIbsHistory(self, start: Optional[datetime] = None, end: Optional[datetime] = None) -> List[dict]:
        """
        Returns IBs data from the given time range.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            start               datetime	yes          Start of IBs history block. Default: 0001-01-01 00:00:00
            end                 datetime	yes          End of IBs history block. Default: current time

        Returns:
            A list of dictionaries containing the IBs data.

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                closePrice	        float	    IB close price or null if not allowed to view
                login	            string	    IB user login or null if not allowed to view
                nominal	            float	    IB nominal or null if not allowed to view
                openPrice	        float	    IB open price or null if not allowed to view
                side	            integer	    Operation code or null if not allowed to view
                surname	            string	    IB user surname or null if not allowed to view
                symbol	            string	    Symbol or null if not allowed to view
                timestamp	        timestamp	Time the record was created or null if not allowed to view
                volume	            float	    Volume in lots or null if not allowed to view

            Possible values of "side" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                BUY	                0	        buy
                SELL	            1	        sell
        
        Raises:
            ValueError: If the start time is greater than the end time.
            NotImplementedError: This method is deprecated and cannot be used.
        """
        
        # Convert the start time to unix time
        if not start:
            # If no start time is given, set it to the minimum time 0001-01-01 00:00:00
            start_ux = datetime_to_unixtime(datetime.min)
        else:
            start_ux = datetime_to_unixtime(start)

        # Convert the end time to unix time
        if not end:
            # If no end time is given, set it to the current time
            end_ux = datetime_to_unixtime(datetime.now())
        else:
            end_ux = datetime_to_unixtime(end) 

        # Check if the start time is greater than the end time
        if start_ux > end_ux:
            self._logger.error("Start time is greater than end time.")
            raise ValueError("Start time is greater than end time.")
        
        # Check if the end time is greater than the current time
        if end_ux > datetime_to_unixtime(datetime.now()):
            self._logger.error("End time is greater than current time.")
            raise ValueError("End time is greater than current time.")
        
        # This method is deprecated
        raise NotImplementedError("getIbsHistory is deprecated and cannot be used.")

        return self._open_data_channel(command = "getIbsHistory", end = end_ux, start = start_ux)
    
    def getMarginLevel(self) -> dict:
        """
        Returns various account indicators.

        Returns:
            Dictionary: A Dictionary with the account indicators.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------    
                balance	            float	    balance in account currency
                credit	            float	    credit
                currency	        string	    user currency
                equity	            float	    sum of balance and all profits in account currency
                margin	            float	    margin requirements in account currency
                margin_free	        float	    free margin in account currency
                margin_level	    float	    margin level percentage
        """

        return self._open_data_channel(command = "getMarginLevel")
    
    def getMarginTrade(self, symbol: str, volume: float) -> dict:
        """
        Returns expected margin for given instrument and volume. The value is calculated as expected margin value,
        and therefore might not be perfectly accurate.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            symbol              string	    no          The symbol for which to retrieve margin trade information.
            volume              float	    no          The volume of the trade.

        Returns:
            Dictionary: A Dictionary with the margin trade information.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------    
                margin	            float	    calculated margin in account currency

        Raises:
            ValueError: If the volume is less than or equal to 0.
        """

        # Check if the volume is less than or equal to 0
        if volume <= 0:
            self._logger.error("Volume must be greater than 0.")
            raise ValueError("Volume must be greater than 0.")

        return self._open_data_channel(command = "getMarginTrade", symbol = symbol, volume = volume)
    
    def getNews(self, start: Optional[datetime] = None, end: Optional[datetime] = None) -> List[dict]:
        """
        Returns news from trading server which were sent within specified period of time.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            start               datetime	yes          Start of news data range. Default: 0001-01-01 00:00:00
            end                 datetime	yes          End of news data range. Default: current time

        Returns:
            A list of dictionaries containing the news data.

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                body	            string      Body
                bodylen	            integer	    Body length
                key	                string      News key
                time	            timestamp   Time
                timeString	        string      Time string
                title	            string      News title

        Raises:
            ValueError: If the start time is greater than the end time.
            ValueError: If the end time is greater than the current time.
        """

        # Convert the start time to unix time
        if not start:
            # If no start time is given, set it to the minimum time 0001-01-01 00:00:00
            start_ux = datetime_to_unixtime(datetime.min)
        else:
            start_ux = datetime_to_unixtime(start)

        # Convert the end time to unix time
        if not end:
            # If no end time is given, set it to the current time
            end_ux = datetime_to_unixtime(datetime.now())
        else:
            end_ux = datetime_to_unixtime(end)


        # Check if the start time is greater than the end time
        if start_ux > end_ux:
            self._logger.error("Start time is greater than end time.")
            raise ValueError("Start time is greater than end time.")
        
        # Check if the end time is greater than the current time
        if end_ux > datetime_to_unixtime(datetime.now()):
            self._logger.error("End time is greater than current time.")
            raise ValueError("End time is greater than current time.")

        return self._open_data_channel(command = "getNews", end = end_ux, start = start_ux)
    
    def getProfitCalculation(self, symbol: str, volume: float, open_price: float, close_price: float, cmd: int) -> dict:
        """
        Calculates estimated profit for given deal data. Should be used for calculator-like apps only.
        Profit for opened transactions should be taken from server, due to higher precision of server calculation.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            symbol              string	    no          The symbol of the trade.
            volume              float	    no          The volume of the trade.
            open_price          float	    no          theoretical open price of order
            close_price         float	    no          theoretical close price of order
            cmd                 int	        no          Operation code

            Possible values of "cmd" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                BUY	                0	        buy
                SELL	            1	        sell
                BUY_LIMIT	        2	        buy limit
                SELL_LIMIT	        3	        sell limit
                BUY_STOP	        4	        buy stop
                SELL_STOP	        5	        sell stop
                BALANCE	            6	        Read only
                CREDIT	            7	        Read only

        Returns:
            Dictionary: A Dictionary with the profit calculation.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                profit	            float	    Profit in account currency
        
        Raises:
            ValueError: If the command is invalid.
            ValueError: If the volume is less than or equal to 0.
            ValueError: If the open price is less than or equal to 0.
            ValueError: If the close price is less than or equal to 0.
        """

        # List of valid commands
        cmds = [0, 1, 2, 3, 4, 5]

        # Check if the command is valid
        if cmd not in cmds:
            valid_cmds = ", ".join(map(str, cmds))
            self._logger.error(f"Invalid cmd. Choose from: {valid_cmds}")
            raise ValueError(f"Invalid cmd. Choose from: {valid_cmds}")
        
        # Check if the volume is less than or equal to 0
        if volume <= 0:
            self._logger.error("Volume must be greater than 0.")
            raise ValueError("Volume must be greater than 0.")
        
        # Check if the open price is less than or equal to 0
        if open_price <= 0:
            self._logger.error("Open price must be greater than 0.")
            raise ValueError("Open price must be greater than 0.")
        
        # Check if the close price is less than or equal to 0
        if close_price <= 0:
            self._logger.error("Close price must be greater than 0.")
            raise ValueError("Close price must be greater than 0.")

        return self._open_data_channel(
            command = "getProfitCalculation",
            closePrice = close_price,
            cmd = cmd,
            openPrice = open_price,
            symbol = symbol,
            volume = volume
        )
        
    def getServerTime(self) -> dict:
        """
        Returns current time on trading server.

        Returns:
            Dictionary: A Dictionary with the server time.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                time	            timestamp	Time
                timeString	        string      Time described in form set on server (local time of server)
        """

        return self._open_data_channel(command = "getServerTime")
    
    def getStepRules(self) -> List[Dict[str, Union[int, str, List[dict]]]]:
        """
        Returns a list of step rules for DMAs.

        Returns:
            A list of dictionaries containing the step rules.

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                id	                integer	    Step rule ID
                name	            string      Step rule name
                steps	            list	    List of dictionaries containing the step records

            Format of the "step record" dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                fromValue	        float	    Lower border of the volume range
                step	            float	    lotStep value in the given volume range
        """

        return self._open_data_channel(command = "getStepRules")

    def getSymbol(self, symbol: str) -> dict:
        """
        Returns information about symbol available for the user.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            symbol              string	    no          The symbol to retrieve information for.

        Returns:
            Dictionary: A Dictionary with the symbol information.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                ask	                float	    Ask price in base currency
                bid	                float	    Bid price in base currency
                categoryName	    string	    Category name
                contractSize	    integer     Size of 1 lot
                currency	        string	    Currency
                currencyPair	    boolean	    Indicates whether the symbol represents a currency pair
                currencyProfit	    string	    The currency of calculated profit
                description	        string	    Description
                expiration	        timestamp	Null if not applicable
                groupName	        string	    Symbol group name
                high	            float	    The highest price of the day in base currency
                initialMargin	    integer    	Initial margin for 1 lot order, used for profit/margin calculation
                instantMaxVolume    integer	    Maximum instant volume multiplied by 100 (in lots)
                leverage	        float	    Symbol leverage
                longOnly	        boolean	    Long only
                lotMax	            float	    Maximum size of trade
                lotMin	            float	    Minimum size of trade
                lotStep	            float	    A value of minimum step by which the size of trade can be changed (within "lotMin" - "lotMax" range)
                low	                float	    The lowest price of the day in base currency
                marginHedged	    integer	    Used for profit calculation
                marginHedgedStrong  boolean	    For margin calculation
                marginMaintenance   integer	    For margin calculation, null if not applicable
                marginMode	        integer	    For margin calculation
                percentage	        float	    Percentage
                pipsPrecision	    integer	    Number of symbol's pip decimal places
                precision	        integer	    Number of symbol's price decimal places
                profitMode	        integer	    For profit calculation
                quoteId     	    integer	    Source of price
                shortSelling	    boolean	    Indicates whether short selling is allowed on the instrument
                spreadRaw	        float	    The difference between raw ask and bid prices
                spreadTable	        float	    Spread representation
                starting	        timestamp	Null if not applicable
                stepRuleId	        integer	    Appropriate step rule ID from "getStepRules" command response
                stopsLevel	        integer	    Minimal distance (in pips) from the current price where the stopLoss/takeProfit can be set
                swap_rollover3days	integer	    timestamp when additional swap is accounted for weekend
                swapEnable	        boolean	    Indicates whether swap value is added to position on end of day
                swapLong	        float	    Swap value for long positions in pips
                swapShort	        float	    Swap value for short positions in pips
                swapType	        integer	    Type of swap calculated
                symbol	            string	    Symbol name
                tickSize	        float	    Smallest possible price change, used for profit/margin calculation, null if not applicable
                tickValue	        float	    Value of smallest possible price change (in base currency), used for profit/margin calculation, null if not applicable
                time	            timestamp	Ask & bid tick time
                timeString	        string	    Time in String
                trailingEnabled	    boolean 	Indicates whether trailing stop (offset) is applicable to the instrument.
                type	            integer	    Instrument class number

            Possible values of "quoteId" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                fixed	            1	        fixed
                float	            2	        float
                depth	            3	        depth
                cross	            4	        cross

            Possible values of "marginMode" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                Forex	            101	        Forex
                CFD leveraged	    102	        CFD leveraged
                CFD	                103	        CFD

            Possible values of "profitMode" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                FOREX	            5	        FOREX
                CFD	                6	        CFD
        """

        return self._open_data_channel(command = "getSymbol", symbol = symbol)
    
    def getTickPrices(self, symbols: List[str], time: datetime, level: int = -1) -> Dict[str, List[dict]]:
        """
        Returns array of current quotations for given symbols, only quotations that changed from given timestamp are returned.
        New timestamp obtained from output will be used as an argument of the next call of this command.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            symbols             list	    no          A list of symbols for which tick prices are to be retrieved.
            time                datetime	no          The time from which the most recent tick should be looked for. 
            level               int	        yes         The level of tick prices to retrieve. Defaults to -1.

            Possible values of "level" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                                    -1	        all available levels
                                     0	        base level bid and ask price for instrument
                                    >0	        specified level      

        Returns:
            Dictionary: A Dictionary with the tick prices.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                quotations  	    list        List of dictionaries containing the tick prices

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                ask	                float	    Ask price in base currency
                askVolume	        int	        Number of available lots to buy at given price or null if not applicable
                bid	                float	    Bid price in base currency
                bidVolume	        int	        Number of available lots to buy at given price or null if not applicable
                high	            float	    The highest price of the day in base currency
                level	            int	        Price level
                low	                float	    The lowest price of the day in base currency
                spreadRaw	        float	    The difference between raw ask and bid prices
                spreadTable	        float	    Spread representation
                symbol	            string	    Symbol
                timestamp	        timestamp	Timestamp

                Possible values of "level" field correspond to the level field in the input arguments.

        Raises:
            ValueError: If the level is invalid.
            ValueError: If the time lies in the future.
        """

        # Check if the level is valid
        levels = [-1, 0]
        if level not in levels and level <= 0:
            self._logger.error("Invalid level. Must be -1, 0, or greater than 0.")
            raise ValueError("Invalid level. Must be -1, 0, or greater than 0.")
        
        # Convert the time to unix time
        timestamp = datetime_to_unixtime(time)

        # Check if time lies in the future
        if timestamp < datetime_to_unixtime(datetime.now()):
            self._logger.error("Time must lie in the future.")
            raise ValueError("Time must lie in the future.")

        return self._open_data_channel(command = "getTickPrices", level = level, symbols = symbols, timestamp = timestamp)
    
    def getTradeRecords(self, orders: List[int]) -> List[dict]:
        """
        Returns array of trades listed in orders argument.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            orders              list	    no          A list of order IDs.

        Returns:
            A list of dictionaries containing the trade records.

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                close_price	        float       Close price in base currency
                close_time	        timestamp	Null if order is not closed
                close_timeString	string      Null if order is not closed
                closed	            boolean	    Closed
                cmd	                integer	    Operation code
                comment	            string      Comment
                commission	        float       Commission in account currency, null if not applicable
                customComment	    string      The value the customer may provide in order to retrieve it later.
                digits	            integer	    Number of decimal places
                expiration	        timestamp	Null if order is not closed
                expirationString	string      Null if order is not closed
                margin_rate     	float       Margin rate
                offset	            integer	    Trailing offset
                open_price	        float       Open price in base currency
                open_time	        timestamp	Open time
                open_timeString	    string      Open time string
                order	            integer	    Order number for opened transaction
                order2	            integer	    Order number for closed transaction
                position	        integer	    Order number common both for opened and closed transaction
                profit	            float       Profit in account currency
                sl	                float       Zero if stop loss is not set (in base currency)
                storage	            float       Order swaps in account currency
                symbol	            string      Symbol name or null for deposit/withdrawal operations
                timestamp	        timestamp	Timestamp
                tp	                float       Zero if take profit is not set (in base currency)
                volume	            float       Volume in lots

            Possible values of "cmd" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                BUY	                0	        buy
                SELL	            1	        sell
                BUY_LIMIT	        2	        buy limit
                SELL_LIMIT	        3	        sell limit
                BUY_STOP	        4	        buy stop
                SELL_STOP	        5	        sell stop
                BALANCE	            6	        Read only
                CREDIT	            7	        Read only
        """

        return self._open_data_channel(command = "getTradeRecords", orders = orders)
    
    def getTrades(self, opened_only: bool) -> List[dict]:
        """
        Returns array of user's trades.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            opened_only         bool	    no          If True, only retrieves opened trades. If False, retrieves all trades.

        Returns:
            A list of dictionaries containing the trades.

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                close_price	        float       Close price in base currency
                close_time	        timestamp	Null if order is not closed
                close_timeString	string      Null if order is not closed
                closed	            boolean	    Closed
                cmd	                integer	    Operation code
                comment	            string      Comment
                commission	        float       Commission in account currency, null if not applicable
                customComment	    string      The value the customer may provide in order to retrieve it later.
                digits	            integer	    Number of decimal places
                expiration	        timestamp	Null if order is not closed
                expirationString	string      Null if order is not closed
                margin_rate     	float       Margin rate
                offset	            integer	    Trailing offset
                open_price	        float       Open price in base currency
                open_time	        timestamp	Open time
                open_timeString	    string      Open time string
                order	            integer	    Order number for opened transaction
                order2	            integer	    Order number for closed transaction
                position	        integer	    Order number common both for opened and closed transaction
                profit	            float       Profit in account currency
                sl	                float       Zero if stop loss is not set (in base currency)
                storage	            float       Order swaps in account currency
                symbol	            string      Symbol name or null for deposit/withdrawal operations
                timestamp	        timestamp	Timestamp
                tp	                float       Zero if take profit is not set (in base currency)
                volume	            float       Volume in lots

            Possible values of "cmd" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                BUY	                0	        buy
                SELL	            1	        sell
                BUY_LIMIT	        2	        buy limit
                SELL_LIMIT	        3	        sell limit
                BUY_STOP	        4	        buy stop
                SELL_STOP	        5	        sell stop
                BALANCE	            6	        Read only
                CREDIT	            7	        Read only

        """
        
        return self._open_data_channel(command = "getTrades", openedOnly = opened_only)
    
    def getTradesHistory(self, start: Optional[datetime] = None, end: Optional[datetime] = None) -> List[dict]:
        """
        Returns array of user's trades which were closed within specified period of time.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            start               datetime	yes          Start of trade history block. Default: 0001-01-01 00:00:00
            end                 datetime	yes          End of trade history block. Default: current time

        Returns:
            A list of dictionaries containing the trade history.

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                close_price	        float       Close price in base currency
                close_time	        timestamp	Null if order is not closed
                close_timeString	string      Null if order is not closed
                closed	            boolean	    Closed
                cmd	                integer	    Operation code
                comment	            string      Comment
                commission	        float       Commission in account currency, null if not applicable
                customComment	    string      The value the customer may provide in order to retrieve it later.
                digits	            integer	    Number of decimal places
                expiration	        timestamp	Null if order is not closed
                expirationString	string      Null if order is not closed
                margin_rate     	float       Margin rate
                offset	            integer	    Trailing offset
                open_price	        float       Open price in base currency
                open_time	        timestamp	Open time
                open_timeString	    string      Open time string
                order	            integer	    Order number for opened transaction
                order2	            integer	    Order number for closed transaction
                position	        integer	    Order number common both for opened and closed transaction
                profit	            float       Profit in account currency
                sl	                float       Zero if stop loss is not set (in base currency)
                storage	            float       Order swaps in account currency
                symbol	            string      Symbol name or null for deposit/withdrawal operations
                timestamp	        timestamp	Timestamp
                tp	                float       Zero if take profit is not set (in base currency)
                volume	            float       Volume in lots

            Possible values of "cmd" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                BUY	                0	        buy
                SELL	            1	        sell
                BUY_LIMIT	        2	        buy limit
                SELL_LIMIT	        3	        sell limit
                BUY_STOP	        4	        buy stop
                SELL_STOP	        5	        sell stop
                BALANCE	            6	        Read only
                CREDIT	            7	        Read only

        Raises:
            ValueError: If the start time is greater than the end time.
            ValueError: If the end time is greater than the current time.
        """

        # Convert the start time to unix time
        if not start:
            # If no start time is given, set it to the minimum time 0001-01-01 00:00:00
            start_ux = datetime_to_unixtime(datetime.min)
        else:
            start_ux = datetime_to_unixtime(start)

        # Convert the end time to unix time
        if not end:
            # If no end time is given, set it to the current time
            end_ux = datetime_to_unixtime(datetime.now())
        else:
            end_ux = datetime_to_unixtime(end)

        # Check if the start time is greater than the end time
        if end_ux > datetime_to_unixtime(datetime.now()):
            self._logger.error("End time is greater than current time.")
            raise ValueError("End time is greater than current time.")

        # Check if the start time is greater than the end time
        if start_ux > end_ux:
            self._logger.error("Start time is greater than end time.")
            raise ValueError("Start time is greater than end time.")

        return self._open_data_channel(command = "getTradesHistory", end = end_ux, start = start_ux)

    def getTradingHours(self, symbols: List[str]) -> List[Dict[str, Union[List[dict], str]]]:
        """
        Returns quotes and trading times.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            symbols             list	    no          A list of symbols for which to retrieve trading hours.

        Returns:
            A list of dictionaries containing the trading hours.

            Format of the dictionary: 
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                quotes	            list        List of dictionaries containing the quotes records
                symbol	            string      Symbol
                trading	            list        List of dictionaries containing the trading records

            Format of the "quote record" dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                day	                integer	    Day of week
                fromT	            timestamp	Start time in ms from 00:00 CET / CEST time zone (see Daylight Saving Time, DST)
                toT	                timestamp	End time in ms from 00:00 CET / CEST time zone (see Daylight Saving Time, DST)

            Format of the "trading record" dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                day	                integer	    Day of week
                fromT	            timestamp	Start time in ms from 00:00 CET / CEST time zone (see Daylight Saving Time, DST)
                toT             	timestamp	End time in ms from 00:00 CET / CEST time zone (see Daylight Saving Time, DST)

            Possible values of "day" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                                    1	        Monday
                                    2	        Tuesday
                                    3	        Wednesday
                                    4	        Thursday
                                    5	        Friday
                                    6	        Saturday
                                    7	        Sunday
        """

        return self._open_data_channel(command = "getTradingHours", symbols = symbols)

    def getVersion(self) -> dict:
        """
        Returns the current API version.

        Returns:
            Dictionary: A Dictionary with the API version.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                version	            string	    current API version      
        """

        return self._open_data_channel(command = "getVersion")
    
    def tradeTransaction(self,
        type: int,
        order: Optional[int] = None,
        cmd: Optional[int] = None,
        symbol: str = '',
        volume: float = 0.0,
        price: float = 0.0,
        expiration: Optional[datetime] = None,
        sl: float = 0.0,
        tp: float = 0.0,
        offset: int = 0,
        custom_comment: str = '',               
        ) -> dict:
        """
       Starts trade transaction. tradeTransaction sends main transaction information to the server.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            type                int	        no          Trade transaction type
            order               int	        *           0 or position number for closing/modifications
            cmd                 int	        *           Operation code
            symbol              string	    *           Trade symbol
            volume              float	    *           Trade volume
            price               float	    *           Trade price
            expiration          datetime	*           Pending order expiration time
            sl                  float	    *           Stop loss
            tp                  float	    *           Take profit
            offset              int	        *           Trailing offset
            custom_comment      string	    yes         The value the customer may provide in order to retrieve it later.

            * If an argument is optional or not, depends on the "type" and "cmd" field.

            Possible values of "cmd" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                BUY	                0	        buy
                SELL	            1	        sell
                BUY_LIMIT	        2	        buy limit
                SELL_LIMIT	        3	        sell limit
                BUY_STOP	        4	        buy stop
                SELL_STOP	        5	        sell stop
                BALANCE	            6	        Read only
                CREDIT	            7	        Read only

            Possible values of "type" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                OPEN	            0	        order open, used for opening orders
                PENDING	            1	        order pending, only used in the "streamTrades" command
                CLOSE	            2	        order close
                MODIFY	            3	        order modify, only used in the "tradeTransaction" command
                DELETE	            4	        order delete, only used in the "tradeTransaction" command

        Returns:
            Dictionary: A Dictionary with the symbol information.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                order	            integer	    order

                To analyse the status of the transaction (for example to verify if it was accepted or rejected) use the 
                tradeTransactionStatus  command with the order number, that came back with the response 

        Raises:
            ValueError: If the type is invalid.
            ValueError: If the position number is not given to close, modify or delete orders.
            ValueError: If the command is invalid.
            ValueError: If the expiration time is in the past
        """

        # List of valid commands and types
        cmds = [0, 1, 2, 3, 4, 5]
        types = [0, 2, 3, 4]

        # Check if the type is valid
        if type not in types:
            self._logger.error("Invalid type. Choose from: "+", ".join(map(str, types)))
            raise ValueError("Invalid type. Choose from: "+", ".join(map(str, types)))
        
        # Check if the position number is given to close, modify or delete orders
        if type in [2, 3, 4] and (order is None or order <= 0):
            self._logger.error("Position number must be given to close, modify or delete orders.")
            raise ValueError("Position number must be given to close, modify or delete orders.")
        
        # Check if the command is valid
        if cmd and cmd not in cmds:
            self._logger.error("Invalid cmd for opening order. Choose from: "+", ".join(map(str, cmds)))
            raise ValueError("Invalid cmd for opening order. Choose from: "+", ".join(map(str, cmds)))
         
        # Check if the expiration time is in the future
        if expiration is not None and expiration <= datetime.now():
            self._logger.error("Expiration time must be in the future.")
            raise ValueError("Expiration time must be in the future.")
            
        # Convert order to integer
        if order is None:
            order = 0

        # Convert the expiration time to unix time
        if expiration:
            expiration_ux = datetime_to_unixtime(expiration)
        else:
            expiration_ux = 0

        return self._open_data_channel(
            command = "tradeTransaction",
            tradeTransInfo = dict(
                cmd = cmd,
                customComment = custom_comment,
                expiration = expiration_ux,
                offset = offset,
                order = order,
                price = price,
                sl = sl,
                symbol = symbol,
                tp = tp,
                type = type,
                volume = volume
            )
        )
    
    def tradeTransactionStatus(self, order: int) -> dict:
        """
        Returns current transaction status.

        Args:
            name                type        optional    description
            -----------------------------------------------------------------------------------------------
            order               int	        no          The order ID for which to retrieve the transaction status.

        Returns:
            Dictionary: A Dictionary with the transaction status.

            Format of the dictionary:
                name	            type	    description
                -----------------------------------------------------------------------------------------------
                ask	                float	    Price in base currency
                bid	                float	    Price in base currency
                customComment	    string	    The value the customer may provide in order to retrieve it later.
                message	            string	    Can be null
                order	            integer	    Unique order number
                requestStatus	    integer	    Request status code, described below

            Possible values of "requestStatus" field:
                name	            value	    description
                -----------------------------------------------------------------------------------------------
                ERROR	            0	        error
                PENDING	            1	        pending
                ACCEPTED	        3	        The transaction has been executed successfully
                REJECTED	        4       	The transaction has been rejected
        """

        return self._open_data_channel(command = "tradeTransactionStatus", order = order)
