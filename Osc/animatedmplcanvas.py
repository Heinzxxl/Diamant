from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.animation import FuncAnimation
import numpy as np


class AnimatedMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        fig.set_tight_layout(True)
        self.axes = fig.add_subplot(111)
        self.axes.set_ylim(-4, 4)
        self.axes.set_xlim(0, 4)
        self.axes.grid(True)

        self.line, = self.initial_plot()

        super().__init__(fig)
        self.setParent(parent)

        self.anim = FuncAnimation(fig, self.animate,
                                  init_func=self.init_animation,
                                  interval=20, blit=True)
        self.animation_is_running = True

    def initial_plot(self):
        return self.axes.plot(np.random.rand(5))

    def init_animation(self):
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        x = [0, 1, 2, 3, 4]
        y = 2 * np.random.rand(5) - 1
        self.line.set_data(x, y)
        return self.line,
