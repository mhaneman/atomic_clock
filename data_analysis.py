from tqdm import tqdm
import time

from graphics import PlotObject
import modeling


class FreqAnalysis:
    def __init__(self, interface, freq_base) -> None:
        self.interface = interface
        self.freq_base = freq_base

    # return information about scanned data
    def single_scan(self, detune_low, detune_high):
        freq_data, intensity_data = self.interface.get_data(
            self.freq_base, 
            detune_low + self.freq_base, 
            detune_high + self.freq_base)

        # fit_y = modeling.lorentzain_fit(
        #     x_data=freq_data,
        #     y_data=intensity_data)

        # scan_plot = PlotObject(x_label="detune freq [Hz]", y_label="Intensity")
        # scan_plot.plot_line(x_data=freq_data, y_data=intensity_data, label="measured")
        # scan_plot.plot_line(x_data=freq_data, y_data=fit_y, label="modified guass fit")
        # scan_plot.show_plot()

        # res_freq, res_intensity = modeling.find_min_val(freq_data[2:], intensity_data[2:])
        # return res_freq

        return None


    # continous scanning of clock
    def cont_scan(self, detune_low, detune_high):
        start_t = time.time()
        res_freqs = []
        res_times = []

        for _ in tqdm(range(100), desc="scanning..."):
            scan = self.single_scan(
                detune_low=detune_low, 
                detune_high=detune_high)

            res_freqs.append(scan)
            res_times.append(time.time() - start_t) 

        # plot = PlotObject(
        #     x_label="ellapsed time [S]",
        #     y_label="detuning frequency [Hz]",
        #     show_annotate=True)

        # plot.plot_points(res_times, res_freqs)
        # plot.show_plot()