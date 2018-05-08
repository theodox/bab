import org.babylonjs.api as api
import logging
import math
logger = logging.getLogger(__name__)


class KeyState:

    def __init__(self, mgr):
        self.keys = {}
        mgr.registerAction(api.ExecuteCodeAction([mgr.OnKeyDownTrigger, self._keydown]))
        mgr.registerAction(api.ExecuteCodeAction([mgr.OnKeyUpTrigger, self._keyup]))

    def _keydown(self, event):
        self.keys[event.source.key] = evt.sourceEvent.type == "keydown"
        logger.debug("down: ", event.source.key)

    def _keyup(self, event):
        self.keys[event.source.key] = not (evt.sourceEvent.type == "keyup")
        logger.debug("up: ", event.source.key)


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
          
        fn = api.ExecuteCodeAction(
                {
                'trigger': BABYLON.ActionManager.OnKeyUpTrigger,
                'parameter': self.positive_key
                },
                self._pos_up
                )
        mgr.registerAction(fn)  

        fn = api.ExecuteCodeAction(
                {
                'trigger': BABYLON.ActionManager.OnKeyDownTrigger,
                'parameter': self.positive_key
                },
                self._pos_dn
                )
        mgr.registerAction(fn) 

        negfn = api.ExecuteCodeAction(
                {
                'trigger': BABYLON.ActionManager.OnKeyUpTrigger,
                'parameter': self.negative_key
                },
                self._neg_up
                )
        mgr.registerAction(negfn)  


        negfn2 = api.ExecuteCodeAction(
                {
                'trigger': BABYLON.ActionManager.OnKeyDownTrigger,
                'parameter': self.negative_key
                },
                self._neg_dn
                )
        mgr.registerAction(negfn2)  

        logger.debug("registered {}" .format(self))
        KeyAxis.AXES[self.name] = self

    def update(self, timeslice):
        if self._neg and self._pos:
            self._neg = self._pos = False

        self.value += timeslice * self.gain * self._pos
        self.value -= timeslice * self.gain * self._neg

        if self._neg or self._pos:
            decay = 1 - math.pow(min(self.value, 1), 0.5) * self.decay * timeslice
            decay = min(decay, abs(self.value))
            math.copysign(decay, self.value)
            self.value -= decay
            self.value = min(self.upper, max(self.lower, self.value))
            self._pos = False
            self._neg = False

        if self.value:
            logger.warn("+:{} -{}  v:{}".format(self._neg, self._pos, self.value))

    def _keydown(self, event):
        logger.debug("key event: {}".format(event))
        self._pos = self._pos or event.sourceEvent.key == self.positive_key
        self._neg = self._neg or event.sourceEvent.key == self.negative_key

    def _neg_up(e):
        print ("neg up")

    def _pos_up(e):
        print( "pos up")

    def _neg_dn(e):
        print ("neg dn")

    def _pos_dn(e):
        print( "pos dn")


    @classmethod
    def get(cls, name):
        return cls.AXES[name]

    def __repr__(self):
        return ("<KeyAxis {0} {1}>".format(self.name, self.value))