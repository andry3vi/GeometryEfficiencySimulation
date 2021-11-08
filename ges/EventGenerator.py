from .Geometry import Geometry 

from math import sqrt, pi, cos, sin, acos, asin, atan2
import random

class EventGenerator:
   
    def __init__(self, geometry):
        self.geometry = geometry
        self.events = list()
        self.hit = 0

    def generate(self):

        r_start = self.geometry.Sdiameter * 0.5 * sqrt(random.random())
        phi_start = random.random() * 2 * pi    
        theta_start = pi/2

        x1,y1,z1 = self.PolarToCartesian(r_start,theta_start,phi_start)
        
        theta_decay = acos(2*random.random()-1)
        phi_decay = 2*pi* random.random()
        b2 = -2*x1*cos(phi_decay)*sin(theta_decay) - 2*y1*sin(phi_decay)*sin(theta_decay)
        Delta = (2*x1*cos(phi_decay)*sin(theta_decay)+2*y1*sin(phi_decay)*sin(theta_decay))**2 - 4*(-self.geometry.SPHradius**2+x1**2+y1**2)*(cos(theta_decay)**2+cos(phi_decay)**2 *sin(theta_decay)**2 + sin(phi_decay)**2 *sin(theta_decay)**2)
        if Delta < 0: return
        Deltasqrt =  sqrt(Delta)
        a = 2*(cos(theta_decay)**2 + cos(phi_decay)**2 *sin(theta_decay)**2 + sin(phi_decay)**2 * sin(theta_decay)**2)
        
        t = (b2+Deltasqrt)/a

        x2 = t*cos(phi_decay)*sin(theta_decay)+x1
        y2 = t*sin(phi_decay)*sin(theta_decay)+y1
        z2 = t*cos(theta_decay)

        rad,theta_hit,phi_hit = self.CartesianToPolar(x2,y2,z2)        

        if theta_hit < self.geometry.Dtheta : 
            self.events.append(Event(x1,y1,z1,x2,y2,z2,True))
            self.hit += 1
        else:
            self.events.append(Event(x1,y1,z1,x2,y2,z2,False))

            

        
    def CartesianToPolar(_,x,y,z):
 
        r = sqrt(x**2+y**2+z**2)
        theta = acos(z/r)
        phi = atan2(y,x)

        return r,theta,phi
        
    def PolarToCartesian(_,r,theta,phi):

        x = r*cos(phi)*sin(theta)
        y = r*sin(phi)*sin(theta)
        z = r*cos(theta)

        return x,y,z

class Event:

    def __init__(self, x1,y1,z1,x2,y2,z2,hit):
        self.x1 = x1        
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.hit = hit
 