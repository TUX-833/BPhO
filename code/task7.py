import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import constants as const
import math


class Task7Grapher:
    def __init__(self):
        self.mass = 9.1094 * 10**-31
        self.maxQNum = 3
        self.a = 53/99 * 10**-9


    def particleInnaBoxEnergy(self, a, num):
        energies = []
        for n in np.linspace(0,num):
            energies.append(((const.hbar**2 * math.pi**2 * n**2)/(2*self.mass*a**2))/const.e)
        return energies

    def particleInnaBoxProb(self, a, n):
        probs = []
        for x in np.linspace(0, a, 200, endpoint=False):
            probs.append((math.sqrt(2/a)*math.sin((n*math.pi*x)/a))**2)
        return probs

    def getGraph(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 5))

        xdata = [n for n in np.linspace(0, self.maxQNum)]
        ydata = self.particleInnaBoxEnergy(self.a, self.maxQNum)

        df = pd.DataFrame({"x": xdata, "y": ydata}); df.plot.line("x","y", legend=False, grid=True, ax = ax1, xlim=(0,3), ylim=0, linestyle = '--', xticks = np.linspace(0,3,4))
        ax1.set_xlabel("Quantum number"); ax1.set_ylabel("Energy / eV"); ax1.set_title(f"Particle in a box energy\nm = {round(self.mass/10**-31, 3)}kg*10⁻³¹\nside length = {round(self.a/10**-9, 3)}nm")

        xdata = [x*10**10 for x in np.linspace(0, self.a, 200, endpoint=False)]
        ydata = [self.particleInnaBoxProb(self.a, n) for n in np.linspace(1,3,3)]

        n = 1
        for yplot in ydata:
            df = pd.DataFrame({"x": xdata, f"n = {n}": yplot}); df.plot.line("x", f"n = {n}", grid=True, ax = ax2, xlim=0, ylim=0); n+=1
        ax2.set_xlabel("x / anstrongs"); ax2.set_ylabel("Probability density"); ax2.set_title(f"Particle in a box\nm = {round(self.mass/10**-31, 3)}kg*10⁻³¹\nside length = {round(self.a/10**-9, 3)}nm")

        if __name__ != "__main__":
            plt.close()
        return fig
    
if __name__ == "__main__":
    graph = Task7Grapher()
    graph.getGraph()
    plt.show()
