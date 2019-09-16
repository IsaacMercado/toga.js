from toga.widgets.base import Widget

class Option(Widget):

	type_element = 'OPTION'
	can_have_children = False

	#__pragma__('kwargs')

	def __init__(self, id=None):
		super().__init__(self, id=id)

		self.label = label
		self.value = value

	#__pragma__('nokwargs')

	@property
	def label(self):
		return self.elm.text

	@label.setter
	def label(self, text):
		self.elm.text = text

	@property
	def value(self):
		return self.elm.value

	@value.setter
	def value(self, value):
		self.elm.value = value


class Selection(Widget):

	type_element = 'SELECT'
	MIN_WIDTH = 100

	#__pragma__('kwargs')

	def __init__(self, id=None, style=None, items=None, on_select=None, enabled=True, factory=None):
		super().__init__(self, id=id, style=style, enabled=enabled)
		self.className = "form-control"

		self._items = []
		if items:
			self._items = items
			self._update()

		self.on_select = on_select
		self.enabled = enabled

	#__pragma__('nokwargs')

	def _update(self):
		if self._items:
			while self.elm.firstChild:
				self.elm.removeChild(self.elm.firstChild)
			for text in self._items:
				self.add(Option(label=text, value=text))

	@property
	def items(self):
		return self._items

	@items.setter
	def items(self, items):
		self._items = []
		if items:
			self._items = items
			self._update()

	@property
	def value(self):
		return self.elm.value

	@value.setter
	def value(self, value):
		if value not in self._items:
			raise ValueError("Not an item in the list.")
		self.elm.value = value

	@property
	def on_select(self):
		return self._on_select
	
	@on_select.setter
	def on_select(self, fun):
		self._on_select = fun
		if fun:
			self.elm.onchange = lambda evt: self.on_select(self)
		else:
			self.elm.onchange = None
