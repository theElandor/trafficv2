import getopt
import sys

# create_files(vehicles, model, template, duration, )


def create_files(vehicles, model, template, duration):
    with open(template, "r") as t:
        template = t.read()
    for v in vehicles:  # VS
        for i in range(1, 11):  # AI
            # need to create one for booster and one for random
            with open("configs/Comp/{}{}_{}.yml".format(str(v), "B", str(i)), "w") as booster_config:
                booster_config.write(template.format(str(duration), str(v), "booster", model, str(i), "0"))
            with open("configs/Comp/{}{}_{}.yml".format(str(v), "R", str(i)), "w") as random_config:
                random_config.write(template.format(str(duration), str(v), "random", model, str(i), "1"))


if __name__ == '__main__':
    # default values
    vehicles = []
    model = "hope"
    template = "default_template.txt"
    duration = 5000
    argumentList = sys.argv[1:]
    # Options
    options = "hmo:"
    # Long options
    # need to do name, ai
    long_options = ["help", "template=", "MV=", "VS=", "Stp=", ]
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)

        # checking each argument
        if len(arguments) == 0:
            print("No arguments specified. Use python generate_configs.py -h for help")
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--help"):
                print("Supported options:")
                print("--template=<str> to specify template file.")
                print("--MV=<str> to specifiy model version, default:hope.")
                print("--VS=<int> to specify number of vehicles. default: 120, 130, 140.")
                print("--Stp=<int> to specify experiment duration. default:5000.")
            else:
                if currentArgument in ("-t", "--template"):
                    print("selected template: {}".format(currentValue))
                    template = currentValue
                elif currentArgument in ("-m", "--MV"):
                    print("selected model: {}".format(currentValue))
                    model = currentValue
                elif currentArgument in ("-v", "--VS"):
                    print("number of vehicles: {}".format(currentValue))
                    try:
                        vehicles.append(int(currentValue))
                    except ValueError:
                        print("Invalid number of vehicles. Exiting")
                        exit()
                elif currentArgument in ("-d", "--Stp"):
                    print("selected duration: {}".format(currentValue))
                    try:
                        duration = int(currentValue)
                    except ValueError:
                        print("Invalid number of vehicles. Exiting")
        create_files(vehicles, model, template, duration)
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
