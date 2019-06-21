"""Standard Injector implementation."""

from typing import Mapping

from .base import BaseProvider, BaseInjector, InjectorError
from .provider import InstanceProvider, CachedProvider
from .settings import Settings


class Injector(BaseInjector):
    """Injector implementation with static and dynamic bindings."""

    def __init__(self, settings: Mapping[str, object] = None):
        """Initialize an `Injector`."""
        self._providers = {}
        self._settings = Settings(settings)

    @property
    def settings(self) -> Settings:
        """Accessor for scope-specific settings."""
        return self._settings

    @settings.setter
    def settings(self, settings: Settings):
        """Setter for scope-specific settings."""
        self._settings = settings

    def bind_instance(self, base_cls: type, instance: object):
        """Add a static instance as a class binding."""
        self._providers[base_cls] = InstanceProvider(instance)

    def bind_provider(
        self, base_cls: type, provider: BaseProvider, *, cache: bool = False
    ):
        """Add a dynamic instance resolver as a class binding."""
        if not provider:
            raise ValueError("Class provider binding must be non-empty")
        if cache and not isinstance(provider, CachedProvider):
            provider = CachedProvider(provider)
        self._providers[base_cls] = provider

    def clear_binding(self, base_cls: type):
        """Remove a previously-added binding."""
        if base_cls in self._providers:
            del self._providers[base_cls]

    def get_provider(self, base_cls: type):
        """Find the provider associated with a class binding."""
        return self._providers.get(base_cls)

    async def inject(
        self,
        base_cls: type,
        settings: Mapping[str, object] = None,
        *,
        required: bool = True,
    ):
        """
        Get the provided instance of a given class identifier.

        Args:
            cls: The base class to retrieve an instance of
            params: An optional dict providing configuration to the provider

        Returns:
            An instance of the base class, or None

        """
        if not base_cls:
            raise InjectorError("No base class provided for lookup")
        provider = self._providers.get(base_cls)
        ext_settings = self.settings.extend(settings) if settings else self.settings
        if provider:
            result = await provider.provide(ext_settings, self)
        else:
            result = None
        if result is None:
            if required:
                raise InjectorError(
                    "No instance provided for class: {}".format(base_cls.__name__)
                )
        elif not isinstance(result, base_cls):
            raise InjectorError(
                "Provided instance does not implement the base class: {}".format(
                    base_cls.__name__
                )
            )
        return result

    def copy(self) -> BaseInjector:
        """Produce a copy of the injector instance."""
        result = Injector(self.settings)
        result._providers = self._providers.copy()
        return result

    def __repr__(self) -> str:
        """Provide a human readable representation of this object."""
        return f"<{self.__class__.__name__}>"
