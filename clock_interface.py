import time
from tqdm import tqdm

from plotting import PlotObject
import modeling
import file_io

class ClockInterface:
    def __init__(self, freq_inst, intensity_inst, mock_settings):
        self.freq_inst = freq_inst
        self.intensity_inst = intensity_inst
        
        self.is_mocking = mock_settings["MOCKING"]
        self.is_mock_save = mock_settings["MOCK_SAVE"]
        self.mock_filepath = mock_settings["MOCK_FILEPATH"]
        self.mock_dir = mock_settings["MOCK_DIR"]
        self.setup()


    # setup instruments, if needed
    def setup(self):
        if not self.is_mocking:
            if self.freq_inst.instr is not None:
                self.freq_inst.setup_config()
            if self.intensity_inst.instr is not None:
                self.intensity_inst.setup_config()
            time.sleep(3)

    # terminate instruments, if needed
    def terminate(self):
        if not self.is_mocking:
            if self.freq_inst.instr is not None:
                self.freq_inst.term_config()
            if self.intensity_inst.instr is not None:
                self.intensity_inst.term_config()


    # use sample data saved locally
    def get_mocking_data(self, freq_base, freq_low, freq_high):
        x_data, y_data = file_io.read_data_csv(self.mock_filepath)
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


    # wrapper for getting data (mocking or live)
    def get_data(self, freq_base, freq_low, freq_high):
        if self.is_mocking:
            return self.get_mocking_data(freq_base, freq_low, freq_high)
        
        # maybe do some error checking here
        x_data, y_data = self.get_live_data(freq_base, freq_low, freq_high)
        if self.is_mock_save:
            file_io.save_data_csv(dir=self.mock_dir, x_data=x_data, y_data=y_data)
        return x_data, y_data


    # return information about scanned data
    def single_scan(self, freq_base, freq_low, freq_high):
        freq_data, intensity_data = self.get_data(freq_base, freq_low, freq_high)

        fit_y = modeling.gauss_fit(
            x_data=freq_data,
            y_data=intensity_data)

        scan_plot = PlotObject(x_label="detune freq [Hz]", y_label="Intensity")
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

        for _ in tqdm(range(10), desc="scanning..."):
            scan = self.single_scan(
                freq_base=freq_base, 
                freq_low=freq_low, 
                freq_high=freq_high)

            res_freqs.append(scan)
            res_times.append(time.time() - start_t) 

        plot = PlotObject(
            x_label="ellapsed time [S]",
            y_label="detuning frequency [Hz]",
            show_annotate=True)

        plot.plot_points(res_times, res_freqs)