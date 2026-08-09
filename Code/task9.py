import pandas as pd, numpy as np, matplotlib.pyplot as plt, matplotlib.gridspec as gridspec
from scipy import constants as const
from sklearn.neighbors import NearestNeighbors

class Task9Grapher:
    def __init__(self, E, lock:bool = True, probs:bool = False):
        np.seterr(divide='ignore', invalid='ignore')
        self.startTheta = 0
        self.maxTheta = np.pi

        self.lockAxes = lock
        self.isCarlo = probs
        self.E = E * 10**-3#MeV

        self.N = 10000

        mec2 = (const.m_e * const.c**2) / (const.e * 10**6)
        re = const.physical_constants["classical electron radius"][0]

        self.KleinNishina = lambda theta, E: (E_ratio := 1 / (1 + (E/mec2) * (1 - np.cos(theta))))**2 * (E_ratio + 1/E_ratio - np.sin(theta)**2)

    def sample_Thetas(self, E):
        thetas = []
        maxKN = self.KleinNishina(0, E)

        while len(thetas) < self.N:
            theta = np.random.uniform(0, np.pi)
            u = np.random.uniform(0,maxKN)
            if u < self.KleinNishina(theta, E) * np.sin(theta):
                thetas.append(theta)
        return np.array(thetas)
    
    def density(self, xdata, ydata):
        pts = np.column_stack([xdata, ydata])
        nbrs = NearestNeighbors(n_neighbors=int(self.N/2)).fit(pts)
        distances, _ = nbrs.kneighbors(pts)
        r = distances[:, -1]
        density = 1 / r
        return density/max(density)


    def deltaLambda(self, E, thetas):
        lamb = ((const.h * const.c) / E) / (const.e * 10**6)
        lambdas = (const.h/(const.m_e * const.c)) * (1 - np.cos(thetas))
        return  lambdas/lamb
    
    def recoilSpeed(self, E, thetas):
        E = E * const.e * 10**6
        speeds = []
        lamb = (const.h * const.c)/E
        for theta in thetas:
            dashLamb = lamb + (const.h*(1 - np.cos(theta)))/(const.m_e * const.c)
            dashE = (const.h*const.c)/dashLamb
            K = E - dashE
            gamma = 1 + K/(const.m_e * const.c**2)
            vOverC = np.sqrt(1- 1/gamma**2)

            speeds.append(vOverC)
        return  speeds
    
    def recoilAngle(self, E, thetas):
        E = E * const.e * 10**6
        phis = []
        lamb = (const.h * const.c)/E
        for theta in thetas:
            dividend = np.sin(theta)
            divisor = 1 + (const.h * (1 - np.cos(theta)))/(const.m_e * const.c * lamb) - np.cos(theta)
            quotient = dividend/divisor
            phi = np.atan(quotient) / (np.pi/180)
            phis.append(phi)
        return  phis


    def getGraph(self):
        if self.isCarlo:
            gs = gridspec.GridSpec(2, 7, width_ratios=[1,1,1,1,1,1, 0.4],
                       hspace=0.4, wspace=2)
            fig = plt.figure()

            ax3 = fig.add_subplot(gs[0, :6])   
            ax1 = fig.add_subplot(gs[1, :3])    
            ax2 = fig.add_subplot(gs[1, 3:6])  
            cax = fig.add_subplot(gs[:, 6]) 

            
            xdata = sorted(self.sample_Thetas(self.E))

            #fractional wavelength shift
            ydata = self.deltaLambda(self.E, xdata)
            density = self.density(xdata, ydata)
            cf = ax1.scatter(xdata, ydata, c=density, cmap='jet', marker='.', label = str(round(self.E * 10**3))+"keV", s = (plt.rcParams['lines.markersize']/3) ** 2)
            
            #electron recoil speed
            ydata = self.recoilSpeed(self.E, xdata)
            density = self.density(xdata, ydata)
            ax2.scatter(xdata, ydata, c=density, cmap='jet', marker='.', label = str(round(self.E * 10**3))+"keV", s = (plt.rcParams['lines.markersize']/3) ** 2)
            
            #electron recoil angle
            ydata = self.recoilAngle(self.E, xdata)
            density = self.density(xdata, ydata)
            ax3.scatter(xdata, ydata, c=density, cmap='jet', marker='.', label = str(round(self.E * 10**3))+"keV", s = (plt.rcParams['lines.markersize']/3) ** 2)
            
            cb = fig.colorbar(cf, cax = cax)
            cb.set_label("Probability Density")

        else:
            gs = gridspec.GridSpec(2, 2)
            fig = plt.figure()
            ax1 = fig.add_subplot(gs[1, 0], )
            ax2 = fig.add_subplot(gs[1, 1])
            ax3 = fig.add_subplot(gs[0, :])

            xdata = [theta for theta in np.linspace(self.startTheta, self.maxTheta, 1000)] 

            #fractional wavelenth shift 
            ydata = self.deltaLambda(self.E, xdata)
            df = pd.DataFrame({"x":xdata, str(round(self.E * 10**3))+"keV":ydata}); df.plot.line("x", str(round(self.E * 10**3))+"keV", ax = ax1)
            #electron recoil speed
            ydata = self.recoilSpeed(self.E, xdata)
            df = pd.DataFrame({"x":xdata, str(round(self.E * 10**3))+"keV":ydata}); df.plot.line("x", str(round(self.E * 10**3))+"keV", ax = ax2)
            #electron recoil angle
            ydata = self.recoilAngle(self.E, xdata)
            df = pd.DataFrame({"x":xdata, str(round(self.E * 10**3))+"keV":ydata}); df.plot.line("x", str(round(self.E * 10**3))+"keV", ax = ax3)

        ax1.set_xlabel("Photon scattering angle /rad"); ax1.set_ylabel("Δλ/λ"); ax1.set_xlim(self.startTheta, self.maxTheta); ax1.set_ylim(0, 6 if self.lockAxes else None); ax1.grid(True); 
        if ax1.legend(): ax1.get_legend().remove()
        ax2.set_xlabel("Photon scattering angle /rad"); ax2.set_ylabel("electron recoil speed v/c"); ax2.set_xlim(self.startTheta, self.maxTheta); ax2.set_ylim(0, 1 if self.lockAxes else None); ax2.grid(True)
        if ax2.legend(): ax2.get_legend().remove()
        ax3.set_xlabel("Photon scattering angle /rad"); ax3.set_ylabel("electron recoil angle /deg"); ax3.set_xlim(self.startTheta, self.maxTheta); ax3.set_ylim(0, 90);ax3.grid(True); ax3.set_title("Compton scattering of X-ray photon off an electron")
        if ax3.legend(): ax3.get_legend().remove()

        if __name__ != "__main__":
            plt.close()
        return fig


if __name__ == "__main__":
    graph = Task9Grapher(662, probs=False)
    graph.getGraph()
    plt.show()
