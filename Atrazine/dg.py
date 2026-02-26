include("grammar.py")

## Construct derivation graph
dg = DG(graphDatabase=inputGraphs)
with dg.build() as b:
	b.execute(
		addSubset(inputGraphs)
		>> repeat[10](inputRules)
	)

if False:
	p = DGPrinter()
	p.graphvizPrefix = 'layout = "dot";'
	p.withGraphName = False
	p.pushVertexColour(lambda v: ", label=left:\LARGE\\texttt{" + v.graph.name + "}")
	dg.print(p)
