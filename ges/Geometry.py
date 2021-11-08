from math import sqrt, pi, cos, sin, acos, asin, atan2

class Geometry:

    def __init__(self,Ddiameter,Sdiameter,DSdistance):
        self.Ddiameter = Ddiameter
        self.Sdiameter = Sdiameter
        self.DSdistance = DSdistance

        self.SPHradius = sqrt(DSdistance**2+Ddiameter**2)

        self.Dtheta = acos(DSdistance/self.SPHradius)

        print("###################################")
        print("          Geometry defined         ")
        print("Detector diameter -> ",self.Ddiameter)
        print("Source diameter   -> ",self.Sdiameter)
        print("D-S distance      -> ",self.DSdistance)
        print("-----------------------------------")
        print("Sphere radius     -> ",self.SPHradius)        
        print("Theta condition   -> ",self.Dtheta)     
        print("###################################")
    
    