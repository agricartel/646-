#! /usr/bin/env python3
# masks:
# sa0: ~(1 << idx * 2)
# sa1: 1 << idx * 2 + 1
masks = [(~(1 << idx * 2 + 1), (1 << idx * 2 + 2)) for idx in range(18)]

fault_names = ['Asa0', 'Asa1', 'Bsa0', 'Bsa1', 'Csa0', 'Csa1', 'B1sa0', 'B1sa1', 'B2sa0', 'B2sa1', 'B3sa0', 'B3sa1', 'B4sa0', 'B4sa1', 'B5sa0', 'B5sa1', 'C1sa0',
               'C1sa1', 'C2sa0', 'C2sa1', 'dsa0', 'dsa1', 'esa0', 'esa1', 'fsa0', 'fsa1', 'gsa0', 'gsa1', 'hsa0', 'hsa1', 'ksa0', 'ksa1', 'Ysa0', 'Ysa1', 'Zsa0', 'Zsa1']

fault_tests = [[] for _ in range(36)]

# Values:
# This is the circuit written out in bitwise operations.
# A = (i >> 2 & 1)
# B = (i >> 1 & 1)
# C = (i & 1)
# B1 = B
# B2 = B
# B3 = B
# B4 = B
# B5 = B
# C1 = C
# C2 = C
# d = ~(A & B1)
# e = ~(B2 & C1)
# f = (C2 ^ B4)
# g = ~(d | e)
# h = g
# k = ~(h & f)
# Y = g
# Z = (k ^ B5)


for i in range(8):
    a_val = (i >> 2 & 1)
    b_val = (i >> 1 & 1)
    c_val = (i & 1)
    A = 0
    B = 0
    C = 0
    for j in range(37):
        A += a_val << j
        B += b_val << j
        C += c_val << j
    A = (A & masks[0][0]) | masks[0][1]
    B = (B & masks[1][0]) | masks[1][1]
    C = (C & masks[2][0]) | masks[2][1]
    B1 = (B & masks[3][0]) | masks[3][1]
    B2 = (B & masks[4][0]) | masks[4][1]
    B3 = (B & masks[5][0]) | masks[5][1]
    B4 = (B3 & masks[6][0]) | masks[6][1]
    B5 = (B3 & masks[7][0]) | masks[7][1]
    C1 = (C & masks[8][0]) | masks[8][1]
    C2 = (C & masks[9][0]) | masks[9][1]
    d = ((~(A & B1) & 0x1fffffffff) & masks[10][0]) | masks[10][1]
    e = ((~(B2 & C1) & 0x1fffffffff) & masks[11][0]) | masks[11][1]
    f = ((C2 ^ B4) & masks[12][0]) | masks[12][1]
    g = ((~(d | e) & 0x1fffffffff) & masks[13][0]) | masks[13][1]
    h = (g & masks[14][0]) | masks[14][1]
    k = ((~(h & f) & 0x1fffffffff) & masks[15][0]) | masks[15][1]
    Y = (g & masks[16][0]) | masks[16][1]
    Z = ((k ^ B5) & masks[17][0]) | masks[17][1]

    print(f'{i:03b}: [ ', end='')

    faults = [((Y ^ (Y >> idx)) & 1) | ((Z ^ (Z >> idx)) & 1) for idx in range(1, 37)]
    for idx, fault in enumerate(faults):
        if fault == 1:
            fault_tests[idx].append(i)
            print(f'{fault_names[idx]} ', end='')
    print(']')

for idx, fault_test in enumerate(fault_tests):
    print(f'{fault_names[idx]}: [ ', end='')
    for i in fault_test:
        print(f'{i:03b} ', end='')
    print(']')
