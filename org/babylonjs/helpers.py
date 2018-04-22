from org.transcrypt.stubs.browser import __pragma__
from org.babylonjs.api import ShaderMaterial
import logging
logger = logging.getLogger(__name__)


__pragma__('kwargs')


def create_shader(path, scene, **kwargs):
    shadername = kwargs.get('name') or path.split("/")[-1]  # __: opov
    return ShaderMaterial(shadername, scene, path, kwargs)


__pragma__('nokwargs')
