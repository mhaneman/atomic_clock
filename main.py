import time
from hardware_io import Instr
from clock_interface import ClockInterface


''' ~~~~~~~~~~ SETTINGS ~~~~~~~~~~ '''
mock_settings = {
    "MOCK_DIR": "mock_data/",
    "MOCK_FILEPATH": "mock_data/mock_run_1.csv",
    "MOCKING": True, # use data from mock file to simulate experiment
    "MOCK_RAND": False, # if true, a random file from the mock_data directory will be chosen for dat
    "MOCK_SAVE": True # if true, the measured, live scan will be saved as a mock file
}

SR830_setup_config = {
    'SENS': 8,
    'ILIN': 3,
    'RMOD': 1,
    'OFLT': 10,
    'ISRC': 0,
    'ICPL': 0,
    'IGND': 0
}

SR830_term_config = {}

SG386_setup_config = {
    'ENBH': 1,
    'TYPE': 3,
    'SRAT': 10,
    'SFNC': 0,
    'MODL': 1, # configure modulation before being turned on
    'AMPH': -10
}

SG386_term_config = {
    'ENBH': 0
}


''' <--- initalize devices ---> '''
SR830 = Instr(
    resource = 'GPIB0::8::INSTR', 
    baud_rate = 9600, 
    setup_config = SR830_setup_config, 
    term_config = SR830_term_config)

SG386 = Instr(
    resource = 'GPIB0::27::INSTR', 
    baud_rate = 11500, 
    setup_config = SG386_setup_config, 
    term_config = SG386_term_config)


clock_interface = ClockInterface(
    freq_inst=SG386, 
    intensity_inst=SR830, 
    mock_settings = mock_settings)

''' <--- data collection ---> '''
freq_base = 6_834_682_610
freq_low = freq_base + 7700
freq_high = freq_base + 8600
# freq_low = freq_base + 8150
# freq_high = freq_base + 8300

clock_interface.single_scan(
    freq_base=freq_base,
    freq_low=freq_low,
    freq_high=freq_high)


''' <--- terminate devices ---> '''
clock_interface.terminate()

