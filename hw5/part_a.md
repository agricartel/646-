# Part a
## Question 1
Homework 1: 44 stuck-at faults
TetraMax: 62 stuck-at faults

Before collapsing:
```
sa1   NC   NAND_2/Y
sa0   --   NAND_2/A
sa0   --   NAND_2/B
sa0   --   b
sa0   --   c
sa0   NC   NAND_2/Y
sa1   NC   c
sa1   --   NAND_2/B
sa1   NC   b
sa1   --   NAND_2/A
sa0   NC   f
sa0   --   XOR_1/B
sa0   NC   XOR_1/A
sa1   NC   o3
sa1   --   XOR_1/Y
sa0   NC   o3
sa0   --   XOR_1/Y
sa1   NC   f
sa1   --   XOR_1/B
sa1   NC   o1
sa1   --   NAND_3/Y
sa0   --   NAND_3/B
sa0   --   NAND_3/A
sa0   --   INV_2/Y
sa1   --   INV_2/A
sa0   --   NAND_1/Y
sa1   NC   INV_2/Y
sa0   --   INV_2/A
sa1   --   NAND_3/B
sa0   NC   o1
sa0   --   NAND_3/Y
sa0   NC   XNOR_2/A
sa1   NC   XNOR_2/A
sa0   NC   NAND_4/Y
sa0   NC   o2
sa1   NC   o2
sa1   UR   NAND_1/Y
sa0   --   NAND_1/A
sa0   --   NAND_1/B
sa0   --   a
sa1   --   NAND_3/A
sa1   AN   NAND_1/B
sa1   UR   a
sa1   --   NAND_1/A
sa0   UU   d
sa1   UU   d
sa0   UU   e
sa1   UU   e
sa1   AN   XOR_1/A
sa1   AN   NAND_4/Y
sa0   --   NAND_4/A
sa0   --   NAND_4/B
sa0   --   INV_1/Y
sa1   --   INV_1/A
sa1   AN   NAND_4/B
sa1   AN   INV_1/Y
sa0   --   INV_1/A
sa1   --   NAND_4/A
sa0   AN   XNOR_2/Y
sa1   AN   XNOR_2/B
sa0   AN   XNOR_2/B
sa1   AN   XNOR_2/Y
```

After collapsing:
```
sa1   NC   NAND_2/Y
sa0   NC   NAND_2/Y
sa1   NC   c
sa1   NC   b
sa0   NC   f
sa0   NC   XOR_1/A
sa1   NC   o3
sa0   NC   o3
sa1   NC   f
sa1   NC   o1
sa1   NC   INV_2/Y
sa0   NC   o1
sa0   NC   XNOR_2/A
sa1   NC   XNOR_2/A
sa0   NC   NAND_4/Y
sa0   NC   o2
sa1   NC   o2
sa1   UR   NAND_1/Y
sa1   AN   NAND_1/B
sa1   UR   a
sa0   UU   d
sa1   UU   d
sa0   UU   e
sa1   UU   e
sa1   AN   XOR_1/A
sa1   AN   NAND_4/Y
sa1   AN   NAND_4/B
sa1   AN   INV_1/Y
sa0   AN   XNOR_2/Y
sa1   AN   XNOR_2/B
sa0   AN   XNOR_2/B
sa1   AN   XNOR_2/Y
```


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