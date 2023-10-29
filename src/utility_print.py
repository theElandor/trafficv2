'''
Print utility
'''

import matplotlib.pyplot as plt

# Color ASCII used to change color of prints
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'  # Red
ENDC = '\033[0m'  # De-select the current color
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def log_file_initialization(chunk_name, settings, model_chosen, listener, time):
    """
        A globally accessible log file is created to record details of simulation
        :param chunk_name: if 'main.py' is called from outside ('main_multi') the an identifier is used to distinct log files, otherwise, it's omitted
    """
    global log_file
    global l
    l = listener
    file_name = f'logs/{chunk_name}[' + time + ']' + model_chosen

    for s in settings.keys():
        file_name += '_' + s + ':' + str(settings[s])
    log_file = open(file_name + '.txt', "w")

    for s in settings.keys():
        log_file.write("{}: {}\n".format(s, settings[s]))
    log_file.write('\n')
    print(OKGREEN + 'Log file will be written in \'{}\''.format(file_name) + ENDC)


def log_print(text):
    """
        Calling this function allows to write inside the log file created
    """
    global log_file
    log_file.write("{}\t{}\n".format(l.getStep(), text))



def plot(df, xlabel, title, name):
    """
    Create a box plot showing given waiting times
    :param df: dataframe to be accessed to retrieve values to display
    :param xlabel: title to put on X-axis
    :param title: title of the graph
    :param name: file name in which storing the produced graph
    :param index: DataFrame first column index to access
    :return:
    """
    width_figure = max(len(df.index) * 0.5, 10)
    left_margin = max(1 / (len(df.index)), 0.02)
    right_margin = max(1 - 1 / (len(df.index)), 0.8)
    plt.figure(figsize=(width_figure, 5.0))
    box = []
    for k, vs in df.iterrows():
        box.append([vs['max'], vs['min'], vs['mean'], vs['25%'], vs['75%']])
    plt.boxplot(box, widths=0.6, whis=200)
    plt.xticks(range(len(df.index) + 1),
               [""] + df.index.to_list())  # this put cars's id on x-axis
    plt.tick_params(axis='x', which='major', labelsize=10)

    plt.grid(True)
    plt.ylabel("waiting time (s)")
    plt.xlabel(xlabel)
    plt.title(title)

    plt.subplots_adjust(left=left_margin, bottom=0.1, top=0.9, right=right_margin)
    plt.savefig("plots/" + name)
    print(OKGREEN + "Plot saved in plots/" + name + ENDC)

    return