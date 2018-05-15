import bootstrap
import org.babylonjs.api as api
import org.babylonjs.globals as babylon
from behavior import Tickable, BehaviorMeta
from org.transcrypt.stubs.browser import __pragma__, setTimeout, Promise
from input import KeyAxis, ControlSet
import logging
import math

logger = logging.getLogger(__name__)

__pragma__('alias', 'babylon_aliases')

engine = babylon.create_engine()
stage = babylon.create_scene()
babylon.activate_scene(stage)

camera = api.FreeCamera("camera1", api.Vector3(0, 0, -10))
stage.add_camera(camera)
camera.attach_control(babylon.get_canvas())
ground = api.MeshBuilder.CreateGround("gd", stage, width=50, height=50, subdivsions=10)
plight = api.PointLight('light1', api.Vector3(0, 50, -50))
plight.diffuse = api.Color3(0.6, 0.6, 0.45)
hlight = api.HemisphericLight('light2', api.Vector3(1, 0, 0))
hlight.diffuse = api.Color3(0.3, 0.3, 0.5)
stage.actionManager = api.ActionManager(stage)
stage.add_light(hlight)
stage.add_light(plight)


sphere = api.MeshBuilder.create_sphere("sphere", stage)

leftright = KeyAxis('horiz', 'd', 'a', 120, 60)
updown = KeyAxis('vert', 'w', 's', 60, 30)
CS = ControlSet(leftright, updown)
CS.register(stage)


__pragma__('noalias', 'babylon_aliases')

from shaders import ShaderLoader

test = ShaderLoader(stage)
async def assign():
    result = await test.load_promise('tester')
    sphere.material = result
#test.load_promise('tester').then(assign)
#print ("----")
#test.load('tester')
#assign()

test.load_async('tester').then(lambda x: print (x.material))