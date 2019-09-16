import re


NON_ACCESSOR_CHARS = re.compile('[^\w ]')
WHITESPACE = re.compile('\s+')

def to_accessor(heading):

    value = WHITESPACE.sub(
        ' ',
        NON_ACCESSOR_CHARS.sub('', heading.lower()),
    ).replace(' ', '_')

    if len(value) == 0 or value[0].isdigit():
        raise ValueError("Unable to automatically generate accessor from heading '{}'.".format(heading))

    return value

def build_accessors(headings, accessors):

    if accessors:
        if isinstance(accessors, dict):
            result = [
                accessors[h] if h in accessors else to_accessor(h)
                for h in headings
            ]
        else:
            if len(headings) != len(accessors):
                raise ValueError('Number of accessors must match number of headings')

            result = [
                a if a is not None else to_accessor(h)
                for h, a in zip(headings, accessors)
            ]
    else:
        result = [to_accessor(h) for h in headings]

    if len(result) != len(set(result)):
        raise ValueError('Data accessors are not unique.')

    return result

class Source:
    def __init__(self):
        self._listeners = []

    @property
    def listeners(self) -> list:
        return self._listeners

    def add_listener(self, listener):
        self._listeners.append(listener)

    def remove_listener(self, listener):
        self._listeners.remove(listener)

    #__pragma__('kwargs')

    def _notify(self, notification, **kwargs):
        for listener in self._listeners:
            try:
                method = getattr(listener, notification)
            except AttributeError:
                method = None

            if method:
                method(**kwargs)

    #__pragma__('nokwargs')



class Row:
    def __init__(self, **data):
        self._attrs = list(data.keys())
        self._source = None
        for name, value in data.items():
            setattr(self, name, value)

    # --- Utility wrappers ---

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        if attr in self._attrs:
            if self._source is not None:
                self._source._notify('change', item=self)


class ListSource(Source):

    def __init__(self, data, accessors):
        super().__init__()
        self._accessors = accessors
        self._data = []
        for value in data:
            self._data.append(self._create_row(value))

    # --- Methods required by the ListSource interface ---

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    # --- Factory methods for new rows ---

    def _create_row(self, data):

        if isinstance(data, dict):
            row = Row(**data)
        elif hasattr(data, '__iter__') and not isinstance(data, str):
            row = Row(**dict(zip(self._accessors, data)))
        else:
            row = Row(**{self._accessors[0]: data})
        row._source = self
        return row

    # --- Utility methods to make ListSources more list-like ---

    def __setitem__(self, index, value):
        row = self._create_row(value)
        self._data[index] = row
        self._notify('insert', index=index, item=row)

    def __iter__(self):
        return iter(self._data)

    def clear(self):
        self._data = []
        self._notify('clear')

    #__pragma__('kwargs')

    def insert(self, index, *values, **named):
        row = self._create_row(dict(zip(self._accessors, values), **named))
        self._data.insert(index, row)
        self._notify('insert', index=index, item=row)
        return row

    def prepend(self, *values, **named):
        return self.insert(0, *values, **named)

    def append(self, *values, **named):
        return self.insert(len(self), *values, **named)

    #__pragma__('nokwargs')

    def remove(self, row):
        self._data.remove(row)
        self._notify('remove', item=row)
        return row

    def index(self, row):
        return self._data.index(row)



class Node(Row):

    #__pragma__('kwargs')

    def __init__(self, **data):
        super().__init__(**data)
        self._children = None
        self._parent = None

    #__pragma__('nokwargs')

    # --- Methods required by the TreeSource interface ---

    def __getitem__(self, index):
        return self._children[index]

    def __len__(self):
        if self.can_have_children():
            return len(self._children)
        else:
            return 0

    def can_have_children(self):
        return self._children is not None

    # --- Utility methods to make TreeSource more dict-like ---

    def __iter__(self):
        return iter(self._children or [])

    def __setitem__(self, index, value):
        node = self._source._create_node(value)
        self._children[index] = node
        self._source._notify('change', item=node)

    #__pragma__('kwargs')

    def insert(self, index, *values, **named):
        self._source.insert(self, index, *values, **named)

    def prepend(self, *values, **named):
        self._source.prepend(self, *values, **named)

    def append(self, *values, **named):
        self._source.append(self, *values, **named)

    #__pragma__('nokwargs')

    def remove(self, node):
        self._source.remove(self, node)


class TreeSource(Source):
    def __init__(self, data, accessors):
        super().__init__()
        self._accessors = accessors
        self._roots = self._create_nodes(data)

    # --- Methods required by the TreeSource interface ---

    def __len__(self):
        return len(self._roots)

    def __getitem__(self, index):
        return self._roots[index]

    # --- Factory methods for new nodes ---

    #__pragma__('kwargs')

    def _create_node(self, data, children=None):
        if isinstance(data, dict):
            node = Node(**data)
        else:
            node = Node(**dict(zip(self._accessors, data)))

        node._source = self

        if children is not None:
            node._children = []
            for child_node in self._create_nodes(children):
                node._children.append(child_node)
                child_node._parent = node
                child_node._source = self

        return node

    #__pragma__('nokwargs')

    def _create_nodes(self, data):
        if isinstance(data, dict):
            return [
                self._create_node(value, children)
                for value, children in sorted(data.items())
            ]
        else:
            return [
                self._create_node(value)
                for value in data
            ]

    # --- Utility methods to make TreeSources more dict-like ---

    def __setitem__(self, index, value):
        root = self._create_node(value)
        self._roots[index] = root
        self._notify('change', item=root)

    def __iter__(self):
        return iter(self._roots)

    #__pragma__('kwargs')

    def insert(self, parent, index, *values, **named):
        node = self._create_node(dict(zip(self._accessors, values), **named))

        if parent is None:
            self._roots.insert(index, node)
        else:
            if parent._children is None:
                parent._children = []
            parent._children.insert(index, node)

        node._parent = parent
        self._notify('insert', parent=parent, index=index, item=node)
        return node

    def prepend(self, parent, *values, **named):
        return self.insert(parent, 0, *values, **named)

    def append(self, parent, *values, **named):
        return self.insert(parent, len(parent or self), *values, **named)

    #__pragma__('nokwargs')

    def remove(self, node):
        if node._parent is None:
            self._roots.remove(node)
        else:
            node._parent._children.remove(node)

        self._notify('remove', item=node)
        return node

    def index(self, node):
        if node._parent:
            return node._parent._children.index(node)
        else:
            return self._roots.index(node)

class ValueSource(Source):
    def __init__(self, value=None):
        self._source = None
        self.value = value

    def __str__(self):
        if self.value is None:
            return ''
        return str(self.value)

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        if not attr.startswith('_'):
            if self._source is not None:
                self._source._notify('change', item=self)
