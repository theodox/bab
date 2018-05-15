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



# registering keyboard input

Have to be explicit about assigning the actionmgr to the right member 

    stage.actionManager = api.ActionManager(stage)

# behaviors

implemented in the bevavior module.  Don't forget to call super() in the __init__ and to use the @observable decorator to hook into frame event


Transcrypt
===========

*  __getitem__ / __setitem__  and __call__ require the `opov` pragma
* so do _negative_ slice indices!
