simulations are run using v2 of depart_cars loop:
for crossing in crossings:
	for i in range(...)

this way if 2 cars in the ranking have non intercepting trajectories, they use the crossing
at the same time, reducing overall delay.
