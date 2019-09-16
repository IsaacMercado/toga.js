from toga.widgets.base import Widget

class PasswordInput(Widget):

    type_element = 'INPUT'
    MIN_WIDTH = 100
    can_have_children = False

    #__pragma__('kwargs')

    def __init__(self, id=None, style=None, factory=None, initial=None, placeholder=None, readonly=False):
        super().__init__(self, id=id, style=style, enabled=True, factory=factory)
        self.elm.setAttribute('type','password')
        self.elm.className = "form-control"

        self.elm.value = initial
        self.placeholder = placeholder

    #__pragma__('kwargs')

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
        self.elm.value = value

    def clear(self):
        self.value = ''