import matplotlib.pyplot as plt
from scipy import constants as const
import numpy as np

class Task5Grapher:
    def __init__(self):
        self.Z = 1

    def getGraph(self):
        fig, ax = plt.subplots(1, figsize = (6, 5))

        photonE = lambda n, m: (-13.6/(n**2)) - (-13.6/(m**2))
        lamb = lambda n, m: ((8 * const.epsilon_0**2 * const.h**3 * const.c)/(const.m_e * self.Z**2 * const.e**4) * (1/m**2 - 1/n**2)**-1) / 10**-9

        lyman = [[lamb(n, 1) for n in range(2, 10)],[photonE(n, 1) for n in range(2, 10)]]
        balmer = [[lamb(n, 2) for n in range(3, 11)],[photonE(n, 2) for n in range(3, 11)]]
        paschen = [[lamb(n, 3) for n in range(4, 12)],[photonE(n, 3) for n in range(4, 12)]]
        brackett = [[lamb(n, 4) for n in range(5, 13)],[photonE(n, 4) for n in range(5, 13)]]
        pfund = [[lamb(n, 5) for n in range(6, 14)],[photonE(n, 5) for n in range(6, 14)]]
 
        ax.scatter(lyman[0], lyman[1], marker = "2", color = "magenta", label = "Lyman")
        ax.scatter(balmer[0], balmer[1], marker = "2", color = "red", label = "Balmer")
        ax.scatter(paschen[0], paschen[1], marker = "2", color = "blue", label = "Paschen")
        ax.scatter(brackett[0], brackett[1], marker = "2", color = "lime", label = "Brackett")
        ax.scatter(pfund[0], pfund[1], marker = "2", color = "white", label = "Pfund")

        ax.vlines(lyman[0], colors="magenta", ymin = 0, ymax = 14, linestyles= "dashed", lw= 0.7); ax.vlines(balmer[0], colors="red", ymin = 0, ymax = 14, linestyles= "dashed", lw= 0.7)
        ax.vlines(paschen[0], colors="blue", ymin = 0, ymax = 14, linestyles= "dashed", lw= 0.7); ax.vlines(brackett[0], colors="lime", ymin = 0, ymax = 14, linestyles= "dashed", lw= 0.7)
        ax.vlines(pfund[0], colors="white", ymin = 0, ymax = 14, linestyles= "dashed", lw= 0.7)

        ax.set_xlabel("Wavelength /nm")
        ax.set_ylabel("Photon Energy /eV")
        ax.legend()
        ax.grid(True)

        ax.set_ylim(0,14)
        ax.set_xlim(0,8000)

        ax.set_title("Hydrogenic Atom Photon Emmisions\nPhoton Energy vs Wavelength")
        
        if __name__ != "__main__":
            plt.close()
        return fig

if __name__ == "__main__":
    graph = Task5Grapher()
    graph.getGraph()
    plt.show()