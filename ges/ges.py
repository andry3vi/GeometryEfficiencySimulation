import argparse
from tqdm import tqdm
from .Geometry import Geometry
from .EventGenerator import EventGenerator
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_parser():

    parser = argparse.ArgumentParser(description = 'Geometrical Effciency Simulation code')

    parser.add_argument('-ev',
                        default= 1e4,
                        dest='ev',
                        type=int,
                        help='Number of event to be generated')

    parser.add_argument('-graphic',
                        action='count',
                        help='plot graphical results')

    parser.add_argument('-S',
                        dest='Sdiameter',
                        type=float,
                        default = 1e-5,
                        help='Source diameter')
    
    parser.add_argument('-D',
                        dest='Ddiameter',
                        type=float,
                        required=True,
                        help='Detector diameter')    
                        

    parser.add_argument('-DS',
                        required=True,
                        dest='DSdistance',
                        type=float,
                        help='Detector Soruce distance')

    
    args = parser.parse_args()

    return args, parser

def main():
    args, parser = get_parser()

    G = Geometry(args.Ddiameter,args.Sdiameter,args.DSdistance)
    Gen = EventGenerator(G)

    print("              SIMULATING              ")
    for i in tqdm(range(int(args.ev))):
        Gen.generate()

    print("###################################")
    print("              Results              ")
    print("Total number of simulated events -> ",len(Gen.events))
    print("Total number of detected events  -> ",Gen.hit)
    print("-----------------------------------")    
    print("Efficiency [%] -> ",100.0*Gen.hit/len(Gen.events))
    print("###################################")    

    size = 20
    plt.rcParams['font.size']=size

    if args.graphic is not None :
        xs_hit = list()
        ys_hit = list()
        zs_hit = list()
        xs_miss = list()
        ys_miss = list()
        zs_miss = list()
        counter = 0
        ratio = int(args.ev/10000)
        for ev in Gen.events:
            if counter != ratio: 
                counter +=1
                continue
            counter = 0
            if ev.hit:
                xs_hit.append(ev.x2)
                ys_hit.append(ev.y2)
                zs_hit.append(ev.z2)
            else: 
                xs_miss.append(ev.x2)
                ys_miss.append(ev.y2)
                zs_miss.append(ev.z2)
        fig = plt.figure(1,figsize=(9,9),dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(xs_hit, ys_hit, zs_hit,"g*",label="Detected")
        ax.plot(xs_miss, ys_miss, zs_miss,"r*",label="Missed")
        ax.set_title("Spherical distribution of events")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.legend()
        fig2 = plt.figure(2,figsize=(9,9),dpi=100)
        ax2 = fig2.add_subplot(111, projection='3d')

        for ev in Gen.events:
            if counter != ratio: 
                counter +=1
                continue
            counter = 0

            if ev.hit:
                ax2.plot((ev.x1,ev.x2),(ev.y1,ev.y2),(ev.z1,ev.z2),"g-",label="Detected")            
        ax2.set_title("Ray traced detected events")
        ax2.set_xlabel("X")
        ax2.set_ylabel("Y")
        ax2.set_zlabel("Z")

        fig3 = plt.figure(3,figsize=(9,9),dpi=100)

        x1_hit = list()
        y1_hit = list()
        z1_hit = list()
        x2_hit = list()
        y2_hit = list()
        z2_hit = list()
        x1_miss = list()
        y1_miss = list()
        z1_miss = list()

        for ev in Gen.events:

            if ev.hit:
                x1_hit.append(ev.x1)
                y1_hit.append(ev.y1)
                z1_hit.append(ev.z1)
                x2_hit.append(ev.x2)
                y2_hit.append(ev.y2)
                z2_hit.append(ev.z2)
            else: 
                x1_miss.append(ev.x1)
                y1_miss.append(ev.y1)
                z1_miss.append(ev.z1)            
        
        plt.hist2d(x1_hit,y1_hit,bins=(100,100),cmap=plt.cm.Reds)
        plt.title("Source heatmap")
        plt.xlabel("X")
        plt.ylabel("Y")
        
        fig4 = plt.figure(4,figsize=(9,9),dpi=100)
        plt.hist2d(x2_hit,y2_hit,bins=(100,100),cmap=plt.cm.Reds)
        plt.title("Detector heatmap")
        plt.xlabel("X")
        plt.ylabel("Y")


        plt.show()
        
if __name__ == '__main__':
    main()
