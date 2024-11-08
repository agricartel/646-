set WORKDIR [pwd]
set LIBFILE ${WORKDIR}/646-FA24/hw5/benchmarks/GSCLib.v
#set NETLIST ${WORKDIR}/646-FA24/hw5/circuit_a.v
#set NETLIST ${WORKDIR}/646-FA24/hw5/benchmarks/c1908_new.v
set NETLIST ${WORKDIR}/646-FA24/hw5/benchmarks/c2670_new.v

#set TOPMODULE circuit_a
#set TOPMODULE c1908
set TOPMODULE c2670

read_netlist ${LIBFILE}
read_netlist ${NETLIST}

run_build_model $TOPMODULE

run_drc

set_faults -model stuck
add_faults -all
set_faults -report collapsed

write_faults ${WORKDIR}/${TOPMODULE}_all_faults -all -uncollapsed -replace
write_faults ${WORKDIR}/${TOPMODULE}_collapsed_faults -all -collapsed -replace

exit
