from toga.widgets.base import Widget

class ProgressBar(Widget):

    type_element = 'PROGRESS'
    MIN_WIDTH = 100
    can_have_children = False

    #__pragma__('kwargs')

    def __init__(self, id=None, style=None, max=1, value=0, running=False, factory=None):
        super().__init__(self, id=id, style=style, factory=factory)
        self.elm.className = 'progress'

        self.max = max
        self.value = value
        self._is_running = running

        if running:
            self.start()
        else:
            self.stop()

    #__pragma__('nokwargs')

    @property
    def is_running(self):
        return self._is_running

    @property
    def is_determinate(self):
        return self.max != None
    
    
    @property
    def value(self):
        return self.elm.value

    @value.setter
    def value(self, value):
        if value and self.max and self.is_running:
            if 0 < value < self.max:
                self.elm.setAttribute('value', value)
        else:
            self.elm.removeAttribute('value')

    @property
    def max(self):
        return self.elm.max

    @max.setter
    def max(self, value):
        if value  or (value > 0):
            self.elm.setAttribute('value', value)
        else:
            self.elm.removeAttribute('value')

    def start(self):
        self.enabled = True
        self._is_running = True

    def stop(self):
        self.enabled = False
        self._is_running = False

