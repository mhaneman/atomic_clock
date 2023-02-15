from graphics import DashboardGUI
from data_analysis import FreqAnalysis



class Dashboard:
    def __init__(self, clock_interface) -> None:
        self.freq_analysis = FreqAnalysis(
            interface = clock_interface,
            freq_base = 6_834_682_610
        )