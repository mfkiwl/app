#!/usr/bin/env python3

from xml.dom import minidom
import sys
import os, stat

board_driver_array = []
xmldoc = minidom.parse(sys.argv[1])
name = sys.argv[1].split('/')[-1].split('.')[0]

driver_list = xmldoc.getElementsByTagName('ip')

for driver in driver_list:
	board_driver_list = driver.getElementsByTagName('instance')
	for board_driver in board_driver_list:
		board_driver_array.append([str(driver.attributes['name'].value), str(board_driver.attributes['name'].value)])

board_driver_array = sorted(board_driver_array, key=lambda x:x[-1])

try:
	os.chdir('app')
except:
	os.mkdir('app')
	os.chdir('app')

try:
	os.remove('%s_webserver.py'%name)
except:
	pass

with open('%s_webserver.py'%name, 'a') as f:
	f.write('#!/usr/bin/env python\n\n')
	f.write('import liboscimp_fpga\n')
	f.write('import ctypes\n')
	f.write('import os\n')
	f.write('import time\n')
	f.write('from lxml import objectify\n')
	f.write('import lxml.etree\n')
	f.write('import remi.gui as gui\n')
	f.write('from remi import start, App\n\n')

	for elem in board_driver_array:
		if elem[0] == 'redpitaya_converters_12':
			f.write('#Packages for the redpitaya12 board\n')
			f.write('from threading import Timer\n\n')
			f.write('# Initiate the controller input and output switches\n')
			f.write('liboscimp_fpga.RP_12_initController()\n\n')
			f.write('# Power on ADC and DAC\n')
			f.write('os.system("echo 908 > /sys/class/gpio/export")\n')
			f.write('os.system("echo out > /sys/class/gpio/gpio908/direction")\n')
			f.write('os.system("echo 1 > /sys/class/gpio/gpio908/value")\n')
			f.write('os.system("echo 908 > /sys/class/gpio/unexport")\n')
			f.write('os.system("echo 909 > /sys/class/gpio/export")\n')
			f.write('os.system("echo out > /sys/class/gpio/gpio909/direction")\n')
			f.write('os.system("echo 1 > /sys/class/gpio/gpio909/value")\n')
			f.write('os.system("echo 909 > /sys/class/gpio/unexport")\n\n')
			f.write('# Configure the ADCs \n')
			f.write('liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/%s",1,0xff,0x00,1)\n'%elem[1])
			f.write('liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/%s",1,0xff,0x00,0)\n'%elem[1])
			f.write('time.sleep(0.1)\n')
			f.write('liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/%s",1,0x14,0x01,1)\n'%elem[1])
			f.write('liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/%s",1,0x14,0x01,0)\n'%elem[1])
			f.write('time.sleep(0.1)\n')
			f.write('liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/%s",1,0x16,0xa0,1)\n'%elem[1])
			f.write('liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/%s",1,0x16,0xa0,0)\n'%elem[1])
			f.write('time.sleep(0.1)\n')
			f.write('liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/%s",1,0x18,0x1b,1)\n'%elem[1])
			f.write('liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/%s",1,0x18,0x1b,0)\n'%elem[1])
			f.write('time.sleep(0.1)\n')
			f.write('liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/%s",1,0xff,0x01,1)\n\n'%elem[1])

	try:
		board_name = os.environ["BOARD_NAME"].lower()
	except KeyError:
		print("Error: missing BOARD_NAME")
		os.sys.exit()

	if board_name == "redpitaya":
		samp_freq = 125000000
	elif board_name == "redpitaya16":
		samp_freq = 122880000
	elif board_name == "plutosdr":
		samp_freq = 20000000
		rx_lo = 1545520000
		tx_lo = 1545520000
	elif board_name == "redpitaya12":
		samp_freq = 250000000
	elif board_name == "zedboard":
		samp_freq = 100000000

	if board_name == "plutosdr":
		f.write('import iio\n\n')
		f.write('ctx = iio.Context()\n')
		f.write('dev_rx = ctx.find_device("cf-ad9361-lpc")\n')
		f.write('dev_tx = ctx.find_device("cf-ad9361-dds-core-lpc")\n')
		f.write('phy = ctx.find_device("ad9361-phy")\n\n')
		f.write(f'[i for i in phy.channels if i.id == "altvoltage0"][0].attrs["frequency"].value = "{rx_lo}"\n')
		f.write(f'[i for i in phy.channels if i.id == "altvoltage1"][0].attrs["frequency"].value = "{tx_lo}"\n\n')
		f.write(f'[i for i in phy.channels if i.id == "voltage0"][0].attrs["sampling_frequency"].value = "{samp_freq}"\n\n')
		f.write('[i for i in dev_rx.channels if i.id == "voltage0"][0].enabled = True\n')
		f.write('[i for i in dev_rx.channels if i.id == "voltage1"][0].enabled = True\n\n')
		f.write('[i for i in dev_tx.channels if i.id == "voltage0"][0].enabled = True\n')
		f.write('[i for i in dev_tx.channels if i.id == "voltage1"][0].enabled = True\n\n')

	f.write('#Sampling frequency\n')
	f.write(f"samp_freq = {samp_freq}\n\n")

	f.write('vals = objectify.Element("item")\n')
	f.write('vals.config = "%s_defconf.xml"\n'%name)

	if board_name == "plutosdr":
		f.write('vals.tx_lo = 1000000000\n')
		f.write('vals.rx_lo = 1000000000\n')

	for elem in board_driver_array:
		if elem[0] == 'add_constReal':
			f.write('vals.%s = 0\n'%elem[1])

		if elem[0] == 'axi_to_dac':
			f.write('vals.ch1_%s = 0\n'%elem[1])
			f.write('vals.ch2_%s = 0\n'%elem[1])

		if elem[0] == 'pidv3_axi':
			f.write('vals.kp_%s = 0\n'%elem[1])
			f.write('vals.ki_%s = 0\n'%elem[1])
			f.write('vals.rst_int_%s = True\n'%elem[1])
			f.write('vals.sp_%s = 0\n'%elem[1])
			f.write('vals.sign_%s = 0\n'%elem[1])

		if elem[0] == 'redpitaya_converters_12':
			f.write('vals.listView_acdc1 = "ADC1 DC"\n')
			f.write('vals.listView_acdc2 = "ADC2 DC"\n')
			f.write('vals.listView_range1 = "ADC1\\xa01/20"\n')
			f.write('vals.listView_range2 = "ADC2\\xa01/20"\n')
			f.write('vals.listView_ampl1 = "DAC1\\xa02V"\n')
			f.write('vals.listView_ampl2 = "DAC2\\xa02V"\n')
			f.write('vals.listView_extref = "Int\\xa0Clock"\n')

		if elem[0] in ['shifterReal_dyn', 'shifterComplex_dyn', 'delayTempoReal_axi'] :
			f.write('vals.%s = 9\n'%elem[1])

		if elem[0] == 'nco_counter':
			f.write('vals.pinc_%s = 0\n'%elem[1])
			f.write('vals.poff_%s = 0\n'%elem[1])
			f.write('vals.cb_pinc_%s = True\n'%elem[1])
			f.write('vals.cb_poff_%s = True\n'%elem[1])

		if elem[0] in ['switchReal', 'switchComplex'] :
			f.write('vals.%s = True\n'%elem[1])

	f.write('\nclass MyApp(App):\n')
	f.write('\tdef __init__(self, *args):\n')
	f.write('\t\tsuper(MyApp, self).__init__(*args)\n\n')
	f.write('\tdef main(self):\n')
	f.write('\t\tself.w = gui.VBox()\n\n')

	print('\n')

	f.write('\t\tself.hbox_save_load = gui.HBox(margin="10px")\n')
	f.write('\t\tself.dtext_conf_file = gui.TextInput(width=200, height=30)\n')
	f.write('\t\tself.dtext_conf_file.set_value(str(vals.config))\n')
	f.write('\t\tself.dtext_conf_file.set_on_change_listener(self.dtext_conf_file_changed)\n')
	f.write('\t\tself.bt_load = gui.Button("Load", width=200, height=30, margin="10px")\n')
	f.write('\t\tself.bt_load.set_on_click_listener(self.bt_load_changed)\n')
	f.write('\t\tself.bt_save = gui.Button("Save", width=200, height=30, margin="10px")\n')
	f.write('\t\tself.bt_save.set_on_click_listener(self.bt_save_changed)\n')
	f.write('\t\tself.hbox_save_load.append(self.dtext_conf_file)\n')
	f.write('\t\tself.hbox_save_load.append(self.bt_load)\n')
	f.write('\t\tself.hbox_save_load.append(self.bt_save)\n')
	f.write('\t\tself.w.append(self.hbox_save_load)\n\n')

	if board_name == "plutosdr":
		f.write('\t\tself.hbox_tx_lo = gui.HBox(margin="10px")\n')
		f.write('\t\tself.lb_tx_lo = gui.Label("iio:tx_lo", width="20%%", margin="10px")\n')
		f.write('\t\tself.sd_tx_lo = gui.Slider(vals.tx_lo, 0, 7000000000, 1000000, width="60%%", margin="10px")\n')
		f.write('\t\tself.sd_tx_lo.set_on_change_listener(self.sd_tx_lo_changed)\n')
		f.write('\t\tself.sb_tx_lo = gui.SpinBox(vals.tx_lo, 0, 7000000000, 1000000, width="20%%", margin="10px")\n')
		f.write('\t\tself.sb_tx_lo.set_on_change_listener(self.sb_tx_lo_changed)\n')
		f.write('\t\tself.sd_tx_lo_changed(self.sd_tx_lo, self.sd_tx_lo.get_value())\n')
		f.write('\t\tself.hbox_tx_lo.append(self.lb_tx_lo)\n')
		f.write('\t\tself.hbox_tx_lo.append(self.sd_tx_lo)\n')
		f.write('\t\tself.hbox_tx_lo.append(self.sb_tx_lo)\n')
		f.write('\t\tself.w.append(self.hbox_tx_lo)\n\n')

		f.write('\t\tself.hbox_rx_lo = gui.HBox(margin="10px")\n')
		f.write('\t\tself.lb_rx_lo = gui.Label("iio:rx_lo", width="20%%", margin="10px")\n')
		f.write('\t\tself.sd_rx_lo = gui.Slider(vals.rx_lo, 0, 7000000000, 1, width="60%%", margin="10px")\n')
		f.write('\t\tself.sd_rx_lo.set_on_change_listener(self.sd_rx_lo_changed)\n')
		f.write('\t\tself.sb_rx_lo = gui.SpinBox(vals.rx_lo, 0, 7000000000, 1, width="20%%", margin="10px")\n')
		f.write('\t\tself.sb_rx_lo.set_on_change_listener(self.sb_rx_lo_changed)\n')
		f.write('\t\tself.sd_rx_lo_changed(self.sd_rx_lo, self.sd_rx_lo.get_value())\n')
		f.write('\t\tself.hbox_rx_lo.append(self.lb_rx_lo)\n')
		f.write('\t\tself.hbox_rx_lo.append(self.sd_rx_lo)\n')
		f.write('\t\tself.hbox_rx_lo.append(self.sb_rx_lo)\n')
		f.write('\t\tself.w.append(self.hbox_rx_lo)\n\n')

	for elem in board_driver_array:
		print('%s\t%s'%(elem[1], elem[0]))

		if elem[0] == 'add_constReal':
			f.write('\t\tself.hbox_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_%s = gui.Label("/dev/%s", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			if 'f0' not in elem[1]:
				f.write('\t\tself.sd_%s = gui.Slider(vals.%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1],elem[1]))
			else:
				f.write('\t\tself.sd_%s = gui.Slider(vals.%s, 0, samp_freq/2, 1, width="60%%", margin="10px")\n'%(elem[1],elem[1]))
			f.write('\t\tself.sd_%s.set_on_change_listener(self.sd_%s_changed)\n'%(elem[1], elem[1]))
			if 'f0' not in elem[1]:
				f.write('\t\tself.sb_%s = gui.SpinBox(vals.%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1],elem[1]))
			else:
				f.write('\t\tself.sb_%s = gui.SpinBox(vals.%s, 0, samp_freq/2, 0.02, width="20%%", margin="10px")\n'%(elem[1],elem[1]))
			f.write('\t\tself.sb_%s.set_on_change_listener(self.sb_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_%s_changed(self.sd_%s, self.sd_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.lb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sd_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_%s)\n\n'%elem[1])

		if elem[0] == 'axi_to_dac':
			f.write('\t\tself.hbox_ch1_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_ch1_%s = gui.Label("/dev/%s/1", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ch1_%s = gui.Slider(vals.ch1_%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ch1_%s.set_on_change_listener(self.sd_ch1_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_ch1_%s = gui.SpinBox(vals.ch1_%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_ch1_%s.set_on_change_listener(self.sb_ch1_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ch1_%s_changed(self.sd_ch1_%s, self.sd_ch1_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_ch1_%s.append(self.lb_ch1_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ch1_%s.append(self.sd_ch1_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ch1_%s.append(self.sb_ch1_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_ch1_%s)\n\n'%elem[1])

			f.write('\t\tself.hbox_ch2_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_ch2_%s = gui.Label("/dev/%s/2", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ch2_%s = gui.Slider(vals.ch2_%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ch2_%s.set_on_change_listener(self.sd_ch2_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_ch2_%s = gui.SpinBox(vals.ch2_%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_ch2_%s.set_on_change_listener(self.sb_ch2_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ch2_%s_changed(self.sd_ch2_%s, self.sd_ch2_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_ch2_%s.append(self.lb_ch2_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ch2_%s.append(self.sd_ch2_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ch2_%s.append(self.sb_ch2_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_ch2_%s)\n\n'%elem[1])

		if elem[0] == 'pidv3_axi':
			f.write('\t\tself.hbox_kp_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_kp_%s = gui.Label("/dev/%s/kp", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_kp_%s = gui.Slider(vals.kp_%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_kp_%s.set_on_change_listener(self.sd_kp_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_kp_%s = gui.SpinBox(vals.kp_%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_kp_%s.set_on_change_listener(self.sb_kp_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_kp_%s_changed(self.sd_kp_%s, self.sd_kp_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_kp_%s.append(self.lb_kp_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_kp_%s.append(self.sd_kp_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_kp_%s.append(self.sb_kp_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_kp_%s)\n\n'%elem[1])

			f.write('\t\tself.hbox_ki_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_ki_%s = gui.Label("/dev/%s/ki", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ki_%s = gui.Slider(vals.ki_%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ki_%s.set_on_change_listener(self.sd_ki_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_ki_%s = gui.SpinBox(vals.ki_%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_ki_%s.set_on_change_listener(self.sb_ki_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ki_%s_changed(self.sd_ki_%s, self.sd_ki_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_rst_int_%s = gui.CheckBoxLabel("rst_int", vals.rst_int_%s, width="5%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.cb_rst_int_%s.set_on_change_listener(self.cb_rst_int_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ki_%s.append(self.lb_ki_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ki_%s.append(self.sd_ki_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ki_%s.append(self.sb_ki_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ki_%s.append(self.cb_rst_int_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_ki_%s)\n\n'%elem[1])

			f.write('\t\tself.hbox_sp_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_sp_%s = gui.Label("/dev/%s/setpoint", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_sp_%s = gui.Slider(vals.sp_%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_sp_%s.set_on_change_listener(self.sd_sp_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_sp_%s = gui.SpinBox(vals.sp_%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_sp_%s.set_on_change_listener(self.sb_sp_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_sp_%s_changed(self.sd_sp_%s, self.sd_sp_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_sp_%s.append(self.lb_sp_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_sp_%s.append(self.sd_sp_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_sp_%s.append(self.sb_sp_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_sp_%s)\n\n'%elem[1])

			f.write('\t\tself.hbox_sign_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_sign_%s = gui.Label("/dev/%s/sign", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_sign_%s = gui.Slider(vals.sign_%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_sign_%s.set_on_change_listener(self.sd_sign_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_sign_%s = gui.SpinBox(vals.sign_%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_sign_%s.set_on_change_listener(self.sb_sign_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_sign_%s_changed(self.sd_sign_%s, self.sd_sign_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.hbox_sign_%s.append(self.lb_sign_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_sign_%s.append(self.sd_sign_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_sign_%s.append(self.sb_sign_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_sign_%s)\n\n'%elem[1])

		if elem[0] == 'redpitaya_converters_12':
			f.write('\t\tself.hbox_%s = gui.HBox(margin="2px")\n'%elem[1])
			f.write('\t\tself.lb_%s = gui.Label("RP12", width="20%%",height=0, margin="10px")\n'%elem[1])
			f.write('\t\tself.listView_acdc1 = gui.ListView.new_from_list(("ADC1 AC","ADC1 DC"), width=70, height=50, margin="10px")\n')
			f.write('\t\tself.listView_range1 = gui.ListView.new_from_list(("ADC1\\xa01/1","ADC1\\xa01/20"), width=80, height=50, margin="10px")\n')
			f.write('\t\tself.listView_ampl1 = gui.ListView.new_from_list(("DAC1\\xa02V","DAC1\\xa010V"), width=80, height=50, margin="10px")\n')
			f.write('\t\tself.listView_acdc2 = gui.ListView.new_from_list(("ADC2 AC","ADC2 DC"), width=70, height=50, margin="10px")\n')
			f.write('\t\tself.listView_range2 = gui.ListView.new_from_list(("ADC2\\xa01/1","ADC2\\xa01/20"), width=80, height=50, margin="10px")\n')
			f.write('\t\tself.listView_ampl2 = gui.ListView.new_from_list(("DAC2\\xa02V","DAC2\\xa010V"), width=80, height=50, margin="10px")\n')
			f.write('\t\tself.listView_extref = gui.ListView.new_from_list(("Int\\xa0Clock","Ext\\xa0Ref"), width=70, height=50, margin="10px", style={"background-color": "#FE96A0"})\n')
			f.write('\t\tself.listView_acdc1.onselection(self.listView_acdc1_changed)\n')
			f.write('\t\tself.listView_range1.onselection(self.listView_range1_changed)\n')
			f.write('\t\tself.listView_ampl1.onselection(self.listView_ampl1_changed)\n')
			f.write('\t\tself.listView_acdc2.onselection(self.listView_acdc2_changed)\n')
			f.write('\t\tself.listView_range2.onselection(self.listView_range2_changed)\n')
			f.write('\t\tself.listView_ampl2.onselection(self.listView_ampl2_changed)\n')
			f.write('\t\tself.listView_extref.onselection(self.listView_extref_changed)\n')
			f.write('\t\tself.listView_acdc1.select_by_value("ADC1 DC")\n')
			f.write('\t\tself.listView_acdc2.select_by_value("ADC2 DC")\n')
			f.write('\t\tself.listView_range1.select_by_value("ADC1\\xa01/20")\n')
			f.write('\t\tself.listView_range2.select_by_value("ADC2\\xa01/20")\n')
			f.write('\t\tself.listView_ampl1.select_by_value("DAC1\\xa02V")\n')
			f.write('\t\tself.listView_ampl2.select_by_value("DAC2\\xa02V")\n')
			f.write('\t\tself.listView_extref.select_by_value("Int\\xa0Clock")\n')
			f.write('\t\tself.dcolor_extref_state = gui.ColorPicker(width=40, height=40)\n')
			f.write('\t\tself.dcolor_extref_state.set_value("#ff0000")\n')
			f.write('\t\tself.hbox_%s.append(self.lb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.listView_acdc1)\n'%elem[1])
			f.write('\t\tself.hbox_%s.append(self.listView_acdc2)\n'%elem[1])
			f.write('\t\tself.hbox_%s.append(self.listView_range1)\n'%elem[1])
			f.write('\t\tself.hbox_%s.append(self.listView_range2)\n'%elem[1])
			f.write('\t\tself.hbox_%s.append(self.listView_ampl1)\n'%elem[1])
			f.write('\t\tself.hbox_%s.append(self.listView_ampl2)\n'%elem[1])
			f.write('\t\tself.hbox_%s.append(self.listView_extref)\n'%elem[1])
			f.write('\t\tself.hbox_%s.append(self.dcolor_extref_state)\n'%elem[1])
			f.write('\t\tself.w.append(self.hbox_%s)\n\n'%elem[1])
			f.write('\t\tself.stop_flag = False\n')
			f.write('\t\tself.display_extref_state()\n\n')

		if elem[0] in ['shifterReal_dyn', 'shifterComplex_dyn', 'delayTempoReal_axi'] :
			f.write('\t\tself.hbox_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_%s = gui.Label("/dev/%s", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_%s = gui.Slider(vals.%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_%s.set_on_change_listener(self.sd_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_%s = gui.SpinBox(vals.%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_%s.set_on_change_listener(self.sb_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_%s_changed(self.sd_%s, self.sd_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.lb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sd_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_%s)\n\n'%elem[1])


		if elem[0] == 'nco_counter':
			f.write('\t\tself.hbox_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_%s = gui.Label("/dev/%s", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_pinc_%s = gui.Slider(vals.pinc_%s, 0, samp_freq/2, 1, width="25%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_pinc_%s.set_on_change_listener(self.sd_pinc_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_pinc_%s = gui.SpinBox(vals.pinc_%s, 0, samp_freq/2, 0.02, width="10%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_pinc_%s.set_on_change_listener(self.sb_pinc_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_poff_%s = gui.Slider(vals.poff_%s, -8192, 8191, 1, width="25%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_poff_%s.set_on_change_listener(self.sd_poff_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_poff_%s = gui.SpinBox(vals.poff_%s, -8192, 8191, 1, width="10%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_poff_%s.set_on_change_listener(self.sb_poff_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.cb_pinc_%s = gui.CheckBoxLabel("pinc", vals.cb_pinc_%s, width="5%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.cb_pinc_%s.set_on_change_listener(self.cb_pinc_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.cb_poff_%s = gui.CheckBoxLabel("poff", vals.cb_poff_%s, width="5%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.cb_poff_%s.set_on_change_listener(self.cb_poff_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.lb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sd_pinc_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sb_pinc_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sd_poff_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sb_poff_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.cb_pinc_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.cb_poff_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_%s)\n\n'%elem[1])

		if elem[0] in ['switchReal', 'switchComplex'] :
			f.write('\t\tself.hbox_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.cb_%s = gui.CheckBoxLabel("%s", vals.%s, width="5%%", margin="10px")\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_%s.set_on_change_listener(self.cb_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.cb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_%s)\n\n'%elem[1])

	f.write('\t\treturn self.w\n\n')

	f.write('\tdef dtext_conf_file_changed(self, widget, value):\n')
	f.write('\t\tprint(value)\n')
	f.write('\t\tvals.config=value\n\n')

	f.write('\tdef bt_load_changed(self, widget):\n')
	f.write('\t\twith open(str(vals.config), "r") as f:\n')
	f.write('\t\t\t lf = objectify.fromstring(f.read())\n\n')

	if board_name == "plutosdr":
		f.write('\t\tself.sd_tx_lo_changed(self.sd_tx_lo, lf.tx_lo)\n')
		f.write('\t\tself.sb_tx_lo_changed(self.sb_tx_lo, lf.tx_lo)\n')

		f.write('\t\tself.sd_rx_lo_changed(self.sd_rx_lo, lf.rx_lo)\n')
		f.write('\t\tself.sb_rx_lo_changed(self.sb_rx_lo, lf.rx_lo)\n')

	for elem in board_driver_array:
		if elem[0] == 'add_constReal':
			f.write('\t\tself.sd_%s_changed(self.sd_%s, lf.%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_%s_changed(self.sb_%s, lf.%s)\n'%(elem[1], elem[1], elem[1]))
		if elem[0] == 'axi_to_dac':
			f.write('\t\tself.sd_ch1_%s_changed(self.sd_ch1_%s, lf.ch1_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_ch1_%s_changed(self.sd_ch1_%s, lf.ch1_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_ch2_%s_changed(self.sb_ch2_%s, lf.ch2_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_ch2_%s_changed(self.sb_ch2_%s, lf.ch2_%s)\n'%(elem[1], elem[1], elem[1]))
		if elem[0] == 'pidv3_axi':
			f.write('\t\tself.sd_kp_%s_changed(self.sd_kp_%s, lf.kp_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_kp_%s_changed(self.sb_kp_%s, lf.kp_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_ki_%s_changed(self.sd_ki_%s, lf.ki_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_ki_%s_changed(self.sb_ki_%s, lf.ki_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_rst_int_%s_changed(self.cb_rst_int_%s, lf.rst_int_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_sp_%s_changed(self.sd_sp_%s, lf.sp_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_sp_%s_changed(self.sb_sp_%s, lf.sp_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_sign_%s_changed(self.sd_sign_%s, lf.sign_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_sign_%s_changed(self.sb_sign_%s, lf.sign_%s)\n'%(elem[1], elem[1], elem[1]))
		if elem[0] == 'redpitaya_converters_12':
			f.write('\t\tself.listView_acdc1.select_by_value(lf.listView_acdc1)\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAC_DC(liboscimp_fpga.CH1 ,int(lf.listView_acdc1=="ADC1 AC"))\n')
			f.write('\t\tvals.listView_acdc1=lf.listView_acdc1\n')
			f.write('\t\tself.listView_range1.select_by_value(lf.listView_range1)\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAttenuator(liboscimp_fpga.CH1 ,int(lf.listView_range1=="ADC1\\xa01/1"))\n')
			f.write('\t\tvals.listView_range1=lf.listView_range1\n')
			f.write('\t\tself.listView_ampl1.select_by_value(lf.listView_ampl1)\n')
			f.write('\t\tliboscimp_fpga.RP_12_setGainOut(liboscimp_fpga.CH1 ,int(lf.listView_ampl1=="DAC1\\xa010V"))\n')
			f.write('\t\tvals.listView_ampl1=lf.listView_ampl1\n')
			f.write('\t\tself.listView_acdc2.select_by_value(lf.listView_acdc2)\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAC_DC(liboscimp_fpga.CH2 ,int(lf.listView_acdc2=="ADC2 AC"))\n')
			f.write('\t\tvals.listView_acdc2=lf.listView_acdc2\n')
			f.write('\t\tself.listView_range2.select_by_value(lf.listView_range2)\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAttenuator(liboscimp_fpga.CH2 ,int(lf.listView_range2=="ADC2\\xa01/1"))\n')
			f.write('\t\tvals.listView_range2=lf.listView_range2\n')
			f.write('\t\tself.listView_ampl2.select_by_value(lf.listView_ampl2)\n')
			f.write('\t\tliboscimp_fpga.RP_12_setGainOut(liboscimp_fpga.CH2 ,int(lf.listView_ampl2=="DAC2\\xa010V"))\n')
			f.write('\t\tvals.listView_ampl2=lf.listView_ampl2\n')
			f.write('\t\tself.listView_extref.select_by_value(lf.listView_extref)\n')
			f.write('\t\tliboscimp_fpga.redpitaya_converters_12_ext_ref_enable("/dev/%s" ,int(lf.listView_extref=="Ext\\xa0Ref"))\n'%elem[1])
			f.write('\t\tvals.listView_extref=lf.listView_extref\n')
		if elem[0] in ['shifterReal_dyn', 'shifterComplex_dyn', 'delayTempoReal_axi'] :
			f.write('\t\tself.sd_%s_changed(self.sd_%s, lf.%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_%s_changed(self.sb_%s, lf.%s)\n'%(elem[1], elem[1], elem[1]))
		if elem[0] == 'nco_counter':
			f.write('\t\tself.sd_pinc_%s_changed(self.sd_pinc_%s, lf.pinc_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_pinc_%s_changed(self.sb_pinc_%s, lf.pinc_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_poff_%s_changed(self.sd_poff_%s, lf.poff_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_poff_%s_changed(self.sb_poff_%s, lf.poff_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_pinc_%s_changed(self.cb_pinc_%s, lf.cb_pinc_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_poff_%s_changed(self.cb_poff_%s, lf.cb_poff_%s)\n'%(elem[1], elem[1], elem[1]))
		if elem[0] in ['switchReal', 'switchComplex'] :
			f.write('\t\tself.cb_%s_changed(self.cb_%s, lf.%s)\n'%(elem[1], elem[1], elem[1]))

	f.write('\t\tprint("Configuration loaded")\n\n')
	f.write('\tdef bt_save_changed(self, widget):\n')
	f.write('\t\ttry:\n')
	f.write('\t\t\tos.remove(str(vals.config))\n')
	f.write('\t\texcept:\n')
	f.write('\t\t\tpass\n')
	f.write('\t\twith open(str(vals.config), "wb") as f:\n')
	f.write('\t\t\tf.write(lxml.etree.tostring(vals, pretty_print=True))\n')
	f.write('\t\tprint("Saved")\n\n')

	if board_name == "plutosdr":
		f.write('\tdef sd_tx_lo_changed(self, widget, value):\n')
		f.write('\t\tvals.tx_lo=value\n')
		f.write('\t\tprint("iio:tx_lo", int(value))\n')
		f.write('\t\t[i for i in phy.channels if i.id == "altvoltage1"][0].attrs["frequency"].value = value\n')
		f.write('\t\tself.sb_tx_lo.set_value(int(value))\n\n')
		f.write('\tdef sb_tx_lo_changed(self, widget, value):\n')
		f.write('\t\tvals.tx_lo=value\n')
		f.write('\t\tprint("iio:tx_lo", int(value))\n')
		f.write('\t\t[i for i in phy.channels if i.id == "altvoltage1"][0].attrs["frequency"].value = value\n')
		f.write('\t\tself.sd_tx_lo.set_value(int(float(value)))\n\n')

		f.write('\tdef sd_rx_lo_changed(self, widget, value):\n')
		f.write('\t\tvals.rx_lo=value\n')
		f.write('\t\tprint("iio:rx_lo", int(value))\n')
		f.write('\t\t[i for i in phy.channels if i.id == "altvoltage0"][0].attrs["frequency"].value = value\n')
		f.write('\t\tself.sb_rx_lo.set_value(int(value))\n\n')
		f.write('\tdef sb_rx_lo_changed(self, widget, value):\n')
		f.write('\t\tvals.rx_lo=value\n')
		f.write('\t\tprint("iio:rx_lo", int(value))\n')
		f.write('\t\t[i for i in phy.channels if i.id == "altvoltage0"][0].attrs["frequency"].value = value\n')
		f.write('\t\tself.sd_rx_lo.set_value(int(float(value)))\n\n')

	for elem in board_driver_array:
		if elem[0] == 'add_constReal':
			f.write('\tdef sd_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.%s=value\n'%elem[1])
			if 'f0' not in elem[1]:
				f.write('\t\tprint("/dev/%s", int(value))\n'%elem[1])
				f.write('\t\tliboscimp_fpga.add_const_set_offset("/dev/%s", int(value))\n'%elem[1])
			else:
				f.write('\t\tprint("/dev/%s", int(value))\n'%elem[1])
				f.write('\t\tliboscimp_fpga.add_const_set_offset("/dev/%s", int(round(int(value)/(samp_freq/2**40))))\n'%elem[1])
			f.write('\t\tself.sb_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.%s=value\n'%elem[1])
			if 'f0' not in elem[1]:
				f.write('\t\tprint("/dev/%s", int(value))\n'%elem[1])
				f.write('\t\tliboscimp_fpga.add_const_set_offset("/dev/%s", int(value))\n'%elem[1])
			else:
				f.write('\t\tprint("/dev/%s", value)\n'%elem[1])
				f.write('\t\tliboscimp_fpga.add_const_set_offset("/dev/%s", int(round(float(value)/(samp_freq/2**40))))\n'%elem[1])
			f.write('\t\tself.sd_%s.set_value(int(float(value)))\n\n'%elem[1])

		if elem[0] == 'axi_to_dac':
			f.write('\tdef sd_ch1_%s_changed(self, widget, value):\n'% elem[1])
			f.write('\t\tvals.ch1_%s=value\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_conf_enable("/dev/%s", liboscimp_fpga.BOTH_ALWAYS_HIGH)\n'%elem[1])
			f.write('\t\tprint("/dev/%s ch1", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_set_chan("/dev/%s", liboscimp_fpga.CHANA, int(value))\n'%elem[1])
			f.write('\t\tself.sb_ch1_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_ch1_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.ch1_%s=value\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_conf_enable("/dev/%s", liboscimp_fpga.BOTH_ALWAYS_HIGH)\n'%elem[1])
			f.write('\t\tprint("/dev/%s ch1", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_set_chan("/dev/%s", liboscimp_fpga.CHANA, int(value))\n'%elem[1])
			f.write('\t\tself.sd_ch1_%s.set_value(int(float(value)))\n\n'%elem[1])

			f.write('\tdef sd_ch2_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.ch2_%s=value\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_conf_enable("/dev/%s", liboscimp_fpga.BOTH_ALWAYS_HIGH)\n'%elem[1])
			f.write('\t\tprint("/dev/%s ch2", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_set_chan("/dev/%s", liboscimp_fpga.CHANB, int(value))\n'%elem[1])
			f.write('\t\tself.sb_ch2_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_ch2_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.ch2_%s=value\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_conf_enable("/dev/%s", liboscimp_fpga.BOTH_ALWAYS_HIGH)\n'%elem[1])
			f.write('\t\tprint("/dev/%s ch2", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_set_chan("/dev/%s", liboscimp_fpga.CHANB, int(value))\n'%elem[1])
			f.write('\t\tself.sd_ch2_%s.set_value(int(float(value)))\n\n'%elem[1])

		if elem[0] == 'pidv3_axi':
			f.write('\tdef sd_kp_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.kp_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/kp", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set("/dev/%s", liboscimp_fpga.KP, int(value))\n'%elem[1])
			f.write('\t\tself.sb_kp_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_kp_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.kp_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/kp", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set("/dev/%s", liboscimp_fpga.KP, int(value))\n'%elem[1])
			f.write('\t\tself.sd_kp_%s.set_value(int(float(value)))\n\n'%elem[1])

			f.write('\tdef sd_ki_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.ki_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/ki", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set("/dev/%s", liboscimp_fpga.KI, int(value))\n'%elem[1])
			f.write('\t\tself.sb_ki_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_ki_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.ki_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/ki", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set("/dev/%s", liboscimp_fpga.KI, int(value))\n'%elem[1])
			f.write('\t\tself.sd_ki_%s.set_value(int(float(value)))\n\n'%elem[1])
			f.write('\tdef cb_rst_int_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.rst_int_%s=value\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set_int_rst("/dev/%s", 1)\n'%elem[1])
			f.write('\t\tprint("/dev/%s/rst_int", int(value in (True, "True", "true")))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set_int_rst("/dev/%s", int(value in (True, "True", "true")))\n'%elem[1])
			f.write('\t\tself.cb_rst_int_%s.set_value(int(value in (True, "True", "true")))\n\n'%elem[1])

			f.write('\tdef sd_sp_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.sp_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/setpoint", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set_setpoint("/dev/%s", int(value))\n'%elem[1])
			f.write('\t\tself.sb_sp_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_sp_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.sp_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/setpoint", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set_setpoint("/dev/%s", int(value))\n'%elem[1])
			f.write('\t\tself.sd_sp_%s.set_value(int(float(value)))\n\n'%elem[1])

			f.write('\tdef sd_sign_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.sign_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/sign", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set_sign("/dev/%s", int(value))\n'%elem[1])
			f.write('\t\tself.sb_sign_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_sign_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.sign_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/sign", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set_sign("/dev/%s", int(value))\n'%elem[1])
			f.write('\t\tself.sd_sign_%s.set_value(int(float(value)))\n\n'%elem[1])

		if elem[0] == 'redpitaya_converters_12':

			f.write('\tdef display_extref_state(self):\n')
			f.write('\t\tref_state=liboscimp_fpga.redpitaya_converters_12_get_ref_status("/dev/%s")\n'%elem[1])
			f.write('\t\tif ref_state[1]==1:\n')
			f.write('\t\t\tself.dcolor_extref_state.set_value("#0bff00")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tself.dcolor_extref_state.set_value("#ff0000")\n')
			f.write('\t\tif not self.stop_flag:\n')
			f.write('\t\t\tTimer(0.5, self.display_extref_state).start()\n\n')

			f.write('\tdef listView_acdc1_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_acdc1=self.listView_acdc1.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAC_DC(liboscimp_fpga.CH1 ,int(vals.listView_acdc1=="ADC1 AC"))\n')
			f.write('\t\tif vals.listView_acdc1=="ADC1 AC":\n')
			f.write('\t\t\tprint("ADC1 AC")\n')
			f.write('\t\t\tself.listView_acdc1.select_by_value("ADC1 AC")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("ADC1 DC")\n')
			f.write('\t\t\tself.listView_acdc1.select_by_value("ADC1 DC")\n\n')

			f.write('\tdef listView_range1_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_range1=self.listView_range1.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAttenuator(liboscimp_fpga.CH1 ,int(vals.listView_range1=="ADC1\\xa01/1"))\n')
			f.write('\t\tif vals.listView_range1=="ADC1\\xa01/20":\n')
			f.write('\t\t\tprint("ADC1 1/20")\n')
			f.write('\t\t\tself.listView_range1.select_by_value("ADC1\\xa01/20")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("ADC1 1/1")\n')
			f.write('\t\t\tself.listView_range1.select_by_value("ADC1\\xa01/1")\n\n')

			f.write('\tdef listView_ampl1_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_ampl1=self.listView_ampl1.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.RP_12_setGainOut(liboscimp_fpga.CH1 ,int(vals.listView_ampl1=="DAC1\\xa010V"))\n')
			f.write('\t\tif vals.listView_ampl1=="DAC1\\xa02V":\n')
			f.write('\t\t\tprint("DAC1\\xa02V")\n')
			f.write('\t\t\tself.listView_ampl1.select_by_value("DAC1\\xa02V")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("DAC1\\xa010V")\n')
			f.write('\t\t\tself.listView_ampl1.select_by_value("DAC1\\xa010V")\n\n')

			f.write('\tdef listView_acdc2_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_acdc2=self.listView_acdc2.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAC_DC(liboscimp_fpga.CH2 ,int(vals.listView_acdc2=="ADC2 AC"))\n')
			f.write('\t\tif vals.listView_acdc2=="ADC2 AC":\n')
			f.write('\t\t\tprint("ADC2 AC")\n')
			f.write('\t\t\tself.listView_acdc2.select_by_value("ADC2 AC")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("ADC2 DC")\n')
			f.write('\t\t\tself.listView_acdc2.select_by_value("ADC2 DC")\n\n')

			f.write('\tdef listView_range2_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_range2=self.listView_range2.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAttenuator(liboscimp_fpga.CH2 ,int(vals.listView_range2=="ADC2\\xa01/1"))\n')
			f.write('\t\tif vals.listView_range2=="ADC2\\xa01/20":\n')
			f.write('\t\t\tprint("ADC2 1/20")\n')
			f.write('\t\t\tself.listView_range2.select_by_value("ADC2\\xa01/20")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("ADC2 1/1")\n')
			f.write('\t\t\tself.listView_range2.select_by_value("ADC2\\xa01/1")\n\n')

			f.write('\tdef listView_ampl2_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_ampl2=self.listView_ampl2.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.RP_12_setGainOut(liboscimp_fpga.CH2 ,int(vals.listView_ampl2=="DAC2\\xa010V"))\n')
			f.write('\t\tif vals.listView_ampl2=="DAC2\\xa02V":\n')
			f.write('\t\t\tprint("DAC2\\xa02V")\n')
			f.write('\t\t\tself.listView_ampl2.select_by_value("DAC2\\xa02V")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("DAC2\\xa010V")\n')
			f.write('\t\t\tself.listView_ampl2.select_by_value("DAC2\\xa010V")\n\n')

			f.write('\tdef listView_extref_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_extref=self.listView_extref.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.redpitaya_converters_12_ext_ref_enable("/dev/%s" ,int(vals.listView_extref=="Ext\\xa0Ref"))\n'%elem[1])
			f.write('\t\tif vals.listView_extref=="Ext\\xa0Ref":\n')
			f.write('\t\t\tprint("/dev/%s","Ext\\xa0Ref")\n'%elem[1])
			f.write('\t\t\tself.listView_extref.select_by_value("Ext\\xa0Ref")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("/dev/%s","Int\\xa0Clock")\n'%elem[1])
			f.write('\t\t\tself.listView_extref.select_by_value("Int\\xa0Clock")\n\n')

		if elem[0] in ['shifterReal_dyn', 'shifterComplex_dyn', 'delayTempoReal_axi'] :
			f.write('\tdef sd_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.shifter_set("/dev/%s", int(value))\n'%elem[1])
			f.write('\t\tself.sb_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.shifter_set("/dev/%s", int(value))\n'%elem[1])
			f.write('\t\tself.sd_%s.set_value(int(float(value)))\n\n'%elem[1])

		if elem[0] == 'nco_counter':
			f.write('\tdef sd_pinc_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.pinc_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", samp_freq, float(value), 40, int(self.sb_poff_%s.get_value()), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tliboscimp_fpga.nco_counter_send_conf("/dev/%s", samp_freq, ctypes.c_double(float(value)), 40, int(self.sb_poff_%s.get_value()), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_pinc_%s.set_value(float(value))\n\n'%elem[1])
			f.write('\tdef sb_pinc_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.pinc_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", samp_freq, value, 40, int(self.sb_poff_%s.get_value()), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tliboscimp_fpga.nco_counter_send_conf("/dev/%s", samp_freq, ctypes.c_double(float(value)), 40, int(self.sb_poff_%s.get_value()), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_pinc_%s.set_value(value)\n\n'%elem[1])
			f.write('\tdef sd_poff_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.poff_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", samp_freq, self.sb_pinc_%s.get_value(), 40, int(value), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tliboscimp_fpga.nco_counter_send_conf("/dev/%s", samp_freq, ctypes.c_double(float(self.sb_pinc_%s.get_value())), 40, int(value), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_poff_%s.set_value(value)\n\n'%elem[1])
			f.write('\tdef sb_poff_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.poff_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", samp_freq, self.sb_pinc_%s.get_value(), 40, int(value), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tliboscimp_fpga.nco_counter_send_conf("/dev/%s", samp_freq, ctypes.c_double(float(self.sb_pinc_%s.get_value())), 40, int(value), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_poff_%s.set_value(value)\n\n'%elem[1])
			f.write('\tdef cb_pinc_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.cb_pinc_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", samp_freq, self.sb_pinc_%s.get_value(), 40, int(self.sb_poff_%s.get_value()), int(value in (True, "True", "true")), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tliboscimp_fpga.nco_counter_send_conf("/dev/%s", samp_freq, ctypes.c_double(float(self.sb_pinc_%s.get_value())), 40, int(self.sb_poff_%s.get_value()), int(value in (True, "True", "true")), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_pinc_%s.set_value(int(value in (True, "True", "true")))\n\n'%elem[1])
			f.write('\tdef cb_poff_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.cb_poff_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", samp_freq, self.sb_pinc_%s.get_value(), 40, int(self.sb_poff_%s.get_value()), int(self.cb_pinc_%s.get_value()), int(value in (True, "True", "true")))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tliboscimp_fpga.nco_counter_send_conf("/dev/%s", samp_freq, ctypes.c_double(float(self.sb_pinc_%s.get_value())), 40, int(self.sb_poff_%s.get_value()), int(self.cb_pinc_%s.get_value()), int(value in (True, "True", "true")))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_poff_%s.set_value(int(value in (True, "True", "true")))\n\n'%elem[1])

		if elem[0] in ['switchReal', 'switchComplex'] :
			f.write('\tdef cb_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.%s=value\n'%elem[1])
			f.write('\t\tliboscimp_fpga.switch_send_conf("/dev/%s", 1)\n'%elem[1])
			f.write('\t\tprint("/dev/%s", int(value in (True, "True", "true")))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.switch_send_conf("/dev/%s", int(value in (True, "True", "true")))\n'%elem[1])
			f.write('\t\tself.cb_%s.set_value(int(value in (True, "True", "true")))\n\n'%elem[1])

	if board_name == "plutosdr":
		f.write('start(MyApp, address="0.0.0.0", port=8080, title="%s_webserver")\n'%name)
	else:
		f.write('start(MyApp, address="0.0.0.0", port=80, title="%s_webserver")\n'%name)

	os.chmod('%s_webserver.py'%name, stat.S_IRWXU | stat.S_IRGRP |
		 stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

print('\ndone')
