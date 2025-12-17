# add term constraint to rule defined via DFS
def addConstraints(rule, conString):
    gmlstr = rule.getGMLString()
    return Rule.fromGMLString(gmlstr[:-1] + conString + gmlstr[-1])

r1f = Rule.fromDFS("[*]1[C]2(=[O]3)[O]4[H]5.[H]11[O]10[C]6([*]7)([*]8)[*]9"
                  +">>"
                  "[*]1[C]2(=[O]3)[O]10[C]6([*]7)([*]8)[*]9.[H]11[O]4[H]5",
                  name="r1f: estrification")
r1b = Rule.fromDFS("[*]1[C]2(=[O]3)[O]4[H]5.[H]11[O]10[C]6([*]7)([*]8)[*]9"
                  +">>"
                  "[*]1[C]2(=[O]3)[O]10[C]6([*]7)([*]8)[*]9.[H]11[O]4[H]5",
                  invert=True, name="r1b: sopification")
#===
r2A = Rule.fromDFS("[*]0[C]1(=[O]2)[O]3[_X]4.[H]5[N]6([H]7)[*]8"
                  +">>"
                  "[*]0[C]1(=[O]2)[N]6([H]7)[*]8.[H]5[O]3[_X]4", add=False)
r2Aconst = """
constrainLabelAny [
   label "_X"
   labels [ label "C" ]
]"""
r2A = addConstraints(r2A, r2Aconst)
r2A.name = "r2A: amide via substitution"
#===
r2B = Rule.fromDFS("[*]0[C]1(=[O]2)[O]3[_X]4.[H]5[N]6([H]7)[*]8"
                  +">>"
                  "[*]0[C]1(=[O]2)[N]6([H]7)[*]8.[H]5[O]3[_X]4", add=False)
r2Bconst = """
constrainLabelAny [
   label "_X"
   labels [ label "H" ]
]"""
r2B = addConstraints(r2B, r2Bconst)
r2B.name = "r2B: amide direct"
#===
r3f = Rule.fromDFS("[*]0[C]1(=[O]2)[N]3([H]4)[*]5.[H]6[O]7[H]8"
                  +">>"
                  "[*]0[C]1(=[O]2)[O]7[H]8.[H]6[N]3([H]4)[*]5", "r3f: amide hydrolysis")
