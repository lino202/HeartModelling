import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors


def calculateBoxPlotParams(data):
    median = np.median(data)
    upQuart = np.percentile(data, 75)
    lowQuart = np.percentile(data, 25)
    iqr = upQuart - lowQuart
    upWhisker = data[data<=upQuart+1.5*iqr].max()
    lowWhisker = data[data>=lowQuart-1.5*iqr].min()
    return median, lowQuart, upQuart, lowWhisker, upWhisker



def plotHistAndBoxPlot(array, title, path=None):
    fig, axs = plt.subplots(1,2)
    plt.subplots_adjust(wspace=0.4)
    axs[0].hist(array)
    axs[1].boxplot(array)
    axs[0].set_ylabel("Frequencies")
    axs[0].set_xlabel(title)
    axs[1].set_xlabel("Samples")
    axs[1].set_ylabel(title)
    if path:
        plt.savefig(path)
    else:
        plt.show(block=True)

def printUsefulStats(data):
    boxplotData = calculateBoxPlotParams(data)
    print("Useful Data: mean-std {0} +/- {1}".format(np.mean(data), np.std(data)))
    print("\t median {0}, lowQuart {1}, upQuart {2}, lowWhisker {3}, upWhisker {4}".format(boxplotData[0], boxplotData[1], boxplotData[2], boxplotData[3], boxplotData[4]))


def writeFibers4JSON(filePath, rbmVersors):
    with open(filePath, "w") as file:
        file.write('"fibers":[[{0:.15f}, {1:.15f}, {2:.15f}],\n'.format(rbmVersors[0,0], rbmVersors[0,1], rbmVersors[0,2]))
        for i in range(1,rbmVersors.shape[0]-1):
            file.write("\t\t\t[{0:.15f}, {1:.15f}, {2:.15f}],\n".format(rbmVersors[i,0], rbmVersors[i,1], rbmVersors[i,2]))
        file.write("\t\t\t[{0:.15f}, {1:.15f}, {2:.15f}]]".format(rbmVersors[-1,0], rbmVersors[-1,1], rbmVersors[-1,2]))