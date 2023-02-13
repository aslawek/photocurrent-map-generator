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

def background_poly_roll(data, list_wavelengths, poly_order, n_pts_fit, n_pts_retention):
    data['I_bckg/mA'] = np.NaN
    data['I_corr/mA'] = np.NaN
    data_to_fit = pd.DataFrame()
    # Fit backgrounds:
    for wavelength in list_wavelengths:
        # Index where peak starts and ends, Indexes for fit ranges
        index_min = data.loc[data['wavelength'] == wavelength].idxmin()[0]
        index_max = data.loc[data['wavelength'] == wavelength].idxmax()[0]
        i1 = index_min - n_pts_retention - n_pts_fit
        i2 = index_min - n_pts_retention
        i3 = index_max + n_pts_retention + 1
        i4 = index_max + n_pts_retention + n_pts_fit + 1
        # Select two ranges of bckg data (before and after peak), including number of points and retention
        data_to_fit_wavelength = data.loc[np.r_[i1 : i2, i3 : i4], :]
        poly_coeffs = np.polyfit(data_to_fit_wavelength['time/s'], data_to_fit_wavelength['I/mA'], poly_order)

        #data['I_bckg/mA'] = np.array([np.sum(np.array([poly_coeffs[len(poly_coeffs) - i - 1] * (j ** i) for i in range(len(poly_coeffs))])) for j in data['time/s']])
        data['I_bckg/mA'].loc[i1:i4] = np.array([np.sum(np.array([poly_coeffs[len(poly_coeffs) - i - 1] * (j ** i) for i in range(len(poly_coeffs))])) for j in data['time/s'].loc[i1:i4]])
        # add resultant current (after background correction)
        data['I_corr/mA'].loc[i1:i4] = data['I/mA'] - data['I_bckg/mA']
        data_to_fit = pd.concat([data_to_fit, data_to_fit_wavelength])

    # add background current

    return [data, data_to_fit]