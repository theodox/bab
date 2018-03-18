from org.babylonjs.engine import Engine
from org.babylonjs.scene import Scene
import org.babylonjs.mesh as mesh
import org.babylonjs.cameras as cameras
import org.babylonjs.lights as lights
from org.babylonjs.math import Vector3, Plane

from org.transcrypt.stubs.browser import document

PIOVERTWO = Math.PI / 2.0


def main():
    canvas = document.getElementById("renderCanvas")
    engine = Engine(canvas, True)

    def setup():
        scene = Scene(engine)

        # Add a camera to the scene and attach it to the canvas
        camera = cameras.ArcRotateCamera("Camera", PIOVERTWO, PIOVERTWO, 2, Vector3(0, 0, 0), scene)
        camera.attachControl(canvas, True)

        # Add lights to the scene
        light1 = lights.HemisphericLight("light1", Vector3(1, 1, 0), scene)
        light2 = lights.PointLight("light2",    Vector3(0, 1, -1), scene)

        # This is where you create and manipulate meshes

        sphere = mesh.MeshBuilder.CreateSphere("sphere", {}, scene)
        opts = {
            'size': 4,
            'width': 4,
            'height': 4,
            'sourcePlane': Plane(0,-1,0, 1)
        }
        box = mesh.MeshBuilder.CreatePlane("plane", opts, scene)
        return scene, sphere

    scene_object, sphere = setup()

    dummy = 0
    delta = Vector3.Up().scaleInPlace(0.001)
    def callback():
        __pragma__('opov', 'fast')
        nonlocal dummy
        dummy += 1
        sphere.position  +=  delta
        __pragma__('noopov')
        scene_object.render()
        if dummy > 100:
            dummy = 0
    engine.runRenderLoop(callback)

    window.addEventListener("resize", lambda : engine.resize())


main()


