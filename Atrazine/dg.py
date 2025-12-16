include("grammar.py")

## Construct derivation graph
dg = DG(graphDatabase=inputGraphs)
with dg.build() as b:
	b.execute(
		addSubset(inputGraphs)
		>> repeat[10](inputRules)
	)

#p = DGPrinter()
#p.graphvizPrefix = 'layout = "dot";'
#dg.print(p)
