from vpython import *
from scipy import constants as const
import math
import random as ran

class Particle():
    def __init__(self, m, r, T, pos=(0,0,0), transparency=0.99, trail = False, colour = color.white):
        self.timer = 0

        self.mass = m
        self.radius = r
        self.temp = T

        self.s = math.sqrt((3*const.k*T)/m)/800 #speed in nm/ps
        self.dir = vector(0,0,0)
        self.v = vector(0,0,0)

        self.particle = sphere(pos = pos, radius = self.radius, opacity = transparency, make_trail = trail, color = colour)

    def randomStep(self):
        theta = ran.uniform(0, 2 * math.pi)
        z = ran.uniform(-1, 1)               
        r = math.sqrt(1 - z*z)

        x = r * math.cos(theta)
        y = r * math.sin(theta)

        self.dir = vector(x,y,z)
        self.v.x = self.dir.x * self.s
        self.v.y = self.dir.y * self.s
        self.v.z = self.dir.z * self.s
        
    
    def update(self, dt):
        self.particle.pos += self.v * dt
        self.timer += dt


class Task2Simulator:
    def __init__(self):
        self.screen = canvas(width=1000, height=1000, background=color.black)
        self.screen.select()
        self.caption = label(text="Brownian motion sim: t = 0", screen=False, xoffset=0, yoffset=400, color=color.white)

        self.N = 1000        #number of particles
        self.T = 373         #temp / K
        self.m = (28.96*10**-3)/(6.02*10**23)
        self.M = 10*self.m
        self.r = 0.16
        self.R = 10*self.r
        self.Kn = 15

        self.t = 0
        self.tmax = 200

        self.V = math.sqrt((3*const.k*self.T)/self.M)

        self.a = 7*self.R

        self.v = math.sqrt((3*const.k*self.T)/self.m)/1000 #speed in nm/ps

        self.running = True


    def randomPos(self, a, b, r):
        mod = 0
        while mod < r:
            pos = vector(ran.uniform(a, b),ran.uniform(a, b),ran.uniform(a, b))
            mod = math.sqrt((pos.x**2)+(pos.y**2)+(pos.z**2))
        return pos
    
    def close(self):
        self.running = False
    
    def simulate(self):
        smallParticles = []

        for i in range(self.N):
            pos = self.randomPos(-self.a, self.a, self.R)
            smallParticles.append(Particle(self.m, self.r, self.T, pos))

        quitButton = button( bind = self.close, text = 'Quit' )

        originBox = box(pos=vector(0,0,0), size=vector(0.5,0.5,0.5), color=color.green, opacity = 0.99)

        bigParticle = Particle(self.M, self.R, self.T, vector(0,0,0), 0.5, True, color.red)

        dt = 0.01*self.Kn*self.r/self.v

        while self.t <= self.tmax and self.running: 
            rate(10000)
            self.t+=dt
            self.caption.text = f"Brownian motion sim: t = {round(self.t)}ps"

            bigParticle.update(dt)

            for particle in smallParticles:
                particle.randomStep()
                particle.update(dt)

                #collsions
                if (particle.particle.pos.x - bigParticle.particle.pos.x)**2 +(particle.particle.pos.y - bigParticle.particle.pos.y)**2 + (particle.particle.pos.z - bigParticle.particle.pos.z)**2 <= self.R**2:
                    particle.particle.color = color.blue
                    particle.timer = 0

                    nHat = vector((bigParticle.particle.pos - particle.particle.pos)/mag(bigParticle.particle.pos - particle.particle.pos))

                    bigParticleUPara = dot(bigParticle.v, nHat)*nHat
                    bigParticleVPerp = bigParticle.v - bigParticleUPara

                    particleUPara = dot(particle.v, nHat)*nHat
                    particleVPerp = particle.v - particleUPara

                    bigParticleVPara = ((bigParticle.mass - particle.mass)*bigParticleUPara + 2*particle.mass*particleUPara)/(bigParticle.mass + particle.mass)
                    particleVPara = ((particle.mass - bigParticle.mass)*particleUPara + 2*bigParticle.mass*bigParticleUPara)/(bigParticle.mass + particle.mass)

                    bigParticle.v = bigParticleVPara + bigParticleVPerp
                    particle.v = particleVPara + particleVPerp
                
                elif particle.particle.color != color.white and particle.timer > 10:
                    particle.particle.color = color.white


if __name__ == "__main__":
    sim = Task2Simulator()
    sim.simulate()