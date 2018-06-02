from org.babylonjs.reflection import ClassFactory, construct
import logging
logger = logging.getLogger(__name__)


def _gui_class_factory(api_key, api_object):
    '''
    Add python-style constructor, but preserve static methods from the original class
    '''
    __pragma__('ifndef', 'release')
    assert (api_object is not None)
    logger.debug(api_key)
    __pragma__('endif')

    BabylonGUIObject = construct(api_key, api_object, __name__)

    return api_key, BabylonGUIObject


ClassFactory(window.BABYLON.GUI, __all__).reflect(_gui_class_factory)
