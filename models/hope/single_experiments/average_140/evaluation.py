import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
directory = "."
count = 0
traffic_off = []
traffic_booster = []
crossroad_off = []
crossroad_booster = []
for root, dirs, filenames in os.walk(directory):
    for dirname in sorted(dirs, key=int):
        count += 1
        for file in os.listdir(os.path.join(directory, dirname)):
            if file != "saved_74.txt":
                data = pd.read_csv(os.path.join(directory, dirname, file))
                veic = data.iloc[74, 0]
                mean = data.iloc[74, 2]
                std  = data.iloc[74, 3]
                if file == "traffic_off.txt":
                    traffic_off.append(mean)
                if file == "traffic_booster.txt":
                    traffic_booster.append(mean)
                if file == "crossroad_off.txt":
                    crossroad_off.append(mean)
                if file == "crossroad_booster.txt":
                    crossroad_booster.append(mean)

traffic_meanwt_off = np.mean(traffic_off)
traffic_stdwt_off = np.std(traffic_off)

traffic_meanwt_booster = np.mean(traffic_booster)
traffic_stdwt_booster = np.std(traffic_booster)

crossroad_meanwt_off = np.mean(crossroad_off)
crossroad_stdwt_off = np.std(crossroad_off)

crossroad_meanwt_booster = np.mean(crossroad_booster)
crossroad_stdwt_booster = np.std(crossroad_booster)
print("-------Traffic--------")
print("Booster/Off mean\t" + str(traffic_meanwt_booster)[:5]+"\t"+str(traffic_meanwt_off)[:5])
print("Booster/Off std\t\t" + str(traffic_stdwt_booster)[:4]+"\t"+str(traffic_stdwt_off)[:4])
print("-------Crossroad--------")
print("Booster/Off mean\t" + str(crossroad_meanwt_booster)[:5]+"\t"+str(crossroad_meanwt_off)[:5])
print("Booster/Off std\t\t" + str(crossroad_stdwt_booster)[:4]+"\t"+str(crossroad_stdwt_off)[:4])

with open("evaluation_data.txt", "w") as f:
    f.write("mean_traffic, std_traffic, mean_crossroad, std_crossroad\n")
    f.write(str(traffic_meanwt_booster) + ", " + str(traffic_stdwt_booster) + ", " + str(crossroad_meanwt_booster) + ", " + str(crossroad_stdwt_booster) + "\n")
    f.write(str(traffic_meanwt_off) + ", " + str(traffic_stdwt_off) + ", " + str(crossroad_meanwt_off) + ", " + str(crossroad_stdwt_off) + "\n")
    
