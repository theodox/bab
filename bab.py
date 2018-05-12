import bootstrap
import org.babylonjs.api as api
import org.babylonjs.globals as babylon
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
api.MeshBuilder.create_plane("plane", stage, size=4, plane=api.Plane(0, -1, 0, 0))
hlight = api.HemisphericLight('light1', api.Vector3(0, -1, 0))
stage.actionManager = api.ActionManager(stage)

sphere = api.MeshBuilder.create_sphere("sphere", stage)

stage.add_light(hlight)

leftright = KeyAxis('horiz', 'd', 'a', 120, 60)
updown = KeyAxis('vert', 's', 'w', 60, 30)
CS = ControlSet(leftright, updown)
CS.register(stage)
#    logger.debug("action: {}\n\t{}".format(type(entry), entry))

#print (KeyAxis.get('horiz'))

def poll():
    sphere.setAbsolutePosition(api.Vector3(leftright.value, updown.value, 0))

stage.onBeforeRenderObservable.add(poll)


__pragma__('noalias', 'babylon_aliases')

# Actual code to be tested

def timer(length, _):
    def timer_elapse(resolve):
        def inner():
            print ("waited", length)
            resolve(Date.now())
        setTimeout (inner, length * 1000)
        print ("start waiting...")

    return __new__(Promise (timer_elapse, lambda : print ("oops") ))


async def f (waw, _):
    print ('f0')
    await waw (2, _)
    print ('f1')
    w = await waw (5, _)
    print ("got", w)
# Just call async functions for Transcrypt, since in the browser JavaScript is event driven by default
    
if __envir__.executor_name == __envir__.transpiler_name:
    f (timer, None)
    

'''counter = 0
def ticker():
    nonlocal counter
    counter += 1
    if (counter % 60 == 0):
        print("frame", counter)

engine.runRenderLoop(ticker)'''