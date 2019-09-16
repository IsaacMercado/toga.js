from toga.widgets.base import Widget

class NumberInput(Widget):

    type_element = 'INPUT'
    MIN_WIDTH = 100
    can_have_children = False

    #__pragma__('kwargs')

    def __init__(self, id=None, style=None, factory=None, step=1, min_value=None, max_value=None, readonly=False, on_change=None):
        super().__init__(self, id=id, style=style, factory=factory)
        self.elm.setAttribute('type','number')
        self.elm.className = "form-control"

        self.step = step
        self.min_value = min_value
        self.max_value = max_value
        self.readonly = readonly
        self.on_change = on_change

    #__pragma__('nokwargs')

    @property
    def step(self):
        return self.elm.step

    @step.setter
    def set_step(self, value):
        self.elm.step = value

    @property
    def min_value(self):
        return self.elm.min

    @min_value.setter
    def set_min_value(self, value):
        if value:
            self.elm.min = value
        else:
            self.elm.min = None

    @property
    def max_value(self):
        return self.elm.max

    @max_value.setter
    def set_max_value(self, value):
        if value:
            self.elm.max = value
        else:
            self.elm.max = None

    @property
    def readonly(self):
        return self.elm.readonly

    @readonly.setter
    def set_readonly(self, value):
        self.elm.readonly = value

    @property
    def value(self):
        return self.elm.value

    @value.setter
    def set_value(self, value):
        if value:
            self.elm.value = value
            if self.min_value is not None and self.elm.value < self.min_value:
                self.elm.value = self.min_value
            elif self.max_value is not None and self.elm.value > self.max_value:
                self.elm.value = self.max_value
        else:
            self.elm.value = None

    @property
    def on_change(self):
        return self._on_change
    
    @on_change.setter
    def on_change(self, fun):
        self._on_change = fun
        if fun:
            self.elm.onchange = lambda evt: self._on_change(self)
        else:
            self.elm.onchange = None