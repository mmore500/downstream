import logging
from unittest.mock import Mock

import pylib


def test_log_args_and_result() -> None:

    # Mocking logger and log_level
    mock_logger = Mock(spec=logging.Logger)
    log_level = logging.INFO

    # Decorate a simple test function
    @pylib.log_args_and_result(mock_logger, log_level)
    def test_function(a, b, c=None):
        return a + b + (c if c else 0)

    # Call the decorated function
    result = test_function(2, 3, c=4)

    # Check if the function result is correct
    assert result == 9

    # Check if the logger.log was called correctly
    assert mock_logger.log.call_count == 2

    # Checking the first log call
    assert mock_logger.log.call_args_list == [
        (
            {
                "level": log_level,
                "msg": ">>> calling test_function(2, 3, c=4)",
            },
        ),
        (
            {
                "level": log_level,
                "msg": ">> 'test_function' returned 9",
            },
        ),
    ]
