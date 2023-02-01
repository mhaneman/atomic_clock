import time
from tqdm import tqdm

from plots import PlotObject
import modeling

class ClockInterface:
    def __init__(self, freq_inst, intensity_inst, is_mocking, mocking_file_path):
        self.freq_inst = freq_inst
        self.intensity_inst = intensity_inst
        self.is_mocking = is_mocking
        self.mocking_file_path = mocking_file_path

    # use sample data saved locally
    def get_mocking_data(self, freq_low, freq_high):
        x_data = []
        y_data = []
        with open(self.mocking_file_path, 'r') as file:
            pass

        return x_data, y_data

    # use clock hardware to get data
    def get_live_data(self, freq_base, freq_low, freq_high):
        freq_data = []
        intensity_data = []
    
        for f in tqdm(range(freq_low, freq_high, 1), desc="scanning clock..."):
            self.freq_inst.write('FREQ', f)
            measured_intensity = self.intensity_inst.query('OUTP?3')
            freq_data.append(f - freq_base)
            intensity_data.append(float(measured_intensity))

        return freq_data, intensity_data


    # wrapper for getting data
    def get_data(self, freq_base, freq_low, freq_high):
        if self.is_mocking:
            return self.get_mocking_data(freq_low, freq_high)
        return self.get_live_data(freq_base, freq_low, freq_high)


    # return information about scanned data
    def single_scan(self, freq_base, freq_low, freq_high):
        freq_data, intensity_data = self.get_data(freq_base, freq_low, freq_high)

        fit_y = modeling.gauss_fit(
            x_data=freq_data,
            y_data=intensity_data)

        scan_plot = PlotObject(
            x_label="detune freq [Hz]", 
            y_label="Intensity")
        scan_plot.plot_line(x_data=freq_data, y_data=intensity_data, label="measured")
        scan_plot.plot_line(x_data=freq_data, y_data=fit_y, label="guass fit")
        scan_plot.show_plot()

        res_freq, res_intensity = modeling.find_min_val(freq_data[2:], intensity_data[2:])
        print("res freq found: ", res_freq)
        return res_freq


    # continous scanning of clock
    def cont_res_freq_scan(self, freq_base, freq_low, freq_high):
        start_t = time.time()
        res_freqs = []
        res_times = []

        for n in tqdm(range(10), desc="scanning..."):
            scan = self.single_scan(
                freq_base=freq_base, 
                freq_low=freq_low, 
                freq_high=freq_high)

            res_freqs.append(scan)
            res_times.append(time.time() - start_t) 

        cont_scan_plot = PlotObject(
            x_label="ellapsed time [S]",
            y_label="detuning frequency [Hz]",
            show_annotate=True)

        cont_scan_plot.plot_points(res_times, res_freqs)