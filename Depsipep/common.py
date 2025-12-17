include("mols.py")
include("rules.py")

def printGrammar() -> None:
	post.summarySection("Molecule(s)")
	p = GraphPrinter()
	p.setMolDefault()
	#p.withIndex = True
	for m in inputGraphs:
		m.print(p)

	post.summarySection("Rule(s)")
	p = GraphPrinter()
	p.setReactionDefault()
	p.withIndex = True
	for r in inputRules:
		r.print(p)


ls = LabelSettings(LabelType.Term, LabelRelation.Specialisation)


def toFilename(base: str) -> str:
	return base


def numAmideEster(g: Graph) -> tuple[int, int]:
	# don't cache it, might be used in DG strat predicates
	cA = amide_pattern.monomorphism(g, maxNumMatches=2**32)
	cE = ester_pattern.monomorphism(g, maxNumMatches=2**32)
	return cA, cE


def countPatterns(d: Derivation) -> int:
	"""Count ester and amid connections."""
	c = 0
	for g in d.right:
		cA, cE = numAmideEster(g)
		c += cA + cE
	return c


def maxPolyLength(strat: DGStrat, maxNum: int=2) -> DGStrat:
	"""Restrict length of polymer."""
	return rightPredicate[
		lambda d: countPatterns(d) <= maxNum
	](strat)


def reactionRates(e: DG.HyperEdge):
	# ester formation
	if r1f in e.rules:
		return 0.03, True
	# ester hydrolysis
	elif r1b in e.rules:
		return 0.01, True
	# amid formation via ester substitution
	elif r2A in e.rules:
		return 0.3, True
	# amid formation direct
	elif r2B in e.rules:
		return 0.00001, True
	# amid hydrolysis
	elif r3f in e.rules:
		return amideHydrolysisRate, True
	# should not happen
	else:
		assert False


def printFinalState(sim) -> None:
	print('###### composition of mixture (final state) ######')
	for v in sim.dg.vertices:
		if sim._marking[v] > 0:
			print(f'{v.graph.name:10} {sim._marking[v]:3} {v.graph.smiles}')
	print('##################################################')


def printRea(e: DG.HyperEdge) -> None:
	"""Print reaction from edge."""
	educts   = " + ".join(sorted(v.graph.smiles for v in e.sources))
	products = " + ".join(sorted(v.graph.smiles for v in e.targets))
	rea = f'{educts} -> {products} ; {[r.id for r in e.rules]}'
	print(rea)


def evalEdge(cA, cE, e: DG.HyperEdge) -> tuple[int, int]:
	# ester formation
	if r1f in e.rules:
		cE += 1
	# ester hydrolysis
	elif r1b in e.rules:
		cE -= 1
	# amid formation via ester substitution
	elif r2A in e.rules:
		cA += 1
		cE -= 1
	# amid formation direct
	elif r2B in e.rules:
		cA += 1
	# amid hydrolysis
	elif r3f in e.rules:
		cA -= 1
	else:
		assert False
	return cA, cE


def getAmidEsterData(trace, maxPointsPerVertex):
	cA = 0
	cE = 0
	A = [(0, 0)]
	E = [(0, 0)]
	
	if len(trace) == 0:
		return A, E

	binSize = trace[-1].time / maxPointsPerVertex
	nextBinStart = binSize

	state = trace.initialState
	eLast = None
	for e in trace:
		if e.time >= nextBinStart:
			A.append((eLast.time, cA))
			E.append((eLast.time, cE))
			nextBinStart += binSize
		if isinstance(e.action, causality.EdgeAction):
			cA, cE = evalEdge(cA, cE, e.action.edge)

		e.action.applyTo(state)
		eLast = e
	A.append((trace[-1].time, cA))
	E.append((trace[-1].time, cE))
	return A, E


def mytrace2txyPlot(trace, filebase):
	"""Print txy-data."""
	filename = filebase + '.agr'
	cA = 0
	cE = 0
	with open(filename, 'w') as f:
		print('# t amide-bonds ester-bonds H2O', file=f)
		print('@xaxis label "Time [arbitrary units]"', file=f)
		print('@yaxis label "Counts"', file=f)
		print('@legend on', file=f)
		print('@s0 legend "amide bonds"', file=f)
		print('@s1 legend "ester bonds"', file=f)
		print('@s2 legend "water"', file=f)

		state = trace.initialState
		print(f'{state}')
		for e in trace:
			if isinstance(e.action, causality.EdgeAction):
				cA, cE = evalEdge(cA, cE, e.action.edge)

			print(f'{e.time} {cA} {cE} {state[water]}', file=f)
			e.action.applyTo(state)
		print("&", file=f)


def dumpTrace(trace: causality.EventTrace, basename: str):
	fDG = trace.dg.dump(basename + ".dg")
	fTrace = trace.dump(basename + ".eventTrace")
	print(f'Dumped DG to file         {fDG}')
	print(f'Dumped EventTrace to file {fTrace}')


def loadTrace(dg, basename: str):
	trace = causality.EventTrace.load(dg, f"{basename}.eventTrace")
	return trace


def loadTraceAndDG(graphDatabase, ruleDatabase, basename: str):
	dg = DG.load(graphDatabase, ruleDatabase, f"{basename}.dg")
	return loadTrace(dg, basename)


def postProcessTrace(trace: causality.EventTrace, basename):
	mytrace2txyPlot(trace, basename)
	if 'printFullTrace' not in globals() or printFullTrace:
		trace.print()

	p = causality.EventTracePrinter()
	p.pushVertexVisible(lambda v: v.graph == water)
	A, E = getAmidEsterData(trace, p.maxPointsPerVertex)
	prefix = makeUniqueFilePrefix()
	with open(f"{prefix}A.txt", "w") as f:
		f.write(f"time	count\n")
		for time, count in A:
			f.write(f"{time}	{count}\n")
	with open(f"{prefix}E.txt", "w") as f:
		f.write(f"time	count\n")
		for time, count in E:
			f.write(f"{time}	{count}\n")
	s = "\\addplot+[mark=none, color=blue] table {" + prefix + "A.txt};\n"
	s += "\\addlegendentry{Amid}\n"
	s += "\\addplot+[mark=none, color=red] table {" + prefix + "E.txt};\n"
	s += "\\addlegendentry{Ester}\n"
	p.setPostContent(s)
	p.pushVertexOptions(lambda v: "color=ForestGreen")
	trace.print(p)
