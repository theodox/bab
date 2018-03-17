import org.babylonjs as babylon
from org.transcrypt.stubs.browser import document

PIOVERTWO = Math.PI / 2.0


def main():
    canvas = document.getElementById("renderCanvas")
    engine = babylon.Engine(canvas, True)

    def setup():
        scene = babylon.Scene(engine)

        # Add a camera to the scene and attach it to the canvas
        camera = babylon.ArcRotateCamera("Camera", PIOVERTWO, PIOVERTWO, 2, babylon.Vector3(0, 0, 0), scene)
        camera.attachControl(canvas, True)

        # Add lights to the scene
        light1 = babylon.HemisphericLight("light1", babylon.Vector3(1, 1, 0), scene)
        light2 = babylon.PointLight("light2", babylon.Vector3(0, 1, -1), scene)

        # This is where you create and manipulate meshes

        sphere = babylon.MeshBuilder.CreateSphere("sphere", {}, scene)
        opts = {
            'size': 4,
            'width': 4,
            'height': 4,
            'sourcePlane': babylon.Plane(0, -1, 0, 1)
        }
        box = babylon.MeshBuilder.CreatePlane("plane", opts, scene)
        return scene, sphere

    scene_object, sphere = setup()

    dummy = 0
    delta = babylon.Vector3.Up().scaleInPlace(0.001)
    def callback():
        nonlocal dummy
        dummy += 1 #__:fopov
        sphere.position  +=  delta #__:fopov
        scene_object.render()
        if dummy > 100:
            dummy = 0
    engine.runRenderLoop(callback)

    window.addEventListener("resize", lambda : engine.resize())


main()


def run():
    def foo():
        x = 42

        def bar():
            print(x)

        bar()

    foo()
    print("----")

