# Create instance: redpitaya_converters_0, and set properties
add_ip_and_conf redpitaya_converters redpitaya_converters_0 {
	CLOCK_DUTY_CYCLE_STABILIZER_EN {false} }
connect_to_fpga_pins redpitaya_converters_0 phys_interface phys_interface_0

# Create instance: adc1_offset, and set properties
add_ip_and_conf add_constReal adc1_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }
connect_proc adc1_offset s00_axi 0x50000

# Create instance: adc2_offset, and set properties
add_ip_and_conf add_constReal adc2_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} }
connect_proc adc2_offset s00_axi 0x40000

# Create instance: convertComplexToReal_0, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_0 {
	DATA_SIZE {14} }

# Create instance: convertComplexToReal_1, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_1 {
	DATA_SIZE {14} }

# Create instance: convertComplexToReal_4, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_4 {
	DATA_SIZE {14} }

# Create instance: convertComplexToReal_5, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_5 {
	DATA_SIZE {14} }

# Create instance: dataReal_to_ram_fast, and set properties
add_ip_and_conf dataReal_to_ram dataReal_to_ram_fast {
	DATA_SIZE {16} \
	NB_INPUT {2} \
	NB_SAMPLE {1024} }
connect_proc dataReal_to_ram_fast s00_axi 0x00000

# Create instance: dataReal_to_ram_slow, and set properties
add_ip_and_conf dataReal_to_ram dataReal_to_ram_slow {
	DATA_SIZE {16} \
	NB_INPUT {2} \
	NB_SAMPLE {2048} }
connect_proc dataReal_to_ram_slow s00_axi 0xB0000

# Create instance: dds1_f0, and set properties
add_ip_and_conf add_constReal dds1_f0 {
	DATA_IN_SIZE {40} \
	DATA_OUT_SIZE {40} \
	format {unsigned} }
connect_proc dds1_f0 s00_axi 0x190000

# Create instance: dds1_nco, and set properties
add_ip_and_conf nco_counter dds1_nco {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o dds1_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o dds1_nco ref_rst_i
connect_proc dds1_nco s00_axi 0x1A0000

# Create instance: dds1_offset, and set properties
add_ip_and_conf add_constReal dds1_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	format {signed} }
connect_proc dds1_offset s00_axi 0x200000

# Create instance: dds2_f0, and set properties
add_ip_and_conf add_constReal dds2_f0 {
	DATA_IN_SIZE {40} \
	DATA_OUT_SIZE {40} \
	format {unsigned} }
connect_proc dds2_f0 s00_axi 0x1B0000

# Create instance: dds2_nco, and set properties
add_ip_and_conf nco_counter dds2_nco {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o dds2_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o dds2_nco ref_rst_i
connect_proc dds2_nco s00_axi 0x1D0000

# Create instance: dds2_offset, and set properties
add_ip_and_conf add_constReal dds2_offset {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	format {signed} }
connect_proc dds2_offset s00_axi 0x210000

# Create instance: dds_ampl, and set properties
add_ip_and_conf axi_to_dac dds_ampl {
	DATA_SIZE {14} \
	SYNCHRONIZE_CHAN {false} }
connect_intf redpitaya_converters_0 clk_o dds_ampl ref_clk_i
connect_intf redpitaya_converters_0 rst_o dds_ampl ref_rst_i
connect_proc dds_ampl s00_axi 0x130000

# Create instance: dds_range, and set properties
add_ip_and_conf axi_to_dac dds_range {
	DATA_SIZE {14} \
	SYNCHRONIZE_CHAN {false} }
connect_intf redpitaya_converters_0 clk_o dds_range ref_clk_i
connect_intf redpitaya_converters_0 rst_o dds_range ref_rst_i
connect_proc dds_range s00_axi 0x120000

# Create instance: demod1_nco, and set properties
add_ip_and_conf nco_counter demod1_nco {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o demod1_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o demod1_nco ref_rst_i
connect_proc demod1_nco s00_axi 0x60000

# Create instance: demod2_nco, and set properties
add_ip_and_conf nco_counter demod2_nco {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }
connect_intf redpitaya_converters_0 clk_o demod2_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o demod2_nco ref_rst_i
connect_proc demod2_nco s00_axi 0x70000

# Create instance: dupplReal_1_to_2_1, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_1 {
	DATA_SIZE {14} }

# Create instance: dupplReal_1_to_2_2, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_2 {
	DATA_SIZE {14} }

