from org.transcrypt.stubs.browser import __pragma__, __new__, window


def construct(cls, cls_name, module):
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

    def __init__(self, original, namespace):
        self.namespace = namespace
        self.original = original

    def reflect(self, handler, namespace):

        __pragma__('jsiter')

        for eachobj in self.original:
            if not eachobj.startswith('_'):
                api_obj = self.original[eachobj]
                new_name, result = handler(eachobj, api_obj)
                if result is not None:
                    self.namespace[new_name] = result
                    api_obj.prototype.__class__ = result
                    window.Object.setPrototypeOf(result, api_obj)

        __pragma__('nojsiter')
