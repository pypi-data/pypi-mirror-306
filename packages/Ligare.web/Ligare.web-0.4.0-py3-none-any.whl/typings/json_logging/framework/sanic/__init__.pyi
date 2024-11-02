"""
This type stub file was generated by pyright.
"""

import logging
import logging.config
import sys
import json_logging
import json_logging.framework
from json_logging.framework_base import AppRequestInstrumentationConfigurator, FrameworkConfigurator, RequestAdapter, ResponseAdapter
from json_logging.util import is_not_match_any_pattern

def is_sanic_present(): # -> bool:
    ...

class SanicAppConfigurator(FrameworkConfigurator):
    def config(self): # -> None:
        ...
    


class SanicAppRequestInstrumentationConfigurator(AppRequestInstrumentationConfigurator):
    def config(self, app, exclude_url_patterns=...): # -> None:
        ...
    
    def get_request_logger(self): # -> Logger:
        ...
    


class SanicRequestAdapter(RequestAdapter):
    @staticmethod
    def get_current_request():
        ...
    
    @staticmethod
    def support_global_request_object(): # -> Literal[False]:
        ...
    
    @staticmethod
    def get_request_class_type():
        ...
    
    def get_remote_user(self, request): # -> None:
        ...
    
    def get_http_header(self, request, header_name, default=...): # -> None:
        ...
    
    def set_correlation_id(self, request, value): # -> None:
        ...
    
    def get_correlation_id_in_request_context(self, request): # -> None:
        ...
    
    def get_protocol(self, request): # -> Literal['-']:
        ...
    
    def get_path(self, request):
        ...
    
    def get_content_length(self, request): # -> Literal['-']:
        ...
    
    def get_method(self, request):
        ...
    
    def get_remote_ip(self, request):
        ...
    
    def get_remote_port(self, request): # -> Literal['-']:
        ...
    


class SanicResponseAdapter(ResponseAdapter):
    def get_status_code(self, response):
        ...
    
    def get_response_size(self, response): # -> Literal['-']:
        ...
    
    def get_content_type(self, response):
        ...
    


