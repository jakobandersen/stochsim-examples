include("grammar.py")

def reactionRate(e):
	if r1 in e.rules:
		return 0.0000000332, True
	elif r2 in e.rules:
		return 0.0000000265, True
	elif r3 in e.rules or r4 in e.rules:
		return 0.000000005, True
	else:
		assert False

def inputRate(v):
	if v.graph == A:
		return 0.000004, True
	else:
		return 0, True

def outputRate(v):
	if v.graph == P:
		return 0.00000001, True
	else:
		return 0, True

sim = causality.Simulator(
	graphDatabase=inputGraphs,
	expandNetwork=causality.Simulator.ExpandByStrategy(inputRules),
	initialState={A: 0},  # A must be mentioned in order for the inputRate to have effect
	draw=causality.Simulator.DrawMassAction(
		reactionRate=reactionRate,
		inputRate=inputRate,
		outputRate=outputRate
	)
)

def setCallbacks(sim):
	def onIterationBegin(sim):
		if sim.iteration % 10000 == 0:
			print(f"Iteration: {sim.iteration:7}, t={sim.time:12.0f}")
	def onExpand(sim):
		print("Expand:", sim.iteration)
	def onExpandAvoided(sim):
		print("ExpandAvoided:", sim.iteration)
	def onDeadlock(sim):
		print(f"Deadlock: {sim.iteration}, t={sim.time}")
	def onIterationEnd(sim):
		print(f"Iteration end: {sim.iteration}, t={sim.time}, event={sim.trace[-1]}")
		return True

	sim.onIterationBegin = onIterationBegin
	#sim.onExpand = onExpand
	#sim.onExpandAvoided = onExpandAvoided
	sim.onDeadlock = onDeadlock
	#sim.onIterationEnd = onIterationEnd

setCallbacks(sim)

trace = sim.simulate(time=10e9)

styles = {
	A: "Cerulean,solid,thick",
	B: "Orange,solid",
	C: "Green,solid",
	D: "Orchid,solid",
	E: "olive,solid",
	F: "BlueGreen,solid",
	G: "Tan,solid",
	H: "Rhodamine,solid",
	I: "TealBlue,solid", 
	J: "LimeGreen,solid",
	K: "CornflowerBlue,solid",
	L: "Periwinkle,solid",
	M: "CornflowerBlue,solid",
	N: "Thistle,solid",
	O: "OrangeRed,solid",
	P: "LimeGreen,solid,thick",
}
p = causality.EventTracePrinter()
p.pushVertexOptions(lambda v: styles[v.graph])
trace.print(p)
