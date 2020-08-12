from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.animation import FuncAnimation
from PyQt5 import QtCore
import numpy as np


class AnimatedMplCanvas(FigureCanvas):

    runAgain = QtCore.pyqtSignal()

    def __init__(self, parent=None, demoFlag=False):
        # creating the main figure
        self.fig = Figure()
        self.fig.set_tight_layout(True)
        self.readyToDraw = False
        self.readyToRunAgain = True
        self.DMode = demoFlag

        # setting values for scaling
        self.voltsScaleLimits = ((-0.08, 0.08), (-0.2, 0.2), (-0.4, 0.4),
                                 (-0.8, 0.8), (-2, 2), (-4, 4), (-8, 8),
                                 (-20, 20), (-40, 40), (-80, 80),
                                 (-200, 200), (-400, 400))
        
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

        self.vPDiv = ("20 mV", "50 mV", "100 mV", "200 mV", "500 mV",
                      "1 V", "2 V", "5 V", "10 V", "20 V", "50 V", "100 V")
        
        self.sPDiv = ("2 ns", "4 ns", "10 ns", "20 ns", "40 ns", "100 ns",
                      "200 ns", "400 ns", "1 us",
                      "2 us", "4 us", "10 us", "20 us", "40 us", "100 us",
                      "200 us", "400 us", "1 ms",
                      "2 ms", "4 ms", "10 ms", "20 ms", "40 ms", "100 ms",
                      "200 ms", "400 ms", "1 s",)

        self.vPDiv_num = (20000, 50000, 100000, 200000,
                          500000, 1000000, 2000000, 5000000,
                          10000000, 20000000, 50000000, 100000000)        

        self.sPDiv_num = (500000000000, 250000000000, 100000000000,
                          50000000000, 25000000000, 10000000000,
                          5000000000, 2500000000, 1000000000,
                          500000000, 250000000, 100000000,
                          50000000, 25000000, 10000000,
                          5000000, 2500000, 1000000, 500000,
                          250000, 100000, 50000,
                          25000, 10000, 5000, 2500, 1000)

        self.currentVoltsScaleNumber = {"CH1": 3, "CH2": 3}

        self.currentSecondsScaleNumber = 17
        
        self.channelNum = {"CH1": 0, "CH2": 1}

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
        self.animation_is_running = False
        if self.DMode is False:
            self.anim = FuncAnimation(self.fig, self.animate,
                                      interval=20, blit=True)
        else:
            self.anim = FuncAnimation(self.fig, self.demo_animate,
                                      interval=20, blit=True)

        self.rescale_axes()

        # drawing data
        self.drawDataX = []
        self.drawDataY_1 = []
        self.drawDataY_2 = []

    # animation function: updating plot data
    def animate(self, i):
        if self.animation_is_running:
            if self.channel_is_enabled["CH1"]:
                if self.readyToDraw:
                    self.lines["CH1"].set_data(self.drawDataX,
                                               self.drawDataY_1)
                    self.lines["CH2"].set_data(self.drawDataX,
                                               self.drawDataY_2)
                    self.readyToDraw = False
                    self.animation_is_running = False
                    if self.readyToRunAgain is True:
                        self.runAgain.emit()
            if self.channel_is_enabled["CH2"]:
                if self.readyToDraw:
                    self.lines["CH2"].set_data(self.drawDataX,
                                               self.drawDataY_2)
                    self.readyToDraw = False
                    self.animation_is_running = False
                    if self.readyToRunAgain is True:
                        self.runAgain.emit()
        return tuple(self.lines.values())

    # demo animation function: updating plot data
    def demo_animate(self, i):
        if self.animation_is_running:
            x = np.linspace(-5,5,20)
            y = np.random.rand(20)-0.5
            y2 = np.random.rand(20)-0.5
            if self.channel_is_enabled["CH1"]:
                self.lines["CH1"].set_data(x,y)
            if self.channel_is_enabled["CH2"]:
                self.lines["CH2"].set_data(x,y2)
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
            self.axesDict[ch_name].tick_params(labelbottom=False,
                                               labelleft=False,
                                               labelright=False)

        self.draw()
        self.flush_events()

    def enable_drawing(self):
        self.readyToDraw = True

    def stopFurtherCapture(self):
        self.readyToRunAgain = False
