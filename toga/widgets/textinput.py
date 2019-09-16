from toga.widgets.base import Widget

class TextInput(Widget):

    MIN_WIDTH = 100
    type_element = "INPUT"
    can_have_children = False

    def __init__(self, id=None, style=None, factory=None, initial=None, placeholder=None, readonly=False, on_change=None):
        super().__init__(id=id, style=style, factory=factory)
        
        self.elm.setAttribute('type','text')
        self.elm.className = "form-control"

        self.on_change = on_change
        self.placeholder = placeholder
        self.readonly = readonly
        self.value = initial

    @property
    def readonly(self):
        return self.elm.readonly

    @readonly.setter
    def readonly(self, value):
        self.elm.readonly = value

    @property
    def placeholder(self):
        return self.elm.placeholder

    @placeholder.setter
    def placeholder(self, value):
        if value:
            self.elm.placeholder = str(value)
        else:
            self.elm.placeholder = ''

    @property
    def value(self):
        return self.elm.value

    @value.setter
    def value(self, value):
        v = ''
        if value:
            v = str(value)
        self.elm.value = v

    def clear(self):
        self.value = ''

    @property
    def on_change(self):
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = handler
        if handler:
            self.elm.onchange = lambda evt: self._on_change(self)
        else:
            self.elm.onchange = None