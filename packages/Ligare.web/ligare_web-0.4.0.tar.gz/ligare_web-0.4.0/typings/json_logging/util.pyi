"""
This type stub file was generated by pyright.
"""

import sys

def is_env_var_toggle(var_name): # -> bool:
    ...

def get_library_logger(logger_name): # -> Logger:
    """

    :param logger_name: name
    :return: logger
    """
    ...

def update_formatter_for_loggers(loggers_iter, formatter): # -> None:
    """
    :param formatter:
    :param loggers_iter:
    """
    ...

def parse_int(input_int, default): # -> int:
    ...

def validate_subclass(subclass, superclass): # -> Literal[True]:
    """

    :param subclass
    :param superclass
    :return: bool
    """
    ...

_epoch = ...
def epoch_nano_second(datetime_):
    ...

def iso_time_format(datetime_): # -> str:
    ...

if hasattr(sys, '_getframe'):
    currentframe = ...
else:
    def currentframe(_no_of_go_up_level):
        """Return the frame object for the caller's stack frame."""
        ...
    
class RequestUtil:
    """
        util for extract request's information
    """
    def __new__(cls, *args, **kw): # -> Self@RequestUtil:
        ...
    
    def get_correlation_id(self, request=..., within_formatter=...): # -> str:
        """
        Gets the correlation id from the header of the request. \
        It tries to search from json_logging.CORRELATION_ID_HEADERS list, one by one.\n
        If found no value, new id will be generated by default.\n
        :param request: request object
        :return: correlation id string
        """
        ...
    
    def get_request_from_call_stack(self, within_formatter=...): # -> Any | None:
        """

        :return: get request object from call stack
        """
        ...
    


def is_not_match_any_pattern(path, patterns): # -> bool:
    ...

