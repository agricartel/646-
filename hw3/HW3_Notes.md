# HW3 Notes

Need a graph

each node contains: Net name, tuple(input_gate, output_gate), enum(input, output, internal)

or we could go by each node is a gate?

gate list: each node contains: Gate type, net_list(<net, input/output>)

net list: containing each net and the faults it has


data structures:
GateType: (AND2X1, OR2X1, NAND2X1, NOR2X1, XOR2X1, INVX1, BUFX1)
gate_list: <sGate, eGateType, astInputNets, astOutputNets>
net_list: <sNet, eNetType, asFaults>

parse file(param filename):
open file
read input list
read output list
read wire list
- during those reads, initialize the faults at the same time
read gates until line matches endmodule

collapse faults:
list of primary inputs: curr_level
while curr_level is not all primary outputs,
- list of gates with inputs in curr_level: curr_gates
- for curr_gates,
  - remove equivalent faults(gate)
- set curr_level to outputs in curr_gates

remove equivalent faults(param gate):
switch on gate type,
- lookup table for faults to remove
- retrieve respective nets from entry in gate_list
- remove those faults in net_list

N1
N2
N4
N5

fanout can have a variable number of outputs, how to approach that?
make gate_list.nets be variable length

yeah this is getting done in python, no point in reinventing the wheel in c

Definition of the fanout modules is not in the library file


so no fanout definition, we need to see if a net is an input to multiple gates

what does that mean for fault collapsing?

it means that the same wire on 2 gates are separate nets

meaning it gets harder to count the number of faults...

we can count the number of times a net shows up on gate inputs



equivalent fault list: (array of collapsed, fault that stayed)



so 

AND2X1  i0,y0     if output is (1,x) then set input faults to (0,x)
OR2X1   i1,y1     if output is (x,1) then set input faults to (x,0)
NAND2X1 i0,y1     if output is (x,1) then set input faults to (0,x)
NOR2X1  i1,y0     if output is (1,x) then set input faults to (x,0)
XOR2X1  None      do nothing
INVX1   i0,y1     if output is (x,1) then set input faults to (0,x)
        i1,y0     if output is (1,x) then set input faults to (x,0)
BUFX1   i0,y0     if output is (1,x) then set input faults to (0,x)
        i1,y1     if output is (x,1) then set input faults to (x,0)


where are equivalencies in this list?
Lump in INV with NAND and NOR
Lump in BUF with AND and OR


just make a big switch statement



(modname)_BF.txt
"sa1     `netname`"
"sa0     `netname`"

Total Faults_BF=`num_of_faults`


(modname)_AF.txt
"sa1     `netname`"
"sa0     `netname`"

Total Faults_AF=`num_of_faults`
Collapse_ratio=`collapse_ratio`

Equivalent Classes:
`list of equivalent faults`
