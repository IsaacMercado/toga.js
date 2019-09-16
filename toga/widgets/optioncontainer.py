#__pragma__('skip')

from browser import document

#__pragma__('noskip')

from toga.widgets.base import Widget
from toga.utils import identifier


class OptionContainer(Widget):

    #__pragma__('kwargs')

    def __init__(self, id=None, style=None, content=None, on_select=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        self._div_bar_nav = document.createElement('DIV')
        self._div_bar_nav.className = "nav nav-tabs"
        self._div_bar_nav.setAttribute('role','tablist')

        self._bar_nav = document.createElement('NAV')
        self._bar_nav.appendChild(self._div_bar_nav)

        self._div_windows = document.createElement('DIV')
        self._div_windows.className = "tab-content"

        self.elm.appendChild(self._bar_nav)
        self.elm.appendChild(self._div_windows)

        self.on_select = on_select

        self._content = []
        self.initial = True
        if content:
            for label, widget in content:
                self.add(label, widget)

    #__pragma__('nokwargs')

    @property
    def content(self):
        return self._content

    #__pragma__('kwargs')

    def add(self, label, widget):

        if self._children == None:
            raise ValueError('Cannot add children')

        widget.app = self.app

        # --- revisar ---
        widget.parent = self
        widget.root = self.root
        widget.window = self.window
        self.children.append(widget)

        # --- New ---

        self._content.append(widget)

        new_window = document.createElement('DIV')
        new_window.id = identifier()

        new_href = document.createElement('A')
        new_href.id = identifier()

        if self.initial:
            new_href.className = "nav-item nav-link active"
            new_href.setAttribute('aria-selected', True)

            new_window.className = "tab-pane fade show active"
        else:
            new_href.className = "nav-item nav-link"
            new_href.setAttribute('aria-selected', False)

            new_window.className = "tab-pane fade"

        new_href.innerHTML = label
        new_href.href = "#" + new_window.id
        new_href.setAttribute('data-toggle','tab')
        new_href.setAttribute('role','tab')
        new_href.setAttribute('aria-controls', new_window.id)

        new_window.setAttribute('role','tabpanel')
        new_window.setAttribute('aria-labelledby', new_href.id)
        new_window.appendChild(widget.elm)

        self._div_windows.appendChild(new_window)
        self._div_bar_nav.appendChild(new_href)

        self.initial = False
        widget.refresh()

    #__pragma__('nokwargs')

    def refresh_sublayouts(self):
        for widget in self._content:
            widget.refresh()

    @property
    def on_select(self):
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        self._on_select = handler
        if handler:
            self._bar_nav.onclick = lambda evt: self.on_select(self)
        else:
            self._bar_nav.onclick = None
