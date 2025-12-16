# atrazine degradation model
#
# A -> B : k2   # B -> E : k3   # C -> E : k2
# A -> C : k3   # B -> F : k1   # C -> G : k1
# A -> D : k1   # B -> H : k1   # C -> I : k1
#
# D -> F : k2   # E -> J : k1   # F -> J : k3
# D -> G : k3   # E -> K : k1   # F -> L : k1
#
# G -> J : k2   # H -> K : k3   # I -> K : k2
# G -> M : k1   # H -> L : k1   # I -> M : k1
#
# J -> O : k1   # K -> N : k1   # L -> O : k3
#               # K -> O : k1
#		
# M -> O : k2   # N -> P : k1   # O -> P : k1
#

# loading some usefull julia addon packages
using DifferentialEquations
using Catalyst
using Plots

# define reaction network
rn = @reaction_network Atrazine begin
     @parameters k1 k2 k3
     (k2, k3, k1), A --> (B, C, D)
     (k3, k1, k1), B --> (E, F, H)
     (k2, k1, k1), C --> (E, G, I)
         (k2, k3), D --> (F, G)
         (k1, k1), E --> (J, K)
         (k3, k1), F --> (J, L)
         (k2, k1), G --> (J, M)
         (k2, k1), H --> (K, L)
         (k2, k1), I --> (K, M)
               k1, J --> O
         (k1, k1), K --> (N, O)
               k3, L --> O
	       k2, M --> O
	       k1, N --> P
	       k1, O --> P
end

# initial value array [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P]
u0 = [1000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]

# parameter array [s, r, b]
p = [0.0005, 0.00332, 0.00265]

# simulation time (start, stop)
tspan = (0.1, 1000000.0)

# setup ODE problem
odes = ODEProblem(rn, u0, tspan, p)

# solve ODES problem
sol = solve(odes)

# plot time course
plot(sol, xscale = :log10)
