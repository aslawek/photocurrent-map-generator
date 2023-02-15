import numpy as np

def assign_wavelengths(data, list_wavelengths):
    # +1 to wavelength on any positive change in Analog signal (0 -> 1)
    data['wavelength/nm'] = np.floor(data['Analog IN 1/V'].gt(data['Analog IN 1/V'].shift()).cumsum()).astype('int')
    # modulo according to length of list_wavelengths
    data['wavelength/nm'] = ((data['wavelength/nm'] - 1) % len(list_wavelengths)) + 1
    # clear all points with Analog off
    data.loc[(data['Analog IN 1/V'] == 0), 'wavelength/nm'] = 0
    # replace integers with wavelength list items
    for i in range(len(list_wavelengths)):
        data['wavelength/nm'].replace({i+1: list_wavelengths[i]}, inplace=True)
    return data

def filter_by_voltage_value(data, filter_V):
    data_filtered = data.loc[data['control/V'] == filter_V]
    if len(data_filtered) == 0:
        raise TypeError("filter_by_cycles: I filtered to empty dataset, check ranges.")
    else:
        return data_filtered

def filter_by_Analog_borders(data):
    index_min = data.loc[data['Analog IN 1/V'] == 1].idxmin()[0]
    index_max = data.loc[data['Analog IN 1/V'] == 1].idxmax()[0]
    data = data.loc[index_min : index_max]
    return data

def filter_by_Analog_borders_extra(data):
    data = data.loc[data['Analog IN 1/V'] == 0]
    return data

def integer_Analog(data):
    analog_threshold = data.iloc[0]['Analog IN 1/V']
    data['Analog IN 1/V'] = np.rint(np.absolute((data['Analog IN 1/V'] - analog_threshold) / analog_threshold)).astype('int')
    return data