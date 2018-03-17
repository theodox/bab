import org.babylonjs.core as core
import org.babylonjs.geometry as geometry
import org.babylonjs.cameras as cameras
import org.babylonjs.lights as lights

from org.babylonjs.core import Vector3

from org.transcrypt.stubs.browser import document

PIOVERTWO = Math.PI / 2.0


def main():
    canvas = document.getElementById("renderCanvas")
    engine = core.Engine(canvas, True)

    def setup():
        scene = core.Scene(engine)

        # Add a camera to the scene and attach it to the canvas
        camera = cameras.ArcRotateCamera("Camera", PIOVERTWO, PIOVERTWO, 2, Vector3(0, 0, 0), scene)
        camera.attachControl(canvas, True)

        # Add lights to the scene
        light1 = lights.HemisphericLight("light1", Vector3(1, 1, 0), scene)
        light2 = lights.PointLight("light2",    Vector3(0, 1, -1), scene)

        # This is where you create and manipulate meshes

        sphere = geometry.MeshBuilder.CreateSphere("sphere", {}, scene)
        opts = {
            'size': 4,
            'width': 4,
            'height': 4,
            'sourcePlane': geometry.Plane(0, -1, 0, 1)
        }
        box = geometry.MeshBuilder.CreatePlane("plane", opts, scene)
        return scene, sphere

    scene_object, sphere = setup()

    dummy = 0
    delta = core.Vector3.Up().scaleInPlace(0.001)
    def callback():
        __pragma__('opov')
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


