recipes:
========

# pick mesh with a click:
result =  s.pick(s.pointerX, s.pointerY).pickedMesh 

# click location
result =  s.pick(s.pointerX, s.pointerY).pickedPoint

# Javascript timer with promise:


def timer(length, _):
    def timer_elapse(resolve):
        def inner():
            print("waited", length)
            resolve(Date.now())
        setTimeout(inner, length * 1000)
        print("start waiting...")

    return __new__(Promise(timer_elapse, lambda: print("oops")))


# registering keyboard input

Have to be explicit about assigning the actionmgr to the right member 

    stage.actionManager = api.ActionManager(stage)



Transcrypt
===========

*  __getitem__ / __setitem__  and __call__ require the `opov` pragma
* so do _negative_ slice indices!
