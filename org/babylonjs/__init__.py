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
    if necessary, use kwargs to choose the native function that
    becomes a magic method
    '''
    obj.prototype['__add__'] = obj.prototype[add]
    obj.prototype['__sub__'] = obj.prototype[subtract]
    obj.prototype['__mul__'] = obj.prototype[multiply]
    obj.prototype['__div__'] = obj.prototype[divide]

    base = _js_class(obj)
    return base

__pragma__('nokwargs')

console.time("babylonjs loaded")
__pragma__('js', '{}' , __include__('org/babylonjs/__javascript__/babylon.custom.js'))
console.timeEnd("babylonjs loaded")


console.time("api initialized");

def _promote(member):  
    """
    apply wrappers to js_classes where appropriate
    """
    MATH_CLASSES = (
    'Vector3',
    'Vector4',
    'Color3',
    'Color4',
    'Matrix',
    'Quaternion'
    )

    if member not in MATH_CLASSES \
        and member.hasOwnProperty('prototype') \
        and member.prototype.hasOwnProperty('constructor'):
        if member.prototype.hasOwnProperty('multiply'):
            return _js_math_class(member)
        return _js_class(member)
    return member

__pragma__('jsiter')
for k in BABYLON:
    __all__[k] = _promote(BABYLON[k])
#api = {k: _promote(BABYLON[k]) for k in BABYLON}
__pragma__('nojsiter')


console.timeEnd("api initialized")