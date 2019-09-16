#__pragma__('skip')

from browser import document

#__pragma__('noskip')

from toga.utils import identifier
from toga.style import Pack
from toga.style import TogaApplicator

def set_root(node, root):
    node._root = root
    for child in node.children:
        set_root(child, root)

class Widget:

    type_element = "DIV"
    parent = None
    can_have_children = True

    #__pragma__('kwargs')

    def __init__(self, id=None, enabled=True, style=None, factory=None):
        self.elm = document.createElement(self.type_element)

        # --- Node ---
        self.applicator = TogaApplicator(self)
        self.style = style if style else Pack().copy(self.applicator)
        self.intrinsic = self.style.IntrinsicSize()
        self.layout = self.style.Box(self)

        if style != None:
            self.elm.style = style
        self.style = self.elm.style

        self._parent = None
        self._root = None
        self.enabled = enabled
        self._children = [] #None

        # --- Widget ---

        self.id = id if id else identifier(self)
        self._window = None
        self._app = None

    def __repr__(self):
        return "<"+str(self.__name__)+":"+identifier(self)+">"

    def __str__(self):
        return "<"+str(self.__name__)+":"+identifier(self)+">"


    def add(self, *children):
        if self._children == None:
            raise ValueError('Cannot add children')

        if self.can_have_children:
            for child in children:

                child.app = self.app

                # --- revisar ---
                child.parent = self
                child.root = self.root
                child.window = self.window

                self.children.append(child)
                self.elm.appendChild(child.elm)
        else:
            raise NotImplementedError("Can not have children")

    @property
    def root(self):
        return self._root if self._root else self

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        if self._children is None:
            return []
        else:
            return self._children

    @property
    def can_have_children(self):
        return self._children != None
    

    @property
    def id(self):
        return self.elm.id

    @id.setter
    def id(self, id):
        self.elm.id = id

    @property
    def app(self):
        return self._app
    
    @app.setter
    def app(self, app):
        if self._app != None:
            if self._app != app:
                raise ValueError("Widget %s is already associated with an App" % self)
        elif app != None:
            self._app = app
            if self._children != None:
                for child in self._children:
                    child.app = app

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, window):
        self._window = window
        if self._children != None:
            for child in self._children:
                child.window = window

    @property
    def enabled(self):
        return False if self.elm.disabled else True
    
    @enabled.setter
    def enabled(self, value):
        if value:
            self.elm.removeAttribute('disabled')
        else:
            self.elm.setAttribute('disabled', True)
    
    def set_bounds(self, *args):
        pass

    #__pragma__('nokwargs')

    def refresh(self):
        if self._root:
            self._root.refresh()
        else:
            # --- super().refresh(self._impl.viewport) ---
            self.refresh_sublayouts()

    def refresh_sublayouts(self):
        """
        for widget in self.children:
            widget.refresh()
        """
        if self._children != None:
            for child in self._children:
                child.refresh_sublayouts()

    def set_alignment(self, alignment):
        self.elm.style

    def set_hidden(self, hidden):
        self.elm.style.display = 'auto'
        if hidden:
            self.elm.style.display = hidden

    def set_font(self, font):
        self.elm.style

    def set_color(self, color):
        self.elm.style

    def set_background_color(self, color):
        self.elm.style