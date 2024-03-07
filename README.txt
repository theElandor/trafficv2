modelv4_2 current most updated version
Example command to generate config files:
python3 generate_configs.py --MV=hopev4_2 --VS=120 --Stp=5000 --B=100 --CT=random --RS=10 --RS=15 --RS=20 --RS=25 --RS=30 --RS=35

This command generates configuration files for both random bidder and booster,
varying the random pool percentage, with fixed number of vehicles.
By default the script generates 10 experiments for each one of the possible settings: "AI" stands
for the index of the experiment.
crossroad_vehicles.to_csv("./models/{}/compared_exp/average_{}T/{}/crossroad_{}.txt".format(configs['MV'], folder_name, str(configs['AI']), str(simulationName)),header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])

Main configurations
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
	of the simulation will be written.
	crossroad_vehicles.to_csv("./models/{}/compared_exp/average_{}T/{}/crossroad_{}.txt".format(configs['MV'], folder_name, str(configs['AI']), str(simulationName)),header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])	
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
	crossroad_vehicles.to_csv("./models/{}/compared_exp/average_{}T/{}/crossroad_{}.txt".format(configs['MV'], folder_name, str(configs['AI']), str(simulationName)),header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
	
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
