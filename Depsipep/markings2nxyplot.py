# usage: mod -e 'filebase="FOO"' -f markings2nxyplot.py
include("common.py")

trace = loadTraceAndDG(inputGraphs, inputRules, filebase)
dg = trace.dg

vs = sorted(dg.vertices)
names = [v.graph.name for v in vs]
filename = filebase + '-tc.agr'
with open(filename, 'w') as f:
	state = trace.initialState
	print('# ', *names, file=f)
	for e in trace:
		print(e.time, *[state[v] for v in vs], file=f)
		e.action.applyTo(state)
	print("&", file=f)

print(f'Wrote time course to file {filename}.')
print(f"Use 'xmgrace -nxy {filename}' to render the plot.")
