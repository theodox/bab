import org.babylonjs as babylon
from org.transcrypt.stubs.browser import document




PIOVERTWO = Math.PI / 2.0

canvas = document.getElementById("renderCanvas")

engine = babylon.Engine(canvas, True)


scene = babylon.Scene(engine)

#Add a camera to the scene and attach it to the canvas
camera = babylon.ArcRotateCamera("Camera", PIOVERTWO, PIOVERTWO, 2, babylon.Vector3(0,0,0), scene)
camera.attachControl(canvas, True)

# Add lights to the scene
light1 = babylon.HemisphericLight("light1", babylon.Vector3(1, 1, 0), scene)
light2 = babylon.PointLight("light2", babylon.Vector3(0, 1, -1), scene)

#This is where you create and manipulate meshes

sphere = babylon.MeshBuilder.CreateSphere("sphere", {}, scene)
opts = {
    'size': 4,
    'width': 4,
    'height': 4,
    'sourcePlane': babylon.Plane(0,-1,0,1)
}
box = babylon.MeshBuilder.CreatePlane("plane", opts, scene )

def cb():
    sphere.translate(v, .01, babylon.BABYLON.Space.Local)
    v.x += .001
    v.normalize()

    return scene.render()

engine.runRenderLoop(cb)

window.addEventListener("resize", engine.resize)
