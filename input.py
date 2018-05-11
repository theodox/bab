import org.babylonjs.api as api
import logging
import math
logger = logging.getLogger(__name__)


PRESS = api.ActionManager.OnKeyDownTrigger
RELEASE = api.ActionManager.OnKeyUpTrigger


def keystroke(key, press_release, fn):
    return api.ExecuteCodeAction({'trigger': press_release, 'parameter': key}, fn)


class KeyAxis:

    AXES = {}

    def __init__(self, name, mgr, positiveKey, negativeKey, gain=2, decay=0.5):
        self.value = 0
        self.lower = -1
        self.upper = 1
        self.positive_key = positiveKey
        self.negative_key = negativeKey
        self._pos = False
        self._neg = False
        self.gain = gain
        self.decay = decay
        self.name = name

        mgr.registerAction(keystroke(self.positive_key, PRESS, self._pos_dn))
        mgr.registerAction(keystroke(self.positive_key, RELEASE, self._pos_up))
        mgr.registerAction(keystroke(self.negative_key, PRESS, self._neg_dn))
        mgr.registerAction(keystroke(self.negative_key, RELEASE, self._neg_up))

        logger.debug("registered {}" .format(self))
        KeyAxis.AXES[self.name] = self

    def update(self, timeslice):

        self.value += timeslice * self.gain * self._pos
        self.value -= timeslice * self.gain * self._neg

        if self._neg or self._pos:
            decay = 1 - math.pow(min(self.value, 1), 0.5) * self.decay * timeslice
            decay = min(decay, abs(self.value))
            math.copysign(decay, self.value)
            self.value -= decay
            self.value = min(self.upper, max(self.lower, self.value))

        if self.value:
            logger.warn("+:{} -{}  v:{}".format(self._neg, self._pos, self.value))

    def _neg_up(e):
        self._neg = False

    def _pos_up(e):
        self._pos = False

    def _neg_dn(e):
        self._neg = True

    def _pos_dn(e):
        self._pos = True
 
    @classmethod
    def get(cls, name):
        return cls.AXES[name]

    def __repr__(self):
        return ("<KeyAxis {0} {1}>".format(self.name, self.value))
