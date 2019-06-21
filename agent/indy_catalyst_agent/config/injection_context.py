"""Injection context implementation."""

from collections import namedtuple
import copy
from typing import Mapping

from .base import BaseInjector, InjectorError
from .injector import Injector
from .settings import Settings

Scope = namedtuple("Scope", "name injector")


class InjectionContextError(InjectorError):
    """Base class for issues in the injection context."""


class InjectionContext(BaseInjector):
    """Manager for configuration settings and class providers."""

    ROOT_SCOPE = "application"

    def __init__(self, *, settings: Mapping[str, object] = None):
        """Initialize a `ServiceConfig`."""
        self._injector = Injector(settings)
        self._scope_name = self.ROOT_SCOPE
        self._scopes = []

    @property
    def injector(self) -> Injector:
        """Accessor for scope-specific injector."""
        return self._injector

    @injector.setter
    def injector(self, injector: Injector):
        """Setter for scope-specific injector."""
        self._injector = injector

    @property
    def scope_name(self) -> str:
        """Accessor for the current scope name."""
        return self._scope_name

    @scope_name.setter
    def scope_name(self, scope_name: str):
        """Accessor for the current scope name."""
        self._scope_name = scope_name

    @property
    def settings(self) -> Settings:
        """Accessor for scope-specific settings."""
        return self.injector.settings

    @settings.setter
    def settings(self, settings: Settings):
        """Setter for scope-specific settings."""
        self.injector.settings = settings

    def update_settings(self, settings: Mapping[str, object]):
        """Update the scope with additional settings."""
        if settings:
            self.injector.settings = self.injector.settings.extend(settings)

    def start_scope(
        self, scope_name: str, settings: Mapping[str, object] = None
    ) -> "InjectionContext":
        """Begin a new named scope.

        Args:
            scope_name: The unique name for the scope being entered
            settings: An optional mapping of additional settings to apply

        Returns:
            A new injection context representing the scope

        """
        if not scope_name:
            raise InjectionContextError("Scope name must be non-empty")
        if self.scope_name == scope_name:
            raise InjectionContextError("Cannot re-enter scope: {}".format(scope_name))
        for scope in self._scopes:
            if scope.name == scope_name:
                raise InjectionContextError(
                    "Cannot re-enter scope: {}".format(scope_name)
                )
        result = self.copy()
        result._scopes.append(Scope(name=self.scope_name, injector=self.injector))
        result.scope_name = scope_name
        if settings:
            result.update_settings(settings)
        return result

    def injector_for_scope(self, scope_name: str) -> Injector:
        """Fetch the injector for a specific scope.

        Args:
            scope_name: The unique scope identifier
        """
        if scope_name == self.scope_name:
            return self.injector
        for scope in self._scopes:
            if scope.name == scope_name:
                return scope.injector
        return None

    async def inject(
        self,
        base_cls: type,
        settings: Mapping[str, object] = None,
        *,
        required: bool = True
    ) -> object:
        """
        Get the provided instance of a given class identifier.

        Args:
            cls: The base class to retrieve an instance of
            settings: An optional mapping providing configuration to the provider

        Returns:
            An instance of the base class, or None

        """
        return await self.injector.inject(base_cls, settings, required=required)

    def copy(self) -> "InjectionContext":
        """Produce a copy of the injector instance."""
        result = copy.copy(self)
        result._injector = self.injector.copy()
        result._scopes = self._scopes.copy()
        return result
