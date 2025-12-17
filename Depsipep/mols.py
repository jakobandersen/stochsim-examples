# amino acids
gly = Graph.fromSMILES("NCC(=O)O", "Gly")
ala = Graph.fromSMILES("NC(C)C(=O)O", "Ala")
leu = Graph.fromSMILES("CC(C)CC(N)C(=O)O", "Leu")

# alpha hydroxy acids
gla = Graph.fromSMILES("OCC(=O)O", "Gla")
lac = Graph.fromSMILES("OC(C)C(=O)O", "Lac")
mal = Graph.fromSMILES("OC(=O)CC(O)C(=O)O", "Mal")

# helper mols
water = Graph.fromSMILES("O", "H2O")

# flow target
flowTarget = Graph.fromSMILES("C(C(C)N)(NC(C(OCC(O)=O)=O)C)=O", "Flow target")

# patterns
amide_pattern = Graph.fromSMILES("[C]C(=O)[NH][C]", "ester-pattern")
ester_pattern = Graph.fromSMILES("[C]C(=O)[O][C]", "amide-pattern")

sourceGraphs = [gly, ala, gla, lac, water]
