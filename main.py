import time
from hardware_io import Instr
from clock_interface import ClockInterface
from data_analysis import FreqAnalysis


''' ~~~~~~~~~~ SETTINGS ~~~~~~~~~~ '''
clock_settings = {
    "WARMUP_TIME": 5, # time given for the hardware to warmup
    "MOCK_DIR": "./mock_data/",
    "MOCKING_FILE": "./mock_data/mock_run_1.csv",
    "MOCKING": False, # if true, use data from mock file to simulate experiment
    "MOCK_RAND": False, # if true, a random file from the mock_data directory will be chosen for data
    "MOCK_SAVE": True, # if true, the live scan will be saved as a mock file
}

SR830_setup_commands = {
    'SENS': 8,
    'ILIN': 3,
    'RMOD': 1,
    'OFLT': 10,
    'ISRC': 0,
    'ICPL': 0,
    'IGND': 0
}

SR830_term_commands = {
    
}

SG386_setup_commands = {
    'ENBH': 1,
    'TYPE': 3,
    'SRAT': 10,
    'SFNC': 0,
    'MODL': 1, # configure modulation before being turned on
    'AMPH': -10
}

SG386_term_commands = {
    'ENBH': 0
}


''' <--- initalize devices ---> '''
SR830 = Instr(
    resource = 'GPIB0::8::INSTR', 
    baud_rate = 9600, 
    setup_commands = SR830_setup_commands, 
    term_commands = SR830_term_commands)

SG386 = Instr(
    resource = 'GPIB0::27::INSTR', 
    baud_rate = 11500, 
    setup_commands = SG386_setup_commands, 
    term_commands = SG386_term_commands)


''' <--- data analysis ---> '''
freq_base = 6_834_682_610
detune_low = 7700
detune_high = 8600
# detune_low = 8200
# detune_high = 8300

clock_interface = ClockInterface(
    freq_inst=SG386, 
    intensity_inst=SR830, 
    clock_settings = clock_settings)

freq_analysis = FreqAnalysis(
    interface=clock_interface,
    freq_base=freq_base
)


freq_analysis.cont_scan(
    detune_low=detune_low,
    detune_high=detune_high)


''' <--- terminate devices ---> '''
clock_interface.terminate()

