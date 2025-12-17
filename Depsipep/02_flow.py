include("dg.py")

flow = hyperflow.Model(dg)

for v in sourceGraphs:
	flow.addSource(v)
for v in dg.vertices:
	flow.addSink(v)

flow.addConstraint(outFlow[flowTarget] == 1)

flow.allowIOReversal = False
flow.findSolutions(maxNumSolutions=3)
flow.solutions.print()
