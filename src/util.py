from datetime import datetime


def current_time_as_str():
    """
    read current time and process it to string to be used in a file name.
    :return: str, current time value
    """
    return str(datetime.now()).replace(" ", '-').replace(":", '-')[:-7]

def flatten_list(txts):
    """
    flatten list of texts by concatenating
    :param txts: str, list of texts
    :return: str, flattened text as string
    """
    flatten = str()
    for txt in txts:
        flatten = flatten + txt
    return flatten
