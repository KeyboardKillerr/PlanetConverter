from abc import ABC, abstractmethod


class Logger(ABC):

    @staticmethod
    @abstractmethod
    async def log(message: str) -> None:
        pass


class AsyncConsoleLogger(Logger):

    def __init__(self):
        self.logs = list()

    @staticmethod
    async def log(message: str) -> None:
        print(message)
