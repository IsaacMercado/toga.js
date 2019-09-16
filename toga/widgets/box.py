from toga.widgets.base import Widget

class Box(Widget):
    def __init__(self, id=None, style=None, children=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._children = []
        if children:
            for child in children:
                self.add(child)

