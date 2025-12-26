waterMin = 5
waterMax = 50
waterInFlow = True


def iRate(v):
	global waterInFlow

	rs = {water: 5.0, gly: 1.0, ala: 1.0, gla: 1.0, lac: 1.0}
	r = rs.get(v.graph, 0.0)
	if v.graph != water:
		return r, True

	waterCnt = sim.state(water)
	if waterInFlow:
		# waterinflow is on
		if waterCnt <= waterMax:
			return r, False
		else:
			waterInFlow = False
			print(f'Closing water inflow at {sim.time:3.3f}, water={waterCnt}')
			return 0.0, False
	else:
		# waterinflow is off
		if waterCnt <= waterMin:
			waterInFlow = True
			print(f'Opening water inflow at {sim.time:3.3f}, water={waterCnt}')
			return r, False
		else:
			return 0.0, False

def oRate(v):
	rs = {water: 0.1, gly: 0.1, ala: 0.1, gla: 0.1, lac: 0.1}
	r = rs.get(v.graph, 0.0)
	return r, True


sim = causality.Simulator(
	graphDatabase=inputGraphs,
	labelSettings=ls,
	expandNetwork=causality.Simulator.ExpandByStrategy(maxPolyLength(inputRules, 2)),
	initialState={ala: 100, gly: 100, gla: 100, lac: 100},
	draw=causality.Simulator.DrawMassAction(
		reactionRate=reactionRates, inputRate=iRate, outputRate=oRate)
)

trace = sim.simulate(time=tMax)
dumpTrace(trace, basename)
printFinalState(sim)
postProcessTrace(trace, basename)
