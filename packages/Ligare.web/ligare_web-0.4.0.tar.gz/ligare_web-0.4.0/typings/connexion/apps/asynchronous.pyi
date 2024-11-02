"""
This type stub file was generated by pyright.
"""

import pathlib
import typing as t
from starlette.responses import Response as StarletteResponse
from starlette.types import Receive, Scope, Send
from connexion.apps.abstract import AbstractApp
from connexion.jsonifier import Jsonifier
from connexion.lifecycle import ConnexionRequest, ConnexionResponse
from connexion.middleware.abstract import RoutedAPI, RoutedMiddleware
from connexion.middleware.lifespan import Lifespan
from connexion.operations import AbstractOperation
from connexion.options import SwaggerUIOptions
from connexion.resolver import Resolver
from connexion.types import MaybeAwaitable
from connexion.uri_parsing import AbstractURIParser

"""
This module defines a native connexion asynchronous application.
"""
logger = ...
class AsyncOperation:
    def __init__(self, fn: t.Callable, jsonifier: Jsonifier, operation_id: str, pythonic_params: bool) -> None:
        ...
    
    @classmethod
    def from_operation(cls, operation: AbstractOperation, *, pythonic_params: bool, jsonifier: Jsonifier) -> AsyncOperation:
        ...
    
    @property
    def fn(self) -> t.Callable:
        ...
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> StarletteResponse:
        ...
    


class AsyncApi(RoutedAPI[AsyncOperation]):
    def __init__(self, *args, pythonic_params: bool, jsonifier: t.Optional[Jsonifier] = ..., **kwargs) -> None:
        ...
    
    def make_operation(self, operation: AbstractOperation) -> AsyncOperation:
        ...
    


class AsyncASGIApp(RoutedMiddleware[AsyncApi]):
    api_cls = AsyncApi
    def __init__(self) -> None:
        ...
    
    def add_api(self, *args, name: str = ..., **kwargs): # -> AsyncApi:
        ...
    
    def add_url_rule(self, rule, endpoint: str = ..., view_func: t.Callable = ..., methods: t.List[str] = ..., **options): # -> None:
        ...
    


class AsyncApp(AbstractApp):
    """Connexion Application based on ConnexionMiddleware wrapping a async Connexion application
    based on starlette tools."""
    def __init__(self, import_name: str, *, lifespan: t.Optional[Lifespan] = ..., middlewares: t.Optional[list] = ..., specification_dir: t.Union[pathlib.Path, str] = ..., arguments: t.Optional[dict] = ..., auth_all_paths: t.Optional[bool] = ..., jsonifier: t.Optional[Jsonifier] = ..., pythonic_params: t.Optional[bool] = ..., resolver: t.Optional[t.Union[Resolver, t.Callable]] = ..., resolver_error: t.Optional[int] = ..., strict_validation: t.Optional[bool] = ..., swagger_ui_options: t.Optional[SwaggerUIOptions] = ..., uri_parser_class: t.Optional[AbstractURIParser] = ..., validate_responses: t.Optional[bool] = ..., validator_map: t.Optional[dict] = ..., security_map: t.Optional[dict] = ...) -> None:
        """
        :param import_name: The name of the package or module that this object belongs to. If you
            are using a single module, __name__ is always the correct value. If you however are
            using a package, it’s usually recommended to hardcode the name of your package there.
        :param lifespan: A lifespan context function, which can be used to perform startup and
            shutdown tasks.
        :param middlewares: The list of middlewares to wrap around the application. Defaults to
            :obj:`middleware.main.ConnexionMiddleware.default_middlewares`
        :param specification_dir: The directory holding the specification(s). The provided path
            should either be absolute or relative to the root path of the application. Defaults to
            the root path.
        :param arguments: Arguments to substitute the specification using Jinja.
        :param auth_all_paths: whether to authenticate not paths not defined in the specification.
            Defaults to False.
        :param jsonifier: Custom jsonifier to overwrite json encoding for json responses.
        :param pythonic_params: When True, CamelCase parameters are converted to snake_case and an
            underscore is appended to any shadowed built-ins. Defaults to False.
        :param resolver: Callable that maps operationId to a function or instance of
            :class:`resolver.Resolver`.
        :param resolver_error: Error code to return for operations for which the operationId could
            not be resolved. If no error code is provided, the application will fail when trying to
            start.
        :param strict_validation: When True, extra form or query parameters not defined in the
            specification result in a validation error. Defaults to False.
        :param swagger_ui_options: Instance of :class:`options.ConnexionOptions` with
            configuration options for the swagger ui.
        :param uri_parser_class: Class to use for uri parsing. See :mod:`uri_parsing`.
        :param validate_responses: Whether to validate responses against the specification. This has
            an impact on performance. Defaults to False.
        :param validator_map: A dictionary of validators to use. Defaults to
            :obj:`validators.VALIDATOR_MAP`.
        :param security_map: A dictionary of security handlers to use. Defaults to
            :obj:`security.SECURITY_HANDLERS`
        """
        ...
    
    def add_url_rule(self, rule, endpoint: str = ..., view_func: t.Callable = ..., **options): # -> None:
        ...
    
    def add_error_handler(self, code_or_exception: t.Union[int, t.Type[Exception]], function: t.Callable[[ConnexionRequest, Exception], MaybeAwaitable[ConnexionResponse]]) -> None:
        ...
    


