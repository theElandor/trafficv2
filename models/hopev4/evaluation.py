import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
folder = "compared_exp"
for d in os.listdir(folder):
    directory = os.path.join(folder, d)
    count = 0
    traffic_disabled = []
    traffic_booster = []
    crossroad_disabled = []
    crossroad_booster = []
    gain_disabled = []
    gain_booster = []
    for root, dirs, filenames in os.walk(directory):
        for dirname in sorted(dirs, key=int):
            count += 1
            for file in os.listdir(os.path.join(directory, dirname)):
                if file != "gained_booster.txt" and file != "gained_disabled.txt":
                    data = pd.read_csv(os.path.join(directory, dirname, file))
                    veic = data.iloc[74, 0]
                    mean = data.iloc[74, 2]
                    std  = data.iloc[74, 3]
                    if file == "traffic_disabled.txt":
                        traffic_disabled.append(mean)
                    if file == "traffic_booster.txt":
                        traffic_booster.append(mean)
                    if file == "crossroad_disabled.txt":
                        crossroad_disabled.append(mean)
                    if file == "crossroad_booster.txt":
                        crossroad_booster.append(mean)
                else:
                    with open(os.path.join(directory, dirname, file)) as g:
                        gained = [int(el.strip()) for el in g.readlines()]
                        if file == "gained_disabled.txt":
                            gain_disabled.append(gained[0]/(gained[1]*100))
                        else:
                            gain_booster.append(gained[0]/(gained[1]*100))

    traffic_meanwt_disabled = np.mean(traffic_disabled)
    traffic_stdwt_disabled = np.std(traffic_disabled)

    traffic_meanwt_booster = np.mean(traffic_booster)
    traffic_stdwt_booster = np.std(traffic_booster)

    crossroad_meanwt_disabled = np.mean(crossroad_disabled)
    crossroad_stdwt_disabled = np.std(crossroad_disabled)

    crossroad_meanwt_booster = np.mean(crossroad_booster)
    crossroad_stdwt_booster = np.std(crossroad_booster)


    with open(os.path.join(directory, "evaluation_data.txt"), "w") as f:
        f.write("mean_traffic, std_traffic, mean_crossroad, std_crossroad\n")
        f.write(str(traffic_meanwt_booster) + ", " + str(traffic_stdwt_booster) + ", " + str(crossroad_meanwt_booster) + ", " + str(crossroad_stdwt_booster) + "\n")
        f.write(str(traffic_meanwt_disabled) + ", " + str(traffic_stdwt_disabled) + ", " + str(crossroad_meanwt_disabled) + ", " + str(crossroad_stdwt_disabled) + "\n")

    with open(os.path.join(directory, "disabled_gained_data.txt"), "w") as f:
        f.write("mean, std\n")
        f.write(str(np.mean(gain_booster)*100) + "," + str(np.std(gain_booster)*100) + "\n")
        f.write(str(np.mean(gain_disabled)*100) + "," + str(np.std(gain_disabled)*100))
