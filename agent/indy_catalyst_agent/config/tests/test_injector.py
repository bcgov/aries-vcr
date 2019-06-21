from asynctest import TestCase as AsyncTestCase

from ..base import BaseProvider, BaseInjector, BaseSettings, InjectorError
from ..injector import Injector
from ..provider import ClassProvider, CachedProvider


class MockProvider(BaseProvider):
    def __init__(self, value):
        self.settings = None
        self.injector = None
        self.value = value

    async def provide(self, settings: BaseSettings, injector: BaseInjector):
        self.settings = settings
        self.injector = injector
        return self.value


class MockInstance:
    def __init__(self, value, **kwargs):
        self.opened = False
        self.value = value
        self.kwargs = kwargs

    async def open(self):
        self.opened = True


class TestInjector(AsyncTestCase):
    def setUp(self):
        self.test_key = "TEST"
        self.test_value = "VALUE"
        self.test_settings = {self.test_key: self.test_value}
        self.test_instance = Injector(settings=self.test_settings)

    def test_settings_init(self):
        """Test settings initialization."""
        for key in self.test_settings:
            assert key in self.test_instance.settings
            assert self.test_instance.settings[key] == self.test_settings[key]

    async def test_inject_simple(self):
        """Test a basic injection."""
        assert (await self.test_instance.inject(str, required=False)) is None
        with self.assertRaises(InjectorError):
            await self.test_instance.inject(str)
        with self.assertRaises(ValueError):
            await self.test_instance.bind_instance(str, None)
        self.test_instance.bind_instance(str, self.test_value)
        assert (await self.test_instance.inject(str)) is self.test_value

    async def test_inject_provider(self):
        """Test a provider injection."""
        mock_provider = MockProvider(self.test_value)
        self.test_instance.bind_provider(str, mock_provider)
        assert self.test_instance.get_provider(str) is mock_provider
        override_settings = {self.test_key: "NEWVAL"}
        assert (
            await self.test_instance.inject(str, override_settings)
        ) is self.test_value
        assert mock_provider.settings[self.test_key] == override_settings[self.test_key]
        assert mock_provider.injector is self.test_instance

    async def test_bad_provider(self):
        """Test empty and invalid provider results."""
        self.test_instance.bind_provider(str, MockProvider(None))
        with self.assertRaises(InjectorError):
            await self.test_instance.inject(str)
        await self.test_instance.inject(str, required=False)
        self.test_instance.bind_provider(str, MockProvider(1))
        self.test_instance.clear_binding(str)
        assert self.test_instance.get_provider(str) is None
        with self.assertRaises(InjectorError):
            await self.test_instance.inject(str)

    async def test_inject_class(self):
        """Test a provider class injection."""
        provider = ClassProvider(MockInstance, self.test_value, async_init="open")
        self.test_instance.bind_provider(MockInstance, provider)
        assert self.test_instance.get_provider(MockInstance) is provider
        instance = await self.test_instance.inject(MockInstance)
        assert isinstance(instance, MockInstance)
        assert instance.value is self.test_value
        assert instance.opened

    async def test_inject_class_name(self):
        """Test a provider class injection with a named class."""
        provider = ClassProvider("indy_catalyst_agent.config.settings.Settings")
        self.test_instance.bind_provider(BaseSettings, provider)
        instance = await self.test_instance.inject(BaseSettings)
        assert (
            isinstance(instance, BaseSettings)
            and instance.__class__.__name__ == "Settings"
        )

    async def test_inject_class_dependency(self):
        """Test a provider class injection with a dependency."""
        test_str = "TEST"
        test_int = 1
        self.test_instance.bind_instance(str, test_str)
        self.test_instance.bind_instance(int, test_int)
        provider = ClassProvider(
            MockInstance, ClassProvider.Inject(str), param=ClassProvider.Inject(int)
        )
        self.test_instance.bind_provider(object, provider)
        instance = await self.test_instance.inject(object)
        assert instance.value is test_str
        assert instance.kwargs["param"] is test_int

    async def test_inject_cached(self):
        """Test a provider class injection."""
        with self.assertRaises(ValueError):
            CachedProvider(None)
        provider = ClassProvider(MockInstance, self.test_value, async_init="open")
        cached = CachedProvider(provider)
        self.test_instance.bind_provider(MockInstance, cached)
        assert self.test_instance.get_provider(MockInstance) is cached
        i1 = await self.test_instance.inject(MockInstance)
        i2 = await self.test_instance.inject(MockInstance)
        assert i1 is i2

        provider = ClassProvider(MockInstance, self.test_value, async_init="open")
        self.test_instance.bind_provider(MockInstance, provider, cache=True)
        i1 = await self.test_instance.inject(MockInstance)
        i2 = await self.test_instance.inject(MockInstance)
        assert i1 is i2
