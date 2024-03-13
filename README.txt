------PRE-READ stuff---------
+ I will refer to elements in the appendix as [1], [2], ecc...
+ You will find messy code in this repo. There is still a lot of stuff to do:
  in general, the code needs to be cleaned and refactored.
  Also the scripts can be improved and extended as far as functionalities are concerned.
  You will find more specific references to what can be improved while you read.
+ Logs file are not mantained. During developement I preferred to use the console
  and print stuff at runtime. A better debugger is needed. If you want, you can try to
  create one!

+ Remember: please use the 3.9 version of Python, don't use python 3.10 as some things
  could go wrong. You can use python3.10 to run the plotting scripts.
--------TESTING A MODEL PART1, SINGLE SIMULATION------------


Each run has a configuration file (yml file), that you must place in the configs/Comp/
directory. Here's a sample configuration file:

# Standard configs
model: Coop
CP: owp
MCA: 1
E: y
Bdn: b
Rts: f
RUNS: 1
TV: 74

# Simulation settings
Vr: RS
Stp: 5000
VS: 120
UB: 7
RS: 10


# Startup configuration
train: False
load: True
name: booster
MV: hopev4_2
AI: 1

#sponsorship policy
B: 100
Spn: 10
betaL: 0.05
betaU: 0.15
betaR: 0.1

# hyperparameters
alpha: 0.3
TF: 10
UF: 10
EXE: 1
EVE: 0
BS: 32
G: 0.3

we don't need to go in the details of the parameters right now, as you can find
a detailed description of each parameter below. For now, just note that
1 file = 1 simulation.
If you want to understand how the simulator works, try to tweak the parameters
of the simulation after reading the description of them at the end of this file.
I strongly recommend to read my thesis/paper([2],[3]) to fully understand the meaning of most of the parameters.
Focus on the "simulation settings" at first, as they are the simplest parameters to play with.

As we haven't seen the training part yet, you don't have to care too much about the "hyperparameters"
for the moment.
You can find the output file of your simulation in the "data" folder, but also in the /models/<model_version>/compared_exp....
folder, according to your model version and some other parameters. Check the "OUTPUT FILES GENERATION" chapter,"SIMULATION PARAMETERS DESCRIPTION" chapter
and [1] for more details.
This choice was driven by the fact that, when running multiple simulations at once, it would be nice to have
the output files automatically saved in a target folder, so that we can plot data using scripts in a more versatile way.
There will be a separate chapter on plotting scripts, for now just note the fact that they need files to be stored
in a specific way inside the mentioned folder.

To run your single simulation, just use

python main.py


-----PART2, MULTIPLE SIMULATIONS

During testing you might want to run multiple experiments, varying (for example)
the ratio of vehicles behaving randomly. To do that, you should run multiple
experiments for each one of the configurations, then plot your result.
This means that you should create (for example) 10 files for 10% ratio (that are all the same),
then 10 files for the 15% ratio, ecc...
Instead of creating them manually, you can use the script that I created (generate_configs.py)
that takes care of everything. For example, look at the following command:

python3 generate_configs.py --MV=hopev4_2 --VS=120 --Stp=5000 --B=100 --CT=random --RS=10 --RS=15 --RS=20 --RS=25 --RS=30 --RS=35

This command floods the configuration folder with the following files:
+ 10 files where the test vehicle is using the trained bidder (the file name has a B in it) for the 10% ratio;
+ 10 files where the test vehicle is using the trained bidder (the file name has a B in it) for the 15% ratio;
+ 10 files where the test vehicle is using the trained bidder (the file name has a B in it) for the 20% ratio;
....
As the --CT flag is set to random, it means that we want to compare the trained bidder behaviour with the
random behaviour, so we also have:
+ 10 files where the test vehicle is using the random bidder (the file name has a R in it) for the 10% ratio;
+ 10 files where the test vehicle is using the random bidder (the file name has a R in it) for the 15% ratio;
+ 10 files where the test vehicle is using the random bidder (the file name has a R in it) for the 20% ratio;
....
Note also that:
+ for the trained bidder config files, the loaded model is hopev4_2, as specified with the MV flag;
+ in every simulation the number of vehicles is fixed to 120, as specified with the VS paramter;
+ the starting budget for the test vehicle is 100, as specified in the B parameter;
+ the duration of the simulation is always 5000;
After the generation of the config files, you are ready to start your experiments. If you run the
program with

python main.py

you can immediatly see that the simulator detects all of your files. It takes them in chunks of 5
and run them in parallel, stressing a bit the CPU but saving time.
Obviously, don't use the graphical user interface for this kind of task.

---------OUTPUT FILES GENERATION----------
When you run main.py, all of the configuration files will be read and the simulation will start.
Before actually starting, the simulator will take care of creating the folders in which the
output files will be placed. The only needed thing is to have a folder called compared_exp in
the models/<model_name> folder. The last stable (published) model is hopev4_2, so take that
one as a reference. If the compared_exp folder is not present, the simulation will not start.
If you try to run the currently loaded simulation (the configuration files are in the main branch)
you can see that the program automatically generates some folders inside the compared_exp folder.
Inside each one of the subfolders there is one folder for each one of the 10 experiments related
to that specific simulation setting.
Here's the structure of the compared_exp folder


