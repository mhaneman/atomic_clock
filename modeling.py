import numpy as np
from scipy.optimize import curve_fit


def find_min_val(x_data, y_data):
    min_y = min(y_data)
    min_y_index = y_data.index(min_y)
    return x_data[min_y_index], min_y

def gauss_func(x, a, x0, sigma, H, r):
        return a * np.exp( -np.absolute(x - x0)**r / (2 * sigma **2) ) + H

def gauss_fit(x_data=[], y_data=[]):
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    
    mean = sum(x_data * y_data) / sum(y_data)
    sigma = np.sqrt(sum(y_data * (x_data - mean) ** 2) / sum(y_data))
    height = 7e-7
    r = 2

    popt, pcov = curve_fit(gauss_func, x_data, y_data, p0=[max(y_data), mean, sigma, height, r])
    ym = gauss_func(x_data, popt[0], popt[1], popt[2], popt[3], popt[4])
    return ym


def lorentzain_func(x, x0, width, height):
     f = (0.5*width) / ((x -x0)**2 + (0.5*width)**2)
     return (1/np.pi) * -f + height


def lorentzain_fit(x_data=[], y_data=[]):
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    
    mean = sum(x_data * y_data) / sum(y_data)
    sigma = np.sqrt(sum(y_data * (x_data - mean) ** 2) / sum(y_data))
    height = 7e-7

    popt, pcov = curve_fit(lorentzain_func, x_data, y_data, p0=[max(y_data), mean, height])
    ym = lorentzain_func(x_data, popt[0], popt[1], popt[2])
    return ym