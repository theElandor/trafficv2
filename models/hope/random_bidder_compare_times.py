import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

# REQUIRMENTS (needs to be generalized):
# ./average_120B
# ./average_130B
# ./average_150B
# each one of theese folders needs to contain a file called evaluation_data.txt
# It is a csv formatted this way:

# mean_traffic, std_traffic, mean_crossroad, std_crossroad
# 20.24450180808092, 1.267402893222875, 14.856783061555536, 0.7008861785015196
# 20.947898067067158, 0.9329796667319809, 16.140463411779805, 1.6073432761431514

# the above example contains the mean and std of waiting times of the test vehicle.
# first line -->  bidder is active
# second line --> random bidder is active

# the scripts produces a barplot that compares the waiting times
# of the test vehicle (each bar corresponds to a different number of vehicles on the map).

matplotlib.use('TkAgg')
data_120 = pd.read_csv("compared_exp/average_120T/evaluation_data.txt")
data_130 = pd.read_csv("compared_exp/average_130T/evaluation_data.txt")
data_140 = pd.read_csv("compared_exp/average_140T/evaluation_data.txt")

data = {
    'traffic': np.array([data_120.iloc[0,0], data_120.iloc[1,0], data_130.iloc[0,0], data_130.iloc[1,0], data_140.iloc[0,0], data_140.iloc[1,0]]),
    'crossroad': np.array([data_120.iloc[0,2], data_120.iloc[1,2], data_130.iloc[0,2], data_130.iloc[1,2], data_140.iloc[0,2], data_140.iloc[1,2]]),
}
errs = {
    'traffic': np.array([data_120.iloc[0,1], data_120.iloc[1,1], data_130.iloc[0,1], data_130.iloc[1,1], data_140.iloc[0,1], data_140.iloc[1,1]]),
    'crossroad': np.array([data_120.iloc[0,3], data_120.iloc[1,3], data_130.iloc[0,3], data_130.iloc[1,3], data_140.iloc[0,3], data_140.iloc[1,3]]),
}
# colors = {
#     'traffic_bidder': 'mediumblue',
#     'traffic_random': 'cornflowerblue',
#     'crossroad_bidder': 'rebeccapurple',
#     'crossroad_random': 'mediumpurple',
# }
colors = {
    'traffic': 'cornflowerblue',
    'crossroad': 'mediumpurple',
}

# labels = ('120B', '120R', '130B', '130R', '140B', '140R')
fig, ax = plt.subplots()
N = 3 # number of groups
ind = np.arange(N)
width = 0.30  # the width of the bars: can also be len(x) sequence
# {traffic: [], crossroad[]}
print(data['traffic'])
traffic_b = [round(el,2) for i,el in enumerate(data['traffic']) if i%2 == 0]
traffic_r = [round(el,2) for i,el in enumerate(data['traffic']) if i%2 != 0]
errs_traffic_b = [round(el,2) for i,el in enumerate(errs['traffic']) if i%2 == 0]
errs_traffic_r = [round(el,2) for i,el in enumerate(errs['traffic']) if i%2 != 0]

crossroad_b = [round(el,2) for i,el in enumerate(data['crossroad']) if i%2 == 0]
crossroad_r = [round(el,2) for i,el in enumerate(data['crossroad']) if i%2 != 0]
errs_crossroad_b = [round(el,2) for i,el in enumerate(errs['crossroad']) if i%2 == 0]
errs_crossroad_r = [round(el,2) for i,el in enumerate(errs['crossroad']) if i%2 != 0]

# traffic = [traffic_b, traffic_r]
# crossroad = [crossroad_b, crossroad_r]
# total = [traffic, crossroad]

offset = 0.05
#traffic and crossroad b
p = ax.bar(ind, traffic_b, width, bottom=0, yerr=errs_traffic_b, label='traffic', color=colors['traffic'])
ax.bar_label(p, label_type='center')
p = ax.bar(ind, crossroad_b, width, bottom=traffic_b, yerr=errs_crossroad_b, label='crossroad', color=colors['crossroad'])
ax.bar_label(p, label_type='center')

p = ax.bar(ind + width+offset, traffic_r, width, bottom=0, yerr=errs_traffic_r, color=colors['traffic'])
ax.bar_label(p, label_type='center')
p = ax.bar(ind + width+offset, crossroad_r, width, bottom=traffic_r, yerr=errs_crossroad_r, color=colors['crossroad'])
ax.bar_label(p, label_type='center')

ax.set_title('Tempo di attesa nel traffico e agli incroci, Bidder(B) e Random(R)')
ax.set_xticks(ind + (width/2)+(offset/2), labels = ['120B, 120R', '130B,130R', '150B, 150R'])

ax.legend()
ax.autoscale_view()

ax.set_xlabel("Numero di veicoli")
ax.set_ylabel("Tempo di attesa")
ax.legend()
plt.savefig("output.png")
# fig, ax = plt.subplots()
# bottom = np.zeros(6)
# i = 0
# for cat, arr in data.items():
#     cropped = [round(n, 2) for n in arr]    
#     p = ax.bar(veicoli, cropped, width, label=cat, bottom=bottom, yerr=errs[cat], color=colors[cat])
#     bottom += arr

#     ax.bar_label(p, label_type='center')

# ax.set_title('Tempo di attesa nel traffico e agli incroci, bidderV1 e Random')

# plt.savefig("output.png")
