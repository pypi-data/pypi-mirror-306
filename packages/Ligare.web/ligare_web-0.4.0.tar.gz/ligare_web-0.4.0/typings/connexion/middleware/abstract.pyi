"""
This type stub file was generated by pyright.
"""

import abc
import typing as t
from starlette.types import ASGIApp, Receive, Scope, Send
from connexion.operations import AbstractOperation
from connexion.resolver import Resolver
from connexion.spec import Specification

logger = ...
ROUTING_CONTEXT = ...
class SpecMiddleware(abc.ABC):
    """Middlewares that need the specification(s) to be registered on them should inherit from this
    base class"""
    @abc.abstractmethod
    def add_api(self, specification: Specification, **kwargs) -> t.Any:
        """
        Register an API represented by a single OpenAPI specification on this middleware.
        Multiple APIs can be registered on a single middleware.
        """
        ...
    
    @abc.abstractmethod
    async def __call__(self, scope: Scope, receive: Receive, send: Send): # -> None:
        ...
    


class AbstractSpecAPI:
    """Base API class with only minimal behavior related to the specification."""
    def __init__(self, specification: Specification, base_path: t.Optional[str] = ..., resolver: t.Optional[Resolver] = ..., uri_parser_class=..., *args, **kwargs) -> None:
        ...
    


OP = t.TypeVar("OP")
class AbstractRoutingAPI(AbstractSpecAPI, t.Generic[OP]):
    """Base API class with shared functionality related to routing."""
    def __init__(self, *args, pythonic_params=..., resolver_error_handler: t.Optional[t.Callable] = ..., **kwargs) -> None:
        ...
    
    def add_paths(self, paths: t.Optional[dict] = ...) -> None:
        """
        Adds the paths defined in the specification as operations.
        """
        ...
    
    def add_operation(self, path: str, method: str) -> None:
        """
        Adds one operation to the api.

        This method uses the OperationID identify the module and function that will handle the operation

        From Swagger Specification:

        **OperationID**

        A friendly name for the operation. The id MUST be unique among all operations described in the API.
        Tools and libraries MAY use the operation id to uniquely identify an operation.
        """
        ...
    
    @abc.abstractmethod
    def make_operation(self, operation: AbstractOperation) -> OP:
        """Build an operation to register on the API."""
        ...
    


class RoutedAPI(AbstractSpecAPI, t.Generic[OP]):
    def __init__(self, specification: Specification, *args, next_app: ASGIApp, **kwargs) -> None:
        ...
    
    def add_paths(self) -> None:
        ...
    
    def add_operation(self, path: str, method: str) -> None:
        ...
    
    @abc.abstractmethod
    def make_operation(self, operation: AbstractOperation) -> OP:
        """Create an operation of the `operation_cls` type."""
        ...
    


API = t.TypeVar("API", bound="RoutedAPI")
class RoutedMiddleware(SpecMiddleware, t.Generic[API]):
    """Baseclass for middleware that wants to leverage the RoutingMiddleware to route requests to
    its operations.

    The RoutingMiddleware adds the operation_id to the ASGI scope. This middleware registers its
    operations by operation_id at startup. At request time, the operation is fetched by an
    operation_id lookup.
    """
    api_cls: t.Type[API]
    def __init__(self, app: ASGIApp) -> None:
        ...
    
    def add_api(self, specification: Specification, **kwargs) -> API:
        ...
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Fetches the operation related to the request and calls it."""
        ...
    


class MissingOperation(Exception):
    """Missing operation"""
    ...


