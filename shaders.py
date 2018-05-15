import logging
logger = logging.getLogger('__name__')
from org.transcrypt.stubs.browser import JSON, XMLHttpRequest
from org.babylonjs.api import ShaderMaterial

# constants to avoid typ
POSITION = 'position'
NORMAL = 'normal'
UV = 'uv'
WORLD = 'world'
WORLDVIEW = 'worldView'
WVP = 'worldViewProjection'
VIEW = 'view'
PROJECTION = 'projection'


class ShaderAttributes:
    def __init__(self, attribs, uniforms):
        self.attributes = attribs
        self.uniforms = uniforms


DEFAULT = ShaderAttributes(
    [POSITION, NORMAL, UV],
    [WORLD, WORLDVIEW, WVP, VIEW, PROJECTION]
)


class ShaderLoader:

    def __init__(self, scene, root="./src/shaders/"):
        self.scene = scene
        self.root = root

    def load_async(self, relpath):
        fullpath = self.root + relpath
        shaderfile = fullpath + ".shader"
        logger.debug("requesting {}".format(shaderfile))

        def sender(resolve, reject):

            xobj = __new__(XMLHttpRequest())
            xobj.overrideMimeType("application/json")
            xobj.open('GET', shaderfile, True)

            def handle_result():
                descriptor = JSON.parse(xobj.responseText)
                shader_name = descriptor.name
                del descriptor.name
                mtl = ShaderMaterial(shader_name, self.scene, fullpath, descriptor)
                def shader_result(target):
                    target.material = mtl
                shader_result.material = mtl
                resolve(shader_result)
                
            def handle_err():
                reject(xob.responseText)

            xobj.onload = handle_result
            xobj.onerror = handle_err

            xobj.send(None)

        return __new__(Promise(sender))

