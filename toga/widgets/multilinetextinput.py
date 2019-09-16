from toga.widgets.base import Widget

class MultilineTextInput(Widget):

    type_element = 'TEXTAREA'
    can_have_children = False
    MIN_HEIGHT = 100
    MIN_WIDTH = 100

    #__pragma__('kwargs')

    def __init__(self, id=None, style=None, factory=None, initial=None, readonly=False, placeholder=None):
        super().__init__(self, id=id, style=style, enabled=True, factory=factory)
        self.elm.className = "form-control"
        self.value = initial
        self.placeholder = placeholder
        self.readonly = readonly

    #__pragma__('nokwargs')

    @property
    def readonly(self):
        return self.elm.readonly

    @readonly.setter
    def set_readonly(self, value):
        self.elm.readonly = value

    @property
    def placeholder(self):
        return self.elm.placeholder

    @placeholder.setter
    def set_placeholder(self, value):
        if value:
            self.elm.placeholder = value

    @property
    def value(self):
        return self.elm.value

    @value.setter
    def set_value(self, value):
        if value:
            self.elm.value = value