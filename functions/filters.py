import numpy as np


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