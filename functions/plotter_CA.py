import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
mpl.use('Qt5Agg'); #mpl.use('TkAgg')

def plotter_CA_with_Analog(data, filename):
    ax1 = plt.figure().add_subplot()
    ax2 = ax1.twinx()
    # a lines so ax1 is on top of ax2:
    ax1.set_zorder(ax2.get_zorder() + 1); ax1.set_frame_on(False)
    ax1.plot(data['time/s'], data['I/mA'], color="red", zorder=3)
    ax2.plot(data['time/s'], data['control/V'], color="blue", zorder=2)
    ax2.plot(data['time/s'], data['Analog IN 1/V'], color="green", zorder=1)
    ax1.set_title(filename.replace("/", " ").split()[-1])
    ax1.set_xlabel("time / s", fontsize=12)
    ax1.set_ylabel("I / mA", fontsize=12)
    ax2.set_ylabel("Analog IN 1 / control / V", fontsize=12)
    #ax1.legend()

def plotter_CA_with_wavelengths(data, filename):
    ax1 = plt.figure().add_subplot()
    ax2 = ax1.twinx()
    # a lines so ax1 is on top of ax2:
    ax1.set_zorder(ax2.get_zorder() + 1); ax1.set_frame_on(False)
    ax1.plot(data['time/s'], data['I/mA'], color="red", zorder=3, label="current")
    ax2.plot(data['time/s'], data['control/V'], color="blue", zorder=2, label="potential")
    ax2.plot(data['time/s'], data['wavelength'] / data['wavelength'].max(), color="black", zorder=1, label=f"wavelength / {data['wavelength'].max()}")
    #ax2.plot(data['time/s'], data['Analog IN 1/V'], color="green", zorder=1)
    ax1.set_title(filename.replace("/", " ").split()[-1])
    ax1.set_xlabel("time / s", fontsize=12)
    ax1.set_ylabel("I / mA", fontsize=12)
    ax2.set_ylabel("Wavelength / nm", fontsize=12)
    ax1.legend()
    ax2.legend()

def plotter_CA_with_Analog_and_bckg(data, filename):
    ax1 = plt.figure().add_subplot()
    ax2 = ax1.twinx()
    ax1.plot(data['time/s'], data['I/mA'], color="grey", label='raw data')
    ax1.plot(data['time/s'], data['I_bckg/mA'], color="red", label='background')
    ax1.plot(data['time/s'], data['I_corr/mA'], color="blue", label='bckg corrected')
    ax2.plot(data['time/s'], data['control/V'], color="blue")
    ax2.plot(data['time/s'], data['Analog IN 1/V'], color="green")
    ax1.set_title(filename.replace("/", " ").split()[-1])
    ax1.set_xlabel("time / s", fontsize=12)
    ax1.set_ylabel("I / mA", fontsize=12)
    ax2.set_ylabel("Analog IN 1 / control / V", fontsize=12)
    #ax1.legend()

def plotter_CA_with_bckg(data, data_to_fit, filename, voltage):
    ax1 = plt.figure().add_subplot()
    ax2 = ax1.twinx()
    ax1.plot(data['time/s'], data['I/mA'], color="grey", label='raw data')
    ax1.plot(data_to_fit['time/s'], data_to_fit['I/mA'], color="black", label='fitted data')
    ax1.plot(data['time/s'], data['I_bckg/mA'], color="red", label='background')
    ax1.plot(data['time/s'], data['I_corr/mA'], color="blue", label='bckg corrected')
    ax2.plot(data['time/s'], data['Analog IN 1/V'], color="green")
    ax1.set_title(f'{filename.replace("/", " ").split()[-1]}, voltage: {voltage}')
    ax1.set_xlabel("time / s", fontsize=12)
    ax1.set_ylabel("I / mA", fontsize=12)
    ax2.set_ylabel("Analog IN 1 / control / V", fontsize=12)
    ax1.legend()
    plt.show()