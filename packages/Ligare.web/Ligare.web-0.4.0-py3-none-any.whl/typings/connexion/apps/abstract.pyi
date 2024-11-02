"""
This type stub file was generated by pyright.
"""

import abc
import pathlib
import typing as t

from connexion.jsonifier import Jsonifier
from connexion.lifecycle import ConnexionRequest, ConnexionResponse
from connexion.middleware import MiddlewarePosition, SpecMiddleware
from connexion.middleware.lifespan import Lifespan
from connexion.options import SwaggerUIOptions
from connexion.resolver import Resolver
from connexion.types import MaybeAwaitable
from connexion.uri_parsing import AbstractURIParser
from starlette.testclient import TestClient
from starlette.types import ASGIApp, Receive, Scope, Send

"""
This module defines an AbstractApp, which defines a standardized user interface for a Connexion
application.
"""

class AbstractApp:
    """
    Abstract class for a Connexion Application. A Connexion Application provides an interface for a
    framework application wrapped by Connexion Middleware. Since its main function is to provide an
    interface, it delegates most of the work to the middleware and framework application.
    """

    _middleware_app: SpecMiddleware
    def __init__(
        self,
        import_name: str,
        *,
        lifespan: t.Optional[Lifespan] = ...,
        middlewares: t.Optional[list[t.Any]] = ...,
        specification_dir: t.Union[pathlib.Path, str] = ...,
        arguments: t.Optional[dict[t.Any, t.Any]] = ...,
        auth_all_paths: t.Optional[bool] = ...,
        jsonifier: t.Optional[Jsonifier] = ...,
        pythonic_params: t.Optional[bool] = ...,
        resolver: t.Optional[t.Union[Resolver, t.Callable[..., t.Any]]] = ...,
        resolver_error: t.Optional[int] = ...,
        strict_validation: t.Optional[bool] = ...,
        swagger_ui_options: t.Optional[SwaggerUIOptions] = ...,
        uri_parser_class: t.Optional[AbstractURIParser] = ...,
        validate_responses: t.Optional[bool] = ...,
        validator_map: t.Optional[dict[t.Any, t.Any]] = ...,
        security_map: t.Optional[dict[t.Any, t.Any]] = ...,
    ) -> None:
        """
        :param import_name: The name of the package or module that this object belongs to. If you
            are using a single module, __name__ is always the correct value. If you however are
            using a package, it’s usually recommended to hardcode the name of your package there.
        :param lifespan: A lifespan context function, which can be used to perform startup and
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
    def add_middleware(
        self,
        middleware_class: t.Type[ASGIApp] | t.Any,
        position: MiddlewarePosition = ...,
        **options: t.Any,
    ) -> None:
        """Add a middleware to the stack on the specified position.

        :param middleware_class: Middleware class to add
        :param position: Position to add the middleware, one of the MiddlewarePosition Enum
        :param options: Options to pass to the middleware_class on initialization
        """
        ...
    def add_api(
        self,
        specification: t.Union[pathlib.Path, str, dict[t.Any, t.Any]],
        *,
        base_path: t.Optional[str] = ...,
        name: t.Optional[str] = ...,
        arguments: t.Optional[dict[t.Any, t.Any]] = ...,
        auth_all_paths: t.Optional[bool] = ...,
        jsonifier: t.Optional[Jsonifier] = ...,
        pythonic_params: t.Optional[bool] = ...,
        resolver: t.Optional[t.Union[Resolver, t.Callable[..., t.Any]]] = ...,
        resolver_error: t.Optional[int] = ...,
        strict_validation: t.Optional[bool] = ...,
        swagger_ui_options: t.Optional[SwaggerUIOptions] = ...,
        uri_parser_class: t.Optional[AbstractURIParser] = ...,
        validate_responses: t.Optional[bool] = ...,
        validator_map: t.Optional[dict[t.Any, t.Any]] = ...,
        security_map: t.Optional[dict[t.Any, t.Any]] = ...,
        **kwargs: t.Any,
    ) -> t.Any:
        """
        Register an API represented by a single OpenAPI specification on this application.
        Multiple APIs can be registered on a single application.

        :param specification: OpenAPI specification. Can be provided either as dict, or as path
            to file.
        :param base_path: Base path to host the API. This overrides the basePath / servers in the
            specification.
        :param name: Name to register the API with. If no name is passed, the base_path is used
            as name instead.
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
        :param swagger_ui_options: A :class:`options.ConnexionOptions` instance with configuration
            options for the swagger ui.
        :param uri_parser_class: Class to use for uri parsing. See :mod:`uri_parsing`.
        :param validate_responses: Whether to validate responses against the specification. This has
            an impact on performance. Defaults to False.
        :param validator_map: A dictionary of validators to use. Defaults to
            :obj:`validators.VALIDATOR_MAP`
        :param security_map: A dictionary of security handlers to use. Defaults to
            :obj:`security.SECURITY_HANDLERS`
        :param kwargs: Additional keyword arguments to pass to the `add_api` method of the managed
            middlewares. This can be used to pass arguments to middlewares added beyond the default
            ones.

        :return: The Api registered on the middleware application wrapping the framework.
        """
        ...
    def add_url_rule(
        self,
        rule: t.Any,
        endpoint: str = ...,
        view_func: t.Callable[..., t.Any] = ...,
        **options: t.Any,
    ) -> None:
        """
        Connects a URL rule.  Works exactly like the `route` decorator.

        Basically this example::

            @app.route('/')
            def index():
                pass

        Is equivalent to the following::

            def index():
                pass
            app.add_url_rule('/', 'index', index)

        Internally`route` invokes `add_url_rule` so if you want to customize the behavior via
        subclassing you only need to change this method.

        :param rule: the URL rule as string.
        :param endpoint: the name of the endpoint for the registered URL rule, which is used for
            reverse lookup. Flask defaults to the name of the view function.
        :param view_func: the function to call when serving a request to the provided endpoint.
        :param options: the options to be forwarded to the underlying ``werkzeug.routing.Rule``
            object.  A change to Werkzeug is handling of method options. methods is a list of
            methods this rule should be limited to (`GET`, `POST` etc.).  By default a rule just
            listens for `GET` (and implicitly `HEAD`).
        """
        ...
    def route(
        self, rule: str, **options: t.Any
    ) -> t.Callable[..., t.Callable[..., t.Any]]:
        """
        A decorator that is used to register a view function for a
        given URL rule.  This does the same thing as `add_url_rule`
        but is intended for decorator usage::

            @app.route('/')
            def index():
                return 'Hello World'

        :param rule: the URL rule as string
        :param options: the options to be forwarded to the underlying ``werkzeug.routing.Rule``
                        object. A change to Werkzeug is handling of method options. methods is a
                        list of methods this rule should be limited to (`GET`, `POST` etc.).
                        By default a rule just listens for `GET` (and implicitly `HEAD`).
        """
        ...
    @abc.abstractmethod
    def add_error_handler(
        self,
        code_or_exception: t.Union[int, t.Type[Exception]],
        function: t.Callable[
            [ConnexionRequest, Exception], MaybeAwaitable[ConnexionResponse]
        ],
    ) -> None:
        """
        Register a callable to handle application errors.

        :param code_or_exception: An exception class or the status code of HTTP exceptions to
            handle.
        :param function: Callable that will handle exception, may be async.
        """
        ...
    def test_client(self, **kwargs: t.Any) -> TestClient:
        """Creates a test client for this application. The keywords arguments passed in are
        passed to the ``StarletteClient``."""
        ...
    def run(self, import_string: str = ..., **kwargs: t.Any) -> None:
        """Run the application using uvicorn.

        :param import_string: application as import string (eg. "main:app"). This is needed to run
                              using reload.
        :param kwargs: kwargs to pass to `uvicorn.run`.
        """
        ...
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None: ...

__all__ = (
    "abc",
    "pathlib",
    "t",
    "Jsonifier",
    "ConnexionRequest",
    "ConnexionResponse",
    "MiddlewarePosition",
    "SpecMiddleware",
    "Lifespan",
    "SwaggerUIOptions",
    "Resolver",
    "MaybeAwaitable",
    "AbstractURIParser",
    "TestClient",
    "ASGIApp",
    "Receive",
    "Scope",
    "Send",
    "AbstractApp",
)
