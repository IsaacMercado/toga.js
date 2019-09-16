#__pragma__('skip')

from browser import document

#__pragma__('noskip')

from toga.widgets.base import Widget

class Switch(Widget):

	type_element = 'LABEL'
	can_have_children = False

	#__pragma__('kwargs')

	def __init__(self, label, id=None, style=None, on_toggle=None, is_on=False, enabled=True, factory=None):
		super().__init__(self, id=id, style=style, enabled=enabled, factory=factory)

		self.checkbox = document.createElement('INPUT')
		self.checkbox.setAttribute('type','checkbox')

		self.label = label
		self.on_toggle = on_toggle
		self.is_on = is_on
		self.enabled = enabled

	#__pragma__('nokwargs')

	@property
	def label(self):
		return self.elm.innerHTML

	@label.setter
	def label(self, text):
		while self.elm.firstChild:
			self.elm.removeChild(self.elm.firstChild)
		if text:
			self.elm.innerHTML = text
		else:
			self.elm.innerHTML = ''
		self.elm.appendChild(self.checkbox)

	@property
	def is_on(self):
		return self.checkbox.checked

	@is_on.setter
	def set_is_on(self, value):
		self.checkbox.checked = value

	@property
	def on_toggle(self):
		return self._on_toggle
	
	@on_toggle.setter
	def on_toggle(self, fun):
		self._on_toggle = fun
		if fun:
			self.checkbox.onclick = lambda evt: self.on_toggle(self)
		else:
			self.checkbox.onclick = None
