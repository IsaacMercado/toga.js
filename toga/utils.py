
#__pragma__('skip')

from browser import navigator

#__pragma__('noskip')

from random import randint

def identifier(obj=None,length=6, pre='id_', suf='toga'):
    id_code = pre
    if obj:
    	id_code += str(obj.__name__).lower()
    for i in range(length):
        id_code += str(randint(0, 9))
    id_code += suf
    return id_code

def platform():
	return str(navigator.platform)

def current_script_path():
    path = list(document.querySelectorAll('script[src]')).pop().src.split('/')
    return '/'.join(path[:len(path)-1])