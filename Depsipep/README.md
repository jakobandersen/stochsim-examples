# Wet-Dry-Cycling Example

| reaction name                      | rate constant |
|------------------------------------|---------------|
| r1f (ester formation)              | 0.03          |
| r1b (ester hydrolysis)             | 0.01          |
| r2A (amide formation substitution) | 0.3           |
| r2B (amide formation direct)       | 0.00001       |


## Closed System
### Parameters

| molecule                         | count |
|----------------------------------|-------|
| ala (initial count amino acid)   | 10    |
| gly (initial count amino acid)   | 10    |
| gla (initial count hydroxy acid) | 10    |
| lac (initial count hydroxy acid) | 10    |
| water (initial count)            |  0    |

Inflows and outflows of all compounds are zero.

| reaction name                      | rate constant |
|------------------------------------|---------------|
| r3f (amide hydrolysis)             | 0.1           |

```
$ mod -f 03_stochsim-closed.py 
```

### Generated files

1. `closed.dg` sampled space as derivation graph that can be loaded.
2. `closed.eventTrace` trace of the simulation.
3. `closed.agr` nxy data of ester bonds, amide bonds, and water vs time.

### Plot time-course of all species

The file `summary/summary.pdf` contains a plot of both the full trace of the simulation
but also an aggregated time course of the number of ester bonds, amide bonds, and water.


## Open System
### Parameters

| initial counts                   | value        |
|----------------------------------|--------------|
| ala (initial count amino acid)   | 100          |
| gly (initial count amino acid)   | 100          |
| gla (initial count hydroxy acid) | 100          |
| lac (initial count hydroxy acid) | 100          |
| water (initial count)            |   0          |

| inflows                          | value        |
|----------------------------------|--------------|
| water                            | 5.0          |
| ala                              | 1.0          |
| gly                              | 1.0          |
| gla                              | 1.0          |
| lac                              | 1.0          |

| outflows                         | value        |
|----------------------------------|--------------|
| water                            | 0.1          |
| ala                              | 0.1          |
| gly                              | 0.1          |
| gla                              | 0.1          |
| lac                              | 0.1          |

inflow of water is turend off if water count exeeds 50, and turned back on
again if water count falls below 10. This mimics the wet-dry cycling thast
drives the amid-bond formation in the system.

| reaction name                      | rate constant |
|------------------------------------|---------------|
| r3f (amide hydrolysis)             | 0.01  (a)     |
| r3f (amide hydrolysis)             | 0.1   (b)     |
| r3f (amide hydrolysis)             | 0.015 (c)     |

```
$ mod -f 04a_stochsim-open.py 
$ mod -f 04b_stochsim-open.py 
$ mod -f 04c_stochsim-open.py 
```

## Literature

1. Forsythe, JG et al "Ester-Mediated Amide Bond Formation Driven by
   Wet–Dry Cycles: A Possible Path to Polypeptides on the Prebiotic Earth",
   Angew Chem Int Ed 2015, 54:9871-9875
   [doi:10.1002/anie.201503792](http://dx.doi.org/10.1002/anie.201503792)

2. Forsythe, JG et al "Surveying the sequence diversity of model prebiotic
   peptides by mass spectrometry", PNAS 2017, 114(37):E7652-E7659
   [doi:10.1073/pnas.1711631114](https://doi.org/10.1073/pnas.17116311)
