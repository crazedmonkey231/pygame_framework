from config import *


#
# Component class
#
class Component(object):
    def __init__(self, parent):
        self.parent = parent
        self.needs_update: bool = True
        self.comp_tags: set[str] = set()

    def comp_activate(self):
        pass

    def comp_deactivate(self):
        pass

    def comp_reset(self):
        pass

    def comp_update(self):
        pass

    def comp_draw(self):
        pass

    def comp_destroy(self):
        self.parent = None


#
# Game Component class
#
class GameComponent(Component):
    def __init__(self, parent):
        super().__init__(parent)
        from game import Game
        self.parent: Game = self.parent if (
            isinstance(self.parent, Game)) else None


#
# Game Object Component
#
class GameObjectComponent(Component):
    def __init__(self, parent):
        super().__init__(parent)
        from game_object import GameObjectWithComponents
        self.parent: GameObjectWithComponents = self.parent if (
            isinstance(self.parent, GameObjectWithComponents)) else None


#
# Level Component
#
class LevelComponent(Component):
    def __init__(self, parent):
        super().__init__(parent)
        from level import Level
        self.parent: Level = self.parent if (
            isinstance(self.parent, Level)) else None


# Utils-----------------------------------------------------------------------------------------------------------------


def get_components_by_class(component_list: list[Component], component_class: type) -> list[Component]:
    return [c for c in component_list if isinstance(c, component_class)]


def get_component_by_class(component_list: list[Component], component_class: type) -> Component:
    comps = get_components_by_class(component_list, component_class)
    if comps:
        return get_components_by_class(component_list, component_class)[0]
    return None


def add_component(comp_type: type, comp_list: list[Component], component: Component | type, parent: object):
    is_instance_of_comp = isinstance(component, comp_type)
    is_type_of_comp = isinstance(component, type) and issubclass(component, comp_type)
    is_valid = is_instance_of_comp or is_type_of_comp
    if is_valid and component:
        comp: Component = None
        if is_instance_of_comp:
            comp = component
        elif is_type_of_comp:
            comp = component(parent)
        if comp:
            comp_list.append(comp)
            comp.comp_activate()


def remove_component(comp_type: type, comp_list: list[Component], component: Component | type, optional_tags: set[str] = None):
    is_instance_of_comp = isinstance(component, comp_type)
    is_type_of_comp = isinstance(component, type) and issubclass(component, comp_type)
    is_valid = is_instance_of_comp or is_type_of_comp
    if is_valid and comp_list and (component or optional_tags):
        for comp in comp_list:
            f1 = (component and
                  (is_instance_of_comp and comp == component) or (is_type_of_comp and comp.__class__ == component))
            f2 = optional_tags and bool(comp.comp_tags & optional_tags)
            if f1 or f2:
                comp.comp_deactivate()
                comp.comp_destroy()
                comp_list.remove(comp)
