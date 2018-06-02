import logging
from org.babylonjs.api import Tools
from org.transcrypt.stubs.browser import __pragma__

logger = logging.getLogger(__name__)


class Heartbeat:
    """
    Provides a standardized way to share frame deltas for a given scene.

    It's intended that all Tickables share one of these, at least one per scene
    """
    INSTANCES = dict()
    HISTORY_FRAMES = 30

    def __init__(self, scene):
        self.delta_time = 0
        self.last_tick_time = 0
        # add the observer to the head of the queue -- which means we have
        # to turn on all the masks
        self.observer = scene.onBeforeAnimationsObservable.add(self.tick, -1, True)
        self.history = [0.1666 for i in range(self.HISTORY_FRAMES)]
        self.history_pointer = 0
        self.elapsed_time = 0

    def tick(self):
        """ratchet the internal timer"""
        now = Tools.Now
        self.delta_time = (now - self.last_tick_time) * .001
        self.elapsed_time += self.delta_time
        self.last_tick_time = now
        self.history[self.history_pointer] = self.delta_time
        self.history_pointer += 1
        self.history_pointer = self.history_pointer % self.HISTORY_FRAMES

    def delta(self):
        """returns the last frame delta"""
        return self.delta_time

    def elapsed(self):
        """returns the elapsed time in seconds since the hearbeat ticker began"""
        return self.elapsed_time

    def running_average(self):
        """average of recent frame times"""
        return sum(self.history) / float(self.HISTORY_FRAMES)

    @classmethod
    def get(cls, scene):
        """ gets the heartbeat associated with this scene"""
        if not cls.INSTANCES.get(scene):
            cls.INSTANCES[scene] = cls(scene)
        return cls.INSTANCES[scene]


def observable(fn):
    """
    use this decorator to identify oberserver functions on a Behavior
    """
    def obs(*args):
        return fn(*args)

    obs.observable = True
    obs.inner = fn
    return obs


class BehaviorMeta:
    """
    This metaclass looks for functions that are marked with an @observable  decorator and 
    sets them up to be attached/detached when a class using the meta is attached to an object
    """

    OBSERVABLES = set([
        'onAfterActiveMeshesEvaluationObservable',
        'onAfterAnimationsObservable',
        'onAfterCameraRenderObservable',
        'onAfterDrawPhaseObservable',
        'onAfterParticlesRenderingObservable',
        'onAfterPhysicsObservable',
        'onAfterRenderObservable',
        'onAfterRenderTargetsRenderObservable',
        'onAfterSpritesRenderingObservable',
        'onAfterStepObservable',
        'onBeforeActiveMeshesEvaluationObservable',
        'onBeforeAnimationsObservable',
        'onBeforeCameraRenderObservable',
        'onBeforeDrawPhaseObservable',
        'onBeforeParticlesRenderingObservable',
        'onBeforePhysicsObservable',
        'onBeforeRenderObservable',
        'onBeforeRenderTargetsRenderObservable',
        'onBeforeSpritesRenderingObservable',
        'onBeforeStepObservable',
        'onCameraRemovedObservable',
        'onDataLoadedObservable',
        'onDisposeObservable',
        'onGeometryRemovedObservable',
        'onKeyboardObservable',
        'onLightRemovedObservable',
        'onMeshRemovedObservable',
        'onNewCameraAddedObservable',
        'onNewGeometryAddedObservable',
        'onNewLightAddedObservable',
        'onNewMeshAddedObservable',
        'onNewTransformNodeAddedObservable',
        'onPointerObservable',
        'onPreKeyboardObservable',
        'onPrePointerObservable',
        'onReadyObservable',
        'onRenderingGroupObservable',
        'onTransformNodeRemovedObservable'
    ])

    def __new__(cls, name, bases, dct):

        observables = dict()
        # the pragmas here are necessary to work around Transcrypt issue 526
        # 'dct' is not a python dict.   We loop over the names in the class
        # looking for those marked as observable, look up the corresponding
        # observable name, and store them as a class level dictionary

        # collect the observable dictionaries from the parent clases
        for x in cls.iter_bases(bases):
            parent_observables = getattr(x, "_observables")
            observables.update(parent_observables)

        __pragma__('jsiter')  # transcrypt no. 526
        for k in dct:
            v = dct[k]
            if v.observable:
                target_names = cls.name_patterns(k)
                obs_name = target_names.intersection(cls.OBSERVABLES)
                if len(obs_name) != 1:
                    # somebody has decorated a function which is not a known observable
                    raise Exception("No observable found for function {}".format(k))
                observables[obs_name[0]] = k
        __pragma__('nojsiter')

        dct['_observables'] = observables
        # todo -- how to make this work recursively?

        return type.__new__(cls, name, bases, dct)

        # these methods will be attached to all classes using this metaclass

    @classmethod
    def name_patterns(cls, fn_name):
        """
        Converts a python function name to an observablename

             onPrePointerObservable  -> onPrePointerObservable
             prePointer -> onPrePointerObservable
             on_pre_pointer_observable -> onPrePointerObservable
             pre_ppointer -> onPrePointerObservable

        """
        tokens = fn_name.split('_')
        first, rest = tokens[0], tokens[1:]
        camel = first + ''.join(word.capitalize() for word in rest)
        capCamel = first.capitalize() + ''.join(word.capitalize() for word in rest)
        return set([fn_name, "on" + fn_name.capitalize() + "Observable",
                    camel, "on" + capCamel + "Observable"])

    @classmethod
    def iter_bases(cls, bases):
        """recursively yield the class tree so we can get the observables stored there"""
        for b in bases:
            for item in cls.iter_bases(b.__bases__):
                yield item
            yield b


class BehaviorBase(metaclass=BehaviorMeta):
    """base class for behaviors"""
    UUID = 0

    def __init__(self, scene, name=None):
        self.owner = None
        '''the object this behavior controls'''
        self.scene = scene
        '''the scene handling any events we need to track'''
        self._handlers = {}
        '''an internal list of event observers we need to manage'''
        BehaviorBase.UUID += 1
        self.name = name or "{}_{}".format(self.__class__.__name__, BehaviorBase.UUID)

    def attach(self, target):
        """
        attach this behavior to object <target>
        """
        self.owner = target
        for k, v in self._observables.items():
            observable = getattr(self.scene, k)
            observer = getattr(self, v)  # ensures the observer is bound as an instancemethod
            self._handlers[k] = observable.add(observer)
            logger.debug("added {} to {}.{}".format(self, target.name or target.py_name or target.js_name, k))

    def detach(self):
        """
        Remove this behavior from target
        """
        for k, observer in self._handlers.items():
            observable = getattr(self.scene, k)
            observable.remove(observer)
            logger.debug("removed {}".format(self, k))
        self.owner = None

    def __str__(self):
        return "<{}: '{}'>".format(self.__class__.__name__, self.name)


class Tickable (BehaviorBase, metaclass=BehaviorMeta):
    """
    Base class for behaviors that tick every frame.  Override the `tick()` method
    in derived classes to update functionality
    """

    def __init__(self, scene, name=None):
        super().__init__(scene, name)
        self.time = Heartbeat.get(scene)
        self.counter = 0

    @observable
    def before_animations(self, *args):
        """
        This is forwarded to the tick() function as a convenience so 
        there are not competing ways to get the delta time.  Derived classes 
        should not override it.
        """
        self.tick(self.time.delta())

    def tick(self, delta):
        """override in derived classes to add functionality.  Delta is in fractional seconds"""
        logger.debug("ticked {}".format(delta))
