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

import pytest
from tests.helper import generate_logger, write_logs, GREEN, RESET
import xwrpr
from xwrpr.handler import _StreamHandler
from datetime import datetime, timedelta


def test_31_stream_trade_status(
    demo_flag: bool,
    log_level: int,
    caplog: pytest.LogCaptureFixture,
    capsys: pytest.CaptureFixture
) -> None:
    # Create a logger with the specified name
    logger = generate_logger(log_level)

    # Capture the logs
    with caplog.at_level(log_level):
        try:
            # Creating Wrapper
            logger.debug("Creating Wrapper")
            xtb = xwrpr.Wrapper(demo = demo_flag, logger = logger)
        except Exception as e:
            logger.error("Error creating Wrapper: %s. Did you forget to enter your credentials?", e)
            pytest.fail(f"Failed to create Wrapper: {e}")

        try:
            # Start streaming trade status
            logger.debug("Starting streaming trade status")
            exchange = xtb.streamTrades()
            
            # Check if the return value is a exchange object
            logger.debug("Checking if the return value is a exchange object")
            assert isinstance(exchange, _StreamHandler.exchange), "Expected a exchange object"

            # Log balance
            logger.info("Trade Status")
            stop_time = datetime.now() + timedelta(seconds=5)
            while datetime.now() < stop_time:
                # Get the data
                data = exchange.get(timeout = 1)
                
                if data:
                    # Check if the return value is a dict
                    logger.debug("Checking if the return value is a dict")
                    assert isinstance(data, dict), "Expected a dict"
                    
                    # Log the data
                    details = ', '.join([f"{key}: {value}" for key, value in data.items()])
                    logger.info(details)
            # Stop the stream
            logger.debug("Stopping the stream")
            exchange.stop()
        finally:
            # Close Wrapper
            logger.debug("Closing Wrapper")
            xtb.delete()

    # Write records to log file
    with capsys.disabled():
        log_file_path = write_logs(caplog, __file__)
        print(f"\nLog files written to: {GREEN}{log_file_path}{RESET}\n")
                
    # Clear the captured logs
    caplog.clear()