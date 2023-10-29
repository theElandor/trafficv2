import matplotlib.pyplot as plt
import matplotlib
import statistics as s
import getopt
import sys


def plot(file_to_read, gran, zoom, mode):
    matplotlib.use("TkAgg")
    filename = file_to_read
    with open(filename) as f:
        data = [float(s.strip()) for s in f.readlines()]
        blocks = []
        chunk = []
        y = []
        for i in range(1, int(len(data)/zoom)):
            chunk.append(data[i])
            if i % gran == 0:
                blocks.append(chunk[:])
                chunk = []
        y = [s.mean(c) for c in blocks]
        x = [i for i in range(len(y))]
        plt.title("{} plot".format(file_to_read[:-4]))
        plt.xlabel("Set of {} function calls".format(str(gran)))
        plt.ylabel("{} measured".format(file_to_read[:-4]))
        plt.plot(x, y, mode)
        plt.show()
        # plt.savefig(name, dpi=300)


if __name__ == '__main__':
    # default values
    file_to_read = "reward.txt"
    gran = 100
    zoom = 1
    mode = "--bo"
    argumentList = sys.argv[1:]
    # Options
    options = "hmo:"

    # Long options
    long_options = ["help", "file=", "zoom=", "gran=", "mode="]
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)

        # checking each argument
        if len(arguments) == 0:
            print("No arguments specified. Use python plotter.py -h for help")
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--help"):
                print("Supported options:")
                print("--file=<filename> to specifiy file. default=reward.txt")
                print("--zoom=<zoom value> to specifiy zoom. default=1")
                print("--gran=<gran value> to specifiy granularity value. default=100")
                print("--mode=<mode> to specifiy plotting style. default=--bo")
            else:
                if currentArgument in ("-f", "--file"):
                    print("file to read: {}".format(currentValue))
                    file_to_read = currentValue
                elif currentArgument in ("-z", "--zoom"):
                    print("applied zoom: {}".format(currentValue))
                    zoom = int(currentValue)
                elif currentArgument in ("-g", "--gran"):
                    print("applied granularity: {}".format(currentValue))
                    gran = int(currentValue)
                elif currentArgument in ("-m", "--mode"):
                    print("applied granularity: {}".format(currentValue))
                    mode = currentValue
        print("read file: {}, gran: {}, zoom:{}\n".format(file_to_read, str(gran), str(zoom)))
        plot(file_to_read, gran, zoom, mode)
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
