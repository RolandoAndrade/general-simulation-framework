import unittest

import injector

from core.modules.base_module import BaseModule


class Logger:
    def log(self, str: str):
        print(str)


class ServiceA:
    logger: Logger

    @injector.inject
    def __init__(self, logger: Logger):
        self.logger = logger

    def doA(self):
        self.logger.log("Doing A")


class ServiceB:
    logger: Logger
    serviceA: ServiceA

    @injector.inject
    def __init__(self, serviceA: ServiceA, logger: Logger):
        self.logger = logger
        self.serviceA = serviceA

    def doB(self):
        self.serviceA.doA()
        self.logger.log("Doing B")


class A(BaseModule):
    classes = [Logger, ServiceA, ServiceB]

    def __init__(self):
        super().__init__()






class BaseModuleTest(unittest.TestCase):
    def test_something(self):
        inj = injector.Injector()
        a: A = inj.get(A)

if __name__ == '__main__':
    unittest.main()
