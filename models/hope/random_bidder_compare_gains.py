import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

width = 0.5
data_120 = pd.read_csv("compared_exp/average_120T/random_gained_data.txt")
data_130 = pd.read_csv("compared_exp/average_130T/random_gained_data.txt")
data_140 = pd.read_csv("compared_exp/average_140T/random_gained_data.txt")
print(data_120)
matplotlib.use('TkAgg')

# veics = ("120B, 120R", "130B, 130R", "140B, 140R")
veics = (120,130,140)
means = {
    'BidderV1': (round(data_120.iloc[0, 0], 2), round(data_130.iloc[0, 0], 2), round(data_140.iloc[0, 0],2)),
    'Random': (round(data_120.iloc[1, 0],2), round(data_130.iloc[1, 0],2), round(data_140.iloc[1, 0],2)),
}
errors = {
    'BidderV1': (round(data_120.iloc[0, 1],2), round(data_130.iloc[0, 1],2), round(data_140.iloc[0, 1], 2)),
    'Random': (round(data_120.iloc[1, 1],2), round(data_130.iloc[1, 1],2), round(data_140.iloc[1, 1],2)),
}
colors = {
    'BidderV1': "yellowgreen",
    'Random': "greenyellow"
}
x = np.arange(len(veics))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in means.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute, color=colors[attribute], yerr=errors[attribute])
    ax.bar_label(rects, fmt='{:,.2f}%',padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Valuta media risparmiata')
ax.set_xlabel('Numero di veicoli')
ax.set_title('Valuta risparmiata, Bidder(B) e Random(R)')
ax.set_xticks(x+width/2, labels = ['120B, 120R', '130B,130R', '150B, 150R'])
ax.legend(loc='upper left', ncols=3)
ax.set_ylim(0, 100)

plt.savefig("output.png")
