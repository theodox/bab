import logging
from org.babylonjs.api import Tools

logger = logging.getLogger(__name__)


class Heartbeat:

    INSTANCE = None

    def __init__(self, scene):
        self.last_frame_time = 0
        self.last_tick = 0
        # add the observer to the head of the queue -- which means we have
        # to turn on all the masks
        self.observer = scene.onBeforeAnimationsObservable.add(self.tick, -1, True)

    def tick(self):
        now = Tools.Now
        self.last_frame_time = (now - self.last_tick) * .001
        self.last_tick = now

    @classmethod
    def get(cls, scene):
        if not cls.INSTANCE:
            cls.INSTANCE = cls(scene)
        return cls.INSTANCE


class BehaviorBase:
    """Implements the Babylon Behavior interface"""
    
    def __init__(self, name):
        self.name = name
        self.owner = None
        self._pointer_observer = None
        self._update_observer = None
        self._hearbeat = None

    def attach(self, object):
        self.owner = object
        scene = object.getScene()
        self._hearbeat = Heartbeat.get(scene)
        self._pointer_observer = scene.onPrePointerObservable.add(self.mouse_function)
        self._update_observer = scene.onBeforeRenderObservable.add(self.tick)

    def detach(self):
        scene = self.owner.getScene()
        scene.onPrePointerObservable.remove(self._pointer_observer)
        scene.onBeforeRenderObservable.remove(self._update_observer)

    def mouse_function(self, mouseinfo):
        logger.debug(mouseinfo)

    def tick(self):
        logger.debug(self._hearbeat.last_frame_time)

class Mover (BehaviorBase):

    def tick(self):
        self.owner.scaling.scaleInPlace(1.0 + self._hearbeat.last_frame_time)
