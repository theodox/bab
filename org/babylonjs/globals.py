from org.transcrypt.stubs.browser import __pragma__, document, window
from org.babylonjs.api import ShaderMaterial, MeshBuilder, Scene, Engine
import logging
logger = logging.getLogger(__name__)

DEFAULT_CANVAS = "game_canvas"

_ENGINE = None
_CANVAS = None
_SCENE = None


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
    nonlocal _ENGINE
    return _ENGINE


def get_canvas():
    nonlocal _CANVAS
    return _CANVAS


def create_scene(activate=True):
    nonlocal _SCENE
    scene = Scene(_ENGINE)
    return scene


def activate_scene(scene):
    nonlocal _SCENE
    _SCENE = scene

