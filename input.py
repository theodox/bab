import org.babylonjs.api as api
import logging
import math
import utils

logger = logging.getLogger(__name__)


PRESS = api.ActionManager.OnKeyDownTrigger
RELEASE = api.ActionManager.OnKeyUpTrigger


def keystroke(key, press_release, fn):
    """returns an ExecuteCodeAction tied to the press or release of <key>"""
    return api.ExecuteCodeAction({'trigger': press_release, 'parameter': key}, fn)


class KeyAxis:
    """Similar to a Unity InputAxis"""

    def __init__(self, name, positiveKey, negativeKey, gain=75.0, decay=25.0):
        self.value = 0
        self.positive_key = positiveKey
        self.negative_key = negativeKey
        self._pos = False
        self._neg = False
        self.gain = gain
        self.decay = decay
        self.name = name

    def _register(self, mgr):
        mgr.registerAction(keystroke(self.positive_key, PRESS, self._pos_dn))
        mgr.registerAction(keystroke(self.positive_key, RELEASE, self._pos_up))
        mgr.registerAction(keystroke(self.negative_key, PRESS, self._neg_dn))
        mgr.registerAction(keystroke(self.negative_key, RELEASE, self._neg_up))
        logger.debug("registered {}" .format(self))

    def _update(self, timeslice):
        self.value += self.gain * (self._pos - self._neg) * timeslice
        if self.decay and not (self._pos or self._neg):
            step = self.decay * timeslice
            if abs(self.value) > 0.5 * step:
                v = utils.smoothstep(abs(self.value), -1, 1)
                decay = v * self.decay * timeslice * math.copysign(1, self.value)
                self.value -= decay
            else:
                self.value = 0

        if self.value != self.value:
            raise ValueError("bad value: " + str(self.value))
        self.value = min(1, max(-1, self.value))

    def _neg_up(self, e):
        self._neg = 0

    def _pos_up(self, e):
        self._pos = 0

    def _neg_dn(self, e):
        self._neg = 1

    def _pos_dn(self, e):
        self._pos = 1

    def __str__(self):
        return ("<KeyAxis: '{0}' {1}>".format(self.name, self.value))


class ControlSet:
    """
    connects a group of input axes to a scene
    eg;
        leftright = KeyAxis('horiz', 'd', 'a', 120, 60)
        updown = KeyAxis('vert', 's', 'w', 60, 30)
        CS = ControlSet(leftright, updown)
        CS.register(stage)

    """

    def __init__(self, *axes):
        self.axes = {}
        for i in axes:
            self.add(i)

    def add(self, axis):
        self.axes[axis.name] = axis

    def remove(self, name):
        return self.axes.pop(self.name)

    def get(self, name):
        return self.axes[name]

    def update(self, engine):
        interval = engine.getDeltaTime() * 0.001
        for v in self.axes.values():
            v._update(interval)

    def register(self, scene):
        if not scene.actionManager:
            raise ValueError("{} has no actionManager".format(scene))

        for v in self.axes.values():
            v._register(scene.actionManager)
        engine = scene.getEngine()
        scene.onAfterCameraRenderObservable.add(lambda: self.update(engine))
        scene.onDisposeObservable.add(lambda: self.deregister, scene)

    def deregister(cls, scene):
        logger.debug("input deregistered from {}".format(scene))

    def __repr__(self):
        return ("<ControlSet ({0}) >".format(len(self.axes)))
