"""
This type stub file was generated by pyright.
"""

import typing as t

"""
This module contains resolvers, functions that resolves the user defined view functions
from the operations defined in the OpenAPI spec.
"""
logger = ...
class Resolution:
    def __init__(self, function, operation_id) -> None:
        """
        Represents the result of operation resolution

        :param function: The endpoint function
        :type function: types.FunctionType
        """
        ...
    


class Resolver:
    def __init__(self, function_resolver: t.Callable = ...) -> None:
        """
        Standard resolver

        :param function_resolver: Function that resolves functions using an operationId
        """
        ...
    
    def resolve(self, operation): # -> Resolution:
        """
        Default operation resolver

        :type operation: connexion.operations.AbstractOperation
        """
        ...
    
    def resolve_operation_id(self, operation): # -> str:
        """
        Default operationId resolver

        :type operation: connexion.operations.AbstractOperation
        """
        ...
    
    def resolve_function_from_operation_id(self, operation_id):
        """
        Invokes the function_resolver

        :type operation_id: str
        """
        ...
    


class RelativeResolver(Resolver):
    """
    Resolves endpoint functions relative to a given root path or module.
    """
    def __init__(self, root_path, function_resolver=...) -> None:
        """
        :param root_path: The root path relative to which an operationId is resolved.
            Can also be a module. Has the same effect as setting
            `x-swagger-router-controller` or `x-openapi-router-controller` equal to
            `root_path` for every operation individually.
        :type root_path: typing.Union[str, types.ModuleType]
        :param function_resolver: Function that resolves functions using an operationId
        :type function_resolver: types.FunctionType
        """
        ...
    
    def resolve_operation_id(self, operation): # -> str:
        """Resolves the operationId relative to the root path, unless
        x-swagger-router-controller or x-openapi-router-controller is specified.

        :param operation: The operation to resolve
        :type operation: connexion.operations.AbstractOperation
        """
        ...
    


class RestyResolver(Resolver):
    """
    Resolves endpoint functions using REST semantics (unless overridden by specifying operationId)
    """
    def __init__(self, default_module_name: str, *, collection_endpoint_name: str = ...) -> None:
        """
        :param default_module_name: Default module name for operations
        :param collection_endpoint_name: Name of function to resolve collection endpoints to
        """
        ...
    
    def resolve_operation_id(self, operation): # -> str:
        """
        Resolves the operationId using REST semantics unless explicitly configured in the spec

        :type operation: connexion.operations.AbstractOperation
        """
        ...
    
    def resolve_operation_id_using_rest_semantics(self, operation): # -> str:
        """
        Resolves the operationId using REST semantics

        :type operation: connexion.operations.AbstractOperation
        """
        ...
    


class MethodResolverBase(RestyResolver):
    """
    Resolves endpoint functions based on Flask's MethodView semantics, e.g.

    .. code-block:: yaml

        paths:
            /foo_bar:
                get:
                    # Implied function call: api.FooBarView().get

    .. code-block:: python

        class FooBarView(MethodView):
            def get(self):
                return ...
            def post(self):
                return ...

    """
    _class_arguments_type = t.Dict[str, t.Dict[str, t.Union[t.Iterable, t.Dict[str, t.Any]]]]
    def __init__(self, *args, class_arguments: _class_arguments_type = ..., **kwargs) -> None:
        """
        :param args: Arguments passed to :class:`~RestyResolver`
        :param class_arguments: Arguments to instantiate the View Class in the format below
        :param kwargs: Keywords arguments passed to :class:`~RestyResolver`

        .. code-block:: python

            {
              "ViewName": {
                "args": (positional arguments,)
                "kwargs": {
                  "keyword": "argument"
                }
              }
            }
        """
        ...
    
    def resolve_operation_id(self, operation): # -> str:
        """
        Resolves the operationId using REST semantics unless explicitly configured in the spec
        Once resolved with REST semantics the view_name is capitalised and has 'View' added
        to it so it now matches the Class names of the MethodView

        :type operation: connexion.operations.AbstractOperation
        """
        ...
    
    def resolve_function_from_operation_id(self, operation_id):
        """
        Invokes the function_resolver

        :type operation_id: str
        """
        ...
    
    def resolve_method_from_class(self, view_name, meth_name, view_cls):
        """
        Returns the view function for the given view class.
        """
        ...
    


class MethodResolver(MethodResolverBase):
    """
    A generic method resolver that instantiates a class and extracts the method
    from it, based on the operation id.
    """
    def resolve_method_from_class(self, view_name, meth_name, view_cls): # -> Any:
        ...
    


class MethodViewResolver(MethodResolverBase):
    """
    A specialized method resolver that works with flask's method views.
    It resolves the method by calling as_view on the class.
    """
    def __init__(self, *args, **kwargs) -> None:
        ...
    
    def resolve_method_from_class(self, view_name, meth_name, view_cls):
        ...
    


