from config import *


class LevelComponent(object):
    def __init__(self, parent):
        self.parent: Level = parent if isinstance(parent, Level) else None
        self.needs_update: bool = True
        self.comp_tags: set[str] = set()

    def comp_on_load(self):
        pass

    def comp_on_unload(self):
        pass

    def comp_update(self):
        pass

    def comp_destroy(self):
        self.parent = None
