from org.transcrypt.stubs.browser import __pragma__, __new__, window
import logging
logger = logging.getLogger(__name__)

def construct(cls_name, cls, module):
    """returns a wrapping constructor coll for 'cls', which should be am api object"""
    def __init__(*args):
        return __new__(cls(*args))

    __init__.__name__ = cls_name
    __init__.__str__ = lambda self: "<class '{}.{}'>".format(module, cls_name)

    cls.prototype.__str__ = lambda s: "<{}>".format(cls_name)

    return __init__


class ClassFactory:
    """iterate over a namespace and apply a factory function to
    all js classes in it.  Promote them to the owning module"""

    def __init__(self, original, namespace, predicate=None):
        # namespace is where the imported names will go,
        # probably the local __all__
        self.namespace = namespace

        # the original Javascript object, eg window.BABYLON
        self.original = original

        def default_filter(obj_name):
            return not obj_name.startswith("_")
        self.predicate = predicate or default_filter

    def reflect(self, handler, namespace):

        if not self.original:
            logger.critical("ClassFactory cannnot find Javascript object - has it been loaded?")

        __pragma__('jsiter')

        for eachobj in self.original:
            if self.predicate(eachobj):
                api_obj = self.original[eachobj]
                if not api_obj.hasOwnProperty('prototype'):
                    self.namespace[eachobj] = api_obj
                    continue
                new_name, result = handler(eachobj, api_obj)
                if result is None:
                    self.namespace[new_name] = api_obj
                else:
                    self.namespace[new_name] = result
                    api_obj.prototype.__class__ = result
                    window.Object.setPrototypeOf(result, api_obj)

        __pragma__('nojsiter')
