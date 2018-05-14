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

    def delta(self):
        return self.last_frame_time

    def time(self):
        return self.last_tick

    @classmethod
    def get(cls, scene):
        if not cls.INSTANCE:
            cls.INSTANCE = cls(scene)
        return cls.INSTANCE


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
        __pragma__('jsiter')
        for k in dct:
            v = dct[k]
            if v.observable:
                __pragma__('nojsiter')
                target_names = cls.name_patterns(k)
                obs_name = target_names.intersection(cls.OBSERVABLES)
                if len(obs_name) != 1:
                    # somebody has decorated a function which is not a known observable
                    raise Exception("No observable found for function {}".format(k))
                observables[obs_name[0]] = k
                __pragma__('jsiter')
        __pragma__('nojsiter')

        dct['_observables'] = observables

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


class BehaviorBase(metaclass=BehaviorMeta):
    """base class for behaviors"""

    def __init__(self, scene):
        self.owner = None
        '''the object this behavior controls'''
        self.scene = scene
        '''the scene handling any events we need to track'''
        self._handlers = {}
        '''an internal list of event observers we need to manage'''

    def attach(self, target):
        """
        attach this behavior to object <target>
        """
        self.owner = target
        for k, v in self._observables.items():
            observable = getattr(self.scene, k)
            observer = getattr(self, v)  # ensures the observer is bound as an instancemethod
            self._handlers[k] = observable.add(observer)
            logger.debug("{} added {} to {}".format(self.__class__.__name__, observer, target))

    def detach(self):
        """
        Remove this behavior from target
        """
        for k, observer in self._handlers.items():
            observable = getattr(self.scene, k)
            observable.remove(observer)
            logger.debug("{} removed {}".format(self.__class__.__name__, k))
        self.owner = None


class Tickable (BehaviorBase, metaclass=BehaviorMeta):
    """
    Base class for behaviors that tick every frame.  Override the `tick()` method
    in derived classes to update functionality
    """

    def __init__(self, scene):
        super().__init__(scene)
        self.time = Heartbeat.get(scene)
        self.counter = 0

    @observable
    def before_animations(self, *args):
        self.tick(self.time.delta())

    def tick(self, delta):
        """override in derived classes to add functionality.  Delta is in fractional seconds"""
        pass
