from abc import ABC, abstractmethod


class Runner(ABC):
    
    @abstractmethod
    def get_input(self) -> str:
        pass

    @abstractmethod
    def send_output(self, message: str) -> None:
        pass


class ConsoleRunner(Runner):

    def get_input(self) -> str:
        return input("You: ")

    def send_output(self, message: str) -> None:
        print(f"AI: {message}")


class RESTRunner(Runner):

    def __init__(self, url):
        self.url = url
        self.connection = None
        self.initialize()

    def initialize(self):
        pass

    def get_input(self) -> str:
        return 