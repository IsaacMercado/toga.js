from toga.widgets.base import Widget

class Label(Widget):

    type_element = 'DIV'
    can_have_children = False

    #__pragma__('kwargs')

    def __init__(self, text, id=None, style=None, factory=None):
        super().__init__(self, id=id, style=style, enabled=True, factory=factory)
        self.text = text

    #__pragma__('nokwargs')

    @property
    def text(self):
        return self.elm.innerHTML

    @text.setter
    def set_text(self, text):
        if value:
            self.elm.innerHTML = text
        else:
            self.elm.innerHTML = ''
