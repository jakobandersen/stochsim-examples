include("dg.py")

## Flow query
flow = hyperflow.Model(dg)

# add inflow reactions
for v in dg.vertices:
	if v.graph in (A,):
		flow.addSource(v)

# add outflow reactions
for v in dg.vertices:
	if v.graph in (P,):
		flow.addSink(v)

flow.addConstraint(inFlow[A] == 1)
flow.addConstraint(outFlow[P] == 1)
flow.allowIOReversal = False

flow.findSolutions(maxNumSolutions=2**30)
p = hyperflow.Printer()
p.dgPrinter.graphvizPrefix = 'layout = "dot";'

printGrammar()  # from grammar.py
post.summarySection("Reaction Network")
dg.print(p.dgPrinter)
flow.solutions.print(p)
