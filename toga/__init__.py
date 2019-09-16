#__pragma__('skip')

from browser import document, window, alert, confirm

#__pragma__('noskip')

from toga.utils import identifier, platform, current_script_path

# from .app import App, MainWindow <- in file
# DocumentApp <- not implement
from toga.components import Command, CommandSet, Group, GROUP_BREAK, SECTION_BREAK
# from toga.documents import Document <- not implement
# from toga.keys import Key <- not implement

# Resources
from toga.colors import hsl, hsla, rgb, rgba
from toga.components import Font
from toga.components import Icon
from toga.components import Image

# Widgets
from toga.widgets.base import Widget

from toga.widgets.box import Box
from toga.widgets.button import Button
from toga.widgets.canvas import Canvas # <- in progress
# from toga.widgets.detailedlist import DetailedList <- not implement
from toga.widgets.imageview import ImageView
from toga.widgets.datepicker import DatePicker
from toga.widgets.label import Label
from toga.widgets.multilinetextinput import MultilineTextInput
from toga.widgets.numberinput import NumberInput
from toga.widgets.optioncontainer import OptionContainer
from toga.widgets.passwordinput import PasswordInput
from toga.widgets.progressbar import ProgressBar
# from toga.widgets.scrollcontainer import ScrollContainer <- not implement
from toga.widgets.selection import Selection
from toga.widgets.slider import Slider
# from .widgets.splitcontainer import SplitContainer <- not implement
from toga.widgets.swicth import Switch
# from toga.widgets.table import Table <- not implement
from toga.widgets.textinput import TextInput
# from toga.widgets.tree import Tree <- not implement
from toga.widgets.webview import WebView
# from .window import Window <- in file

#__pragma__('kwargs')

class Window:

    _WINDOW_CLASS = 'Window'

    def __init__(self, id=None, title=None, position=(100, 100), size=(640, 480), toolbar=None, resizeable=True, closeable=True, minimizable=True, factory=None):
        self._elm = document.createElement('DIV')
        self._title = document.createElement('H1')

        self._id = id if id else identifier()
        self._app = None
        self._content = None
        self._position = position
        self._size = size
        self._is_full_screen = False

        self.resizeable = resizeable
        self.closeable = closeable
        self.minimizable = minimizable

        #self._toolbar = CommandSet(self, self._impl.create_toolbar)

        self.position = position
        self.size = size
        self.title = title

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
        self._elm.id = value

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")
        self._app = app

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if not title:
            title = "Toga"
        self._title.innerHTML = title

    @property
    def toolbar(self):
        return self._toolbar

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        widget.app = self.app
        widget.window = self
        self._content = widget
        widget.refresh()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        self._elm.style.width = size[0]
        self._elm.style.height = size[1]
        if self.content:
            self.content.refresh()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        if isinstance(position, str):
            self._elm.style.position = position
        elif isinstance(position, tuple):
            print("Position fixed")
            self._elm.style.position = 'fixed'
            self._elm.style.bottom = position[0]
            self._elm.style.left = position[1]

    def show(self):
        if self.content:
            self._elm.appendChild(self.content.elm)

    @property
    def full_screen(self):
        return self._is_full_screen

    @full_screen.setter
    def set_full_screen(self, value):
        elem = document.documentElement
        if value:
            if elem.requestFullscreen:
                elem.requestFullscreen()
                self._is_full_screen = True
            elif elem.mozRequestFullScreen:
                elem.mozRequestFullScreen()
                self._is_full_screen = True
            elif elem.webkitRequestFullscreen:
                elem.webkitRequestFullscreen()
                self._is_full_screen = True
            elif elem.msRequestFullscreen:
                elem.msRequestFullscreen()
                self._is_full_screen = True
            else:
                print("Browser ???")
        else:
            if document.exitFullscreen:
                document.exitFullscreen()
                self._is_full_screen = False
            elif document.mozCancelFullScreen:
                document.mozCancelFullScreen()
                self._is_full_screen = False
            elif document.webkitExitFullscreen:
                document.webkitExitFullscreen()
                self._is_full_screen = False
            elif document.msExitFullscreen:
                document.msExitFullscreen()
                self._is_full_screen = False
            else:
                print("Browser ???")

    def close(self):
        self.on_close()
        while self._elm.firstChild:
            self._elm.removeChild(self._elm.firstChild)
        self._elm.innerHTML = ''

    def on_close(self):
        pass

    def info_dialog(self, title, message):
        alert(title+'\n'+message)
        return None

    def question_dialog(self, title, message):
        return confirm(title+'\n'+message)

    def confirm_dialog(self, title, message):
        return confirm(title+'\n'+message)

    def error_dialog(self, title, message):
        alert(title+'\n'+message)
        return None

    def stack_trace_dialog(self, title, message, content, retry=False):
        print('Not implemented. Show to info dialog')
        alert(title+'\n'+message)
        print('title:', title)
        print('message:', message)
        print('content:', content)
        return None

    def save_file_dialog(self, title, suggested_filename, file_types=None):
        print('Not implemented. Use select folder dialog')
        return self.select_folder_dialog(title) + suggested_filename

    def open_file_dialog(self, title, initial_directory=None, file_types=None, multiselect=False):
        inputfile = document.createElement('INPUT')

        inputfile.setAttribute('type', 'file')
        inputfile.setAttribute('multiple', multiselect)
        inputfile.setAttribute('name', title)
        #inputfile.setAttribute('hidden', True)
        inputfile.style="display:none"

        if file_types:
            inputfile.setAttribute('accept', ", ".join(file_types))

        if initial_directory:
            print('Not recomended used')
            inputfile.value = initial_directory

        self._root.appendChild(inputfile)
        inputfile.click()
        self._root.removeChild(inputfile)
        return inputfile.value

    def select_folder_dialog(self, title, initial_directory=None, multiselect=False):
        inputfile = document.createElement('INPUT')

        inputfile.setAttribute('type', 'file')
        inputfile.setAttribute('webkitdirectory', True)
        inputfile.setAttribute('directory', True)
        inputfile.setAttribute('multiple', multiselect)
        inputfile.setAttribute('name', title)
        #inputfile.setAttribute('hidden', True)
        inputfile.style="display:none"

        if initial_directory:
            print('Not recomended used initial directory')
            inputfile.value = initial_directory

        self._root.appendChild(inputfile)
        inputfile.click()
        self._root.removeChild(inputfile)
        return inputfile.value


