import bootstrap
import org.babylonjs.api as api
import org.babylonjs.globals as babylon
from org.transcrypt.stubs.browser import __pragma__
import logging
logger = logging.getLogger(__name__)

__pragma__('alias', 'babylon_aliases')

engine = babylon.create_engine()
stage = babylon.create_scene()
babylon.activate_scene(stage)

camera = api.FreeCamera("camera1", api.Vector3(0, 5, -10))
stage.add_camera(camera)
camera.attach_control(babylon.get_canvas())
api.MeshBuilder.create_plane("plane", stage, size=4, plane=api.Plane(0, -1, 0, 0))
hlight = api.HemisphericLight('light1', api.Vector3(0, -1, 0))
stage.add_light(hlight)

__pragma__('noalias', 'babylon_aliases')
