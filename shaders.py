import logging
from org.transcrypt.stubs.browser import JSON
from org.babylonjs.api import ShaderMaterial
from org.babylonjs.assets import AssetTask
logger = logging.getLogger(__name__)

# constants to avoid typos
POSITION = 'position'
NORMAL = 'normal'
UV = 'uv'
WORLD = 'world'
WORLDVIEW = 'worldView'
WVP = 'worldViewProjection'
VIEW = 'view'
PROJECTION = 'projection'


class ShaderAttributes:
    def __init__(self,
                 attribs=(POSITION, NORMAL, UV),
                 uniforms=(WORLD, WORLDVIEW, WVP, VIEW, PROJECTION)
                 ):
        self.attributes = attribs
        self.uniforms = uniforms


class ShaderTask(AssetTask):

    def __init__(self, name, url, *_):
        super().__init__(name, url, *_)
        self.shader = None

    def succeeded(self, scene, data):
        descriptor = JSON.parse(data)
        mtl = ShaderMaterial(self.name, scene, self.url.replace(".shader", ""), descriptor)
        self.shader = mtl
        logger.debug('loaded: ' + self.url)


ShaderTask.register()

