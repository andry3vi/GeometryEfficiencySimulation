
import matplotlib.pyplot as plt
import numpy as np
import json

def main():
    size = 20
    plt.rcParams['font.size']=size
    result = dict()
    with open('SIMOUTPUT.json', "r") as jsonFile:
        result = json.load(jsonFile)


    fig,axs = plt.subplots(figsize=(9,9),dpi=100)

    axs.plot(result['DS'],[ 100.0* (result['hita'][i]+result['hite'][i])/result["ev"] for i,sum in enumerate(result['sum'])],'go--',label='total detected [alpha + electron + summed]')
    axs.plot(result['DS'],[ 100.0* (result['hita'][i]-sum)/result["ev"] for i,sum in enumerate(result['sum'])],'go--',label='alpha efficiency')
    axs.plot(result['DS'],[ 100.0* (result['hite'][i]-sum)/result["ev"] for i,sum in enumerate(result['sum'])],'bo--',label='electron efficiency')
    axs.plot(result['DS'],[ 100.0* sum/result["ev"] for sum in result['sum']],'ro--',label='sum efficiency')
    axs.set_xlabel("Detector Source Distance")
    axs.set_ylabel("Efficiency [%]")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
