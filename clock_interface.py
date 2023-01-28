import plots
import time

class ClockInterface:
    def __init__(self, freq_inst, intensity_inst):
        self.freq_inst = freq_inst
        self.intensity_inst = intensity_inst

    def get_res_freq(self, intensity_data, freq_data):
        min_intensity = min(intensity_data)
        min_intensity_index = intensity_data.index(min_intensity)
        return freq_data[min_intensity_index]

    def res_freq_scan(self, base_freq, freq_low, freq_high):
        freq_data = []
        intensity_data = []

        for f in range(freq_low, freq_high, 1):
            self.freq_inst.write('FREQ', f)
            intensity = self.intensity_inst.query('OUTP?3')
            freq_data.append(f - base_freq)
            intensity_data.append(float(intensity))
            # print(f - base_freq, float(intensity))

        # plots.plot_points(x_data=freq_data, y_data=intensity_data)
        return self.get_res_freq(intensity_data[2:], freq_data[2:])
