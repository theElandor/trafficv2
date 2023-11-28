import getopt
import sys

# create_files(vehicles, model, template, duration, )


def create_files_random(vehicles, budget, vehicles_list, model, template, duration, random_percentage, random_percentage_list, budget_list, var, exclude_bidder):
    with open(template, "r") as t:
        template = t.read()
    #this code sooner or later needs to be refactored
    if var == 'VS':
        for v in vehicles_list:  # VS
            for i in range(1, 11):  # AI
                # need to create one for booster and one for random
                if not exclude_bidder:
                    with open("configs/Comp/{}{}_{}.yml".format(str(v), "B", str(i)), "w") as booster_config:
                        booster_config.write(template.format(var, str(duration), str(v), str(random_percentage), "booster", model, str(i), budget, "0"))
                with open("configs/Comp/{}{}_{}.yml".format(str(v), "R", str(i)), "w") as random_config:
                    random_config.write(template.format(var, str(duration), str(v), str(random_percentage) , "random", model, str(i), budget, "1"))
    elif var == 'RS':
        for r in random_percentage_list:  # VS
            for i in range(1, 11):  # AI
                # need to create one for booster and one for random
                if not exclude_bidder:
                    with open("configs/Comp/{}{}_{}.yml".format(str(r), "B", str(i)), "w") as booster_config:
                        booster_config.write(template.format(var, str(duration), str(vehicles), str(r), "booster", model, str(i), budget, "0"))
                with open("configs/Comp/{}{}_{}.yml".format(str(r), "R", str(i)), "w") as random_config:
                    random_config.write(template.format(var, str(duration), str(vehicles), str(r) ,"random", model, str(i), budget, "1"))
    elif var == 'B':
        for b in budget_list:  # VS
            for i in range(1, 11):  # AI
                # need to create one for booster and one for random
                if not exclude_bidder:
                    with open("configs/Comp/{}{}_{}.yml".format(str(b), "B", str(i)), "w") as booster_config:
                        booster_config.write(template.format(var, str(duration), str(vehicles), str(random_percentage), "booster", model, str(i), str(b) ,"0"))
                with open("configs/Comp/{}{}_{}.yml".format(str(b), "R", str(i)), "w") as random_config:
                    random_config.write(template.format(var, str(duration), str(vehicles), str(random_percentage), "random", model, str(i), str(b) ,"1"))
    else:
        print("Unexpected error during configuration file generation")

def create_files_nobidder(vehicles, budget, vehicles_list, model, template, duration, random_percentage, random_percentage_list, budget_list, var, no_bidder_budget, no_bidder_budget_list, exclude_bidder):
    """
    We still use "random" as filename so we don't have to change the plotter script.
    A more appr. script would be "off"
    """
    with open(template, "r") as t:
        template = t.read()
    if var == 'VS':
        for v in vehicles_list:  # VS
            for i in range(1, 11):  # AI
                if not exclude_bidder:
                    # need to create one for booster and one for nobidder
                    with open("configs/Comp/{}{}_{}.yml".format(str(v), "B", str(i)), "w") as booster_config:
                        booster_config.write(template.format(var, str(duration), str(v), str(random_percentage), "booster", model, str(i), budget, "0"))
                with open("configs/Comp/{}{}_{}.yml".format(str(v), "O", str(i)), "w") as random_config:
                    random_config.write(template.format(var, str(duration), str(v), str(random_percentage) , "disabled", model, str(i), no_bidder_budget, "1"))
    elif var == 'RS':
        for r in random_percentage_list:  # VS
            for i in range(1, 11):  # AI
                # need to create one for booster and one for random
                if not exclude_bidder:
                    with open("configs/Comp/{}{}_{}.yml".format(str(r), "B", str(i)), "w") as booster_config:
                        booster_config.write(template.format(var, str(duration), str(vehicles), str(r), "booster", model, str(i), budget, "0"))
                with open("configs/Comp/{}{}_{}.yml".format(str(r), "O", str(i)), "w") as random_config:
                    random_config.write(template.format(var, str(duration), str(vehicles), str(r) , "disabled", model, str(i), no_bidder_budget, "1"))
    elif var == 'NBB':
        for b in no_bidder_budget_list:  # VS
            for i in range(1, 11):  # AI
                # need to create one for booster and one for random
                if not exclude_bidder:
                    print("Warning, you are not excluding generation of config files for standard bidder. This option is not currently supported.")
                    break
                with open("configs/Comp/{}{}_{}.yml".format(str(b), "O", str(i)), "w") as random_config:
                    random_config.write(template.format(var, str(duration), str(vehicles), str(random_percentage), "disabled", model, str(i), str(b) ,"1"))
    else:
        print("{} is currently not a supported variable in this mode.".format(var))
        return

