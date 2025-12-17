include("common.py")

def printDG(hidelist):
	gp = DGPrinter()
	gp.pushVertexVisible(lambda v: v.graph not in hidelist)
	dg.print(gp)

iters = 3
dg = DG(graphDatabase=inputGraphs, labelSettings=ls)
with dg.build() as b:
	b.execute(
		addSubset(sourceGraphs)
		>> maxPolyLength(repeat[iters](inputRules), 2)
	)
