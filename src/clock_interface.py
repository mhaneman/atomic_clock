import time
from tqdm import tqdm
import file_io

class ClockInterface:
    def __init__(self, freq_inst, intensity_inst, clock_settings):
        self.freq_inst = freq_inst
        self.intensity_inst = intensity_inst
        
        self.is_mocking = clock_settings["MOCKING"]
        self.is_mock_save = clock_settings["MOCK_SAVE"]
        self.is_mock_rand = clock_settings["MOCK_RAND"]
        self.mock_filepath = clock_settings["MOCKING_FILE"]
        self.mock_dir = clock_settings["MOCK_DIR"]
        self.warmup_time = clock_settings["WARMUP_TIME"]
        self.setup()
    
    """ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """

    # setup instruments, if needed
    def setup(self):
        if not self.is_mocking:
            self.freq_inst.setup_config()
            self.intensity_inst.setup_config()
            time.sleep(self.warmup_time)

    # terminate instruments, if needed
    def terminate(self):
        if not self.is_mocking:
            self.freq_inst.term_config()
            self.intensity_inst.term_config()

    """ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """

    # wrapper for getting data (mocking or live)
    def get_data(self, freq_base, freq_low, freq_high):
        if self.is_mocking:
            if self.is_mock_rand:
                file = self.mock_dir + file_io.get_random_file(self.mock_dir)
                return self.get_mocking_data(file, freq_base, freq_low, freq_high)
            return self.get_mocking_data(self.mock_filepath, freq_base, freq_low, freq_high)
        
        x_data, y_data = self.get_live_data(freq_base, freq_low, freq_high)
        if self.is_mock_save:
            file_io.save_data_csv(dir=self.mock_dir, x_data=x_data, y_data=y_data)
        return x_data, y_data


    # use sample data saved locally
    def get_mocking_data(self, file, freq_base, freq_low, freq_high):
        x_data, y_data = file_io.read_data_csv(file)
        low = x_data.index(freq_low - freq_base)
        high = x_data.index(freq_high - freq_base)
        return x_data[low:high], y_data[low:high]


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


    def get_live_data_at(self, freq):
        self.freq_inst.write('FREQ', freq)
        measured_intensity = self.intensity_inst.query('OUTP?3')
        return float(measured_intensity)