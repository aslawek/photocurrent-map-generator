import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None

def background_polynomial(data, data_to_fit, poly_order):
    # Fit background:
    polyCoefficients = np.polyfit(data_to_fit['time/s'], data_to_fit['I/mA'], poly_order)
    # add background current
    data['I_bckg/mA'] = np.array([np.sum(np.array([polyCoefficients[len(polyCoefficients) - i - 1] * (j ** i) for i in range(len(polyCoefficients))])) for j in data['time/s']])
    # add resultant current (after background correction)
    data['I_corr/mA'] = data['I/mA'] - data['I_bckg/mA']
    return data

def background_interpolated(data, data_to_fit, interp_points):
    # 1st interpolation
    data_bckg = pd.DataFrame()
    data_bckg['time/s'] = np.linspace(data['time/s'].min(), data['time/s'].max(), num=interp_points)
    data_bckg['I/mA'] = np.interp(data_bckg['time/s'], data_to_fit['time/s'], data_to_fit['I/mA'])

    # 2nd interpolation
    data['I_bckg/mA'] = np.interp(data['time/s'], data_bckg['time/s'], data_bckg['I/mA'])
    data['I_corr/mA'] = data['I/mA'] - data['I_bckg/mA']

    return data