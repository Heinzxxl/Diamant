from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.animation import FuncAnimation
import numpy as np


class AnimatedMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.fig.set_tight_layout(True)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_ylim(-4, 4)
        self.axes.set_xlim(-2, 2)
        self.axes.grid(True)

        self.voltsScaleValues = [(-0.08, 0.08), (-0.2, 0.2), (-0.4, 0.4),
                                 (-0.8, 0.8), (-2, 2), (-4, 4), (-8, 8),
                                 (-20, 20), (-40, 40), (-80, 80),
                                 (-200, 200), (-400, 400)]
        self.currentVoltsScaleNumber = 5

        self.secondsScaleValues = [(-1e-08, 1e-08), (-2e-08, 2e-08),
                                   (-5e-08, 5e-08), (-1e-07, 1e-07),
                                   (-2e-07, 2e-07), (-5e-07, 5e-07),
                                   (-1e-06, 1e-06), (-2e-06, 2e-06),
                                   (-5e-06, 5e-06), (-1e-05, 1e-05),
                                   (-2e-05, 2e-05), (-5e-05, 5e-05),
                                   (-1e-04, 1e-04), (-2e-04, 2e-04),
                                   (-5e-04, 5e-04), (-1e-03, 1e-03),
                                   (-2e-03, 2e-03), (-5e-03, 5e-03),
                                   (-1e-02, 1e-02), (-2e-02, 2e-02),
                                   (-5e-02, 5e-02), (-1e-01, 1e-01),
                                   (-2e-01, 2e-01), (-5e-01, 5e-01),
                                   (-1, 1), (-2, 2), (-5, 5)]
        self.currentSecondsScaleNumber = 25

        super().__init__(self.fig)
        self.setParent(parent)
        self.lines = {}
        self.cachelines = {"CH1": [[], []], "CH2": [[], []]}

        self.anim = FuncAnimation(self.fig, self.animate,
                                  interval=20, blit=True)
        self.animation_is_running = True

        self.channel_is_enabled = {"CH1": False, "CH2": False}
        self.colors = {"CH1": "Blue", "CH2": "Red"}

    def animate(self, i):
        if self.animation_is_running:
            x = [-2, -1, 0, 1, 2]
            y = 2 * np.random.rand(5) - 1
            y2 = 2 * np.random.rand(5) - 3
            if self.channel_is_enabled["CH1"]:
                self.lines["CH1"].set_data(x, y)
            if self.channel_is_enabled["CH2"]:
                self.lines["CH2"].set_data(x, y2)
        return tuple(self.lines.values())

    def enable_channel(self, ch_name):
        self.lines[ch_name] = \
            self.axes.add_line(Line2D([], [], color=self.colors[ch_name]))
        if not self.animation_is_running:
            self.lines[ch_name].set_data(self.cachelines[ch_name])
        self.channel_is_enabled[ch_name] = True

    def disable_channel(self, ch_name):
        self.channel_is_enabled[ch_name] = False
        if not self.animation_is_running:
            self.cachelines[ch_name] = self.lines[ch_name].get_data()
        self.lines.pop(ch_name).remove()

    def rescale_axes(self):
        self.axes.set_ylim(self.voltsScaleValues[self.currentVoltsScaleNumber])
        self.axes.set_xlim(self.secondsScaleValues
                           [self.currentSecondsScaleNumber])
        self.draw()
