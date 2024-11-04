import logging
from typing import Any, TYPE_CHECKING

from pyjudo.idisposable import IDisposable

if TYPE_CHECKING:
    from pyjudo.service_container import ServiceContainer


class ServiceScope:
    """
    Represents a scope for services.
    """
    def __init__(self, service_container: "ServiceContainer") -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._instances: dict[type[Any], Any] = {}
        self._disposables: list[IDisposable] = []
        self._container = service_container
    
    def get[T](self, abstract_class: type[T], **overrides: Any) -> T:
        return self._container._resolve(abstract_class, scope=self, overrides=overrides)

    def has_instance(self, abstract_class: type) -> bool:
        return abstract_class in self._instances
    
    def get_instance[T](self, abstract_class: type[T]) -> T:
        return self._instances[abstract_class]

    def set_instance(self, abstract_class: type, instance: Any) -> None:
        self._instances[abstract_class] = instance
        if isinstance(instance, IDisposable):
            self._disposables.append(instance)
    
    def __enter__(self):
        self._container._push_scope(self)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        for instance in self._disposables:
            instance.dispose()
        self._container._pop_scope()