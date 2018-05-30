import logging
from org.transcrypt.stubs.browser import JSON, XMLHttpRequest, __new__
from org.babylonjs.api import ShaderMaterial, AssetsManager
logger = logging.getLogger(__name__)

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
        self.loader = AssetsManager(scene)
        self.loader.useDefaultLoadingScreen = False

        def loaderui(remainingCount, totalCount, lastFinishedTask):
            self.scene.getEngine().loadingUIText = 'loading {}/{}'.format(remainingCount, totalCount)

        self.loader.onProgress = loaderui

        self.shaders = {}

    def request(self, relpath):
        fullpath = self.root + relpath
        shaderfile = fullpath + ".shader"
        logger.debug("requesting {}".format(shaderfile))

        engine = self.scene.getEngine()

        def handle_result(task):
            descriptor = JSON.parse(task.text)
            shader_name = descriptor.name
            del descriptor.name
            mtl = ShaderMaterial(shader_name, self.scene, fullpath, descriptor)
            logger.debug("retrieved shader descriptor '{}'".format(descriptor.js_name))
            self.shaders[shader_name] = mtl

        def handle_err(task, message, exception):
            logger.warning(message, exception)

        task = self.loader.addTextFileTask(fullpath, shaderfile)
        task.onSuccess = handle_result
        task.onError = handle_err
        return task

    