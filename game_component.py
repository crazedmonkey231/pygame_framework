from config import *


class GameComponent(object):
    def __init__(self, parent: Game):
        self.parent: Game = parent
        self.comp_tags: set[str] = set()

    def comp_update(self):
        pass
