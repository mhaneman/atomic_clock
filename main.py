import time
from hardware_io import Instr
from clock_interface import ClockInterface


# temp imports
import matplotlib.pyplot as plt


''' <--- global variables --> '''
base_freq = 6_834_682_610
# freq_low = base_freq + 7700
# freq_high = base_freq + 8600
freq_low = base_freq + 8150
freq_high = base_freq + 8300


''' <--- initalize devices ---> '''
SR830 = Instr('GPIB0::8::INSTR', 9600)
# SR830.write_and_verify('OUTX', 1)
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
SG386.write_and_verify('MODL', 1) # make sure to turn on the modulation last
SG386.write_and_verify('AMPH', -10)

time.sleep(3)

''' <--- collect data ---> '''
clock_interface = ClockInterface(freq_inst=SG386, intensity_inst=SR830)


start_t = time.time()
res_freqs = []
res_times = []
for n in range(10):
    s = clock_interface.res_freq_scan(
        base_freq=base_freq, 
        freq_low=freq_low, 
        freq_high=freq_high)

    res_freqs.append(s)
    res_times.append(time.time() - start_t) 
    print("finished scan: ", n)


print(res_freqs)

plt.scatter(res_times, res_freqs)
for i in range(len(res_freqs)):
    plt.annotate(res_freqs[i], (res_times[i], res_freqs[i]))

plt.xlabel("ellapsed time [S]")
plt.ylabel("detuning frequency [Hz]")
plt.show()



''' <--- terminate devices ---> '''
SG386.write_and_verify('ENBH', 0) # turn off microwaves at the end of scanning?

