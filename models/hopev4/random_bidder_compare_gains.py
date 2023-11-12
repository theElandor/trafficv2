import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib


# REQUIRMENTS (needs to be generalized):
# ./average_120B
# ./average_130B
# ./average_150B
# each one of theese folders needs to contain a file called random_gained_data.txt
# It is a csv formatted this way:
# mean, std
# 67.70982142857143,11.865344994156603
# 45.13839285714285,12.19822183402113

# the above example contains the mean and std of money that is gained thanks to the model.
# first line -->  bidder is active
# second line --> random bidder is active

# the scripts produces a barplot that compares the amount of gained money
# of the bidder and of the random bidder.
matplotlib.use('TkAgg')
width = 0.5
data = []
directory = './compared_exp'
averages = sorted(os.listdir(directory), key=lambda dirname : int(dirname[8:-1]))
print(averages)
for a in averages:
    data.append(pd.read_csv("compared_exp/{}/random_gained_data.txt".format(a)))
vars = sorted([int(s[8:-1]) for s in averages])  # veics
means = {
    'Bidder': tuple([round(x.iloc[0,0],2) for x in data]),

    'Random': tuple([round(x.iloc[1,0],2) for x in data])
}
errors = {
    'Bidder': tuple([round(x.iloc[0,1],2) for x in data]),
    'Random': tuple([round(x.iloc[1,1],2) for x in data])
}
colors = {
    'Bidder': "yellowgreen",
    'Random': "greenyellow"
}
x = np.arange(len(vars))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in means.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute, color=colors[attribute], yerr=errors[attribute])
    ax.bar_label(rects, fmt='{:,.0f}%', padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Saved currency')
ax.set_xlabel('Initial budget')
ax.set_title('Saved currency based on test vehicle initial budget')
ax.set_xticks(x+width/2, labels = ['{}'.format(str(d)) for d in vars])
ax.legend(loc='upper left', ncols=1)
ax.set_ylim(0, 100)
plt.savefig("gained.png")
plt.show()