class MainWindow(Window):

    _WINDOW_CLASS = 'MainWindow'

    def __init__(self, id=None, title=None, position=(100,100), size=(640, 480), factory=None):
        super().__init__(self, id=None, title=None, position=(100,100), size=(640, 480), factory=None)

class App:

    app = None

    def __init__(self, name, app_id, id=None, icon=None, startup=None, on_exit=None, factory=None):
        print('Start...')

        App.app = self
        App.app_module = self.__module__.split('.')[0]
        App.app_dir = current_script_path()

        self.name = name
        self._app_id = str(app_id)
        self._id = id if id else identifier()
        self._icon = None

        self.commands = CommandSet(None)

        self._startup_method = startup

        self.default_icon = Icon('tiberius', system=True)
        self.icon = icon
        self._main_window = None
        self._on_exit = None

        self._full_screen_windows = None

        self.on_exit = on_exit

        self._elm = document.getElementById(self.app_id)

    @property
    def app_id(self):
        return self._app_id

    @property
    def id(self):
        return self._id

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, name):
        self._icon = Icon.load(name, default=self.default_icon)

    @property
    def main_window(self):
        return self._main_window

    @main_window.setter
    def main_window(self, window):
        self._main_window = window
        window.app = self

    @property
    def current_window(self):
        return self.main_window

    @property
    def is_full_screen(self):
        return self._full_screen_windows is not None

    def set_full_screen(self, *windows):
        if not windows:
            self.exit_full_screen()
        else:
            for window in windows:
                window.full_screen = True
            self._full_screen_windows = windows

    def exit_full_screen(self):
        if self.is_full_screen:
            for window in self._full_screen_windows:
                window.full_screen = False
            self._full_screen_windows = None

    def show_cursor(self):
        self._elm.style.cursor = 'auto'

    def hide_cursor(self):
        self._elm.style.cursor = 'none'

    def startup(self):
        self.main_window = MainWindow(title=self.name)

        if self._startup_method:
            self.main_window.content = self._startup_method(self)

        self.main_window.show()

    def main_loop(self):
        self.startup()
        if self.main_window:
            self._elm.appendChild(self.main_window.title)
            self._elm.appendChild(self.main_window._elm)

    def exit(self):
        if self._on_exit:
            self._on_exit(self)
        window.open('','_self','')
        window.close()


#__pragma__('nokwargs')