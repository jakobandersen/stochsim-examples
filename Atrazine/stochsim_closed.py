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

sim = causality.Simulator(
	graphDatabase=inputGraphs,
	expandNetwork=causality.Simulator.ExpandByStrategy(inputRules),
	initialState={A: 1000},
	draw=causality.Simulator.DrawMassAction(reactionRate=reactionRate)
)

trace = sim.simulate()

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
p.pushOptions("legend columns=5")
p.pushOptions("legend style={at={(0.95, 0.5)}, anchor=east, draw=none}")
trace.print(p)
p.logTime = True
p.popOptions()
p.pushOptions("legend style={at={(0.5, 0.95)}, anchor=north, draw=none}")
trace.print(p)
