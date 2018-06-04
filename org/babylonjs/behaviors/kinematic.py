from org.babylonjs.behaviors import Tickable
import org.babylonjs.api as api
from org.transcrypt.stubs.browser import __pragma__
import logging
logger = logging.getLogger(__name__)
import math

__pragma__('alias', 'babylon_aliases')


class KinematicBehavior(Tickable):
    """
    Given two control objects(ie, InputAxis objects or some thing similar),
    with a value, move the pawn using those inputs multiplied by the supplied
    response values in the XZ plane
    """

    def __init__(self, scene, x_axis, z_axis, x_response=1, z_response=1, name=None):
        super().__init__(scene, name)
        self.x_axis = x_axis
        self.z_axis = z_axis
        self.x_response = x_response
        self.z_response = z_response
        self.vector = api.Vector3(0, 0, 0)

    def tick(self, deltatime):
        self.vector.copyFromFloats(
            self.x_axis.value * self.x_response,
            self.scene.gravity.y,
            self.z_axis.value * self.z_response)
        self.vector *= deltatime  # __:fopov
        self.owner.move_with_collisions(self.vector)


class SteeringBehavior(Tickable):
    """
    Given two control objects(ie, InputAxis objects or some thing similar),
    with a value, move the pawn using those inputs multiplied by the supplied
    response values in the XZ plane
    """

    TWOPI = math.pi * 2.0

    def __init__(self, scene, steering, throttle, steering_response=1, throttle_response=1, name=None):
        super().__init__(scene, name)
        self.steering = steering
        self.throttle = throttle
        self.steering_response = steering_response
        self.throttle_response = throttle_response
        self._yaw = 0.0
        self.vector = api.Vector3(0, -9.8, 0)
        self._speed = 0.0

    @property
    def yaw(self):
        return self._yaw

    @yaw.setter
    def yaw(self, y):
        self._yaw = y

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, s):
        self._speed = s

    def tick(self, deltatime):
        self._yaw += self.steering.value * self.steering_response
        self._yaw = self._yaw % self.TWOPI
        self._speed += self.throttle.value * self.throttle_response

        self.vector.x = math.sin(self.yaw)
        self.vector.z = math.cos(self.yaw)

        self.vector *= (self._speed * deltatime)  # __:fopov
        self.owner.add_rotation(0, self.steering.value * self.steering_response, 0)
        self.owner.move_with_collisions(self.vector)

    def __str__(self):
        return "<{}: '{}' yaw:{} speed {}>".format(
            self.__class__.__name__,
            self.name,
            self._yaw,
            self._speed)


__pragma__('noalias', 'babylon_aliases')
