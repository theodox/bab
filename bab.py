import bootstrap
import org.babylonjs.api as api
import org.babylonjs.globals as babylon
from org.transcrypt.stubs.browser import __pragma__, setTimeout, Promise
from input import KeyAxis
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
stage.actionManager = api.ActionManager(stage)


stage.add_light(hlight)

leftright = KeyAxis('horiz', stage.actionManager, 'a', 's')
#    logger.debug("action: {}\n\t{}".format(type(entry), entry))

#print (KeyAxis.get('horiz'))

def poll():
    pass
    #print(engine.performanceMonitor.instantaneousFrameTime)
    #leftright.update(engine.performanceMonitor.instantaneousFrameTime * 0.001)

engine.runRenderLoop(poll)


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