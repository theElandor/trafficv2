import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib


matplotlib.use('TkAgg')
width = 0.5
data = []
directory = './compared_exp'
averages = sorted(os.listdir(directory), key=lambda dirname : int(dirname[8:-1]))
print(averages)
for a in averages:
    data.append(pd.read_csv("compared_exp/{}/disabled_gained_data.txt".format(a)))
vars = sorted([int(s[8:-1]) for s in averages])  # veics
means = {
    'Bidder': tuple([round(x.iloc[0,0],2) for x in data]),
    'Random': tuple([round(x.iloc[2,0],2) for x in data])
}
errors = {
    'Bidder': tuple([round(x.iloc[0,1],2) for x in data]),
    'Random': tuple([round(x.iloc[2,1],2) for x in data])
}
colors = {
    'Bidder': "yellowgreen",
    'Random': "greenyellow"
}
x = np.arange(len(vars))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained', figsize=(12,8))

labl = ['trained bidder','random bidder']
for attribute, measurement in means.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=labl[multiplier], color=colors[attribute], yerr=errors[attribute])
    ax.bar_label(rects, fmt='{:,.0f}%', padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('% saved budget', fontsize=18)
ax.set_xlabel('number of vehicles', fontsize=18)
ax.set_title('% saved budget based on number of vehicles', fontsize=22)
ax.set_xticks(x+width/2, labels = ['{}'.format(str(d)) for d in vars])
ax.legend(loc='upper left', ncols=1, fontsize=18)
ax.set_ylim(0, 100)
plt.savefig("gains.png", dpi=500)
plt.show()
