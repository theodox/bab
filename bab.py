import org.babylonjs as babylon
from game import Game, SphereActor
from org.transcrypt.stubs.browser import document
import random
from terrain import Bitmap, create_kernel
gui = babylon.GUI


test = Bitmap(5, 5, Float32Array)
test[2,1] = 1.0
test[2,2] = 1.0
test[2,3] = 1.0

k = create_kernel(3,3, [
    -1.0, -1.0, -1.0,
    -1.0, 8.0, -1.0,
    -1.0, -1.0, -1.0
])
q = test.convolve(k)
print(q.data)


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
        spheres  =[]
        for r in range(1000):
            opts = {'size' : 0.5}
            a_sphere = babylon.MeshBuilder.CreateSphere("sphere_" + str(r), {}, scene)

            a_sphere.position = babylon.Vector3(
                (random.random() -0.5) * 10,
                (random.random() * 10),
                (random.random() -0.5) * 10
                )
            spheres.append(a_sphere)
        opts = {
            'size': 4,
            'width': 4,
            'height': 4,
            'sourcePlane': babylon.Plane(0, -1, 0, 1)
        }
        base_plane = babylon.MeshBuilder.CreatePlane("plane", opts, scene)
        return scene, spheres

    scene_object, spheres = setup()
    gameEngine = Game(engine)
    for sph in spheres:
        sphereActor = SphereActor(sph)
        gameEngine.add_actor(sphereActor)

    print(gameEngine)

    def callback():
        gameEngine.update()
        scene_object.render()
        
    engine.runRenderLoop(callback)
    window.addEventListener("resize", lambda : engine.resize())
    window.addEventListener("click", gameEngine.clickHandler)
main()
