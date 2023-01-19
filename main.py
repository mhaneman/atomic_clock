from hardware_io import Instr
from data_collection import DataCollection


''' <--- global variables --> '''
base_freq = 6_834_682_610
# freq_low = base_freq + 7700
# freq_high = base_freq + 8600

freq_low = base_freq + 7900
freq_high = base_freq + 8300


''' <--- initalize devices ---> '''
SR830 = Instr('GPIB0::8::INSTR', 9600)
SR830.query('*IDN?')
SR830.write_and_verify('SENS', 8)
SR830.write_and_verify('ILIN', 3)
SR830.write_and_verify('RMOD', 1)
SR830.write_and_verify('OFLT', 10)
SR830.write_and_verify('ISRC', 0)
SR830.write_and_verify('ICPL', 0)
SR830.write_and_verify('IGND', 0)

SG386 = Instr('GPIB0::27::INSTR', 11500)
SG386.query('*IDN?')
SG386.write_and_verify('TYPE', 3)
SG386.write_and_verify('SRAT', 10)
SG386.write_and_verify('SFNC', 0)
SG386.write_and_verify('MODL', 1)
SG386.write_and_verify('AMPH', -10)
SG386.write_and_verify('ENBH', 1)

''' <--- collect data ---> '''
clock_interface = DataCollection(freq_inst=SG386, intensity_inst=SR830)
res_freq = clock_interface.res_freq_scan(
    base_freq=base_freq, 
    freq_low=freq_low, 
    freq_high=freq_high)

print("detuning freq resonance", res_freq)

''' <--- terminate devices ---> '''
SG386.write_and_verify('ENBH', 0) # turn off microwaves at the end of scanning?

