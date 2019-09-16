#__pragma__('skip')

from browser import document

#__pragma__('noskip')

from toga.widgets.base import Widget

class Canvas(Widget):
    type_element = 'CANVAS'
    can_have_children = False

    #__pragma__('kwargs')

    def arc(self, x, y, radius, startangle=0.0, endangle=6.283185307179586, anticlockwise=False):
        raise NotImplementedError

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        raise NotImplementedError

    def context(self):
        raise NotImplementedError

    #__pragma__('nokwargs')