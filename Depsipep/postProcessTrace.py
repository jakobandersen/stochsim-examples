include("common.py")

trace = loadTraceAndDG(inputGraphs, inputRules, basename)
postProcessTrace(trace, basename)
