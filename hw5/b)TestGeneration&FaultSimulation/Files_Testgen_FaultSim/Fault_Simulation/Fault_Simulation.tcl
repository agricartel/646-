set_messages -log ./fault_sim.log -replace

read_netlist ./mylib.v
read_netlist ./my-circuit.v

run_build_model c6288
#add_clocks 0 { clk_sig } -shift -timing { 100 50 80 40 }
#add_scan_chain chain1 scan_data_in scan_data_out
#add_scan_enables 1 scan_enable

#add_nofaults -module S_DFFX1
#add_nofaults -module S_DFFSRX1

#add_pi_constraint 0 scan_data_in
#add_pi_constraint 0 scan_enable

run_drc

remove_faults -all
set_patterns -delete

set_patterns  -external ./Fault_Sim.pattern
set_simulation -measure sim
run_simulation -override_differences

write_patterns ./patterns_v2.stil -exclude setup -format stil -external -replace
set_patterns -delete
set_patterns -external ./patterns_v2.stil

set_faults -model stuck
read_faults ./fault_list_1

run_fault_sim

report_faults -summary
write_faults ./fault.left -class UD -class PT -class AU -class ND -replace

exit
