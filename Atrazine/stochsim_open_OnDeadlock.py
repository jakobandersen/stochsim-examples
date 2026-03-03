include("grammar.py")

openInOutFlow = False

def reactionRate(e):
	if r1 in e.rules:
		return 0.0000000332, True
	elif r2 in e.rules:
		return 0.0000000265, True
	elif r3 in e.rules or r4 in e.rules:
		return 0.000000005, True
	else:
		assert False

iRateA = 0.0
def inputRate(v):
	if v.graph != A:
		return 0.0, True
	# 0.000004, True
	return iRateA, False

oRateP = 0.0
def outputRate(v):
	if v.graph != P:
		return 0.0, True
	# 0.00000001, True
	return oRateP, False

sim = causality.Simulator(
	graphDatabase=inputGraphs,
	expandNetwork=causality.Simulator.ExpandByStrategy(inputRules),
	initialState={A: 1000},
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
		print(f"Deadlock at iteration {sim.iteration}, t={sim.time:.0f}")
		print(f'Opening system')
		global openInOutFlow
		openInOutFlow = True
	def onIterationEnd(sim):
		return True

	sim.onIterationBegin = onIterationBegin
	#sim.onExpand = onExpand
	#sim.onExpandAvoided = onExpandAvoided
	sim.onDeadlock = onDeadlock
	sim.onIterationEnd = onIterationEnd

setCallbacks(sim)

trace = sim.simulate(keepNetworkOpen=True)
iRateA = 0.000004
oRateP = 0.00000001
deadlockTime = sim.time
trace = sim.simulate(time=4*10e8)

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
p.pushOptions("legend style={at={(0.95, 0.8)}, anchor=east, draw=none}")
p.setPostContent(
	R"\node (source)      at (axis cs:" + str(deadlockTime) + ",1100) {};\n" +
	R"\node (destination) at (axis cs:" + str(deadlockTime) + ",990) {};\n" +
	R"\draw[-latex',very thick,red](source)--(destination);" + "\n" +
	R"\node (closed)   at (axis cs:0,1065) {};" + "\n" +
	R"\node (deadlock) at (axis cs:" + str(deadlockTime) + ",1065) {};\n" +
	R"\node (open)     at (axis cs:" + str(trace.time) + ",1065) {};\n" +
	R"\draw[latex'-latex'] (closed) -- node[below] {closed system} (deadlock);" + "\n" +
	R"\draw[latex'-latex'] (deadlock) -- node[below] {open system} (open);" + "\n"
)
trace.print(p)
