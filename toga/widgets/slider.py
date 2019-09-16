from toga.widgets.base import Widget

class Slider(Widget):

    MIN_WIDTH = 100
    type_element = "INPUT"
    can_have_children = True

    #__pragma__('kwargs')

    def __init__(self, id=None, style=None, default=None, range=None, on_slide=None, enabled=True, factory=None):
        super().__init__(self, id=id, style=style, enabled=enabled, factory=factory)
        self.elm.setAttribute('type','range')
        self.elm.className = "form-control-range"

        
        self.range = range
        self.value = default
        self.enabled = enabled
        self.on_slide = on_slide

    #__pragma__('kwargs')

    @property
    def value(self):
        return self.elm.value

    @value.setter
    def set_value(self, value):
        if value == None:
            self.elm.value = 0.5
        elif self.elm.min <= value <= self.elm.max:
            self.elm.value = value
        else:
            raise ValueError('Slider value ({}) is not in range ({}-{})'.format(value, self.elm.min, self.elm.max))

    @property
    def range(self):
        return tuple(self.elm.min, self.elm.max)

    @range.setter
    def set_range(self, range):
        self.elm.min, self.elm.max = (0.0, 1.0) if range == None else range
        if self.elm.min >= self.elm.max:
            raise ValueError('Range min value has to be smaller than max value.')

    @property
    def on_slide(self):
        return self._on_slide
    
    @on_slide.setter
    def on_slide(self, fun):
        self._on_slide = fun
        if fun:
            self.elm.onchange = lambda evt: self._on_slide(self)
        else:
            self.elm.onchange = None
    
    

        