import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('Qt5Agg'); #mpl.use('TkAgg')
from functions.load_from_mpt import load_from_mpt_with_Analog
from functions.filters import filter_by_voltage_value, integer_Analog, filter_by_Analog_borders, filter_by_Analog_borders_extra, assign_wavelengths
from functions.backgrounders import background_polynomial, background_interpolated, background_poly_roll
from functions.plotter_CA import plotter_CA_with_Analog, plotter_CA_with_Analog_and_bckg, plotter_CA_with_wavelengths, plotter_I_vs_wavelength, plotter_map
from functions.plotter_CA import plotter_CA_with_bckg

filename = './data/ITO_Zn_PzPz_Ar_map_-1.8V_+1V_0.2V_02_CA_C01.mpt'
list_wavelengths = [320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600]

# load data with Analog signals
data = load_from_mpt_with_Analog(filename)
# save control/V as float16
data['control/V'] = data['control/V'].astype('float16')
# modify Analog signal to integer (0 - dark, 1 - light)
data = integer_Analog(data)
# assign wavelengths to the cycles
data_filtered = assign_wavelengths(data, list_wavelengths)

# Method of background correction
polynomial = False  # - type polynomial order or leave False
interpolate = False # - type True if you want some linear interpolation magic :)
poly_roll = True    # - type True if you want MORE linear interpolation magic :)

data_with_bckg = pd.DataFrame()
map = pd.DataFrame()

for voltage in data['control/V'].unique():
    # map for particular potential
    mapie = pd.DataFrame()
    if voltage < -1.7:
        continue
    if voltage > 0.7:
        break
    # Filter data with unique voltage:
    print(f'Working on voltage {voltage} ...')
    data_filtered = filter_by_voltage_value(data, voltage)

    # Doing the background
    if polynomial != False:
        # Filter data to fit
        data_to_fit = filter_by_Analog_borders(data_filtered)
        data_filtered = background_polynomial(data_filtered, data_to_fit, polynomial)
        # Plot!
        plotter_CA_with_bckg(data_filtered, data_to_fit, filename, voltage)

    if interpolate == True:
        # Filter data to fit
        data_to_fit = filter_by_Analog_borders_extra(data_filtered)
        data_filtered = background_interpolated(data_filtered, data_to_fit, interp_points=1000000)
        # Plot!
        plotter_CA_with_bckg(data_filtered, data_to_fit, filename, voltage)

    if poly_roll == True:
        data_filtered, data_to_fit, mapie = background_poly_roll(data_filtered, list_wavelengths, voltage, poly_order=3, n_pts_fit=225, n_pts_retention=10)
        #plotter_CA_with_bckg(data_filtered, data_to_fit, filename, voltage)
        #plotter_I_vs_wavelength(mapie, filename, voltage)
        mapie = mapie

    map = map.append(mapie, ignore_index=True)

print('Our map:')
print(map)

plotter_map(map, filename)

#plotter_CA_with_Analog_and_bckg(data_with_bckg, filename)
#plotter_CA_with_Analog(data_with_bckg, filename)
#plotter_CA_with_Analog(data, filename)
plotter_CA_with_wavelengths(data, filename)