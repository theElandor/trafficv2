import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
folder = "compared_exp"
for d in os.listdir(folder):
    directory = os.path.join(folder, d)
    count = 0
    traffic_random = []
    traffic_booster = []
    crossroad_random = []
    crossroad_booster = []
    gain_random = []
    gain_booster = []
    for root, dirs, filenames in os.walk(directory):
        for dirname in sorted(dirs, key=int):
            count += 1
            for file in os.listdir(os.path.join(directory, dirname)):
                if file != "gained_booster.txt" and file != "gained_random.txt":
                    data = pd.read_csv(os.path.join(directory, dirname, file))
                    veic = data.iloc[74, 0]
                    mean = data.iloc[74, 2]
                    std  = data.iloc[74, 3]
                    if file == "traffic_random.txt":
                        traffic_random.append(mean)
                    if file == "traffic_booster.txt":
                        traffic_booster.append(mean)
                    if file == "crossroad_random.txt":
                        crossroad_random.append(mean)
                    if file == "crossroad_booster.txt":
                        crossroad_booster.append(mean)
                else:
                    with open(os.path.join(directory, dirname, file)) as g:
                        gained = [int(el.strip()) for el in g.readlines()]
                        if file == "gained_random.txt":
                            gain_random.append(gained[0]/(gained[1]*100))
                        else:
                            gain_booster.append(gained[0]/(gained[1]*100))

    traffic_meanwt_random = np.mean(traffic_random)
    traffic_stdwt_random = np.std(traffic_random)

    traffic_meanwt_booster = np.mean(traffic_booster)
    traffic_stdwt_booster = np.std(traffic_booster)

    crossroad_meanwt_random = np.mean(crossroad_random)
    crossroad_stdwt_random = np.std(crossroad_random)

    crossroad_meanwt_booster = np.mean(crossroad_booster)
    crossroad_stdwt_booster = np.std(crossroad_booster)


    with open(os.path.join(directory, "evaluation_data.txt"), "w") as f:
        f.write("mean_traffic, std_traffic, mean_crossroad, std_crossroad\n")
        f.write(str(traffic_meanwt_booster) + ", " + str(traffic_stdwt_booster) + ", " + str(crossroad_meanwt_booster) + ", " + str(crossroad_stdwt_booster) + "\n")
        f.write(str(traffic_meanwt_random) + ", " + str(traffic_stdwt_random) + ", " + str(crossroad_meanwt_random) + ", " + str(crossroad_stdwt_random) + "\n")

    with open(os.path.join(directory, "random_gained_data.txt"), "w") as f:
        f.write("mean, std\n")
        f.write(str(np.mean(gain_booster)*100) + "," + str(np.std(gain_booster)*100) + "\n")
        f.write(str(np.mean(gain_random)*100) + "," + str(np.std(gain_random)*100))
