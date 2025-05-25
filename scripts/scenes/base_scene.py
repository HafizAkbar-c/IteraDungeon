from abc import ABC, abstractmethod


class BaseScene(ABC):
    def __init__(self, game):
        self._game = game

    @property
    def game(self):
        return self._game

    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass
