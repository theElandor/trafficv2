import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


width = 0.5
data_120 = pd.read_csv("average_120/gained_data.txt")
data_140 = pd.read_csv("average_140/gained_data.txt")
data_150 = pd.read_csv("average_150/gained_data.txt")

y = []
err = []

gained_120 = [data_120.iloc[i, 0] for i in range(len(data_120))]
tot_120 = [data_120.iloc[i, 1] for i in range(len(data_120))]
data_120 = [gained_120[i]/tot_120[i] for i in range(len(gained_120))]
y.append(np.mean(data_120))
err.append(np.std(data_120))

gained_140 = [data_140.iloc[i, 0] for i in range(len(data_140))]
tot_140 = [data_140.iloc[i, 1] for i in range(len(data_140))]
data_140 = [gained_140[i]/tot_140[i] for i in range(len(gained_140))]
y.append(np.mean(data_140))
err.append(np.std(data_140))


gained_150 = [data_150.iloc[i, 0] for i in range(len(data_150))]
tot_150 = [data_150.iloc[i, 1] for i in range(len(data_150))]
data_150 = [gained_150[i]/tot_150[i] for i in range(len(gained_150))]
y.append(np.mean(data_150))
err.append(np.std(data_150))
veics = ("120", "140", "150")

fig, ax = plt.subplots()
bar_container = ax.bar(veics, y, color='yellowgreen', yerr=err, width=0.6)
ax.set(ylabel='Valuta risparmiata rispetto al totale', xlabel='numero di veicoli',title='Valuta risparmiata da bidderV2', ylim=(0, 70))
ax.bar_label(bar_container, fmt='{:,.0f}%', padding=5)

plt.savefig("gained.png")
