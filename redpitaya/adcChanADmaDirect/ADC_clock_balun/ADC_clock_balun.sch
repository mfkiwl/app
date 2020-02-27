EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:C C1
U 1 1 5E56A802
P 4050 3350
F 0 "C1" V 3798 3350 50  0000 C CNN
F 1 "100n" V 3889 3350 50  0000 C CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 4088 3200 50  0001 C CNN
F 3 "~" H 4050 3350 50  0001 C CNN
	1    4050 3350
	0    1    1    0   
$EndComp
$Comp
L Device:C C2
U 1 1 5E56B600
P 4100 3750
F 0 "C2" V 3848 3750 50  0000 C CNN
F 1 "100n" V 3939 3750 50  0000 C CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 4138 3600 50  0001 C CNN
F 3 "~" H 4100 3750 50  0001 C CNN
	1    4100 3750
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_Coaxial J1
U 1 1 5E56BDFF
P 3650 3700
F 0 "J1" H 3750 3675 50  0000 L CNN
F 1 "Conn_Coaxial" H 3750 3584 50  0000 L CNN
F 2 "Connector_Coaxial:SMA_Molex_73251-1153_EdgeMount_Horizontal" H 3650 3700 50  0001 C CNN
F 3 " ~" H 3650 3700 50  0001 C CNN
	1    3650 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 3350 3450 3350
Wire Wire Line
	3450 3350 3450 3700
$Comp
L power:GND #PWR0101
U 1 1 5E56D368
P 3650 4000
F 0 "#PWR0101" H 3650 3750 50  0001 C CNN
F 1 "GND" H 3655 3827 50  0000 C CNN
F 2 "" H 3650 4000 50  0001 C CNN
F 3 "" H 3650 4000 50  0001 C CNN
	1    3650 4000
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5E56D9D5
P 3950 4000
F 0 "#PWR0102" H 3950 3750 50  0001 C CNN
F 1 "GND" H 3955 3827 50  0000 C CNN
F 2 "" H 3950 4000 50  0001 C CNN
F 3 "" H 3950 4000 50  0001 C CNN
	1    3950 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 4000 3950 3750
Wire Wire Line
	3650 4000 3650 3900
$Comp
L Device:R R1
U 1 1 5E56F4F8
P 5550 3400
F 0 "R1" H 5480 3354 50  0000 R CNN
F 1 "50" H 5480 3445 50  0000 R CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 5480 3400 50  0001 C CNN
F 3 "~" H 5550 3400 50  0001 C CNN
	1    5550 3400
	-1   0    0    1   
$EndComp
$Comp
L Device:R R2
U 1 1 5E5700A5
P 5550 3750
F 0 "R2" H 5480 3704 50  0000 R CNN
F 1 "50" H 5480 3795 50  0000 R CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 5480 3750 50  0001 C CNN
F 3 "~" H 5550 3750 50  0001 C CNN
	1    5550 3750
	-1   0    0    1   
$EndComp
$Comp
L Device:R R3
U 1 1 5E570403
P 6100 3600
F 0 "R3" H 6030 3554 50  0000 R CNN
F 1 "100" H 6030 3645 50  0000 R CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 6030 3600 50  0001 C CNN
F 3 "~" H 6100 3600 50  0001 C CNN
	1    6100 3600
	-1   0    0    1   
$EndComp
Wire Wire Line
	6100 3450 6100 3250
Wire Wire Line
	6100 3250 5550 3250
Wire Wire Line
	6100 3750 6100 3900
Wire Wire Line
	6100 3900 5550 3900
Wire Wire Line
	5550 3600 5550 3550
$Comp
L Device:C C3
U 1 1 5E570DE7
P 5900 4150
F 0 "C3" H 5785 4104 50  0000 R CNN
F 1 "100n" H 5785 4195 50  0000 R CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 5938 4000 50  0001 C CNN
F 3 "~" H 5900 4150 50  0001 C CNN
	1    5900 4150
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 5E57126A
P 5900 4400
F 0 "#PWR0103" H 5900 4150 50  0001 C CNN
F 1 "GND" H 5905 4227 50  0000 C CNN
F 2 "" H 5900 4400 50  0001 C CNN
F 3 "" H 5900 4400 50  0001 C CNN
	1    5900 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	5900 4400 5900 4300
Wire Wire Line
	5550 3550 5900 3550
Wire Wire Line
	5900 3550 5900 4000
Connection ~ 5550 3550
Wire Wire Line
	6100 3250 6400 3250
Connection ~ 6100 3250
Wire Wire Line
	6100 3900 6350 3900
Connection ~ 6100 3900
$Comp
L power:GND #PWR0104
U 1 1 5E572A78
P 6950 3900
F 0 "#PWR0104" H 6950 3650 50  0001 C CNN
F 1 "GND" H 6955 3727 50  0000 C CNN
F 2 "" H 6950 3900 50  0001 C CNN
F 3 "" H 6950 3900 50  0001 C CNN
	1    6950 3900
	1    0    0    -1  
$EndComp
Connection ~ 5550 3250
Connection ~ 5550 3900
$Comp
L minicircuits:T1-1T-X65 T1
U 1 1 5E57379F
P 4850 3550
F 0 "T1" H 4850 3990 50  0000 C CNN
F 1 "TC1-1-13M+ balun" H 4850 3899 50  0000 C CNN
F 2 "minicircuits:AT224-1A" H 4850 3550 60  0001 C CNN
F 3 "" H 4850 3550 60  0000 C CNN
	1    4850 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	4200 3350 4450 3350
Wire Wire Line
	4450 3750 4250 3750
Wire Wire Line
	5250 3750 5250 3900
Wire Wire Line
	5250 3900 5550 3900
Wire Wire Line
	5250 3350 5250 3250
Wire Wire Line
	5250 3250 5550 3250
NoConn ~ 5250 3550
Wire Wire Line
	6450 3750 6450 3850
$Comp
L Connector_Generic:Conn_02x03_Counter_Clockwise J2
U 1 1 5E579342
P 6750 3650
F 0 "J2" H 6800 3325 50  0000 C CNN
F 1 "Conn_02x03_Counter_Clockwise" H 6800 3416 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical" H 6750 3650 50  0001 C CNN
F 3 "~" H 6750 3650 50  0001 C CNN
	1    6750 3650
	-1   0    0    1   
$EndComp
Wire Wire Line
	6450 3550 6400 3550
Wire Wire Line
	6400 3550 6400 3250
Wire Wire Line
	6450 3850 6950 3850
Wire Wire Line
	6950 3850 6950 3750
Wire Wire Line
	6950 3750 6950 3650
Connection ~ 6950 3750
Wire Wire Line
	6950 3900 6950 3850
Connection ~ 6950 3850
Wire Wire Line
	6950 3550 7150 3550
Wire Wire Line
	7150 3550 7150 4100
Wire Wire Line
	7150 4100 6350 4100
Wire Wire Line
	6350 4100 6350 3900
Wire Wire Line
	6450 3650 6450 3750
Connection ~ 6450 3750
$EndSCHEMATC
