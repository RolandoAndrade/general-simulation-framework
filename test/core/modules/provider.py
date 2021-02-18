from __future__ import annotations

import unittest
from dataclasses import dataclass

from core.modules.component import Component
from core.modules.provider import Provider


@dataclass
class Component1(Component):
    name: str


@dataclass
class Component2(Component):
    number: int


class HelpComponent(Component):
    name: Component1
    number: Component2

    def __init__(self, name: Component1, number: Component2):
        self.number = number
        self.name = name

    def __str__(self):
        return "name: " + self.name.name + ", number: " + str(self.number.number)


class ProviderTest(unittest.TestCase):
    provider: Provider

    def setUp(self) -> None:
        self.provider = Provider(HelpComponent, [Component1("hola"), Component2(1)])

    def test_instance(self):
        hc: HelpComponent = self.provider.instance()
        self.assertEqual(hc.name.name, "hola")
        self.assertEqual(hc.number.number, 1)


if __name__ == '__main__':
    unittest.main()
