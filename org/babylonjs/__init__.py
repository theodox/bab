__pragma__('noanno')


def _cls(obj):
    def _c_(*args):
        return __new__(obj(*args))

    # allows for 'static' functions too
    Object.setPrototypeOf(_c_, obj)

    obj['__str__'] = object.toString
    return _c_


__pragma__('js',
           '''(function () {{
           var exports = {{}};
           {} 
           return exports;
       }}) () .fabric;''', __include__('org/babylonjs/__javascript__/babylon.custom.js'))

Engine = _cls(BABYLON.Engine)
Scene = _cls(BABYLON.Scene)
Camera = _cls(BABYLON.Camera)
ArcRotateCamera = _cls(BABYLON.ArcRotateCamera)
HemisphericLight = _cls(BABYLON.HemisphericLight)
PointLight = _cls(BABYLON.PointLight)
MeshBuilder = BABYLON.MeshBuilder
Plane = _cls(BABYLON.Plane)
Vector3 = _cls(BABYLON.Vector3)

BABYLON.Vector3.prototype['__add__'] = BABYLON.Vector3.prototype.add
BABYLON.Vector3.prototype['__iadd__'] = BABYLON.Vector3.prototype.addInPlace
BABYLON.Vector3.prototype['__sub__'] = BABYLON.Vector3.prototype.subtract
BABYLON.Vector3.prototype['__isub__'] = BABYLON.Vector3.prototype.subtractInPlace
BABYLON.Vector3.prototype['__mul__'] = BABYLON.Vector3.prototype.multiply
BABYLON.Vector3.prototype['__imul__'] = BABYLON.Vector3.prototype.multiplyInPlace
BABYLON.Vector3.prototype['__div__'] = BABYLON.Vector3.prototype.divide
BABYLON.Vector3.prototype['__idiv__'] = BABYLON.Vector3.prototype.divideInPlace