# Create instance: dupplReal_1_to_2_3, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_3 {
	DATA_SIZE {14} }

# Create instance: dupplReal_1_to_2_4, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_4 {
	DATA_SIZE {14} }

# Create instance: expanderReal_2, and set properties
add_ip_and_conf expanderReal expanderReal_2 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {19} }

# Create instance: expanderReal_3, and set properties
add_ip_and_conf expanderReal expanderReal_3 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {19} }

# Create instance: firReal_0, and set properties
add_ip_and_conf firReal firReal_0 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {32} \
	DECIMATE_FACTOR {1} \
	NB_COEFF {25} }
connect_proc firReal_0 s00_axi 0x80000

# Create instance: firReal_1, and set properties
add_ip_and_conf firReal firReal_1 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {32} \
	DECIMATE_FACTOR {1} \
	NB_COEFF {25} }
connect_proc firReal_1 s00_axi 0x90000

# Create instance: meanReal_0, and set properties
add_ip_and_conf meanReal meanReal_0 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {128} \
	SHIFT {7} }

# Create instance: meanReal_1, and set properties
add_ip_and_conf meanReal meanReal_1 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {128} \
	SHIFT {7} }

# Create instance: meanReal_2, and set properties
add_ip_and_conf meanReal meanReal_2 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {8192} \
	SHIFT {13} }

# Create instance: meanReal_3, and set properties
add_ip_and_conf meanReal meanReal_3 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {16} \
	NB_ACCUM {8192} \
	SHIFT {13} }

# Create instance: mixer_sin_0, and set properties
add_ip_and_conf mixer_sin mixer_sin_0 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	NCO_SIZE {16} }

# Create instance: mixer_sin_1, and set properties
add_ip_and_conf mixer_sin mixer_sin_1 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	NCO_SIZE {16} }

# Create instance: mixer_sin_2, and set properties
add_ip_and_conf multiplierReal mixer_sin_2 {
	DATA1_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	DATA2_IN_SIZE {14} }


# Create instance: mixer_sin_3, and set properties
add_ip_and_conf multiplierReal mixer_sin_3 {
	DATA1_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	DATA2_IN_SIZE {14} }

# Create instance: mixer_sin_4, and set properties
add_ip_and_conf mixer_sin mixer_sin_4 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	NCO_SIZE {16} }

# Create instance: mixer_sin_5, and set properties
add_ip_and_conf mixer_sin mixer_sin_5 {
	DATA_IN_SIZE {14} \
	DATA_OUT_SIZE {14} \
	NCO_SIZE {16} }

# Create instance: pidv3_axi_0, and set properties
add_ip_and_conf pidv3_axi pidv3_axi_0 {
	DSR {1} \
	ISR {19} \
	I_SIZE {18} \
	PSR {13} }
connect_proc pidv3_axi_0 s00_axi 0x30000

# Create instance: pidv3_axi_1, and set properties
add_ip_and_conf pidv3_axi pidv3_axi_1 {
	DSR {1} \
	ISR {19} \
	I_SIZE {18} \
	PSR {13} }
connect_proc pidv3_axi_1 s00_axi 0x140000

# Create instance: shifterReal_2, and set properties
add_ip_and_conf shifterReal shifterReal_2 {
	DATA_IN_SIZE {19} \
	DATA_OUT_SIZE {40} }

# Create instance: shifterReal_3, and set properties
add_ip_and_conf shifterReal shifterReal_3 {
	DATA_IN_SIZE {19} \
	DATA_OUT_SIZE {40} }

# Create instance: shifterReal_dyn_0, and set properties
add_ip_and_conf shifterReal_dyn shifterReal_dyn_0 {
	DATA_OUT_SIZE {14} }
connect_proc shifterReal_dyn_0 s00_axi 0x20000

