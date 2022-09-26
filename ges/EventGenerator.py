from .Geometry import Geometry 

from math import sqrt, pi, cos, sin, acos, asin, atan2
import random

class EventGenerator:
   
    def __init__(self, geometry):
        self.geometry = geometry
        self.events_a = list()
        self.events_e = list()
        self.hit_a = 0
        self.hit_e = 0 
        self.summed = 0
        

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
            self.events_e.append(Event(x1,y1,z1,x2,y2,z2,True))
            self.hit_a += 1
        else:
            self.events_a.append(Event(x1,y1,z1,x2,y2,z2,False))

            
    def generateSumming(self):
        r_start = self.geometry.Sdiameter * 0.5 * sqrt(random.random())
        phi_start = random.random() * 2 * pi    
        theta_start = pi/2

        x1,y1,z1 = self.PolarToCartesian(r_start,theta_start,phi_start)
        
        ###################ALPHA#########################
        theta_decay_1  = acos(2*random.random()-1)
        phi_decay_1 = 2*pi* random.random()
   
        b2 = -2*x1*cos(phi_decay_1)*sin(theta_decay_1) - 2*y1*sin(phi_decay_1)*sin(theta_decay_1)
        Delta = (2*x1*cos(phi_decay_1)*sin(theta_decay_1)+2*y1*sin(phi_decay_1)*sin(theta_decay_1))**2 - 4*(-self.geometry.SPHradius**2+x1**2+y1**2)*(cos(theta_decay_1)**2+cos(phi_decay_1)**2 *sin(theta_decay_1)**2 + sin(phi_decay_1)**2 *sin(theta_decay_1)**2)
        if Delta < 0: return
        Deltasqrt =  sqrt(Delta)
        a = 2*(cos(theta_decay_1)**2 + cos(phi_decay_1)**2 *sin(theta_decay_1)**2 + sin(phi_decay_1)**2 * sin(theta_decay_1)**2)
        
        t = (b2+Deltasqrt)/a

        x2_a = t*cos(phi_decay_1)*sin(theta_decay_1)+x1
        y2_a = t*sin(phi_decay_1)*sin(theta_decay_1)+y1
        z2_a = t*cos(theta_decay_1)

        ####################ELECTRON#########################
        theta_decay_2 = acos(2*random.random()-1)
        phi_decay_2 = 2*pi* random.random()

        b2 = -2*x1*cos(phi_decay_2)*sin(theta_decay_2) - 2*y1*sin(phi_decay_2)*sin(theta_decay_2)
        Delta = (2*x1*cos(phi_decay_2)*sin(theta_decay_2)+2*y1*sin(phi_decay_2)*sin(theta_decay_2))**2 - 4*(-self.geometry.SPHradius**2+x1**2+y1**2)*(cos(theta_decay_2)**2+cos(phi_decay_2)**2 *sin(theta_decay_2)**2 + sin(phi_decay_2)**2 *sin(theta_decay_2)**2)
        if Delta < 0: return
        Deltasqrt =  sqrt(Delta)
        a = 2*(cos(theta_decay_2)**2 + cos(phi_decay_2)**2 *sin(theta_decay_2)**2 + sin(phi_decay_2)**2 * sin(theta_decay_2)**2)
        
        t = (b2+Deltasqrt)/a

        x2_e = t*cos(phi_decay_2)*sin(theta_decay_2)+x1
        y2_e = t*sin(phi_decay_2)*sin(theta_decay_2)+y1
        z2_e = t*cos(theta_decay_2)


        rad_a,theta_hit_a,phi_hit_a = self.CartesianToPolar(x2_a,y2_a,z2_a)        
        rad_e,theta_hit_e,phi_hit_e = self.CartesianToPolar(x2_e,y2_e,z2_e)        

        #########################################
        if (theta_hit_a < self.geometry.Dtheta) and (theta_hit_e < self.geometry.Dtheta):
            self.summed +=1

        if theta_hit_a < self.geometry.Dtheta : 
            self.events_a.append(Event(x1,y1,z1,x2_a,y2_a,z2_a,True))
            self.hit_a += 1
        else:
            self.events_a.append(Event(x1,y1,z1,x2_a,y2_a,z2_a,False))

        if theta_hit_e < self.geometry.Dtheta : 
            self.events_e.append(Event(x1,y1,z1,x2_e,y2_e,z2_e,True))
            self.hit_e += 1
        else:
            self.events_e.append(Event(x1,y1,z1,x2_e,y2_e,z2_e,False))

        
        
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
 