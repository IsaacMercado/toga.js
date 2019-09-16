from toga.constants import (
    NORMAL, FONT_STYLES, FONT_VARIANTS, FONT_WEIGHTS, 
    SYSTEM, MESSAGE,
    SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE,
    ITALIC, OBLIQUE,
    SMALL_CAPS,
    BOLD,
)

#__pragma__('kwargs')

class Font:
    def __init__(self, family, size, style=NORMAL, variant=NORMAL, weight=NORMAL):
        if (family[0] == "'" and family[-1] == "'") or (family[0] == '"' and family[-1] == '"'):
            self.family = family[1:-1]
        else:
            self.family = family

        try:
            self.size = int(size)
        except ValueError:
            try:
                if size.strip().endswith('pt'):
                    self.size = int(size[:-2])
                else:
                    raise ValueError("Invalid font size {!r}".format(size))
            except:
                raise ValueError("Invalid font size {!r}".format(size))
        self.style = style if style in FONT_STYLES else NORMAL
        self.variant = variant if variant in FONT_VARIANTS else NORMAL
        self.weight = weight if weight in FONT_WEIGHTS else NORMAL

    def __hash__(self):
        return hash(('FONT', self.family, self.size, self.style, self.variant, self.weight))

    def __repr__(self):
        return '<Font: {}{}{}{}pt {}>'.format(
            '' if self.style is NORMAL else (self.style + ' '),
            '' if self.variant is NORMAL else (self.variant + ' '),
            '' if self.weight is NORMAL else (self.weight + ' '),
            self.size,
            self.family
        )

    def __eq__(self, other):
        return (
            self.family == other.family
            and self.size == other.size
            and self.style == other.style
            and self.variant == other.variant
            and self.weight == other.weight
        )

    def normal_style(self):
        return Font(self.family, self.size, style=NORMAL, variant=self.variant, weight=self.weight)

    def italic(self):
        return Font(self.family, self.size, style=ITALIC, variant=self.variant, weight=self.weight)

    def oblique(self):
        return Font(self.family, self.size, style=OBLIQUE, variant=self.variant, weight=self.weight)

    def normal_variant(self):
        return Font(self.family, self.size, style=self.style, variant=NORMAL, weight=self.weight)

    def small_caps(self):
        return Font(self.family, self.size, style=self.style, variant=SMALL_CAPS, weight=self.weight)

    def normal_weight(self):
        return Font(self.family, self.size, style=self.style, variant=self.variant, weight=NORMAL)

    def bold(self):
        return Font(self.family, self.size, style=self.style, variant=self.variant, weight=BOLD)

    def measure(self, text, tight=False):
        print('Font. Not good implemented')
        return len(text)

#__pragma__('nokwargs')


def font(value):

    if isinstance(value, Font):
        return value

    elif isinstance(value, str):
        parts = value.split(' ')

        style = None
        variant = None
        weight = None
        size = None

        while size is None:
            part = parts.pop(0)
            if part == NORMAL:
                if style is None:
                    style = NORMAL
                elif variant is None:
                    variant = NORMAL
                elif weight is None:
                    weight = NORMAL
            elif part in FONT_STYLES:
                if style is not None:
                    raise ValueError("Invalid font declaration '{}'".format(value))
                style = part
            elif part in FONT_VARIANTS:
                if variant is not None:
                    raise ValueError("Invalid font declaration '{}'".format(value))
                if style is None:
                     style = NORMAL
                variant = part
            elif part in FONT_WEIGHTS:
                if weight is not None:
                    raise ValueError("Invalid font declaration '{}'".format(value))
                if style is None:
                     style = NORMAL
                if variant is None:
                     variant = NORMAL
                weight = part
            else:
                try:
                    if part.endswith('pt'):
                        size = int(part[:-2])
                    else:
                        size = int(part)
                except ValueError:
                    raise ValueError("Invalid size in font declaration '{}'".format(value))

                if parts[0] == 'pt':
                    parts.pop(0)

        family = ' '.join(parts)
        return Font(family, size, style=style, variant=variant, weight=weight)

    raise ValueError("Unknown font '%s'" % value)



#__pragma__('kwargs')

class Image:
    def __init__(self, path, factory=None):
        self.path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        print('Image. Not good implemented')
        self._path = path
        # --- loag_image ---


class ClassProperty(type, property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

class Icon:

    def __init__(self, path, system=False):
        self.path = path
        self.system = system

    @property
    def filename(self):
        if self.system:
            from toga import resources
            return resources.data[self.path]
        else:
            return self.path

    @classmethod
    def load(cls, path_or_icon, default=None):
        if path_or_icon:
            if isinstance(path_or_icon, Icon):
                obj = path_or_icon
            else:
                obj = cls(path_or_icon)
        elif default:
            obj = default
        return obj

    @ClassProperty
    @classmethod
    def TIBERIUS_ICON(cls):
        return cls('tiberius-32', system=True)


class Group:
    def __init__(self, label, order=None):
        self.label = label
        self.order = order if order else 0

    def __lt__(self, other):
        return (
            self.order < other.order
            or self.order == other.order and self.label < other.label
        )

    def __eq__(self, other):
        return self.order == other.order and self.label == other.label

Group.APP = Group('*', order=0)
Group.FILE = Group('File', order=1)
Group.EDIT = Group('Edit', order=10)
Group.VIEW = Group('View', order=20)
Group.COMMANDS = Group('Commands', order=30)
Group.WINDOW = Group('Window', order=90)
Group.HELP = Group('Help', order=100)

class Command:

    def __init__(self, action, label,
                 shortcut=None, tooltip=None, icon=None,
                 group=None, section=None, order=None, factory=None):
        self.action = None # --- wrapped_handler(self, action) ---
        self.label = label

        self.shortcut = shortcut
        self.tooltip = tooltip
        self.icon_id = icon

        self.group = group if group else Group.COMMANDS
        self.section = section if section else 0
        self.order = order if order else 0

        self._enabled = self.action is not None

        self._widgets = []
        self._impl = None

    def bind(self, factory):
        if self._impl is None:
            self._impl = factory.Command(interface=self)
        return self._impl

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        for widget in self._widgets:
            widget.enabled = value
        if self._impl is not None:
            self._impl.enabled = value


class NewObject(object):
    pass

GROUP_BREAK = NewObject()
SECTION_BREAK = NewObject()


def cmd_sort_key(value):
    return (value.group, value.section, value.order, value.label)


class CommandSet:

    def __init__(self, widget, on_change=None):

        self.widget = widget
        self._values = set()
        self.on_change = on_change

    def add(self, *values):
        if self.widget and self.widget.app != None:
            self.widget.app.commands.add(*values)
        self._values.update(values)
        if self.on_change:
            self.on_change()

    def __iter__(self):
        prev_cmd = None
        for cmd in sorted(self._values, key=cmd_sort_key):
            if prev_cmd:
                if cmd.group != prev_cmd.group:
                    yield GROUP_BREAK
                elif cmd.section != prev_cmd.section:
                    yield SECTION_BREAK

            yield cmd
            prev_cmd = cmd

#__pragma__('nokwargs')