from org.transcrypt.stubs.browser import window
from org.babylonjs.api import Tools, AssetTaskState
import logging
logger = logging.getLogger(__name__)


class AssetTask:
    """
    Base class for Python extensions to the AssetsManager task system

    Override the 'succeeded' method to handle data that has been loaded
    by the AssetsManager.  

    After the class is defined call register() as a class method. That will
    add the method 'add<ClassName>' to the AssetsManager prototype.  So,
    a class named 'ShaderTask'  will be available through a new method named
    'addShaderTask'
    """

    def __init__(self, name, url, *_):
        self.name = name
        self.url = url
        self.taskState = AssetTaskState.INIT
        self.isCompleted = False
        self.errorObject = None

        # as with the Javascript version, these are 
        # optional callback functions
        self.onError = None
        self.onSuccess = None

    @classmethod
    def register(cls):
        """register this class with the AssetsManager so it can be
        created in the same manner as built-in tasks"""
        def task_adder(name, url, *args):
            new_task = cls(name, url, *args)
            # 'this' will be supplied by AssetsManager
            this.tasks.append(new_task)
            return new_task

        # this has to go back to the window.BABYLON version -- importing via
        # Transcrypt does not work
        window.BABYLON.AssetsManager.prototype['add' + cls.__name__] = task_adder
        logger.debug("registered add{} with AssetsManager".format(cls.__name__))

    def succeeded(self, scene, data):
        """override in derived classes to handle data on load"""
        logger.debug('loaded: ' + self.url)
        logger.debug('data: \n' + data)

    def run(self, scene, onSuccess, onFail):
        """this just calls runTask for parity with the babylon api"""
        self.runTask(scene, onSuccess, onFail)

    def runTask(self, scene, onSuccess, onFail):
        """run this task"""
        self.state = AssetTask.RUNNING

        def success(data):
            try:
                self.succeeded(scene, data)
                self.taskState = AssetTaskState.DONE
                self.isCompleted = True
                if self.onSuccess:
                    self.onSuccess(self)  # this is not a membe function!
                onSuccess()

            except Exception as e:
                self.onErrorCallback(onError, "Task is done, error executing success callback(s)", e)
            
        def fail(request, exception):
            self.onErrorCallback(onFail, request.status, exception)
            onFail(failure)

        Tools.LoadFile(self.url, success, None, scene.database, False, fail)

    def onErrorCallback(self, onError, message, exception):
        self.taskState = AssetTaskState.ERROR
        self.errorObject = {'message': message, 'exception': exception } 
        if self.onError:
            self.onError(self, message, exception)
        onError()