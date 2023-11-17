import matplotlib.pyplot as plt
import numpy as np
from math import atan2, degrees
import h5py
import os

os.chdir('C:/Users/KWILKES/Desktop/PFAS_Modeling/pseudo_PFR')
# Initialization function to load data
def init():
    global cantera_species, sol, columns, tplot, Tplot, color_dict, species_to_plot, concentrations_glob
    with h5py.File('sol.hdf5', 'r') as f:
        cantera_species = f['column_names'][:].tolist()
        sol = f['data'][:]

    columns = ['Residence Time (seconds)', 'Temperature (K)'] + cantera_species
    columns = [col.decode('utf-8') if isinstance(col, bytes) else col for col in columns]
    cantera_species = [species.decode('utf-8') for species in cantera_species]

    tplot = sol[:, 0]
    Tplot = sol[:, 1]

    species_to_plot = ['H', 'CL', 'CCL4','HCL','CLO','CCLO','CL2']
    concentrations_glob = {species: sol[:, columns.index(species)] for species in species_to_plot}
    color_dict = {'H': 'black', 'CL': 'blue', 'CCL4': 'green', 'HCL': 'red', 'CLO': 'cyan', 'CCLO': 'magenta', 'CL2': 'yellow'}

# Function to label lines on the plot
def labelLines(lines, ax, align=True, **kwargs):
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    labels_added = []

    for line in lines:
        label = line.get_label()
        if "_line" in label:
            continue

        xval = find_best_label_position(line, xlim, ylim, labels_added)
        if xval is not None:
            place_label_on_line(line, xval, ax, align, **kwargs)
            labels_added.append((xval, label))

# Function to find the best position for a label
def find_best_label_position(line, xlim, ylim, labels_added):
    xdata, ydata = line.get_xdata(), line.get_ydata()
    mask = (xdata >= xlim[0]) & (xdata <= xlim[1]) & (ydata >= ylim[0]) & (ydata <= ylim[1])

    if not any(mask):
        return None

    if np.max(ydata[mask]) > ylim[1] * 0.9 or np.min(xdata[mask]) < xlim[0] + (xlim[1] - xlim[0]) * 0.2:
        xval_options = [(x, y) for x, y in zip(xdata[mask], ydata[mask]) if y < ylim[1] * 0.9]
    else:
        y_mid = np.mean(ydata[mask])
        xval_options = [(x, y) for x, y in zip(xdata[mask], ydata[mask]) if abs(y - y_mid) < (ylim[1] - ylim[0]) * 0.1]
    
    xval_options.sort(key=lambda item: item[1], reverse=True)
    for x, _ in xval_options:
        if not any(abs(x - x_existing) < (xlim[1] - xlim[0]) * 0.05 for x_existing, _ in labels_added):
            return x

    return None

# Function to place a label on a line
def place_label_on_line(line, x, ax, align, **kwargs):
    ydata = line.get_ydata()
    idx = np.argmin(np.abs(line.get_xdata() - x))
    y = ydata[idx]

    label = line.get_label()
    if 'color' not in kwargs:
        kwargs['color'] = line.get_color()
    kwargs.setdefault('ha', 'center')
    kwargs.setdefault('va', 'center')
    kwargs.setdefault('backgroundcolor', ax.get_facecolor())
    kwargs.setdefault('clip_on', True)
    kwargs.setdefault('zorder', 2.5)

    if align:
        ip = idx + 1 if idx < len(ydata) - 1 else idx
        dx = line.get_xdata()[ip] - line.get_xdata()[ip - 1]
        dy = ydata[ip] - ydata[ip - 1]
        ang = degrees(atan2(dy, dx))
        trans_angle = ax.transData.transform_angles(np.array((ang,)), np.array([[x, y]]))[0]
    else:
        trans_angle = 0

    ax.text(x, y, label, rotation=trans_angle, **kwargs)

# Running the script
init()
fig, ax = plt.subplots(figsize=(10, 8))
for spec in species_to_plot:
    mask = (tplot >= 0) & (tplot <= 0.001)
    concentrations = concentrations_glob[spec][mask]
    ax.plot(tplot[mask], concentrations, label=spec, color=color_dict[spec])

labelLines(ax.get_lines(), ax, align=True)

ax.set_xlabel('Residence Time (seconds)')
ax.set_ylabel('Concentration (mol/m^3)')
ax.set_xlim([0, 0.001])
ax.set_ylim([-0.05 * 0.00794, 0.00794])
ax.set_title('Concentration vs. Residence Time')
plt.legend()
plt.show()
