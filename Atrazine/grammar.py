## define grammar of atrazine degradation space

# molecule(s)
## atrazine (educt)
A = Graph.fromSMILES("CCNc1nc(Cl)nc(NC(C)C)n1", "A")
B = Graph.fromSMILES("Nc1nc(Cl)nc(NC(C)C)n1", "B")
C = Graph.fromSMILES("CCNc1nc(Cl)nc(N)n1", "C")
D = Graph.fromSMILES("CCNc1nc(O)nc(NC(C)C)n1", "D")
E = Graph.fromSMILES("Nc1nc(Cl)nc(N)n1", "E")
F = Graph.fromSMILES("Nc1nc(O)nc(NC(C)C)n1", "F")
G = Graph.fromSMILES("CCNc1nc(O)nc(N)n1", "G")
H = Graph.fromSMILES("Oc1nc(Cl)nc(NC(C)C)n1", "H")
I = Graph.fromSMILES("CCNc1nc(Cl)nc(O)n1", "I")
J = Graph.fromSMILES("Nc1nc(O)nc(N)n1", "J")
K = Graph.fromSMILES("Oc1nc(Cl)nc(N)n1", "K")
L = Graph.fromSMILES("Oc1nc(O)nc(NC(C)C)n1", "L")
M = Graph.fromSMILES("CCNc1nc(O)nc(O)n1", "M")
N = Graph.fromSMILES("Oc1nc(Cl)nc(O)n1", "N")
O = Graph.fromSMILES("Nc1nc(O)nc(O)n1", "O")
## cyanuric acid (product)
P = Graph.fromSMILES("Oc1nc(O)nc(O)n1", "P")


# reaction(s)
## reductive de-ethylation
r1 = Rule.fromDFS("[H][C]1([H])([H])[C]2([H])([H])[N]3([H]4)>>[H]4[N]3[H]", name="CCNH -> NH2")
## reductive de-isopropylation
r2 = Rule.fromDFS("[H][C]1([H])([H])[C]2([C]3([H])([H])[H])([H])[N]4([H]5)>>[H]5[N]4[H]", name="CC(C)NH -> NH2")
## halogen hydrolysis
r3 = Rule.fromDFS("[Cl]1[C]2>>[C]2[O]3[H]", name="Cl-c -> HO-c")
## primary amine hydrolysis
r4 =  Rule.fromDFS("[H][N]1([H])[C]2>>[C]2[O]3[H]", name="c-NH2 -> C-OH")


def printGrammar():
	post.summarySection("Molecule(s)")
	p = GraphPrinter()
	p.setMolDefault()
	p.withIndex = True
	for m in inputGraphs:
		m.print(p)

	post.summarySection("Rule(s)")
	p = GraphPrinter()
	p.setReactionDefault()
	p.withIndex = True
	for r in inputRules:
		r.print(p)

#printGrammar()
