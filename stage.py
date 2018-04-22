import org.babylonjs.api as api
import org.babylonjs.globals as helpers
import math

PIOVERTWO = math.pi / 2.0


def create_stage(scene, canvas):
    # Add a camera to the scene and attach it to the canvas
    camera = api.ArcRotateCamera(
        "Camera", PIOVERTWO, PIOVERTWO, 2, api.Vector3(0, 0, 0), scene)
    camera.attachControl(canvas, True)

    # Add lights to the scene
    api.HemisphericLight("light1", api.Vector3(1, 1, 0), scene)
    api.PointLight("light2", api.Vector3(0, 1, -1), scene)

    helpers.create_plane("plane", scene, size=4, sourcePlane=api.Plane(0, 0, -1, 0))

    return camera
