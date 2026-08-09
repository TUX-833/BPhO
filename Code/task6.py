from vpython import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import constants as const
import math
 
class Task6Simulator:
    def __init__(self):
        #set up vpython output
        self.screen = canvas(width=1000, height=1000, background=color.black)
        self.screen.select()

        self.R = 65 * 10**-3
        self.ds = [(0.213 * 10**-9, 1.0), (0.123 * 10**-9, 0.6)]
        self.v = 5000
        self.ringThickness = 0.0005
        self.running = True

        #create sphere and beginning rings
        self.diffractionSphere = sphere(radius = self.R, opacity = 0.15)
        
        #user input
        vSlider = slider(bind = self.changeVoltage, min=1, max=5, step=1, value = self.v, id='x')
        self.vTxt = wtext()

        

    def getGraph(self):
        startV = 1000
        endV = 5000
        d = 0.123 * 10**-9

        fig, ax = plt.subplots(1, figsize = (6, 5))
        
        Vs = np.linspace(startV, endV)
        xdata = []
        for v in Vs:
            lamb = const.h/math.sqrt(2*const.m_e*const.e*v) 
            phi = 2 * math.asin((lamb)/(2 * d))
            sinPhiBy2 = math.sin(phi/2)
            xdata.append(sinPhiBy2)

        ydata = [1/math.sqrt(x) for x in Vs]


        df = pd.DataFrame({"x": xdata, "y": ydata}); graph = df.plot.line("x","y",legend=False, grid=True, ax = ax, xlim=(0), ylim=(0))

        ax.set_xlabel("Sin(1/Φ)"); ax.set_ylabel("1/√V"); ax.set_title("1/√V against Sin(1/Φ)\nfor V between 1kV and 5kV")

        if __name__ != "__main__":
            plt.close()      
        return fig

    def createRings(self): 
        lamb = const.h/math.sqrt(2*const.m_e*const.e*self.v) 

        for d, weight in self.ds:
            maxN = int((2 * d)/lamb * math.sin(math.pi/4))
            for n in range(1, maxN): 
                phi = 2 * math.asin((n * lamb)/(2 * d))
                r = self.R * math.sin(phi)

                distDiff = math.sqrt(self.R**2 - r**2)

                intensity =4 * weight * (math.cos(phi/2)**2) / (n**2)  #intensity approximation based on lattice spacing, I ∝ 1/n^2, and I ∝ cos2(theta)
                if intensity > 0.0001:
                    self.diffractionRings.append(ring(pos = vec(0, 0, distDiff-(self.ringThickness/2)), color = color.green, 
                                    opacity = min(0.99, intensity), axis = vec(0,0,1), radius = r, thickness = self.ringThickness, ))
    
    def changeVoltage(self, evt):
        if evt.id == 'x':
            self.v = evt.value * 1000

    def close(self):
        self.running = False

    def simulate(self):
        self.diffractionRings = []
        self.createRings()
        oldV = self.v

        quitButton = button( bind = self.close, text = 'Quit', pos = scene.title_anchor)

        #vpython loop
        while self.running:
            rate(10000)
            self.vTxt.text = f'voltage = {self.v}V'

            #check for change in voltage and lattice spacing
            if oldV != self.v:
                for diffRing in self.diffractionRings:
                    diffRing.visible = False
                    del diffRing
                    self.diffractionRings = []

                self.createRings()

            oldV = self.v


if __name__ == "__main__":
    sim = Task6Simulator()
    sim.simulate()
    sim.getGraph()
    plt.show()