# Create instance: shifterReal_dyn_1, and set properties
add_ip_and_conf shifterReal_dyn shifterReal_dyn_1 {
	DATA_OUT_SIZE {14} }
connect_proc shifterReal_dyn_1 s00_axi 0xA0000

# Create interface connections
connect_proc_rst redpitaya_converters_0 adc_rst_i

#connect_intf dds_range dataB_rst_o mixer_sin_3 nco_rst_i
connect_intf adc1_offset data_out mixer_sin_0 data_in
connect_intf adc2_offset data_out mixer_sin_1 data_in
connect_intf convertComplexToReal_0 dataI_out firReal_0 data_in
connect_intf convertComplexToReal_1 dataI_out firReal_1 data_in

connect_intf mixer_sin_2 data_out expanderReal_2 data_in
connect_intf expanderReal_2 data_out shifterReal_3 data_in
connect_intf mixer_sin_3 data_out expanderReal_3 data_in
connect_intf expanderReal_3 data_out shifterReal_2 data_in

connect_intf convertComplexToReal_4 dataI_out dds1_offset data_in
connect_intf convertComplexToReal_5 dataI_out dds2_offset data_in
connect_intf dds1_nco sine_out mixer_sin_4 nco_in
connect_intf dds1_offset data_out redpitaya_converters_0 dataA_in
connect_intf dds2_nco sine_out mixer_sin_5 nco_in
connect_intf dds2_offset data_out redpitaya_converters_0 dataB_in
connect_intf dds_ampl dataA_out mixer_sin_4 data_in
connect_intf dds_ampl dataB_out mixer_sin_5 data_in
connect_intf dupplReal_1_to_2_1 data1_out pidv3_axi_0 data_in
connect_intf dupplReal_1_to_2_1 data2_out dupplReal_1_to_2_4 data_in
connect_intf dupplReal_1_to_2_2 data1_out dupplReal_1_to_2_3 data_in
connect_intf dupplReal_1_to_2_2 data2_out pidv3_axi_1 data_in
connect_intf dupplReal_1_to_2_3 data1_out meanReal_1 data_in
connect_intf dupplReal_1_to_2_3 data2_out meanReal_3 data_in
connect_intf dupplReal_1_to_2_4 data1_out meanReal_0 data_in
connect_intf dupplReal_1_to_2_4 data2_out meanReal_2 data_in
connect_intf firReal_0 data_out shifterReal_dyn_0 data_in
connect_intf firReal_1 data_out shifterReal_dyn_1 data_in
connect_intf dataReal_to_ram_fast data1_in meanReal_0 data_out
connect_intf dataReal_to_ram_fast data2_in meanReal_1 data_out
connect_intf dataReal_to_ram_slow data1_in meanReal_2 data_out
connect_intf dataReal_to_ram_slow data2_in meanReal_3 data_out
connect_intf convertComplexToReal_0 data_in mixer_sin_0 data_out
connect_intf convertComplexToReal_1 data_in mixer_sin_1 data_out
connect_intf convertComplexToReal_4 data_in mixer_sin_4 data_out
connect_intf convertComplexToReal_5 data_in mixer_sin_5 data_out
connect_intf demod1_nco sine_out mixer_sin_0 nco_in
connect_intf demod2_nco sine_out mixer_sin_1 nco_in
connect_intf mixer_sin_2 data1_in pidv3_axi_0 data_out
connect_intf dds_range dataA_out mixer_sin_2 data2_in
connect_intf mixer_sin_3 data1_in pidv3_axi_1 data_out
connect_intf dds_range dataB_out mixer_sin_3 data2_in
connect_intf adc1_offset data_in redpitaya_converters_0 dataA_out
connect_intf adc2_offset data_in redpitaya_converters_0 dataB_out
connect_intf dds1_nco pinc_in dds1_f0 data_out
connect_intf dds2_nco pinc_in dds2_f0 data_out
connect_intf dds2_f0 data_in shifterReal_2 data_out
connect_intf dds1_f0 data_in shifterReal_3 data_out
connect_intf dupplReal_1_to_2_1 data_in shifterReal_dyn_0 data_out
connect_intf dupplReal_1_to_2_2 data_in shifterReal_dyn_1 data_out
