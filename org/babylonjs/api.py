from org.transcrypt.stubs.browser import __pragma__, __new__, window, this, console, __include__, __all__
from org.babylonjs import bootstrap
from org.babylonjs.reflection import ClassFactory, construct
import logging
logger = logging.getLogger(__name__)


__pragma__('noanno')


def _load_api():

    # not all functions are defined here to keep the scope clean

    def _js_class(api_key, api_object):
        '''
        Add python-style constructor, but preserve static methods from the original class
        '''

        result = construct(api_key, api_object, __name__)
        return api_key, result

    def _js_math_class(api_key, api_object):
        '''
        Add python constructor and python magic methods for operator overloading
        if necessary, use kwargs to choose the native function that
        becomes a magic method
        '''
        proto = api_object.prototype
        proto.__add__ = proto.add
        proto.__sub__ = proto.subtract
        proto.__mul__ = proto.multiply
        proto.__truediv__ = proto.divide
        proto.__eq__ = proto.equals

        def _ne_(other):
            return not (this.__eq__(other))

        proto.__ne__ = _ne_

        return _js_class(api_key, api_object)

    def _js_vec3(api_key, api_object):

        def vec3mul(other):
            if other['_width'] == this._width:
                return this.multiply(other)
            return this.scale(other)

        def vec3div(other):
            if other['_width'] == this._width:
                return this.divide(other)
            return this.scale(1.0 / other)

        def vec3imul(other):
            if other['_width'] == this['_width']:
                return this.multiplyInPlace(other)
            return this.scaleInPlace(other)

        def vec3idiv(other):
            if other['_width'] == this['_width']:
                return this.divideInPlace(other)
            return this.scaleInPlace(1.0 / other)

        def vec3rmul(other):
            return this.__mul__(other)

        def vec3rdiv(other):
            return this.__truediv__(other)

        proto = api_object.prototype
        proto._width = 3
        proto.__mul__ = vec3mul
        proto.__imul__ = vec3imul
        proto.__truediv__ = vec3div
        proto.__itruediv__ = vec3idiv
        proto.__rmul__ = vec3rmul
        proto.__rtruediv__ = vec3rdiv
        proto.__add__ = proto['add']
        proto.__iadd__ = proto['addInPlace']
        proto.__sub__ = proto['subtract']
        proto.__isub__ = proto['subtractInPlace']
        proto.__eq__ = proto['equals']

        def vec3ne(other):
            return not (this.__eq__(other))

        proto.__ne__ = vec3ne

        return _js_class(api_key, api_object)

    def _promote(classname, member):
        '''
        apply wrappers to js_classes where appropriate
        '''

        if classname == 'Vector3':
            return _js_vec3(classname, member)  

        if member.prototype:
            if member.prototype.hasOwnProperty('multiply'):
                return _js_math_class(classname, member)
            else:
                return _js_class(classname, member)

        # this is something like a constant or static class
        # return unwrapped
        return classname, member

    # wrap api classes where useful, promote to
    # the __all__ namespace of this so they look like
    # memberts for import
    console.time('api initialized')

    ClassFactory(window.BABYLON, __all__).reflect(_promote)

    console.timeEnd('api initialized')

    def _add_kwargs(cls, member):
        """convert the syntax of the meshbuilder, which is ugly"""
        __pragma__('ifndef', 'release')
        orig = cls[member]
        if not orig:
            raise KeyError('No member named', member)
        __pragma__('endif')

        __pragma__('kwargs')

        def kwargified(name, scene, **kwargs):
            return orig(name, kwargs, scene)
        __pragma__('nokwargs')

        cls[member] = kwargified

    # these are static creation unctions which want kwargs
    TAGS = ('CreateBox', 'CreateCylinder', 'CreateDashedLines', 'CreateDecal', 'CreateDisc', 'CreateGround',
            'CreateGroundFromHeightMap', 'CreateIcoSphere', 'CreateLathe', 'CreateLineSystem', 'CreateLines',
            'CreatePlane', 'CreatePolygon', 'CreatePolyhedron', 'CreateRibbon', 'CreateSphere',
            'CreateTiledGround', 'CreateTorus', 'CreateTorusKnot', 'CreateTube')

    mb = __all__['MeshBuilder']
    for tag in TAGS:
        _add_kwargs(mb, tag)




# load the Babylonjs module into __all__
console.time('babylonjs loaded')
__pragma__('js', '{}', __include__('org/babylonjs/__javascript__/babylon.custom.js'))
console.timeEnd('babylonjs loaded')

_load_api()
