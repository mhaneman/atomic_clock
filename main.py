import time
from hardware_io import Instr
from clock_interface import ClockInterface


''' ~~~~~~~~~~ GLOBAL SETTINGS ~~~~~~~~~~ '''
MOCKING_FILE_PATH = "mock_data/sample_run.txt"
MOCKING = False  # use data from mock file to simulate experiment


''' ~~~~~~~~~~ EXPERIMENT VARIABLES  ~~~~~~~~~~ '''

freq_base = 6_834_682_610
# freq_low = base_freq + 7700
# freq_high = base_freq + 8600
freq_low = freq_base + 8150
freq_high = freq_base + 8300


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
    is_mocking = MOCKING,
    mocking_file_path = MOCKING_FILE_PATH)

time.sleep(3)

clock_interface.single_scan(
    freq_base=freq_base,
    freq_low=freq_low,
    freq_high=freq_high)


''' <--- terminate devices ---> '''
SG386.write_and_verify('ENBH', 0) # turn off microwaves at the end of scanning?