if __name__ == '__main__':
    # default values
    vehicles = 120
    model = "hope"
    template = "default_template.txt"
    duration = 5000
    random_percentage = 40
    budget = 100
    var = 'VS'
    compare_to = 'random'
    no_bidder_budget = None
    exclude_bidder = False
    
    supported_variables = ['VS', 'Rs', 'B']
    supported_b = ['random', 'nobidder']

    vehicles_list = []
    random_percentage_list = []
    budget_list = []
    no_bidder_budget_list = []

    argumentList = sys.argv[1:]
    # Options
    options = "hmo:"
    # Long options
    long_options = ["help", "template=", "MV=", "VS=", "Stp=", "RS=", "B=", "CT=", "NBB=", "EB="]
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
                print("--RS=<int> to specify random pool percentage. default:40.")
                print("--B=<int> to specify the starting budget of the test vehicle. default:100.")
                print("--CT=<string> to specify the behaviour compared to thew bidder. default: random")
                print("--NBB=<int> to specify the starting budget of the vehicle in case of nobidder.")
                print("If you want to compare to random, there is no need to specify this parameter.")
                print("--EB= (exclude bidder) <bool> to exclude config file generation for the bidder.")
                print("The script currently supports the following commands:")
                print("1) Use --VS=100, --VS=110, ... to run simulations where the number of vehicles varies.")
                print("2) Use --RS=10, --RS=15, ... to run simulations where the size of the random pool varies.")
                print("2) Use --B=80, --RS=90, ... to run simulations where the budget of the test vehicle varies.")
                print("Warning: please do not use any of the previous options in the same command.")
                print("The output will be written in the configuration folder.")
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
                        vehicles_list.append(int(currentValue))
                    except ValueError:
                        print("Invalid number of vehicles. Exiting")
                        sys.exit()
                elif currentArgument in ("-d", "--Stp"):
                    print("selected duration: {}".format(currentValue))
                    try:
                        duration = int(currentValue)
                    except ValueError:
                        print("Invalid number of vehicles. Exiting")
                elif currentArgument in ("-r", "--RS"):
                    print("selected random pool percentage: {}%".format(currentValue))
                    try:
                        random_percentage = int(currentValue)
                        random_percentage_list.append(random_percentage)
                    except ValueError:
                        print("Invalid percentage. Exiting")
                elif currentArgument in ("--CT"):
                    print("selected compared behaviour: {}".format(currentValue))
                    if currentValue in supported_b:
                        compare_to = currentValue
                    else:
                        print("selected compared behaviour is not valid. Exiting")
                        sys.exit()
                elif currentArgument in ("--NBB"):
                    print("selected nobidder starting budet: {}".format(currentValue))
                    try:
                        no_bidder_budget = int(currentValue)
                        no_bidder_budget_list.append(no_bidder_budget)
                    except ValueError:
                        print("Invalid no bidder starting budget selected. Exiting")
                elif currentArgument in ("-b", "--B"):
                    print("selected starting budget: {}".format(currentValue))
                    try:
                        budget = int(currentValue)
                        budget_list.append(budget)
                    except ValueError:
                        print("Invalid budget found. Exiting")
                elif currentArgument in ("--EB"):
                    try:
                        exclude_bidder = bool(currentValue)
                    except ValueError:
                        print("Invalid choice for exclude_bidder variable (True or False are supported). Exiting")
                    if exclude_bidder:
                        print("WARNING: Not generating configuration file for RL bidder.")
                    else:
                        print("Generating file for compared model and RL bidder.")
        if compare_to == 'nobidder' and no_bidder_budget is None:
            print("nobidder selected as compared mode but no budget specified. Exiting")
            sys.exit()
        if len(random_percentage_list) > 1:
            print("multiple random percentages have been selected. Considering Rs as the variable.")
            var = 'RS'
        elif len(vehicles_list) > 1:
            print("multiple vehicles have been selected. Considering VS as the variable.")
            var = 'VS'
        elif len(budget_list) > 1:
            print("multiple budget values have been selected. Considering B as the variable.")
            var = 'B'
        elif len(no_bidder_budget_list) > 1:
            print("multiple budgets for nobidder have been selected. Considering NBB as the variable.")
            var = 'NBB'
        if compare_to == 'random':
            create_files_random(vehicles, budget, vehicles_list, model, template, duration, random_percentage, random_percentage_list, budget_list, var, exclude_bidder)
        elif compare_to == 'nobidder':
            create_files_nobidder(vehicles, budget, vehicles_list, model, template, duration, random_percentage, random_percentage_list, budget_list, var, no_bidder_budget,no_bidder_budget_list, exclude_bidder)
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
