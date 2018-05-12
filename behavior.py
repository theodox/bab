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

    def __init__(self, name, mouse=False, keyboard=False):
        self.name = name
        self.owner = None
        self._ticker = None
        self._hearbeat = None
        self._mouse = mouse
        self._keyboard = keyboard

    def init(self):
        """this will be called when the behavior is attached"""
        pass

    def attach(self, object):
        self.owner = object
        scene = object.getScene()
        self._hearbeat = Heartbeat.get(scene)
        self._ticker = scene.onBeforeRenderObservable.add(self.tick)
        if self._mouse:
            self._mouse = scene.onPrePointerObservable.add(self.mouse_function)
        if self._keyboard:
            self._keyboard = scene.onPreKeyboardObservable.add(self.keyboard_function)

    def detach(self):
        scene = self.owner.getScene()
        scene.onBeforeRenderObservable.remove(self._ticker)
        if self._mouse:
            scene.onPrePointerObservable.remove(self._mouse)
        if self._keyboard:
            scene.onPreKeyboardObservable.remove(self._keyboard)

    def mouse_function(self, mouseinfo):
        pass

    def keyboard_function(self, keyInfo):
        pass

    def tick(self):
        pass


class Mover (BehaviorBase):

    def keyboard_function(self, evt):
        print("got", evt)

    def tick(self):
        self.owner.scaling.scaleInPlace(1.0 + self._hearbeat.last_frame_time)
