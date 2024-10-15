#!/usr/bin/env python3

import sys

from collections import namedtuple
from enum import Enum


class GateType(Enum):
    AND2X1 = 1
    OR2X1 = 2
    NAND2X1 = 3
    NOR2X1 = 4
    XOR2X1 = 5
    INVX1 = 6
    BUFX1 = 7


Gate = namedtuple('Gate', ['name', 'type', 'level', 'inputs', 'output'])
# Fault is a tuple of (stuck-at-zero, stuck-at-one)
# where 0 means fault was collapsed, 1 means fault still present
Net = namedtuple('Net', ['name', 'fault'])
EquivalentFault = namedtuple('EquivalentFault', ['collapsed', 'uncollapsed'])


class Collapser:
    def __init__(self, filename):
        self.equivalent_faults = []
        with open(filename, 'r') as f:
            # read lines until matching the first line with 'module'
            # this assumes that the order of 'module', 'input', 'output', and 'wire'
            # is fixed within the file.
            line = f.readline()
            while 'module' not in line:
                line = f.readline()
            self.module_name = line.split('module ')[1].split('(')[0].strip()
            line = f.readline()
            while 'input' not in line:
                line = f.readline()
            # parse line, to get an array of inputs, the strip is to remove leading/trailing whitespaces
            inputs = [net.strip() for net in line.split('input ')[1].split(';')[0].split(',')]

            line = f.readline()
            while 'output' not in line:
                line = f.readline()
            outputs = [net.strip() for net in line.split('output ')[1].split(';')[0].split(',')]

            line = f.readline()
            while 'wire' not in line:
                line = f.readline()
            wires = [net.strip() for net in line.split('wire ')[1].split(';')[0].split(',')]
            self.primary_inputs = [Net(input, (1, 1)) for input in inputs]
            self.primary_outputs = [Net(output, (1, 1)) for output in outputs]
            self.inner_wires = [Net(wire, (1, 1)) for wire in wires]
            netlist = self.primary_inputs + self.inner_wires + self.primary_outputs
            self.net_list = {net.name: net.fault for net in netlist}
            # print(f'module name: {module_name}\ninputs: {inputs}\noutputs: {outputs}\nwires: {wires}')
            self.net_count = {net: 0 for net in inputs + wires + outputs}
            # initialize net count for primary outputs
            for net in outputs:
                self.net_count[net] = 1

            # populate gate list
            self.gate_list = []
            for line in f:
                # break out if end of module
                if 'endmodule' in line:
                    break
                # ignore comments
                if '//' in line:
                    line = line.split('//')[0]
                # ignore empty lines
                if not line.strip():
                    continue
                # split line by whitespaces to get gate type and name
                tokens = line.strip().split()
                gate_type = tokens[0]
                gate_name = tokens[1]
                # get inputs and outputs
                tokens = line.split('(', 1)[1].strip(';\n').split(',')
                output = [t for t in tokens if '.Y' in t][0]
                inputs = [t for t in tokens if '.Y' not in t]
                # strip input/output names, and only keep the net names
                output = output[2:].strip('()')
                inputs = [i[2:].strip('()') for i in inputs]
                # update net counts for fanout information
                for input in inputs:
                    # if input is not in the net list, add it
                    if input not in self.net_count.keys():
                        self.net_list[input] = (1, 1)
                        self.net_count[input] = 1
                    else:
                        self.net_count[input] += 1
                # if output not in self.net_count.keys():
                #     self.net_list[output] = (1, 1)
                #     self.net_count[output] = 1
                self.gate_list.append(Gate(gate_name, GateType[gate_type], 0, inputs, output))

        # initialize fanouts
        self.fanout_count = 0
        for net, count in self.net_count.items():
            if count > 1:
                self.fanout_count += count
                gates_updated = 1

                # update fanout net names in gate list
                for gate in self.gate_list:
                    for i, input in enumerate(gate.inputs):
                        if input == net:
                            fanout_net = Net(net + f'_{gates_updated}', (1, 1))
                            gate.inputs[i] = fanout_net.name
                            self.net_list[fanout_net.name] = fanout_net.fault
                            gates_updated += 1

        self.uncollapsed_faults = (len(self.primary_inputs) + len(self.gate_list) + self.fanout_count) * 2

    def set_gate_levels(self, inputs=None, level=0):
        if inputs is None:
            inputs = [net.name for net in self.primary_inputs]
        if inputs == []:
            return
        # get gates with these inputs
        gates = []
        for i, gate in enumerate(self.gate_list):
            for input in gate.inputs:
                if input in inputs:
                    gates.append(gate)
                    g = self.gate_list[i]
                    self.gate_list[i] = Gate(g.name, g.type, level, g.inputs, g.output)
        # get outputs of these gates
        outputs = [gate.output for gate in gates]
        self.set_gate_levels(outputs, level + 1)
        self.gate_list = sorted(self.gate_list, key=lambda x: x.level, reverse=True)

    def get_fault_count(self):
        count = 0
        for net in self.net_list:
            fault = self.net_list[net]
            count += fault[0] + fault[1]
        return count

    def get_collapse_ratio(self):
        return self.get_fault_count() / self.uncollapsed_faults

    def make_output_files(self):
        with open(f'{self.module_name}_BF.txt', 'w') as f:
            for net in self.net_list:
                fault = self.net_list[net]
                f.write(f'sa1    {net}\n')
            for net in self.net_list:
                fault = self.net_list[net]
                f.write(f'sa0    {net}\n')
            f.write('\n')
            f.write(f'Total Faults_BF={self.uncollapsed_faults}\n')

        with open(f'{self.module_name}_AF.txt', 'w') as f:
            for net in self.net_list:
                fault = self.net_list[net]
                if fault[1] == 1:
                    f.write(f'sa1    {net}\n')
            for net in self.net_list:
                fault = self.net_list[net]
                if fault[0] == 1:
                    f.write(f'sa0    {net}\n')
            f.write('\n')
            f.write(f'Total Faults_AF={self.get_fault_count()}\n')
            f.write(f'Collapse_ratio={self.get_collapse_ratio()}\n\n')
            f.write('Equivalent Classes:\n')
            for fault in self.equivalent_faults:
                for collapsed in fault.collapsed:
                    f.write(f'{collapsed}, ')
                f.write(f'{fault.uncollapsed}\n')

    def collapse(self):
        for gate in self.gate_list:
            out_net = gate.output
            in_nets = gate.inputs
            out_fault = self.net_list[out_net]
            collapsed = []
            uncollapsed = ""
            match gate.type:
                case GateType.AND2X1:
                    if out_fault[0] == 1:
                        for in_net in in_nets:
                            sa0 = 0
                            sa1 = self.net_list[in_net][1]
                            self.net_list[in_net] = (sa0, sa1)
                            collapsed.append(f'sa0 {in_net}')
                            uncollapsed = f'sa0 {out_net}'
                        self.equivalent_faults.append(EquivalentFault(collapsed, uncollapsed))
                case GateType.OR2X1:
                    if out_fault[1] == 1:
                        for in_net in in_nets:
                            sa0 = self.net_list[in_net][0]
                            sa1 = 0
                            self.net_list[in_net] = (sa0, sa1)
                            collapsed.append(f'sa1 {in_net}')
                            uncollapsed = f'sa1 {out_net}'
                        self.equivalent_faults.append(EquivalentFault(collapsed, uncollapsed))
                case GateType.NAND2X1:
                    if out_fault[1] == 1:
                        for in_net in in_nets:
                            sa0 = 0
                            sa1 = self.net_list[in_net][1]
                            self.net_list[in_net] = (sa0, sa1)
                            collapsed.append(f'sa0 {in_net}')
                            uncollapsed = f'sa1 {out_net}'
                        self.equivalent_faults.append(EquivalentFault(collapsed, uncollapsed))
                case GateType.NOR2X1:
                    if out_fault[0] == 1:
                        for in_net in in_nets:
                            sa0 = self.net_list[in_net][0]
                            sa1 = 0
                            self.net_list[in_net] = (sa0, sa1)
                            collapsed.append(f'sa1 {in_net}')
                            uncollapsed = f'sa0 {out_net}'
                        self.equivalent_faults.append(EquivalentFault(collapsed, uncollapsed))
                case GateType.INVX1:
                    if out_fault[0] == 1:
                        sa0 = self.net_list[in_nets[0]][0]
                        sa1 = 0
                        self.net_list[in_nets[0]] = (sa0, sa1)
                        collapsed.append(f'sa1 {in_nets[0]}')
                        uncollapsed = f'sa0 {out_net}'
                        self.equivalent_faults.append(EquivalentFault(collapsed, uncollapsed))
                    if out_fault[1] == 1:
                        sa0 = 0
                        sa1 = self.net_list[in_nets[0]][1]
                        self.net_list[in_nets[0]] = (sa0, sa1)
                        collapsed.append(f'sa0 {in_nets[0]}')
                        uncollapsed = f'sa1 {out_net}'
                        self.equivalent_faults.append(EquivalentFault(collapsed, uncollapsed))
                case GateType.BUFX1:
                    if out_fault[0] == 1:
                        sa0 = 0
                        sa1 = self.net_list[in_nets[0]][1]
                        self.net_list[in_nets[0]] = (sa0, sa1)
                        collapsed.append(f'sa0 {in_nets[0]}')
                        uncollapsed = f'sa0 {out_net}'
                        self.equivalent_faults.append(EquivalentFault(collapsed, uncollapsed))
                    if out_fault[1] == 1:
                        sa0 = self.net_list[in_nets[0]][0]
                        sa1 = 0
                        self.net_list[in_nets[0]] = (sa0, sa1)
                        collapsed.append(f'sa1 {in_nets[0]}')
                        uncollapsed = f'sa1 {out_net}'
                        self.equivalent_faults.append(EquivalentFault(collapsed, uncollapsed))


def main():
    if len(sys.argv) != 2:
        print('Usage: ./hw3.py <filename>')
        sys.exit(1)
    collapser = Collapser(filename=sys.argv[1])
    collapser.set_gate_levels()
    print(f'Fault count: {collapser.get_fault_count()}')
    collapser.collapse()
    print(f'Fault count: {collapser.get_fault_count()}')
    print(f'Collapse ratio: {collapser.get_collapse_ratio()}')
    collapser.make_output_files()


if sys.version_info[1] < 10:
    print('Python 3.10 or higher is required.')
    sys.exit(1)

if __name__ == '__main__':
    main()
