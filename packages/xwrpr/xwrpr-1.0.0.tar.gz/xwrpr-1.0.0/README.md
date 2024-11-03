xwrpr - A wrapper for the xAPI of XTB
=================

xwrpr is a Python library that provides a high-level wrapper around the xAPI for XTB, offering convenient functions for managing both data and streaming commands. Designed to make interaction with XTB’s trading API simple and effective, it provides comprehensive support for data retrieval, account management, and trading operations.

<br/>

# **Table of contents**

<!--ts-->
* [Features](#features)
* [API-Version](#api-version)
* [Installation](#installation)
* [Initialization](#initialization)
    * [List of Arguments](#list-of-arguments)
    * [Example](#example-wrapper)
* [Data commands](#data-commands)
    * [List of Commands](#list-of-commands-data)
    * [Example](#example-data)
* [Streaming commands](#streaming-commands)
     * [List of Commands](#list-of-commands-stream)
     * [Example](#example-stream)
* [Contribution](#contribution)
* [Caution](#caution)
* [License](#license)
* [Sources](#sources)
<!--te-->

<br/>

# **Features**

* **User friendly installation**: Easy installation via ```pip```.
* **Comprehensive support**: Supports all data and streaming commands of the xAPI.
* **High level interface**: Manages connection and background tasks automatically.
* **Examples**: Sample code provided for both data and streaming commands.
* **Documentation**: Complete documentation for each command available in docstrings.


<br/>

# **API-Version**
xwrpr relies on the xAPI Version 2.5.0

* [XTB](https://www.xtb.com/)
* [xAPI Protocol Documentation](http://developers.xstore.pro/documentation/)
* [xAPIConnector](http://developers.xstore.pro/public/files/xAPI25-XTB-python.zip)

<br/>

# **Installation**

You can install xwrpr via pip:
```bash
pip install xwrpr
```

<br/>

# **Initialization**

* After installation a file ```.xwrpr/user.ini``` is created in your home directory.
* To get accesd to your XTB account via xwrpr, you must enter your XTB credentials in ```user.ini```.
* **Important!**: Make sure this file is secured from unauthorized access
* To change the default location of ```user.ini```, use the ```path``` argument for this.
* Additionally you can enter your XTB credentials directly in the wrapper

## **List of Argumentss** <a name="list-of-arguments"></a>

* All available arguments for the wrapper are listed below:

   * ```demo (bool)```: A boolean indicating whether the handler is for demo or real trading.
   * ```username (str, optional)```: The username for the XTB API. Defaults to None.
   * ```password (str, optional)```: The password for the XTB API. Defaults to None.
   * ```path (str, optional)```: The path to the XTB API credentials file. Defaults to None.
   * ```max_connections (int)```: Max allowed data and stream connections to server [-]. Default and upper limit is 50
   * ```max_send_data (int)```: Max size of data sent to server at once [bytes]. Default and upper limit is 960
   * ```max_received_data (int)```: Max size of data received from server at once [bytes]. Default is 4096
   * ```max_retries (int)```: Max retries for request to server [-]. Default is 5
   * ```min_request_interval (float)```: Min allowed interval for server requests [s]. Default and lower limit is 0.205
   * ```socket_timeout (float)```: The timeout for blocking stream socket connection [s]. Default is 0.1
   * ```max_queue_elements (int)```: The max number of elements in the stream queue [-]. Default is 1000
   * ```dynamic_shifting (bool)```: Flag to allow dynamic shifting of streaming tasks. Default is True
   * ```logger (logging.Logger, (optional)```: The logger object to use for logging. Defaults to None.
 
* Setting ```dynamic_shifting (bool)``` to True, enables xwrpr to dynamically shift stream tasks between streaming connections reducing the risk of queue overflow. For more Information see [List of commands](#list-of-commands-stream)

## **Example** <a name="example-wrapper"></a>

The following example will show how to initialize the xwrpr.
You will find a example like this also in ```tests``` directory.

```python
import xwrpr

# Creating Wrapper
xtb=xwrpr.Wrapper()
```

<br/>

# **Data commands**

xwrpr includes all Data commands of the xAPI exept:
   * ```ping```
</n>
This command is automatically executed in the background.

## **List of Commands** <a name="list-of-commands-data"></a>

* All available data commands are listed below:

   * ```getAllSymbols```: Returns array of all symbols available for the user.
   * ```getCalendar```: Returns calendar with market events.
   * ```getChartLastRequest```: Returns chart info, from start date to the current time.
   * ```getChartRangeRequest```: Returns chart info with data between given start and end dates.
   * ```getCommissionDef```: Returns calculation of commission and rate of exchange for a given symbol and volume.
   * ```getCurrentUserData```: Returns information about account currency, and account leverage.
   * ```getIbsHistory```: Returns IBs data from the given time range. (deprecated)
   * ```getMarginLevel```: Returns various account indicators.
   * ```getMarginTrade```: Returns expected margin for given instrument and volume.
   * ```getNews```: Returns news from trading server which were sent within specified period of time.
   * ```getProfitCalculation```: Calculates estimated profit for given deal data.
   * ```getServerTime```: Returns current time on trading server.
   * ```getStepRules```: Returns a list of step rules for DMAs.
   * ```getSymbol```: Returns information about symbol available for the user.
   * ```getTickPrices```: Returns array of current quotations for given symbols.
   * ```getTradeRecords```: Returns array of trades listed in orders argument.
   * ```getTrades```: Returns array of trades for the user.
   * ```getTradesHistory```: Returns array of trades history for the user.
   * ```getTradingHours```: Returns quotes and trading times.
   * ```getVersion```: Returns the current API version.
   * ```tradeTransaction```: Starts trade transaction.
   * ```tradeTransactionStatus```: Returns current transaction status.

* The return value debends on the command. Please see the docstrings of the commands for further information.
* You will find a full documentation of all xAPI data commands here: [xAPI Protocol Documentation](http://developers.xstore.pro/documentation/)

## **Example** <a name="example-data"></a>

The following example will show how to retrieve data with xwrpr.
You will find a example like this also in ```tests/test_18_get_symbol.py```.

```python
import xwrpr

# Creating Wrapper
xtb = xwrpr.Wrapper()

# Getting data for the symbol
symbol = xtb.getSymbol(symbol="BITCOIN")

# Printing the data
details = ', '.join([f"{key}: {value}" for key, value in symbol.items()])
print(details)
```

<br/>

# **Streaming commands**

xwrpr includes all Streaming commands of the xAPI exept:
   * ```ping```
   * ```streamKeepAlive```
</n>
This two commands are automatically executed in the background.

## **List of Commands** <a name="list-of-commands-stream"></a>

Unlike the official API, where streaming commands are named get *Command* , the xwrpr library
uses the stream *Command* naming convention. This change was necessary to avoid conflicts
caused by the official API's duplicate command names.

* All available streaming commands are listed below with their Input arguments and format.

   * ```streamBalance```: Allows to get actual account indicators values in real-time.
   * ```streamCandles```: Subscribes for and unsubscribes from API chart candles.
   * ```streamNews```: Subscribes for and unsubscribes from news.
   * ```streamProfits```: Subscribes for and unsubscribes from profits.
   * ```streamTickPrices```: Establishes subscription for quotations.
   * ```streamTrades```: Establishes subscription for user trade status data.
   * ```streamTradeStatus```: Allows to get status for sent trade requests in real-time.

* The return value will be an object of the exchange class. Please see the docstrings of the commands for further information.
* To retrieve the stream data use ```exchange.get()``` for stopping the stream use ```exchange.stop()```
* If the stream data is not continuosly retirieved, a queue overflow could happen.
* You will find a full documentation of all xAPI data commands here: [xAPI Protocol Documentation](http://developers.xstore.pro/documentation/)

## **Example** <a name="example-stream"></a>

The following example will show how to stream data with xwrpr.
You will find a example like this also in ```tests/test_29_stream_tick_prices.py```.

```python
import xwrpr
from datetime import datetime, timedelta

# Creating Wrapper
xtb=xwrpr.Wrapper()

# Starting the stream of the tick prices
exchange = xtb.streamTickPrices(symbol="BITCOIN")

# Streaming the tick prices
stop_time = datetime.now() + timedelta(seconds=10)
while datetime.now() < stop_time:
    # Get the data
    data = exchange.get(timeout = 1)
    
    if data:
         # Printing the data
        details = ', '.join([f"{key}: {value}" for key, value in data.items()])
        print(details)

# Stop the stream
exchange.stop()

# Close Wrapper
xtb.delete()
```

<br/>

# **Contribution**

Improvements to the xwrpr project are welcome, whether it's a request, a suggestion, or a bug report. Just reach out!
Visit also the GiutHub repository of xwrpr: [xwrpr on GitHub](https://github.com/AustrianTradingMachine/xwrpr)

<br/>

# **Caution**

Please consider that xwrpr is still in beta stage and needs more development to run stable and reliant.

<br/>

# **License**

This project is licensed under the GNU General Public License v3.0.
You should have received a copy of the GNU General Public License
along with this program.  If not, see [GNU GPL 3](https://www.gnu.org/licenses/)

<br/>

# **Sources**

* [XTB](https://www.xtb.com/)
* [xAPI Protocol Documentation](http://developers.xstore.pro/documentation/)
* [xAPIConnector](http://developers.xstore.pro/public/files/xAPI25-XTB-python.zip)
* [xwrpr on GitHub](https://github.com/AustrianTradingMachine/xwrpr)
* [GNU GPL 3](https://www.gnu.org/licenses/)

<br/>
