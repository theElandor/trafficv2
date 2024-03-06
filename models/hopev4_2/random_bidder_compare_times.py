import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
import os

#TODO: documentation and how to use

matplotlib.use('TkAgg')
width = 0.5
data = []
directory = './compared_exp'
averages = sorted(os.listdir(directory), key=lambda dirname : int(dirname[8:-1]))
for a in averages:
    data.append(pd.read_csv("compared_exp/{}/evaluation_data.txt".format(a)))
means = {
    'traffic': np.array([[x.iloc[0,0], x.iloc[1,0],x.iloc[2,0]] for x in data]).flatten(),
    'crossroad': np.array([[x.iloc[0,2], x.iloc[1,2],x.iloc[2,2]] for x in data]).flatten()
}
errs = {
    'traffic': np.array([[x.iloc[0,1], x.iloc[1,1], x.iloc[2,1]] for x in data]).flatten(),
    'crossroad': np.array([[x.iloc[0,3], x.iloc[1,3],x.iloc[2,3]] for x in data]).flatten()
}
colors = {
    'traffic_b': 'cornflowerblue',
    'crossroad_b': 'mediumpurple',
    'traffic_r': 'mediumseagreen',
    'crossroad_r': 'forestgreen',
    'traffic_c': 'skyblue',
    'crossroad_c': 'deepskyblue'
}
N = len(averages)
fig, ax = plt.subplots(layout="constrained",figsize=(12, 8))
ind = np.arange(N)
precision = 1
font_size = 8

# booster, disabled(classic), random
width = 0.20  # the width of the bars: can also be len(x) sequence
traffic_b = [round(el,precision) for i,el in enumerate(means['traffic']) if i%3 == 0]
traffic_c = [round(el,precision) for i,el in enumerate(means['traffic']) if i%3 == 1]
traffic_r = [round(el,precision) for i,el in enumerate(means['traffic']) if i%3 == 2]

errs_traffic_b = [round(el,precision) for i,el in enumerate(errs['traffic']) if i%3 == 0]
errs_traffic_c = [round(el,precision) for i,el in enumerate(errs['traffic']) if i%3 == 1]
errs_traffic_r = [round(el,precision) for i,el in enumerate(errs['traffic']) if i%3 == 2]


crossroad_b = [round(el,precision) for i,el in enumerate(means['crossroad']) if i%3 == 0]
crossroad_c = [round(el,precision) for i,el in enumerate(means['crossroad']) if i%3 == 1]
crossroad_r = [round(el,precision) for i,el in enumerate(means['crossroad']) if i%3 == 2]

errs_crossroad_b = [round(el,precision) for i,el in enumerate(errs['crossroad']) if i%3 == 0]
errs_crossroad_c = [round(el,precision) for i,el in enumerate(errs['crossroad']) if i%3 == 1]
errs_crossroad_r = [round(el,precision) for i,el in enumerate(errs['crossroad']) if i%3 == 2]

vars = sorted([int(s[8:-1]) for s in averages])  # veics

offset = 0.05

# bidder----------------
p = ax.bar(ind, traffic_b, width, bottom=0, yerr=errs_traffic_b, label='trained bidder traffic w.t.', color=colors['traffic_b'])
ax.bar_label(p, label_type='center', fontsize=font_size)

p = ax.bar(ind, crossroad_b, width, bottom=traffic_b, yerr=errs_crossroad_b, label='trained bidder crossroad w.t.', color=colors['crossroad_b'])
ax.bar_label(p, label_type='center', fontsize=font_size)
# random ---------------

p = ax.bar(ind + width+offset, traffic_r, width, bottom=0, yerr=errs_traffic_r,label='random bidder traffic w.t.',color=colors['traffic_r'])
ax.bar_label(p, label_type='center', fontsize=font_size)

p = ax.bar(ind + width+offset, crossroad_r, width, bottom=traffic_r, yerr=errs_crossroad_r, label='random bidder crossroad w.t.',color=colors['crossroad_r'])
ax.bar_label(p, label_type='center', fontsize=font_size)

# classic ------------
p = ax.bar(ind + (2*width) + (2*offset), traffic_c, width, bottom=0, yerr=errs_traffic_c,label='standard bidder traffic w.t.',color=colors['traffic_c'])
ax.bar_label(p, label_type='center', fontsize=font_size)

p = ax.bar(ind + (2*width) + 2*offset, crossroad_c, width, bottom=traffic_c, yerr=errs_crossroad_c, label='standard bidder crossroad w.t.',color=colors['crossroad_c'])
ax.bar_label(p,label_type='center', fontsize=font_size)

ax.set_title("Waiting times based on test vehicle's max budget", fontsize=22)
ax.set_xticks(ind + width + offset, labels = ['{}'.format(str(d)) for d in vars])

ax.autoscale_view()

ax.set_ylabel("waiting time", fontsize=18)
ax.set_xlabel("max budget", fontsize=18)
ax.legend(loc='upper left', fontsize=16)
plt.ylim(0, 100)
plt.savefig("output.png", dpi=500)
plt.show()
