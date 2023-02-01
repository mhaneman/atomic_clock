import time
from hardware_io import Instr
from clock_interface import ClockInterface
from data_analysis import DataAnalysis


''' ~~~~~~~~~~ SETTINGS ~~~~~~~~~~ '''
mock_settings = {
    "MOCK_DIR": "../mock_data/",
    "MOCK_FILEPATH": "../mock_data/mock_run_1.csv",
    "MOCK_RAND": False, # if true, a random file from the mock_data directory will be chosen for data
    "MOCK_SAVE": True, # if true, the live scan will be saved as a mock file
    "MOCKING": True, # use data from mock file to simulate experiment
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


''' <--- data analysis ---> '''
detune_low = 7700
detune_high = 8600

data_analysis = DataAnalysis(
    interface = clock_interface,
    freq_base = 6_834_682_610
)

data_analysis.single_scan(
    detune_low=detune_low,
    detune_high=detune_high)

data_analysis.cont_scan(
    detune_low=detune_low,
    detune_high=detune_high)


''' <--- terminate devices ---> '''
clock_interface.terminate()

