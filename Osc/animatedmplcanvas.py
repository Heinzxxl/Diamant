from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.animation import FuncAnimation
import numpy as np


class AnimatedMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        # creating the main figure
        self.fig = Figure()
        self.fig.set_tight_layout(True)

        # setting values for scaling
        self.voltsScaleLimits = ((-0.08, 0.08), (-0.2, 0.2), (-0.4, 0.4),
                                 (-0.8, 0.8), (-2, 2), (-4, 4), (-8, 8),
                                 (-20, 20), (-40, 40), (-80, 80),
                                 (-200, 200), (-400, 400))
        self.vPDiv = ("20 mV", "50 mV", "100 mV", "200 mV", "500 mV",
                      "1 V", "2 V", "5 V", "10 V", "20 V", "50 V", "100 V")
        self.currentVoltsScaleNumber = {"CH1": 5, "CH2": 5}

        self.secondsScaleLimits = ((-1e-08, 1e-08), (-2e-08, 2e-08),
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
                                   (-1, 1), (-2, 2), (-5, 5))
        self.currentSecondsScaleNumber = 25

        # initialising FigureCanvas, adding axes and lines
        super().__init__(self.fig)
        self.setParent(parent)

        self.axes = self.fig.add_subplot(111)
        self.axes2 = self.axes.twinx()
        self.fig.add_axes(self.axes2)
        self.axesDict = {"CH1": self.axes, "CH2": self.axes2}

        self.channel_is_enabled = {"CH1": False, "CH2": False}
        self.colors = {"CH1": "Blue", "CH2": "Red"}

        self.lines = {}
        for ch_name in self.axesDict.keys():
            self.lines[ch_name] = \
                self.axesDict[ch_name].add_line(Line2D([], [],
                                                color=self.colors[ch_name]))
            self.lines[ch_name].set_visible(False)
        self.saved_lines_data = {"CH1": [[], []], "CH2": [[], []]}
        # creating animation
        self.animation_is_running = True
        self.anim = FuncAnimation(self.fig, self.animate,
                                  interval=20, blit=True)

        self.rescale_axes()

    # animation function: updating plot data
    def animate(self, i):
        if self.animation_is_running:
            x = [-2, -1, 0, 1, 2]
            y = 2 * np.random.rand(5) - 1
            y2 = 2 * np.random.rand(5) - 1
            if self.channel_is_enabled["CH1"]:
                self.lines["CH1"].set_data(x, y)
            if self.channel_is_enabled["CH2"]:
                self.lines["CH2"].set_data(x, y2)
        return tuple(self.lines.values())

    # making lines visible
    def enable_channel(self, ch_name):
        self.lines[ch_name].set_visible(True)
        if not self.animation_is_running:
            self.lines[ch_name].set_data(self.saved_lines_data[ch_name])
        self.channel_is_enabled[ch_name] = True

    # making lines non-visible
    def disable_channel(self, ch_name):
        self.lines[ch_name].set_visible(False)
        if not self.animation_is_running:
            self.saved_lines_data[ch_name] = self.lines[ch_name].get_data()
        self.channel_is_enabled[ch_name] = False

    # rescaling axes
    def rescale_axes(self):
        for ch_name in self.axesDict.keys():
            self.axesDict[ch_name].clear()
        self.axes.grid(True)

        ax_sec_limits = self.secondsScaleLimits[self.currentSecondsScaleNumber]
        self.axes.set_xlim(ax_sec_limits)
        ax_xstart, ax_xstop = ax_sec_limits
        major_xticks = np.linspace(ax_xstart, ax_xstop, num=11)
        self.axes.set_xticks(major_xticks)

        for ch_name in self.axesDict.keys():
            ax_volts_limits = \
                self.voltsScaleLimits[self.currentVoltsScaleNumber[ch_name]]
            self.axesDict[ch_name].set_ylim(ax_volts_limits)
            ax_ystart, ax_ystop = ax_volts_limits
            major_yticks = np.linspace(ax_ystart, ax_ystop, num=9)
            self.axesDict[ch_name].set_yticks(major_yticks)

        self.draw()
        self.flush_events()
