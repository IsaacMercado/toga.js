from toga.widgets.base import Widget
import datetime


class DatePicker(Widget):

    MIN_WIDTH = 200
    type_element = 'INPUT'
    can_have_children = False

    def __init__(self, id=None, style=None, factory=None, initial=None, min_date=None, max_date=None, on_change=None):
        super().__init__(id=id, style=style, factory=factory)
        self.elm.setAttribute('type','date')
        self.elm.className = "form-control"

        self.value = initial
        self.min_date = min_date
        self.max_date = max_date
        self.on_change = on_change

    @property
    def value(self):
        return self.elm.value

    @value.setter
    def value(self, value):
        if value:
            self.elm.value = str(value)
        else:
            self.elm.value = str(datetime.date.today())

    @property
    def min_date(self):
        return self.elm.min

    @min_date.setter
    def min_date(self, value):
        if value:
            self.elm.min = None
        else:
            self.elm.min = str(value)

    @property
    def max_date(self):
        return self.elm.max

    @max_date.setter
    def max_date(self, value):
        if value:
            self.elm.max = None
        else:
            self.elm.max = str(value)

    @property
    def on_change(self):
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = handler
        if handler:
            self.elm.onchange = None
        else:
            self.elm.onchange = lambda evt: self.on_change(self)

