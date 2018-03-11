__pragma__ ('noanno')
def _cls(obj, *statics):

	def _c_( *args):
		return __new__(obj, (*args))

	for s in statics:
		_c_[s] = obj[s]
	
	return _c_

# class BabylonBase(type):

# 	def __new__(meta, bases, namespace):
# 		parent_class = namespace.pop('base')
# 		def _c_(self, *args):
# 			self.__instance__ = __new__(parent_class, *args)
# 		namespace['__init__'] = _c_
# 	return type.__new__(meta, bases, namespace)

#https://cdn.babylonjs.com/babylon.js

__pragma__ ('js',
    '{}',
    __include__('org/babylonjs/__javascript__/babylon.custom.js')
)


Engine = _cls(BABYLON.Engine)
Scene = _cls(BABYLON.Scene)
Camera = _cls(BABYLON.Camera)
ArcRotateCamera = _cls(BABYLON.ArcRotateCamera)
HemisphericLight = _cls(BABYLON.HemisphericLight)
PointLight = _cls(BABYLON.PointLight)
Vector3 = _cls(BABYLON.Vector3, 'Zero')
MeshBuilder = BABYLON.MeshBuilder 
Plane = _cls(BABYLON.Plane)
