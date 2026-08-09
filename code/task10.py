from vpython import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from mpl_toolkits.mplot3d import Axes3D


class Task10Grapher:
    def __init__(self, orbital: str = "1S", M: int = 0, A: int = 1, Z: int = 1, numPlots: int = 40, size: tuple = 10):
        orbitals = {
            "S": 0,
            "P": 1,
            "D": 2,
            "F": 3,
            "G": 4
        }
        
        self.orbital = orbital.upper()
        self.Z = Z
        self.A = A
        self.n = int(self.orbital[0])
        self.L = orbitals[self.orbital[1]]
        self.M = M

        self.maxBound = size/2
        self.minBound = size/-2
        self.numPlots = numPlots

        self.sideLength = (abs(self.minBound) + abs(self.maxBound))/self.numPlots
        self.colourmap = [
                        (0.0, vec(0, 0, 255)),     # blue
                        (0.25, vec(0, 255, 255)),  # cyan
                        (0.5, vec(0, 255, 0)),     # green
                        (0.75, vec(255, 255, 0)),  # yellow
                        (1.0, vec(255, 0, 0)),     # red
                    ]
        
    def laguerre(self, x):
        y = 0.0
        for k in range(self.n - self.L):
            a1 = factorial(self.L + self.n)
            a2 = factorial(2 * self.L + 1 + k)
            a3 = factorial(self.n - self.L - 1 - k)
            a4 = factorial(k)
            y += a1 * ((-x) ** k) / (a2 * a3 * a4)
        return y
    
    def Hradial(self, r):
        e0 = 8.854187817e-12  
        h = 6.6260755e-34    
        qe = 1.60217733e-19      
        me = 9.1093897e-31       
        u = 1.6605402e-27 

        a0 = (e0 * h**2)/(np.pi * me * qe**2)
        a0 = a0 / 1e-10

        mu = me * self.A * u / (me + self.A * u)

        a = me * a0 / (mu*self.Z)

        E = -mu * (qe**4) * (self.Z**2) / (8 * (e0**2) * (h**2) * (self.n**2))
        E = E/qe

        x = 2 * r/(a*self.n)

        w1 = sqrt(factorial(self.n-self.L-1) / (2 * self.n * factorial(self.n+self.L)))
        w2 = (2/(a * self.n))**(3/2)
        w3 = x**self.L * np.exp(-x/2)
        w4 = self.laguerre(x)
        w = w1 * w2 * w3 * w4

        return w, E, a0

    def WavFunc(self, azi, elev, r):
        if np.isnan(self.L):
            raise ValueError("input correct stuff")
        
        else:
            radial, E, a0 = self.Hradial(r)

            if self.M == 0:
                angular = scipy.special.sph_harm_y(self.L, 0, elev, azi)
            elif self.M < 0:
                angular = scipy.special.sph_harm_y(self.L, abs(self.M), elev, azi) - scipy.special.sph_harm_y(self.L, self.M, elev, azi)
            else:
                angular = scipy.special.sph_harm_y(self.L, self.M, elev, azi) + scipy.special.sph_harm_y(self.L, -self.M, elev, azi)

            w = abs(radial * angular)
            w = w * np.conj(w)

            return w, E

    def getWavFunc(self, zPlane: int, graph: bool):
        xy_vals = np.linspace(self.minBound, self.maxBound, self.numPlots)
        if self.numPlots%2 != 0:
            xy_vals = xy_vals[xy_vals != 0]

        xx, yy = np.meshgrid(xy_vals, xy_vals)

        zz = np.full_like(xx, zPlane)

        r_grid = np.sqrt(xx**2 + yy**2 + zz**2)
        azi_grid = np.arctan2(yy, xx)
        elev_grid = np.full_like(r_grid, np.pi/2)
        elev_grid = np.arccos(np.clip(zPlane / r_grid, -1.0, 1.0))

        W, E = self.WavFunc(azi_grid, elev_grid, r_grid) 

        if graph:
            W = W/np.max(W)
        
        return xx, yy, W, E

    def getGraph(self, zPlane = 0):
        xx, yy, W, E= self.getWavFunc(zPlane, True)

        fig, ax = plt.subplots(1)
        c = ax.contourf(xx, yy, W, levels = 500, cmap = "jet")
        fig.colorbar(c, ax = ax, label = "Probability density", ticks = [x/10 for x in range(0,11,1)])

        ax.set_aspect('equal', adjustable='box')
        ax.set_title(f"z={zPlane} plane, Z={self.Z}, {self.orbital}, L={self.L}, M={self.M}")


        if __name__ != "__main__":
            plt.close()
        return fig
    
    def getRadialGraph(self):
        r = np.linspace(0, 4, 1000)
        data = self.Hradial(r)
        
        fig, ax = plt.subplots(1)
        df = pd.DataFrame({"x": r, "y": data[0]**2}); graph = df.plot.line("x","y",legend=False, grid=True, ax = ax, xlim=(0, 4), ylim=(0))

        ax.set_title(f"Hydrogenic atom: Z={self.Z}, A={self.A}, n={self.n}, L={self.L}")
        ax.set_ylabel("Probability density"); ax.set_xlabel("Radius/Å")

        if __name__ != "__main__":
            plt.close()
        return fig

    def get3dGraph(self):

        zz = np.linspace(self.minBound, self.maxBound, self.numPlots)
        
        step = (self.maxBound-self.minBound)/(self.numPlots - 1)

        values = np.zeros((self.numPlots, self.numPlots, self.numPlots))
        for zi in range(len(zz)):
            xx, yy, W, E = self.getWavFunc(zz[zi], False)
            for iList in range(len(xx)):
                for i in range(len(xx[iList])):
                    values[zi][iList][i] = W[iList][i]

        normValues = values/np.max(values)

        xy_vals = np.linspace(self.minBound, self.maxBound, self.numPlots)
        xx, zz, yy = np.meshgrid(xy_vals, xy_vals, xy_vals)

        mask = normValues > 0.15
        xi = xx[mask]
        yi = yy[mask]
        zi = zz[mask]
        pi = normValues[mask]

        fig = plt.figure(figsize=(9, 8))
        ax = fig.add_subplot(111, projection='3d')

        cmap = plt.get_cmap('jet')
        alpha = np.clip(pi, 0.02, 1.0) ** 0.5  

        cf = ax.scatter(xi, yi, zi, c=pi, cmap=cmap, s=6, marker='.', linewidths=0, depthshade=False, alpha=alpha)

        ax.set_xlabel("X / Å"); ax.set_ylabel("Y / Å"); ax.set_zlabel("Z / Å")
        ticks = np.linspace(self.minBound, self.maxBound, 5)
        ax.set_xticks(ticks); ax.set_yticks(ticks); ax.set_zticks(ticks)
        ax.set_title(f"Z={self.Z}, A={self.A}, orbital={self.orbital}, E={E:.3f}eV, M={self.M}")

        cb = fig.colorbar(cf, ax = ax)
        cb.set_label("Probability Density")

        if __name__ != "__main__":
            plt.close()
        return fig


if __name__ == "__main__":
    grapher = Task10Grapher("3s", 0, 1, 1, 50, 1)
    
    #grapher.getGraph(0)
        
    grapher.get3dGraph()

    #grapher.getRadialGraph()

    plt.show()