import subprocess
import os
directory = "compared_exp"
averages = sorted(os.listdir(directory), key=lambda dirname : int(dirname[8:-1]))
for a in averages:
    print(a)
    # print("compared_exp/{}/evaluation.py".format(a))
    subprocess.run(["python", "compared_exp/{}/evaluation.py".format(a)])
