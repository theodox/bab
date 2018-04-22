from org.babylonjs.api import Vector3, Space, Engine, Scene
from org.transcrypt.stubs.browser import window, console
import time
import random
import logging
logger = logging.getLogger(__name__)


class Game:

    def __init__(self, canvas="renderCanvas"):

        canvas = window.document.getElementById("renderCanvas")
        self.engine = Engine(canvas, True)
        self.canvas = canvas
        self.started = time.time()
        self.last_frame = self.started
        self.paused = False
        self.active_scene = None
        self.click_handlers = []

        window.addEventListener("click", self._click_handler)
        window.addEventListener("resize", lambda: engine.resize())

    def create_scene(self):
        self.active_scene = Scene(self.engine)
        return self.active_scene


    def set_camera(self, camera):
        self.active_scene.cameraToUseForPointers = camera

    def update(self):
        now = time.time()
        delta = (now - self.last_frame)
        if not self.paused:
            for actor in self.pick_map.values():
                actor.tick(delta)
        self.last_frame = now

    def _click_handler(self, val):
        scn = self.active_scene
        if not scn or not self._click_handlers:
            return

        pick_result = scn.pick(scn.pointerX, scn.pointerY)
        for handler in self.click_handlers:
            handler(pick_result)


class Actor:
    """base class for updatables"""

    def __init__(self, mesh):
        self.mesh = mesh
        pass

    def tick(self, interval):
        pass