├── average_10T
│   ├── 1
│   │   ├── crossroad_booster.txt
│   │   ├── crossroad_random.txt
│   │   ├── gained_booster.txt
│   │   ├── gained_random.txt
│   │   ├── traffic_booster.txt
│   │   └── traffic_random.txt
│   ├── 2
│   │   ├── crossroad_booster.txt
│   │   ├── crossroad_random.txt
│   │   ├── gained_booster.txt
│   │   ├── gained_random.txt
│   │   ├── traffic_booster.txt
│   │   └── traffic_random.txt
│   ├── 3
│   │   ├── crossroad_booster.txt
│   │   ├── crossroad_random.txt
│   │   ├── gained_booster.txt
│   │   ├── gained_random.txt
│   │   ├── traffic_booster.txt
│   │   └── traffic_random.txt
│   ├── 4
│   │   ├── crossroad_booster.txt
│   │   ├── crossroad_random.txt
│   │   ├── gained_booster.txt
│   │   ├── gained_random.txt
│   │   ├── traffic_booster.txt
│   │   └── traffic_random.txt
.....
.....
.....
│   ├── 9
│   │   ├── crossroad_booster.txt
│   │   ├── crossroad_random.txt
│   │   ├── gained_booster.txt
│   │   ├── gained_random.txt
│   │   ├── traffic_booster.txt
│   │   └── traffic_random.txt
│   └── 10
│       ├── crossroad_booster.txt
│       ├── crossroad_random.txt
│       ├── gained_booster.txt
│       ├── gained_random.txt
│       ├── traffic_booster.txt
│       └── traffic_random.txt
├── average_15T
│   ├── 1
│   │   ├── crossroad_booster.txt
│   │   ├── crossroad_random.txt
│   │   ├── gained_booster.txt
│   │   ├── gained_random.txt
│   │   ├── traffic_booster.txt
│   │   └── traffic_random.txt
│   ├── 2
│   │   ├── crossroad_booster.txt
│   │   ├── crossroad_random.txt
│   │   ├── gained_booster.txt
│   │   ├── gained_random.txt
│   │   ├── traffic_booster.txt
│   │   └── traffic_random.txt
│   ├── 3
│   │   ├── crossroad_booster.txt
│   │   ├── crossroad_random.txt
│   │   ├── gained_booster.txt
│   │   ├── gained_random.txt
│   │   ├── traffic_booster.txt
│   │   └── traffic_random.txt

....
....
....


I created this specific tree structure because i thought that it would result usefull
during the "plotting" phase, where you have to somehow summarize all of the data.
The generated text files for each subdirs are the following:
+ crossroad_booster.txt --> contains crossroad waiting times (CWT) for a simulation where the trained bidder was active.
  Remember that the "trained bidder" is often called "booster".
+ traffic booster.txt --> same as crossroad booster but for traffic waiting times (TWT).
+ traffic random.txt --> contains TWT for a simulation in which the random bidder was active.
+ crossroad random.txt --> CWT for random bidder.
+ gained bidder.txt--> data related to the amount of currenct saved by the trained bidder (or booster)
+ gained random.txt --> data related to the amount of currency saved by the random bidder.

For simulations in which the test vehicle uses the "classic" policy, you will find in these folders
files called "traffic disabled" or "crossroad disabled". They contain the related waiting times.
You will never find "gained classic" files because the classic policy does not save any currency.

----------------------PLOTTING DATA---------------------
Plotting data is pretty simple.
Once you did your simulations (so you filled the model/<model_name>/compared_exp folder, you might want to compare the performance in wating times and saved currency
for the different behaviours of the bidder. There are 2 scripts (that must be placed in the model/<model_name> folder) that take care of this:
1) random_bidder_compare_gains.py
   This script is used to check the amount of currency saved by the bidder.
   This script only takes into account the random bidder and the trained bidder. This is because the
   classic behaviour doesn't save any money, as it spends all of its starting budget at each run.
   The script will look in the compared_exp/ folder and look for simulations related to either
   the random bidder and trained bidder, and compare the results.
   Make sure to change the labels of the bars and the title of the plot according to what you
   saved in the compared_exp/ folder: for example, if you ran a simulation where the random pool percentage varies (like in the currently loaded example),
   then make sure to put a % in the bar labels.
2) random_bidder_compare_times.py
   This script is used to check the waiting times of the test vehicle based on the type of bidder used.
   Originally, this script was created to handle only random_bidder vs trained_bidder comparisons, but
   then I added also the classic_bidder related bar in the plot.
   This means that the script will look for simulations where the bidder is trained, random or classic
   and plot the traffic waiting time and crossroad waiting time for each one of the behaviours.
   If you look in the BACKUP folder, you can find some examples of plots and related data (just explore
   the compared_exp folder)
   Also in this case, make sure to change the title and the bar labels according to the simulation variable.

