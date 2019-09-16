#__pragma__('skip')

from browser import document

#__pragma__('noskip')

from toga.widgets.base import Widget

class WebView(Widget):

    type_element = 'IFRAME'
    can_have_children = False
    MIN_HEIGHT = 100
    MIN_WIDTH = 100

    #__pragma__('kwargs')

    def __init__(self, id=None, style=None, factory=None, url=None, user_agent=None, on_key_down=None, on_webview_load=None):
        super().__init__(self, id=id, style=style, factory=factory)
        self.elm.className = "embed-responsive"

        self.url = url
        self.user_agent = user_agent
        self.on_key_down = on_key_down
        self.on_webview_load = on_webview_load

        self._user_agent = None

    #__pragma__('nokwargs')

    @property
    def url(self):
        return self.elm.src

    @url.setter
    def set_url(self, new_url):
        self.elm.setAttribute('src', new_url)

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def set_user_agent(self, value):
        if value and self.elm.contentWindow:
            if self.elm.contentWindow.__defineGetter__:
                self.elm.contentWindow.__defineGetter__('userAgent', lambda:value)
            else:
                self.elm.contentWindow.defineProperty('userAgent', {'get': (lambda:value)})
        self._user_agent = value

    @property
    def dom(self):
        return self.elm.contentDocument

    @property
    def on_webview_load(self):
        return self.elm.onload

    @on_webview_load.setter
    def set_on_webview_load(self, value):
        def onload():
            if value:
                value(self)
            self.user_agent = self._user_agent
        self.elm.onload = onload

    @property
    def on_key_down(self):
        return self._set_on_key_down

    @on_key_down.setter
    def set_on_key_down(self, value):
        self._set_on_key_down = value
        if value:
            self.elm.onkeydown = lambda evt: self.on_key_down(self)
        else:
            self.elm.onkeydown = None

    def set_content(self, root_url, content):
        self.url = root_url
        print("WebView. N")

    def evaluate_javascript(self, javascript):
        print('Not recomended use function. Return promise.')
        async_eval = eval("(async () => {"+javascript+"})")
        promise = async_eval()
        return promise


    def invoke_javascript(self, javascript):
        print('Not recomended use function')
        eval(javascript)

