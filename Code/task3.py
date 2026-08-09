import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import constants as const
import math

class Task3Grapher:
    def __init__(self):
        #Black body radiation
        #vars to change data
        self.startLambda = 7 #any lower you get overflow
        self.maxLambda = 3000
        self.deltaLambda = 10
        self.beginT = 3000
        self.endT = 6000

        #Einstein's solid molar heat capacity
        #vars to change data
        self.startT = 6 #any lower you get overflow
        self.maxT = 800
        self.deltaT = 10
        self.metals = {
            #  metal: debye temp/K
                "Au": 170,
                "Cu": 343.5,
                "Ti": 420,
                "Al": 428,
                "Fe": 470,
                "Si": 645,
                "C": 2230}

    def B(self, T, num):
        irradiance = []
        for lamb in range(self.startLambda, num, self.deltaLambda): 
            lamb = lamb*(10**(-9))
            irradiance.append(((2 * const.h * const.c**2) / lamb**5) * (1 / (np.exp((const.h * const.c) / (lamb * const.k * T)) - 1))*10**-13)
        return  irradiance

    def heatCapacity(self, Td):
        capacity = []

        Te = Td*math.cbrt(math.pi/6) #Einteins Temp
        f = (const.k*Te)/const.h

        for T in range(self.startT, self.maxT, self.deltaT):
            x = (const.h*f)/(const.k*T)
            C = 3*const.R *(((x**2)*(math.e**x))/(((math.e**x)-1)**2))
            capacity.append(C)

        return capacity

    def getGraph(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12,5))
        fig.set_constrained_layout(True)

        #Black body radiation
        xdata = [x for x in range(self.startLambda, self.maxLambda, self.deltaLambda)]
        yData = [self.B(x, self.maxLambda) for x in range(self.beginT, self.endT+1000, 1000)]

        for yPlot in yData:
            df = pd.DataFrame({"x":xdata, str(self.beginT)+"K": yPlot}); df.plot.line("x",str(self.beginT)+"K",ax=ax1, grid=True); self.beginT+=1000

        ax1.set_xlabel("Wavelength / nm"); ax1.set_ylabel("Radiance / Wm⁻²/nm x10⁴"); ax1.set_title("Spectral Radiance vs Wavelength"); ax1.set_xlim(0,3000); ax1.set_ylim(0); ax1.vlines([380, 750], ymin=0, ymax=10, colors=['#FF0000', "#7F00FF"], linestyles=['--', '--'])


        #Einstein's solid molar heat capacity
        xdata = [T for T in range(self.startT, self.maxT, self.deltaT)]
        ydata = [self.heatCapacity(temp) for name, temp in self.metals.items()]

        for i, yPlot in enumerate(ydata):
            daf = pd.DataFrame({"x":xdata, list(self.metals)[i]: yPlot}); daf.plot.line("x",list(self.metals)[i], ax=ax2, grid=True); self.startT+=1000

        ax2.set_xlabel("Temp / K"); ax2.set_ylabel("Molar heat capacity / Jmol⁻¹K⁻¹ "); ax2.set_title("Einstein model of solid molar heat capacity"); ax2.set_xlim(0,self.maxT); ax2.set_ylim(0); ax2.hlines([3*const.R],xmin=0, xmax=self.maxLambda, colors="white", linestyles=['--'])
        
        if __name__ != "__main__":
            plt.close()
        return fig
    
if __name__ == "__main__":
    graph = Task3Grapher()
    graph.getGraph()
    plt.show()