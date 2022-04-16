from datetime import datetime
import os


def current_time_as_str():
    """
    read current time and process it to string to be used in a file name.
    :return: str, current time value
    """
    return str(datetime.now()).replace(" ", '-').replace(":", '-')[:-7]
