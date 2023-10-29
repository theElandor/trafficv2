import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np


x = []
test_veic = 74
final_data = {}
final_data['mean_off'] = []
final_data['std_off'] = []
final_data['mean_booster'] = []

final_data['std_booster'] = []
# final_data['mean_on']  = []
# final_data['std_on']   = []
# final_data['mean_simple'] = []
# final_data['std_simple'] = []


# used for pre-testing fase. It reads in qlearn_data folder.
# as the output of tree command shows, each subdir contains
# 1) crossroad waiting times of veics without bidder (crossroad_off)
# 2) traffic waiting times of veics without bidder (traffic_off)
# 3) crossroad waiting times of veics with bidder (crossroad_booster)
# 4) traffic waiting times of veics with bidder (traffic_booster)
# 5) The saved.txt file, that contains information about the amount of saved money.
# actually, booster is not the proper name, it should have been "bidder").

# The '*_booster.txt' files are related to simulations where the bidder is active on the test vehicle.
# On the other hand, '*_off.txt' files are related to simulations where the bidder is either disabled or
# it is set to behave like a random bidder (So it applies a random discount at each iteration).


# The script (which is quite naive honestly) plots for each number of vehicles the mean and std of bot
# traffic waiting time and crossroad waiting time for the test vehicle.
# TODO: refactor this whole plotter, need a better one.

# I used this script mainly to have an idea if the bidding strategy that I was testing influenced
# kinda heavily the waiting times of the test vehicle. (I run 1 simulation for each number of vehicles, with
# and without the bidder, then run this script).
# If the results were encouraging, then I made more simulations and plot the average times (check /traffic/models/hope folder).

# ├── 100
# │   ├── crossroad_booster.txt
# │   ├── crossroad_off.txt
# │   ├── saved_74.txt
# │   ├── traffic_booster.txt
# │   └── traffic_off.txt
# ├── 110
# │   ├── crossroad_booster.txt
# │   ├── crossroad_off.txt
# │   ├── saved_74.txt
# │   ├── traffic_booster.txt
# │   └── traffic_off.txt
# ├── 120
# │   ├── crossroad_booster.txt
# │   ├── crossroad_off.txt
# │   ├── saved_74.txt
# │   ├── traffic_booster.txt
# │   └── traffic_off.txt
# ├── 150
# │   ├── crossroad_booster.txt
# │   ├── crossroad_off.txt
# │   ├── saved_74.txt
# │   ├── traffic_booster.txt
# │   └── traffic_off.txt
# ├── 80
# │   ├── crossroad_booster.txt
# │   ├── crossroad_off.txt
# │   ├── saved_74.txt
# │   ├── traffic_booster.txt
# │   └── traffic_off.txt
# └── 90
#     ├── crossroad_booster.txt
#     ├── crossroad_off.txt
#     ├── saved_74.txt
#     ├── traffic_booster.txt
#     └── traffic_off.txt

evaluate = "crossroad"
directory = "./qlearn_data/"
for root, dirs, filenames in os.walk(directory):
    for dirname in sorted(dirs, key=int):
        x.append(dirname)
        for file in os.listdir(os.path.join(directory, dirname)):
            if file != "saved_74.txt":
                data = pd.read_csv(os.path.join(directory, dirname, file))
                veic = data.iloc[test_veic, 0]
                mean = data.iloc[test_veic, 2]
                std  = data.iloc[test_veic, 3]
                if file == evaluate + "_off.txt":
                    final_data['mean_off'].append(mean)
                    final_data['std_off'].append(std)
                if file == evaluate + "_booster.txt":
                    final_data['mean_booster'].append(mean)
                    final_data['std_booster'].append(std)
points = np.arange(len(x))
width = 0.1
multiplier = 0
# colors = ['orangered','coral', 'forestgreen','limegreen','dodgerblue','deepskyblue']
colors = ['orangered', 'coral', 'darkorchid', 'mediumorchid']
i = 0
fig, ax = plt.subplots(layout = 'constrained')
improv = []
for j in range(len(final_data['mean_booster'])):
    # if final_data['mean_booster'][j] < final_data['mean_off'][j]:
    improv.append(str((1-(final_data['mean_booster'][j]/final_data['mean_off'][j]))*100)[:4]+"%")
print(improv)
for attribute, measurment in final_data.items():
    offset = width * multiplier
    rects = ax.bar(points+offset, measurment, width, label=attribute, color=colors[i])
    multiplier += 1
    if i == 1:
        multiplier += 1
    if i == 2:
        ax.bar_label(container=rects, labels=improv, padding=45)
    i += 1
ax.set_ylabel("Valore")
ax.set_xlabel("Numero di veicoli")
ax.set_title('Media e deviazione standard del tempo di attesa nel traffico')
ax.set_xticks(points + width, x)
ax.set_ylim(0, 60)
ax.legend(loc="upper left", ncols=2)
plt.savefig("./barplot.png", dpi=300)
print(final_data)
