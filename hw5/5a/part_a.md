# Part a
## Question 1
Homework 1: 44 stuck-at faults
TetraMax: 62 stuck-at faults



The discrepancy is from TetraMax counting faults by gate nets instead of the nets connecting each gate.
For example: `m stuck at 0` is counted as `XNOR_1(Y) stuck at 0` and `XNOR_2(B) stuck at 0`.


## Question 2
`c1908`:
- before collapsing: `5580`
- after collapsing: `2056`
- collapse ratio: `36.85%`

`c2670`:
- before collapsing: `8416`
- after collapsing: `2954`
- collapse ratio: `35.10%`