    recipes:
========

# pick mesh with a click:
result =  s.pick(s.pointerX, s.pointerY).pickedMesh 

# click location
result =  s.pick(s.pointerX, s.pointerY).pickedPoint

# Javascript timer with promise:

returns a Promise object with a callback and an error handler function


    def timer(length):
        def timer_elapse(resolve): 
            def inner():
                print("waited", length)
                resolve(Date.now())
            setTimeout(inner, length * 1000)
            print("start waiting...")

        return __new__(Promise(timer_elapse, lambda: print("oops")))

async def will call those functions in series without blocking

    async def f():
        print('first')
        await timer(2)
        print('second')
        w = await timer(5)
        print("got", w)

actually fire it off....

    f()

Another example:



    def load_async(self, relpath):
        fullpath = self.root + relpath
        shaderfile = fullpath + ".shader"
        logger.debug("requesting {}".format(shaderfile))

        def sender(resolve, reject):
            xobj = __new__(XMLHttpRequest())
            xobj.overrideMimeType("application/json")
            xobj.open('GET', shaderfile, True)

            def handle_result():
                descriptor = JSON.parse(xobj.responseText)
                shader_name = descriptor.name
                del descriptor.name
                mtl = ShaderMaterial(shader_name, self.scene, fullpath, descriptor)
                logger.debug("retrieved shader descriptor '{}'".format(descriptor.js_name))
                resolve(mtl)

            def handle_err():
                logger.warning(xobj.responseText)
                reject(xobj.responseText)

            xobj.onload = handle_result
            xobj.onerror = handle_err

            xobj.send(None)

        return __new__(Promise(sender))

    async def assign(self, target, shader):
        def success(shdr):
            target.material = shdr
            logger.debug("assigned '{}' to '{}'", shdr, target.Name or target.name)

        def failure(fail):
            logger.warning("shader {} failed to load".format(shader))

        await(self.load_async(shader)).then(success, failure)

shows an example of awaiting a promise-returning function then executing another step condtionally

# AssetManager

Allows you to queue up a bunch of async jobs and run them. UI for combined progress as it handles all.  

# registering keyboard input

Have to be explicit about assigning the actionmgr to the right member 

    stage.actionManager = api.ActionManager(stage)

# behaviors

implemented in the bevavior module.  Don't forget to call super() in the __init__ and to use the @observable decorator to hook into frame event

Inherit from `Tickable` and override `tick(self, deltatime)`  to implement a ticking behavior.  


# simple physics:

enable physics:

    physics = api.CannonJSPlugin()
    scene.enablePhysics(api.Vector3(0,-9.8,0), physics)

Add physics body to object:

    sphere = api.MeshBuilder.create_sphere("sphere", stage)
    imp = api.PhysicsImpostor(sphere, api.PhysicsImpostor.SphereImpostor, {'mass': 1})

Add an impulse to the imposter:

    imp.applyImpulse(api.Vector3(2,0,0), sphere.getAbsolutePosition()) 

Can apply impulse some other location than the pivot...

Detect collision (take one or more targets as args)

    def on_hit_box(me, him):
        print (me.object, "hit", him.object)

    imp.registerOnPhysicsCollide(boxes, on_hit_box)

Note everything collides; not everything triggers event


# pure kinematic movement

Use `.moveWithCollisions(Vector)`  but the vector has to include gravity -- 'applyGravity' (in the docs) only works on Cameras. 


# modify an existing mesh vertices

    ground = api.MeshBuilder.create_ground("gd", stage, width=50, height=50, subdivsions=10, updatable = True)
    vertices = ground.getVerticesData(api.VertexBuffer.PositionKind)
    vertices[1] = -10
    ground.setVerticesData(api.VertexBuffer.PositionKind, vertices)

here vertices will be a flat array with a stride of 3
# or custom mesh

    customMesh = api.Mesh("custom", scene)
    positions = [-5, 2, -3, -7, -2, -3, -3, -2, -3, 5, 2, 3, 7, -2, 3, 3, -2, 3]
    indices = [0, 1, 2, 3, 4, 5]
    
    normals = []
    vertexData = api.VertexData()
    api.VertexData.ComputeNormals(positions, indices, normals)
    vertexData.positions = positions
    vertexData.indices = indices
    vertexData.normals = normals 
    vertexData.applyToMesh(customMesh)

indices is the index buffer:   here two triangles for vertex (0-1-2) and (3-4-5)


Transcrypt
===========

*  __getitem__ / __setitem__  and __call__ require the `opov` pragma
* so do _negative_ slice indices!
