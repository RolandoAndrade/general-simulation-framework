import logging
from typing import List

from injector import inject, Injector, Module, provider

class BaseModule(Module):

    def __init__(self):
        print("Init module " + str(self.__class__.__name__))
