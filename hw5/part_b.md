# Part b
## Question 1
Minimal test set:
```
{001, 011, 110, 111}
```

Untestable faults:
```
{B1sa1, B2sa1, B4sa1, C2sa1, fsa0, hsa0, ksa1}
```

Faults covered by each test vector:
```
001: [ Bsa1 B3sa1 B5sa1 gsa1 hsa1 Ysa1 Zsa0 ]
011: [ Asa1 dsa0 ]
110: [ Csa1 B3sa0 C1sa1 esa0 ]
111: [ Asa0 Bsa0 Csa0 B1sa0 B2sa0 B4sa0 B5sa0 C1sa0 C2sa0 dsa1 esa1 fsa1 gsa0 ksa0 Ysa0 Zsa1 ]
```

Test vectors that activate each fault:
```
Asa0: [ 111 ]
Asa1: [ 011 ]
Bsa0: [ 010 011 110 111 ]
Bsa1: [ 000 001 100 101 ]
Csa0: [ 111 ]
Csa1: [ 110 ]
B1sa0: [ 111 ]
B1sa1: [ ]
B2sa0: [ 111 ]
B2sa1: [ ]
B3sa0: [ 010 011 110 ]
B3sa1: [ 000 001 100 101 ]
B4sa0: [ 111 ]
B4sa1: [ ]
B5sa0: [ 010 011 110 111 ]
B5sa1: [ 000 001 100 101 ]
C1sa0: [ 111 ]
C1sa1: [ 110 ]
C2sa0: [ 111 ]
C2sa1: [ ]
dsa0: [ 011 ]
dsa1: [ 111 ]
esa0: [ 110 ]
esa1: [ 111 ]
fsa0: [ ]
fsa1: [ 111 ]
gsa0: [ 111 ]
gsa1: [ 000 001 010 011 100 101 110 ]
hsa0: [ ]
hsa1: [ 001 010 101 110 ]
ksa0: [ 000 001 010 011 100 101 110 111 ]
ksa1: [ ]
Ysa0: [ 111 ]
Ysa1: [ 000 001 010 011 100 101 110 ]
Zsa0: [ 000 001 100 101 ]
Zsa1: [ 010 011 110 111 ]
```

## Question 2
Faults detected: 46

Faults detected in Question 1: 36

The output files are provided in the submission zip under part_b/q2


As in part a, the discrepancy is from TetraMax counting faults by gate nets instead of the nets connecting each gate.
For example: `d stuck at 0` is counted as `NAND_1(Y) stuck at 0` and `NOR_1(A) stuck at 0`.
That makes it really annoying to read the fault lists...

Fault classes seen in results:
DS: Detected by Simulation
- Fault simulation detected this fault.
UR: Undetectable Redundant
- Redundant logic path.
UT: Undetectable Tied
- Net is tied to a logic `0` or `1`.
  - In this circuit, net `k` is always `1` no matter what test vector is used.

## Question 3
### Test Generation
Total number of faults: `14568`
Number of test patterns generated: `60`
Fault classes: `14483` detected, `85` undetectable
Test coverage: `100%`

### Fault Simulation
Total Number of faults: `7000`
Fault classes: `6730` detectable, `68` undetectable, `202` not detected
Fault coverage: `6730 / 7000 = 96.14%`
Test coverage: `97.09%`

## Question 4
Total Number of faults: `14568`
Fault classes: `14130` detectable, `68` undetectable, `370` not detected
Fault coverage: `14130 / 14568 = 96.99%`
Test coverage: `97.45%`