import matplotlib.pyplot as plt
import numpy as np
import os
import re
import pandas as pd
import seaborn as sns
from collections import defaultdict
from prettytable import PrettyTable

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'  # Red
ENDC = '\033[0m'  # De-select the current color
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def plot(data, title):
    plt.figure(figsize=(max(width_figure, 15), max(width_figure, 15)))
    plt.boxplot(data, widths=0.5, whis=10)
    plt.title(title, fontsize=20)
    plt.ylabel('waiting time (s)', fontsize=14)
    plt.xlabel(legend, position=(-0.1, -0.5), fontsize=14, horizontalalignment='left')
    plt.xticks(range(len(labels) + 1), [''] + labels)
    plt.tick_params(axis='y', labelsize=16)
    plt.tick_params(axis='x', which='major', labelsize=14)
    plt.grid(True)
    plt.subplots_adjust(left=left_margin, bottom=bot_margin, top=top_margin, right=right_margin)
    n = 1
    for m in data:
        plt.text(n-0.15, m[0]+(0.7-0.7/len(str(m[0]))), f'{m[2]:5.2f}', fontsize=14)
        n+=1
    plt.savefig('plots/' + title + '.png')
    print('Plot saved as \"' + title + '.png\"')
    plt.show()
    plt.close()


data = defaultdict(dict)
date_format = r'\[(.)+\]'
file_format = r'\|(cross-total|traffic-total)'
extra = r'\|(extra_configs)'

# moving in the upper directory level
os.chdir(os.getcwd()+'/../')

print(WARNING + 'Reading simulations results from "data" folder...' + ENDC)
for i in sorted(os.listdir('data')): #for each filename in directory
    print(i)
    # cross_total
    # traffic_total
    p = re.compile(file_format)
    file_type = p.search(str(i))

    q = re.compile(extra)
    file_type_extra = q.search(str(i))

    # Checking that given file matches required file type ('cross_total' or 'traffic_total')
    if file_type:
        file_type = file_type.group(1)  # The second field contains the type of data contained (i.e. 'cross_total)
        p = re.compile(date_format)
        simulation_date = p.search(str(i))
        simulation_date = simulation_date.group(0)  # group(1) will return the 1st capture (stuff within the brackets).
        print("SIMUL_DATE:" + str(simulation_date))
        # group(0) will returned the entire matched text.
        print('Loaded file: ' + str(i))
        df = pd.read_csv('data/' + str(i))
        data[simulation_date][file_type] = df
        data[simulation_date]['config'] = str(i)
        
    if file_type_extra:
        file_type_extra = file_type_extra.group(1)  # The second field contains the type of data contained (i.e. 'cross_total)
        q = re.compile(date_format)
        simulation_date = q.search(str(i))
        simulation_date = simulation_date.group(0)  # group(1) will return the 1st capture (stuff within the brackets).
        with open('data/'+str(i), "r") as f:
            temp = f.read()
            data[simulation_date]['extra_configs'] = temp
    
print(OKGREEN + 'Done' + ENDC)

labels = []
legend = '\n'


crossroad_waiting_times = []
traffic_waiting_times = []
num_sim = 0
file_records = []
for d in data.keys(): #for each simulation
    num_sim += 1
    df = data[d]['cross-total']
    crossroad_waiting_times.append([df['crossroad_waiting_time']['max'], df['crossroad_waiting_time']['min'], df['crossroad_waiting_time']['mean']])
    record = [num_sim, round(df['crossroad_waiting_time']['mean'],2), round(df['crossroad_waiting_time']['std'], 2)]

    df = data[d]['traffic-total']
    traffic_waiting_times.append([df['traffic_waiting_time']['max'], df['traffic_waiting_time']['min'], df['traffic_waiting_time']['mean']])
    record.append(round(df['traffic_waiting_time']['mean'], 2))
    record.append(round(df['traffic_waiting_time']['std'], 2))

    file_records.append(record)

    name = data[d]['config'].replace('.txt', '').replace('|traffic-total', '').replace('|cross-total', '').replace(d, '').replace('_', ' ')
    labels.append(num_sim)
    legend += str(num_sim) + ': ' + name + " " +data[d]['extra_configs']+'\n'


width_figure = num_sim
left_margin = 0.1
right_margin = 0.98
bot_margin = min(0.1 * num_sim, 0.4)
top_margin = 0.95

plot(crossroad_waiting_times, 'Crossroad Waiting Time Simulations Comparison')
plot(traffic_waiting_times, 'Traffic Waiting Time Simulations Comparison')

pt = PrettyTable()
pt.field_names = ["Sim #", "Avg CWT", "Std Dev CWT", "Avg TWT", "Std Dev TWT"]
for i in file_records:
    pt.add_row(i)

file = open('data/cwt-twt.txt', 'w+')
file.write(pt.get_string())
