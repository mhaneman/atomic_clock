import numpy as np
from scipy.optimize import curve_fit


def find_min_val(x_data, y_data):
    min_y = min(y_data)
    min_y_index = y_data.index(min_y)
    return x_data[min_y_index], min_y


def gauss_fit(x_data=[], y_data=[]):
    def gauss_func(x, a, x0, sigma):
        return a*np.exp((x-x0)**2/(2*sigma**2))

    popt, pcov = curve_fit(gauss_func, x_data, y_data)
    ym = gauss_func(x_data, popt[0], popt[1], popt[2])
    return ym