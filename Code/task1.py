import numpy as np
import matplotlib.pyplot as plt
import random as ran

class Task1Walk:
    def __init__(self, numPlots = 50, num = 1000):
        self.num = num
        self.length = 1
        self.numPlots = numPlots # MAX = 1000 walks
        self.x = 0
        self.y = 0

        self.maxCol = int("ffffff", 16)
        

    def getGraph(self):
        fig, ax = plt.subplots(1, figsize = (6, 5))

        for i in range(self.numPlots):
            xs = []
            ys = []

            for _ in range(self.num):
                angle = ran.uniform(0,2*np.pi)
                self.x += self.length*np.cos(angle)
                xs.append(self.x)
                self.y += self.length*np.sin(angle)
                ys.append(self.y)

            col = int(i/self.numPlots * self.maxCol)

            col = "#" + hex(col).replace("0x", "").zfill(6)

            ax.plot(xs, ys, color = col)

            self.x=0
            self.y=0
        
        ax.set_ylabel("Y Displacement")
        ax.set_xlabel("X Displacement")
        ax.set_title("Random Walk") 
        ax.grid(True)

        if __name__ != "__main__":
            plt.close()
        return fig
    
if __name__ == "__main__":
    graph = Task1Walk()
    graph.getGraph()
    plt.show()