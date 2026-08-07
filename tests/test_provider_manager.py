
"""Tests for the provider manager."""

import unittest

from app.providers.manager import ProviderManager
from app.providers.mock import MockProvider
from app.providers.provider_info import ProviderInfo


class ProviderManagerTests(unittest.TestCase):
    """Provider manager tests."""

    def setUp(self):
        self.manager = ProviderManager()
        self.provider = MockProvider()

    def test_register_provider(self):
        self.manager.register(self.provider)

        self.assertEqual(
            self.manager.list_providers(),
            ["mock"],
        )

    def test_get_provider(self):
        self.manager.register(self.provider)

        provider = self.manager.get("mock")

        self.assertIs(provider, self.provider)

    def test_active_provider(self):
        self.manager.register(self.provider)

        self.assertEqual(
            self.manager.active().name,
            "mock",
        )

    def test_set_active_provider(self):
        self.manager.register(self.provider)

        self.manager.set_active("mock")

        self.assertEqual(
            self.manager.active().name,
            "mock",
        )

    def test_remove_provider(self):
        self.manager.register(self.provider)

        self.manager.remove("mock")

        self.assertEqual(
            self.manager.list_providers(),
            [],
        )

    def test_health(self):
        self.manager.register(self.provider)

        self.assertEqual(
            self.manager.health(),
            {
                "mock": True,
            },
        )

    def test_summary(self):
        self.manager.register(self.provider)

        summary = self.manager.summary()

        self.assertEqual(
            len(summary),
            1,
        )

        info = summary[0]

        self.assertIsInstance(
            info,
            ProviderInfo,
        )

        self.assertEqual(
            info.name,
            "mock",
        )

        self.assertTrue(info.active)

        self.assertTrue(info.healthy)

        self.assertEqual(
            info.models,
            ["mock-v1"],
        )

        self.assertTrue(
            info.capabilities.chat,
        )

    def test_unknown_provider(self):
        with self.assertRaises(KeyError):
            self.manager.get("unknown")

    def test_unknown_active_provider(self):
        with self.assertRaises(KeyError):
            self.manager.set_active("unknown")

    def test_no_active_provider(self):
        with self.assertRaises(RuntimeError):
            self.manager.active()


if __name__ == "__main__":
    unittest.main()
