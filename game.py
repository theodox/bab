from org.babylonjs import Engine, Observable, Vector3, Space
import time
import random

class Game:

    def __init__(self, engine):

        self.engine = engine
        engine.onBeginFrameObservable.add(self.beforeRender)
        self.started = time.time()
        self.last_frame = self.started
        self.pick_map = dict()
        self.paused = False
        engine.scenes[0].cameraToUseForPointers = engine.scenes[0].cameras[0]
        window.addEventListener("click", self.click_handler)

    def add_actor(self, tmp):
        self.pick_map[tmp.sphere] = tmp

    def update(self):
        now = time.time()
        delta = (now - self.last_frame)
        if not self.paused:
            for actor in self.pick_map.values():
                actor.tick(delta)
        self.last_frame = now

    def beforeRender(self):
        pass
        #print(self.last_frame)

    def click_handler(self, val):
        s = self.engine.scenes[0]

        if s:
            result =  s.pick(s.pointerX, s.pointerY)
            picked = self.pick_map.get(result.pickedMesh)
            console.log("clicked on:" + result.pickedMesh)
            if picked:
                picked.delta = Vector3.Up()
                self.paused = not self.paused

class Actor:

    def __init__(self):
        pass

    def tick(self, interval):
        pass


class SphereActor (Actor):
    def __init__(self, sphere):
        self.sphere = sphere
        self.delta = Vector3(random.random(),
                random.random(),
                random.random()).scale(random.random() * 0.25)
        super().__init__(self)

    def tick(self, interval):
        self.sphere.translate(self.delta.scale(interval), Space.WORLD)
        super().tick(self, interval)
