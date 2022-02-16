""" Helper functions."""
import logging


def str_to_int(value: str) -> int:
    """
    Return int from string or raise/log error.
    :param value: The string value.
    :return: The int value.
    """
    try:
        int_val = int(value)
        return int_val

    except ValueError as e:
        logging.error(f"Cannot convert string value to integer: {value=}")
        raise e


def str_to_float(value: str) -> float:
    """
    Return float from string or raise/log error.
    :param value: The string value.
    :return: The float value.
    """
    try:
        int_val = float(value)
        return int_val

    except ValueError as e:
        logging.error(f"Cannot convert string value to float: {value=}")
        raise e
