import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import constants as const

class Task8Diagramer:
    def __init__(self, theta, phi):
        self.thetaD = theta
        self.thetaR = theta/180 * np.pi

        self.phiD = phi
        self.phiR = phi/180 * np.pi

        self.hypontenuese = 3/4

    def getPoint(self, angleR):
        m = np.tan(np.pi/2 - angleR)
        x = np.sqrt(self.hypontenuese**2/(m**2 + 1))
        y = m * x

        return (x, y) if angleR >= 0 else (-x, -y)

    def getDiagram(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 5))
        ax1.set_xlim(-1,1); ax1.set_ylim(-1,1); ax2.set_xlim(-1,1); ax2.set_ylim(-1,1)
        ax1.set_xticks([]); ax1.set_yticks([]); ax2.set_xticks([]); ax2.set_yticks([])

        ax1.set_title(f"Detector A"); ax2.set_title(f"Detector B")

        ax1.vlines(0, 0, self.hypontenuese, "#58A6FF", "dashed"); ax2.vlines(0, 0, self.hypontenuese, "#58A6FF", "dashed")

        pointAX = self.getPoint(self.thetaR)
        ax1.annotate("", xy=pointAX, xytext=(0, 0), fontsize=10,
            arrowprops=dict(facecolor = "lime", shrink = 0.01))
        pointAY = self.getPoint(-np.pi/2 + self.thetaR)        
        ax1.annotate("", xy=pointAY, xytext=(0, 0), fontsize=10,
            arrowprops=dict(facecolor = "lime", shrink = 0.01))
        
        pointBX = self.getPoint(self.phiR)
        ax2.annotate("", xy=pointBX, xytext=(0, 0), fontsize=10,
            arrowprops=dict(facecolor = "blue", shrink = 0.01))
        pointBY = self.getPoint(-np.pi/2 + self.phiR)        
        ax2.annotate("", xy=pointBY, xytext=(0, 0), fontsize=10,
            arrowprops=dict(facecolor = "blue", shrink = 0.01))

        if __name__ != "__main__":
            plt.close()
        return fig
    
    def calculateProbs(self):
        classic = 1 - np.cos(self.thetaR)**2 * np.cos(self.phiR)**2 - np.sin(self.thetaR)**2 * np.sin(self.phiR)**2
        QM = np.sin(self.phiR - self.thetaR)**2

        return classic, QM

if __name__ == "__main__":
    graph = Task8Diagramer(-30, 30)
    graph.getDiagram()
    plt.show()