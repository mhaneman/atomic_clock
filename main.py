from hardware_io import Instr
import data_collection


''' <--- global variables --> '''
base_freq = 6_834_682_610
freq_low = base_freq + 7700
freq_high = base_freq + 8600



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
# this is ugly! -> refactor this
data_collection.basic_scan(
    SG386=SG386, SR830=SR830, 
    base_freq=base_freq, 
    freq_low=freq_low, 
    freq_high=freq_high)

''' <--- terminate devices ---> '''
SG386.write_and_verify('ENBH', 0) # turn off microwaves at the end of scanning?

