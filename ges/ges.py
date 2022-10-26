import argparse
from tqdm import tqdm
from .Geometry import Geometry
from .EventGenerator import EventGenerator
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from multiprocessing import Pool
import time
import numpy as np
import json

def get_parser():

    parser = argparse.ArgumentParser(description = 'Geometrical Effciency Simulation code')

    parser.add_argument('-ev',
                        default= 1e4,
                        dest='ev',
                        type=float,
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
                        nargs='+',
                        help='Detector Soruce distance')

    parser.add_argument('-summing',
                        action='count',
                        help='Perform electron-alpha summing sim')
    
    parser.add_argument('-scanning',
                        action='count',
                        help='Perform electron-alpha summing sim scanning ds distance')
    

    args = parser.parse_args()

    return args, parser

def simulate(input):

    D,S,DS, ev = input
    G = Geometry(D,S,DS)
    Gen = EventGenerator(G)
    print("--Generating ",ev," events for ",D," D ",S," S ",DS," DS configuration--")
    for i in range(int(ev)):
        Gen.generateSumming()
    
    print("--finished generating ",ev," events for ",D," D ",S," S ",DS," DS configuration--")


    return DS,Gen.hit_a,Gen.hit_e,Gen.summed

   

def main():
    args, parser = get_parser()

    size = 20
    plt.rcParams['font.size']=size
    if args.scanning is not None:
        inputs = []

        for ds in np.linspace(args.DSdistance[0],args.DSdistance[1],int(args.DSdistance[2])):
            inputs.append([args.Ddiameter,args.Sdiameter,ds,args.ev])
        result = {'DS':[],'hita':[],'hite':[],'sum':[],'ev':args.ev}
        with Pool(processes=4) as pool:
            for data in pool.map(simulate,inputs):
                result["DS"].append(data[0])               
                result["hita"].append(data[1])               
                result["hite"].append(data[2])               
                result["sum"].append(data[3])

        with open('SIMOUTPUT.json', "w") as jsonFile:
            json.dump(result, jsonFile)

        return

    G = Geometry(args.Ddiameter,args.Sdiameter,args.DSdistance[0])
    Gen = EventGenerator(G)


    if args.summing is None:

        print("              SIMULATING              ")
        for i in tqdm(range(int(args.ev))):
            Gen.generate()

        print("###################################")
        print("              Results              ")
        print("Total number of simulated events -> ",len(Gen.events_a))
        print("Total number of detected events  -> ",Gen.hit_a)
        print("-----------------------------------")    
        print("Efficiency [%] -> ",100.0*Gen.hit_a/len(Gen.events_a))
        print("###################################")    



        if args.graphic is not None :
            xs_hit = list()
            ys_hit = list()
            zs_hit = list()
            xs_miss = list()
            ys_miss = list()
            zs_miss = list()
            counter = 0
            ratio_general = int(args.ev/10000)
            ratio_hit = int(Gen.hit_a/1000)
            for ev in Gen.events_a:
                if counter < ratio_general: 
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

            counter = 0

            for ev in Gen.events_a:

                if ev.hit:
                    if counter < ratio_hit: 
                        counter +=1
                        continue
                    counter = 0 
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

            for ev in Gen.events_a:

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

    else:
        
        print("              SIMULATING electron-alpha summing             ")
        for i in tqdm(range(int(args.ev))):
            Gen.generateSumming()
        

        print("###################################")
        print("              Results              ")
        print("Total number of simulated events -> ",len(Gen.events_a))
        print("Total number of alpha    detected events (summed included) -> ",Gen.hit_a)
        print("Total number of electron detected events (summed included) -> ",Gen.hit_e)
        print("Total number of summed alpha electron events  -> ",Gen.summed)
        print("-----------------------------------")    
        print("Efficiency alpha    [%] -> ",100.0*(Gen.hit_a-Gen.summed)/len(Gen.events_a)) 
        print("Efficiency electron [%] -> ",100.0*(Gen.hit_e-Gen.summed)/len(Gen.events_a)) 
        print("Summed events       [%] -> ",100.0*(Gen.summed)/len(Gen.events_a)) 
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
            ratio_general = int(args.ev/10000)
            ratio_hit = int(Gen.hit_a/1000)
            for ev in Gen.events_a:
                if counter < ratio_general: 
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

            counter = 0

            for ev in Gen.events_a:

                if ev.hit:
                    if counter < ratio_hit: 
                        counter +=1
                        continue
                    counter = 0 
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

            for ev in Gen.events_a:

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
