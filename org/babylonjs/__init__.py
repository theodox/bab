VERSION = 3,1  # this code is tested agains this Babylon release

__pragma__('noanno')

def _js_class(api_object):
    '''
    Add python-style constructor, but preserve static methods from the original class
    '''
    def BabylonAPIObject(*args):
        return __new__(api_object(*args))

    # allows for 'static' functions too
    Object.setPrototypeOf(BabylonAPIObject, api_object)
    api_object['__str__'] = api_object.toString
    return BabylonAPIObject

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
# load the Babylonjs module
__pragma__('js', '{}' , __include__('org/babylonjs/__javascript__/babylon.custom.js'))
console.timeEnd("babylonjs loaded")


console.time("api initialized");
# wrap api classes where useful, promote to 
# the __all__ namespace of this so they look like
# memberts for import
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

    if member.hasOwnProperty('prototype') and member.prototype.hasOwnProperty('constructor'):
        if member.prototype.hasOwnProperty('multiply'):
            # return with magic methods for fast operator overload
            return _js_math_class(member)

        # return wrapped with a python constructor
        return _js_class(member)

    # this is something like a constant or static class
    # return unwrapped
    return member

__pragma__('jsiter')
for _k in BABYLON:
    if not _k.startswith("_"):
        __all__[_k] = _promote(BABYLON[_k])
__pragma__('nojsiter')


console.timeEnd("api initialized")
