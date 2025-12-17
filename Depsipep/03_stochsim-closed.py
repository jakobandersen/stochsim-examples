include("common.py")

basename = toFilename('closed')

amideHydrolysisRate = 0.1  # used in the reactionRate function

sim = causality.Simulator(
	graphDatabase=inputGraphs,
	labelSettings=ls,
	expandNetwork=causality.Simulator.ExpandByStrategy(maxPolyLength(inputRules, 2)),
	initialState={ala: 10, gly: 10, gla: 10, lac: 10},
	draw=causality.Simulator.DrawMassAction(reactionRate=reactionRates)
)

trace = sim.simulate(time=1e3)
dumpTrace(trace, basename)
printFinalState(sim)
postProcessTrace(trace, basename)
