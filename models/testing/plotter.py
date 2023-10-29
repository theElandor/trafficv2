import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
data_120 = pd.read_csv("average_120/evaluation_data.txt")
data_140 = pd.read_csv("average_140/evaluation_data.txt")
data_150 = pd.read_csv("average_150/evaluation_data.txt")

data = {
    'traffic': np.array([data_120.iloc[0,0], data_120.iloc[1,0], data_140.iloc[0,0], data_140.iloc[1,0], data_150.iloc[0,0], data_150.iloc[1,0]]),
    'crossroad': np.array([data_120.iloc[0,2], data_120.iloc[1,2], data_140.iloc[0,2], data_140.iloc[1,2], data_150.iloc[0,2], data_150.iloc[1,2]]),
}
errs = {
    'traffic': np.array([data_120.iloc[0,1], data_120.iloc[1,1], data_140.iloc[0,1], data_140.iloc[1,1], data_150.iloc[0,1], data_150.iloc[1,1]]),
    'crossroad': np.array([data_120.iloc[0,3], data_120.iloc[1,3], data_140.iloc[0,3], data_140.iloc[1,3], data_150.iloc[0,3], data_150.iloc[1,3]]),
}
colors = {
    'traffic': 'cornflowerblue',
    'crossroad': 'mediumpurple'
}


veicoli = ('120B', '120', '140B', '140', '150B', '150')
# veicoli = ('120', '140', '150')
width = 0.6  # the width of the bars: can also be len(x) sequence


fig, ax = plt.subplots()
bottom = np.zeros(6)

for cat, arr in data.items():
    cropped = [round(n, 2) for n in arr]
    p = ax.bar(veicoli, cropped, width, label=cat, bottom=bottom, yerr=errs[cat], color=colors[cat])
    bottom += arr

    ax.bar_label(p, label_type='center')

ax.set_title('Tempo di attesa nel traffico e agli incroci, bidderV2')
ax.set_xlabel("Numero di veicoli")
ax.set_ylabel("Tempo di attesa")
ax.legend()

plt.savefig("output.png")
