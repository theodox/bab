__pragma__('noanno')


def _js_class(obj):
    '''
    Add python-style constructor, but preserve static methods from the original class
    '''
    def _c_(*args):
        return __new__(obj(*args))

    # allows for 'static' functions too
    Object.setPrototypeOf(_c_, obj)

    obj['__str__'] = object.toString
    return _c_

__pragma__('kwargs')

def _js_math_class(obj, add ='add', subtract ='subtract', multiply ='multiply', divide ='divide'):
    '''
    Add python constructor and python magic methods for operator overloading
    '''
    obj.prototype['__add__'] = obj.prototype[add]
    obj.prototype['__sub__'] = obj.prototype[subtract]
    obj.prototype['__mul__'] = obj.prototype[multiply]
    obj.prototype['__div__'] = obj.prototype[divide]

    base = _js_class(obj)
    return base

__pragma__('nokwargs')

__pragma__('js', '{}' , __include__('org/babylonjs/__javascript__/babylon.custom.js'))

