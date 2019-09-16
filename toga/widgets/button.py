from toga.widgets.base import Widget

#__pragma__('kwargs')

class Button(Widget):

    type_element = "BUTTON"
    can_have_children = False

    #__pragma__('kwargs')

    def __init__(self, label, id=None, style=None, on_press=None, enabled=True, factory=None):
        super().__init__(id=id, enabled=enabled, style=style, factory=factory)
        self.elm.className = "btn"
        self.label = label
        self.on_press = on_press

    #__pragma__('nokwargs')

    @property
    def label(self):
        return self.elm.innerHTML

    @label.setter
    def label(self, text):
        self.elm.innerHTML = text

    @property
    def on_press(self):
        return self._on_press

    @on_press.setter
    def on_press(self, fun):
        self._on_press = fun
        if fun:
            self.elm.onclick = lambda evt: self.on_press(self)
        else:
            self.elm.onclick = None