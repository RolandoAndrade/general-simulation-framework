from injector import Module


class BaseModule(Module):

    def __init__(self):
        print("Init module " + str(self.__class__.__name__))
