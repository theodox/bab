import bootstrap
import org.babylonjs.api as api
import org.babylonjs.globals as babylon
from behavior import Tickable, observable
from org.transcrypt.stubs.browser import __pragma__, setTimeout, Promise
from input import KeyAxis, ControlSet
import logging
import math 
physics = api.CannonJSPlugin()



logger = logging.getLogger(__name__)

__pragma__('alias', 'babylon_aliases')

engine = babylon.create_engine()
stage = babylon.create_scene()
babylon.activate_scene(stage)

camera = api.UniversalCamera("camera1", api.Vector3(10, 10, -10))
camera.set_target(api.Vector3.Zero())

stage.add_camera(camera)
stage.enablePhysics(api.Vector3(0,-9.8,0), physics)


camera.attach_control(babylon.get_canvas())
ground = api.MeshBuilder.create_ground("gd", stage, width=50, height=50, subdivsions=10)
groundimp = api.PhysicsImpostor(ground, api.PhysicsImpostor.PlaneImpostor, {'mass': 0})

plight = api.PointLight('light1', api.Vector3(0, 50, -50))
plight.diffuse = api.Color3(0.6, 0.6, 0.45)
hlight = api.HemisphericLight('light2', api.Vector3(1, 0, 0))
hlight.diffuse = api.Color3(0.3, 0.3, 0.5)
stage.actionManager = api.ActionManager(stage)
stage.add_light(hlight)
stage.add_light(plight)


sphere = api.MeshBuilder.create_sphere("sphere", stage)
sphere.position = api.Vector3(-1, 3, -1)
imp = api.PhysicsImpostor(sphere, api.PhysicsImpostor.SphereImpostor, {'mass': 1})



# make some obstacles

boxes = []
for item in ( (3.5,3.5), (5,5), (2,0), (0, 2)):
    x, z = item
    obst = api.MeshBuilder.create_box('cube_{}_{}'.format(x,z), stage)
    obst.position = api.Vector3(x, 5.0, z)
    coll = api.PhysicsImpostor(obst, api.PhysicsImpostor.BoxImpostor, {'mass': 0.1, 'restitution': 0.9})
    boxes.append(coll)

leftright = KeyAxis('horiz', 'd', 'a', 120, 60)
updown = KeyAxis('vert', 'w', 's', 60, 30)
CS = ControlSet(leftright, updown)
CS.register(stage)


class Steer (Tickable):

    def __init__(self, scene,  h, v):
        super().__init__(scene)
        self.h = h
        self.v = v

    def tick(self, deltatime):
        x = api.Vector3(self.h.value,0,self.v.value) 
        imp.applyImpulse(x, sphere.getAbsolutePosition()) 


st = Steer(stage, leftright, updown)
st.attach(sphere)

def on_hit_box(me, him):
    print (me.object, "hit", him.object)

imp.registerOnPhysicsCollide(boxes, on_hit_box)

document.getElementById('game_canvas').focus()

__pragma__('noalias', 'babylon_aliases')

#from shaders import ShaderLoader2

#test = ShaderLoader(stage)
#test.load( 'tester')
