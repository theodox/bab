from org.transcrypt.stubs.browser import __pragma__, document, window
from org.babylonjs.api import ShaderMaterial, MeshBuilder, Scene, Engine, Vector3, CannonJSPlugin

import logging
logger = logging.getLogger(__name__)

DEFAULT_CANVAS = "game_canvas"
GRAVITY = Vector3(0, -9.8, 0)


_ENGINE = None
_CANVAS = None
_SCENE = None
_PHYSICS = None


def create_engine(canvas_element=DEFAULT_CANVAS):
    nonlocal _CANVAS
    nonlocal _ENGINE
    _CANVAS = document.getElementById(canvas_element)
    if not _CANVAS:
        raise ValueError("No html5 canvas named", canvas_element)
    _ENGINE = Engine(_CANVAS, True)
    window.addEventListener("resize", lambda: _ENGINE.resize())

    def render_loop():
        if _SCENE:
            _SCENE.render()

    _ENGINE.runRenderLoop(render_loop)
    return _ENGINE


def get_engine():
    return _ENGINE


def get_canvas():
    return _CANVAS


def create_scene(activate=True, physics=True):
    nonlocal _SCENE
    scene = Scene(_ENGINE)
    scene.gravity = GRAVITY  # this is for kinematic physics

    if physics:
        if not _PHYSICS:
            _PHYSICS = CannonJSPlugin()
        scene.enablePhysics(GRAVITY, _PHYSICS)

    if activate:
        activate_scene(scene)

    __pragma__('ifndef', 'release')
    logger.debug("scene created {}".format("with physics" if physics else ""))
    __pragma__('endif')   
     
    return scene


def activate_scene(scene):
    nonlocal _SCENE
    _SCENE=scene
