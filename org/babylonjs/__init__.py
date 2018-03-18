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

Engine = _js_class(BABYLON.Engine)
Scene = _js_class(BABYLON.Scene)
Camera = _js_class(BABYLON.Camera)

class cameras:
    ArcRotateCamera = _js_class(BABYLON.ArcRotateCamera)

class lights:
    HemisphericLight = _js_class(BABYLON.HemisphericLight)
    PointLight = _js_class(BABYLON.PointLight)
MeshBuilder = BABYLON.MeshBuilder
Plane = _js_class(BABYLON.Plane)

# math classes use _opov_cls
Vector3 = _js_math_class(BABYLON.Vector3)

