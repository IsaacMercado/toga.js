from toga.widgets.base import Widget

class ImageView(Widget):

    type_element = 'IMG'
    can_have_children = False

    #__pragma__('kwargs')

    def __init__(self, image=None, id=None, style=None, factory=None):
        super().__init__(self, id=id, style=style, enabled=True, factory=factory)
        self.elm.className = "img-fluid"
        self.image = image

    #__pragma__('nokwargs')

    @property
    def image(self):
        return self._image
    
    @image.setter
    def set_image(self, new_image):
        self._image = new_image
        self.elm.src = new_image.path