----------TRAINING A MODEL----------------
Let's say a couple of things in advance:
+ Training a model means training the bidder for A SINGLE VEHICLE. One of the main things that
  can be implemented is the ability to mount and train the bidder on multiple vehicles. This
  would require keeping in memory the loaded model for each one of the vehicles: it might
  be really expensive if the models are deep-learning models.
  One way to solve this is to change the neural network structure and make it lighter.
  It should be quite easy to do that: just take care of training another model with
  the modified structure, keeping the same configuration file as hopev4-2.
  Another "not-so-crazy" idea is to implement Q-Learning instead of Deep-Q-Learning, so that you can use
  a simple 2D matrix to store learning information instead of a neural network. Read [3] for more details.
  
+ TensorFlow was used in this project. According to my experience, PyTorch might be a better library to
  use for the sake of this project. If you are interested, you might want to re-base the deep-learning model on PyTorch
  instead of TensorFlow.

TODO


---------SIMULATION PARAMETERS DESCRIPTION------------------

model: always Coop (even though the kind of simulation is "competitive".
	   I started working on the "coop" so I kept it. Need to be fixed.)
CP: owp, is the only tested one.
MCA: 1, minimum cars per auction. This means that
	 even with 1 car the auction takes place.
E: enhancement, y for active n for inactive
Bdn: fixed to b, don't change this parameter
Rts: parameter related to rerouting, tested only
	 with fixed ("f") reroutes
RUNS: number of runs for experiment. It's better
	  to keep this parameter to 1 and make multiple
	  files for different experiments. This way more
	  simulations will run at once and it will be
	  much faster. If you want to make 2 identical simulations,
	  just copy the configuration file and change the "AI"
	  parameter.
TV: stands for "test vehicle", meaning the one on which
	the bidder(either RL or random) will be mounted.
	Only vehicle 74 has been tested.
Vr: parameter automatically generated when using the
	generate_config.py script. It indicates the
	"variable" of the simulation. For example, if you
	want to make experiments in which the number
	og vehicles simulated varies, then this variable
	will be set to "VS". This Vr variable will be used
	to determine the "folder_name" parameter, which is
	needed to determine the path in which the output file
	of the simulation will be written ([1]).
Stp: Number of steps of the simulation. Usually fixed to 5000
VS: Total number of vehicles in the simulation
UB: Upper bound of the speed for vehicles. The speed of
	non-test vehicles will be initialized with a random value
	between 4 and UB. The test vehicle will always be initialized
	with a speed of 4.
RS: Random pool size. It is the percentage of vehicles among
	the whole amount that have a random behaviour(speed is
	initialized randomly at each reroute, as well as the beta
	parameter)
train: if set to True, reinforcement learning training will take
	   place.
load: if set to True, it will load the model specified in the
	  MV parameter. Be aware that you can both load and train
	  a model (in this case, you will train even more a pre-trained
	  model).
name: 3 possible values: random, booster or disabled. "random" is used
	  when you want to mount a random bidder on the test vehicle,
	  "booster" is set when you want to load the specified model,
	  "disabled" is set when you want the random vehicle to behave
	  in the "classic" way, so like other vehicles.

MV: stands for "model version". It loads the specified model
	from the "models" folder. The latest most updated version
	of the model is hopev4_2

AI: it is just a numeric value needed to differentiate between
	multiple simulation of the same kind. It is needed to determine
	the path in which the output file will be saved.
	([crossroad_vehicles.to_csv("./models/{}/compared_exp/average_{}T/{}/crossroad_{}.txt".format(configs['MV'], folder_name, str(configs['AI']), str(simulationName)),header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])])
	
B: starting budget of the test vehicle
Spn: beta parameter for the test vehicle when name is "disabled", so
	 when the trained / random bidder is not active and the vehicle
	 behaves normally. It is not needed when the bidder behaves
	 differently (it takes care of placing sponsorships by itself).
	 Actually, to obtain the "real" beta in the simulator this value
	 is divided by 100.
betaL: lower bound for beta when chosen randomly during initialization
	   (for other vehicles). Usually 0.05
betaR: lower bound for beta when chosen randomly during initialization
	   (for other vehicles). Usually 0.15

The following 2 parameters are used only when the trained bidder(booster)
is active.
EXE: Exploration Epsilon. It is the epsilon value used when...
EVE: Evaluation Epsilon. It is the epsilon value used when...


For the following hyperparamters, refer to the paper/thesis
for explanation. Be aware that theese are used only when
you want to train a model. You can leave them with random values
when training is not happening.


alpha: deep learning hyperparameter
TF: training frequency
UF: update frequency
BS: batch size
G: gamma

-------- APPENDIX----------
1) crossroad_vehicles.to_csv("./models/{}/compared_exp/average_{}T/{}/crossroad_{}.txt".format(configs['MV'], folder_name, str(configs['AI']), str(simulationName)),header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
2) https://www.mdpi.com/1424-8220/24/4/1288
3) https://theelandor.github.io/prova/Tesi_Stampa.pdf
