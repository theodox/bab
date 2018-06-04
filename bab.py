import org.babylonjs.api as api
import org.babylonjs.globals as babylon
from org.babylonjs.behaviors.kinematic import SteeringBehavior
from org.transcrypt.stubs.browser import __pragma__  # , setTimeout, Promise
from input import KeyAxis, ControlSet
import logging
from org.babylonjs.hud import HUD, HUDItem, FPSCounter

import math

import org.babylonjs.gui as gui

logger = logging.getLogger(__name__)

__pragma__('alias', 'babylon_aliases')

engine = babylon.create_engine()
stage = babylon.create_scene(activate=True, physics=True)
hud = HUD()
example = HUDItem('test', 'babylonjs')

fps = FPSCounter(engine)
hud.add(example)
hud.add(fps)
hud.flash("hello world")

camera = api.UniversalCamera("camera1", api.Vector3(10, 10, -10))
camera.set_target(api.Vector3.Zero())
stage.add_camera(camera)
camera.attach_control(babylon.get_canvas())

ground = api.MeshBuilder.create_ground("gd", stage, width=50, height=50, subdivsions=10, updatable = True)
vertices = ground.getVerticesData(api.VertexBuffer.PositionKind)
vertices[1] = -10
ground.setVerticesData(api.VertexBuffer.PositionKind, vertices)

groundimp = api.PhysicsImpostor(ground, api.PhysicsImpostor.PlaneImpostor, {'mass': 0})

plight = api.DirectionalLight('light1', api.Vector3(0.707, -0.707, 0.707))
plight.position = (api.Vector3(-10, 10, -10))
plight.diffuse = api.Color3(0.6, 0.6, 0.45)
hlight = api.HemisphericLight('light2', api.Vector3(1, 0, 0))
hlight.diffuse = api.Color3(0.3, 0.3, 0.5)
stage.actionManager = api.ActionManager(stage)
stage.add_light(hlight)
stage.add_light(plight)
shadowgen = api.ShadowGenerator(512, plight)
shadowgen.usePercentageCloserFiltering = True


sphere = api.MeshBuilder.create_box("sphere", stage)
sphere.position = api.Vector3(-1, 3, -1)
shadowgen.addShadowCaster(sphere)
sphere.receiveShadows = True
#imp = api.PhysicsImpostor(sphere, api.PhysicsImpostor.SphereImpostor, {'mass': 1})


ground.receiveShadows = True
# make some obstacles

boxes = []
for item in ((3.5, 3.5), (5, 5), (2, 0), (0, 2)):
    x, z = item
    obst = api.MeshBuilder.create_box('cube_{}_{}'.format(x, z), stage)
    obst.position = api.Vector3(x, 5.0, z)
    coll = api.PhysicsImpostor(obst, api.PhysicsImpostor.BoxImpostor, {'mass': 0.1, 'restitution': 0.9})
    boxes.append(coll)
    shadowgen.addShadowCaster(obst)
    obst.receiveShadows = True

leftright = KeyAxis('horiz', 'd', 'a', 120, 60)
updown = KeyAxis('vert', 'w', 's', 60, 30)
CS = ControlSet(leftright, updown)
CS.register(stage)


k = SteeringBehavior(stage, leftright, updown, 0.1, 0.1)
k.attach(sphere)
sphere.ellipsoid = api.Vector3(0.5, 0.5, 0.5)


stage.collisionsEnabled = True
sphere.checkCollisions = True
ground.checkCollisions = True
document.getElementById('game_canvas').focus()

__pragma__('noalias', 'babylon_aliases')

from shaders import ShaderAssetTask


#api.AssetsManager.prototype.addShaderTask = addShaderTask
"""
__pragma__('js',"{}", '''
window.BABYLON.AssetsManager.prototype.addShaderTask = function (taskName, url) {
    var shader_task = ShaderAssetTask (taskName, url);
    this.tasks.push (shader_task);
    return shader_task;
};''')
"""
am = api.AssetsManager(stage)

sl = am.addShaderTask('test', './src/shaders/tester.shader')
#am.tasks.append(sl)
def t():
    sphere.material = sl.shader
am.onTaskSuccessObservable.add(t)
am.load()

