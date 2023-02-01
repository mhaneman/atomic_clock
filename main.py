import time
from hardware_io import Instr
from clock_interface import ClockInterface


''' ~~~~~~~~~~ SETTINGS ~~~~~~~~~~ '''
mock_settings = {
    "MOCK_DIR": "mock_data/",
    "MOCK_FILEPATH": "mock_data/mock_run_1.csv",
    "MOCKING": False, # use data from mock file to simulate experiment
    "MOCK_RAND": False, # if true, a random file from the mock_data directory will be chosen for dat
    "MOCK_SAVE": True # if true, the measured, live scan will be saved as a mock file
}

SR830_settings = {
    'SENS': 8,
    'ILIN': 3,
    'RMOD': 1,
    'OFLT': 10,
    'ISRC': 0,
    'ICPL': 0,
    'IGND': 0
}

SG386_settings = {
    'ENBH': 1,
    'TYPE': 3,
    'SRAT': 10,
    'SFNC': 0,
    'MODL': 1, # configure modulation before being turned on
    'AMPH': -10
}


''' ~~~~~~~~~~ EXPERIMENT VARIABLES  ~~~~~~~~~~ '''
freq_base = 6_834_682_610
freq_low = freq_base + 7700
freq_high = freq_base + 8600
# freq_low = freq_base + 8150
# freq_high = freq_base + 8300


''' <--- initalize devices ---> '''
SR830 = Instr('GPIB0::8::INSTR', 9600)
# SR830.query_and_print('*IDN?')
SR830.write_and_verify('SENS', 8)
SR830.write_and_verify('ILIN', 3)
SR830.write_and_verify('RMOD', 1)
SR830.write_and_verify('OFLT', 10)
SR830.write_and_verify('ISRC', 0)
SR830.write_and_verify('ICPL', 0)
SR830.write_and_verify('IGND', 0)

SG386 = Instr('GPIB0::27::INSTR', 11500)
# SG386.query_and_print('*IDN?')
SG386.write_and_verify('ENBH', 1)
SG386.write_and_verify('TYPE', 3)
SG386.write_and_verify('SRAT', 10)
SG386.write_and_verify('SFNC', 0)
SG386.write_and_verify('MODL', 1) # configure modulation before turned on
SG386.write_and_verify('AMPH', -10)


''' <--- data collection ---> '''
clock_interface = ClockInterface(
    freq_inst=SG386, 
    intensity_inst=SR830, 
    mock_settings = mock_settings)

time.sleep(3)

clock_interface.single_scan(
    freq_base=freq_base,
    freq_low=freq_low,
    freq_high=freq_high)


''' <--- terminate devices ---> '''
SG386.write_and_verify('ENBH', 0) # turn off microwaves at the end of scanning?

