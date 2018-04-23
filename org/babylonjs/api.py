from org.transcrypt.stubs.browser import __pragma__, __new__, window, this, console, __include__, __all__
import logging
logger = logging.getLogger(__name__)


__pragma__('noanno')


def _js_class(api_object):
    '''
    Add python-style constructor, but preserve static methods from the original class
    '''
    def BabylonAPIObject(*args):
        return __new__(api_object(*args))

    # allows for 'static' functions too
    window.Object.setPrototypeOf(BabylonAPIObject, api_object)
    api_object['__str__'] = api_object.toString
    return BabylonAPIObject


def _js_math_class(obj, add='add', subtract='subtract', multiply='multiply', divide='divide', equals='equals'):
    '''
    Add python constructor and python magic methods for operator overloading
    if necessary, use kwargs to choose the native function that
    becomes a magic method
    '''
    obj.prototype['__add__'] = obj.prototype[add]
    obj.prototype['__sub__'] = obj.prototype[subtract]
    obj.prototype['__mul__'] = obj.prototype[multiply]
    obj.prototype['__truediv__'] = obj.prototype[divide]
    obj.prototype['__eq__'] = obj.prototype[equals]

    def _ne_(other):
        return not (this.__eq__(other))

    obj.prototype['__ne__'] = _ne_

    base = _js_class(obj)
    return base


def _add_kwargs(cls, member):

    orig = cls[member]
    if not orig:
        raise KeyError('No member named', member)
    alias = ''
    for idx, char in enumerate(member):
        if char != char.upper():
            alias += char
        else:
            if idx > 0:
                alias += '_'
            alias += char.lower()
    logger.debug(orig + '>' + alias)

    __pragma__('kwargs')

    def kwargified(name, scene, **kwargs):
        return orig(name, kwargs, scene)
    __pragma__('nokwargs')

    cls[alias] = kwargified


def _promote(member):
    '''
    apply wrappers to js_classes where appropriate
    '''
    if member.hasOwnProperty('prototype') and member.prototype.hasOwnProperty('constructor'):
        if member.prototype.hasOwnProperty('multiply'):
            # return with magic methods for fast operator overload
            return _js_math_class(member)

        # return wrapped with a python constructor
        return _js_class(member)

    # this is something like a constant or static class
    # return unwrapped
    return member


# load the Babylonjs module into __all__
console.time('babylonjs loaded')
__pragma__('js', '{}', __include__(
    'org/babylonjs/__javascript__/babylon.custom.js'))
console.timeEnd('babylonjs loaded')


# wrap api classes where useful, promote to
# the __all__ namespace of this so they look like
# memberts for import
console.time('api initialized')

__pragma__('jsiter')
for _k in window.BABYLON:
    if not _k.startswith('_'):
        __all__[_k] = _promote(window.BABYLON[_k])
__pragma__('nojsiter')

console.timeEnd('api initialized')


# add pep-8 style versions of create functions with kwargs syntax
TAGS = ('CreateBox', 'CreateCylinder', 'CreateDashedLines', 'CreateDecal', 'CreateDisc', 'CreateGround',
        'CreateGroundFromHeightMap', 'CreateIcoSphere', 'CreateLathe', 'CreateLineSystem', 'CreateLines',
        'CreatePlane', 'CreatePolygon', 'CreatePolyhedron', 'CreateRibbon', 'CreateSphere',
        'CreateTiledGround', 'CreateTorus', 'CreateTorusKnot', 'CreateTube')

mb = __all__['MeshBuilder']
for tag in TAGS:
    _add_kwargs(mb, tag)

# clean up the one-time functions
del TAGS, _promote, _js_class, _js_math_class, _add_kwargs
