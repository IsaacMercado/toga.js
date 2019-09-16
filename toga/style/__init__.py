
from toga.style.pack import Pack

class TogaApplicator:
    def __init__(self, widget):
        self.widget = widget

    def set_bounds(self):
        self.widget.set_bounds(
            self.widget.layout.absolute_content_left, self.widget.layout.absolute_content_top,
            self.widget.layout.content_width, self.widget.layout.content_height
        )
        for child in self.widget.children:
            if child.applicator:
                child.applicator.set_bounds()

    def set_text_alignment(self, alignment):
        self.widget.set_alignment(alignment)

    def set_hidden(self, hidden):
        self.widget.set_hidden(hidden)

    def set_font(self, font):
        self.widget.set_font(font)

    def set_color(self, color):
        self.widget.set_color(color)

    def set_background_color(self, color):
        self.widget.set_background_color(color)
