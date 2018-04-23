recipes:
========

# pick mesh with a click:
result =  s.pick(s.pointerX, s.pointerY).pickedMesh 

# click location
result =  s.pick(s.pointerX, s.pointerY).pickedPoint

Transcrypt
===========

*  __getitem__ / __setitem__  and __call__ require the `opov` pragma
* so do _negative_ slice indices!
