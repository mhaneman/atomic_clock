import plots
import time
''' <--- data collection ---> '''
"""
async def calibrate():
    with open('test.csv', 'w', newline='') as csvfile:
        data = csv.writer(csvfile, delimiter=' ')

        for f in range(freq_low, freq_high):
            SR830.write('FREQ', f)
            await asyncio.sleep(0)
            intensity = SR830.query('OUTP?3')
            # data.writerow(["frequency: " + str(f), "instensity: " + str(float(intensity))])
            x_data.append(f)
            y_data.append(float(intensity))

asyncio.run(calibrate())
"""

def basic_scan(SG386, SR830, base_freq, freq_low, freq_high):
    time.sleep(10) # let the machine prepare?
    x_data = []
    y_data = []
    for f in range(freq_low, freq_high, 1):
        SG386.write('FREQ', f)
        time.sleep(0) # allow atoms to settle to freq? 
        intensity = SR830.query('OUTP?3')
        x_data.append(f - base_freq)
        y_data.append(float(intensity))
        print(f - base_freq, float(intensity))

    plots.plot_points(x_data=x_data, y_data=y_data) 