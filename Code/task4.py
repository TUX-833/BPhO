import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import constants as const
import math

class Task4Grapher:
    def __init__(self, workFunc):
        self.startFreq = 0
        self.endFreq = 201
        self.deltaFreq = 1
        self.workFunc = workFunc

    def photoelectric(self, W):
        voltages = []
        for frequency in range(self.startFreq, self.endFreq, self.deltaFreq):
            frequency = frequency*(10**13)
            voltages.append(frequency*(const.h/const.e) - W/const.e)
        return voltages

    def getGraph(self):
        fig, ax = plt.subplots(1, figsize = (6, 5))
        xdata = [frequency*(10**13) for frequency in range(self.startFreq, self.endFreq, self.deltaFreq)]

        W = self.workFunc*(const.e)
        ydata = self.photoelectric(W)
        cutoffF = W/const.h

        df = pd.DataFrame({"x": xdata, "y": ydata}); graph = df.plot.line("x","y",legend=False, grid=True, ax = ax, xlim=(0,2*10**15), ylim=(-5,5))

        ax.set_xlabel("Frequency / Hz"); ax.set_ylabel("Stopping Voltage / V"); ax.set_title(f"Photoelectric effect: W = {W/const.e}eV"); graph.set_yticks(np.linspace(-5,5,11))
        ax.vlines([4*10**14, 5.1*10**14, 5.7*10**14, 6.7*10**14, 7.9*10**14, cutoffF], ymin=-6, ymax=6, colors=['#FF0000', "#FBFF00", "#00FF0D", "#1900FF", "#7F00FF", graph.lines[0].get_color()], linestyles='--')
        ax.annotate(f"Threshold Freq: {cutoffF/10**15:.2f}", xy=(cutoffF, 0), xytext=(cutoffF+(0.25*10**15), -2), fontsize=10,
            arrowprops=dict(facecolor = graph.lines[0].get_color(), shrink = 0.01))

        if __name__ != "__main__":
            plt.close()       
        return fig

if __name__ == "__main__":
    graph = Task4Grapher(4.3)
    graph.getGraph()
    plt.show()