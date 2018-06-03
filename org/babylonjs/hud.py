import org.babylonjs.gui as gui

LEFT = gui.Control.HORIZONTAL_ALIGNMENT_LEFT
TOP = gui.Control.VERTICAL_ALIGNMENT_TOP


class HUDItem:

    def __init__(self, name, message):
        msg = gui.TextBlock(name, message)
        msg.textHorizontalAlignment = LEFT
        msg.paddingLeft = 12
        msg.paddingTop = 8
        msg.color = 'white'
        msg.height = '20px'

        self.msg = msg

    @property
    def text(self):
        return self.msg.text

    @text.setter
    def text(self, t):
        self.msg.text = t

    @property
    def color(self):
        return self.msg.color

    @color.setter
    def color(self, c):
        self.msg.color = c

    def hide(self):
        self.msg.isVisible = False

    def show(self):
        self.msg.isVisible = True


class FPSCounter(HUDItem):

    def __init__(self, engine):
        self.engine = engine
        super().__init__('fps', '0.0fps')
        self.engine.onBeginFrameObservable.add(self.update)

    def update(self):
        afps = int (self.engine.performanceMonitor.averageFrameTime)
        ms = str(afps)
        self.text = "{} ms".format(ms)
        if afps < 20:
            self.color = '#b0f442'
        elif afps < 31:
            self.color = 'yellow'
        else:
            self.color = 'red'


class HUD:

    def __init__(self):
        self.canvas = gui.AdvancedDynamicTexture.CreateFullscreenUI("hud")
        container = gui.StackPanel()
        container.horizontalAlignment = LEFT
        container.verticalAlignment = TOP
        container.fontSize = 12
        container.height = 1.0
        container.left = '1px'
        container.top = '1px'
        self.layout = container
        self.canvas.addControl(self.layout)

    def add(self, item):
        self.layout.addControl(item.msg)

    def remove(self, item):
        self.layout.removeControl(item.msg)

    def hide(self):
        self.canvas.isVisible = False

    def show(self):
        self.canvas.isVisible = True

    def flash(self, message):
        msg = HUDItem(message, message)
        self.add(msg)
        setTimeout(lambda: self.remove(msg), 2500)