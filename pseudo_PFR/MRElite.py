# %%
import time
tot_tic = time.time()
import matplotlib.pyplot as plt
import numpy as np
import os as os
from math import atan2,degrees
import h5py
# %%
injectants =        ['CCL4'] # list of injectants, must be in the mechanism file.
injectant_concs =   [100] # injected species concentrations in furnace @ injection point (ppm)
injectant_units =   ['wt%'] # units of injected species concentration in furnace @ injection point (ppm)
ER = 0.834 
injectant_tot_conc=20 # total injected species concentration in furnace @ injection point (ppm)
injectant_port = 4 # port number of injectant
firing_rate = 45 # firing rate in kW

post_injection_res_time_step = 1e-4 # residence time grid size (seconds)
elsewhere_res_time_step = 1e-2 # residence time grid size (seconds)
os.chdir(os.path.join(os.getcwd(), 'pseudo_PFR'))
# %%
def init():
    global cantera_species, sol, columns, tplot, Tplot, color_dict, species_to_plot, concentrations_glob
    # Read the column names and the data from the HDF5 file
    with h5py.File("sol.hdf5", 'r') as f:
        cantera_species = f['column_names'][:].tolist()
        sol = f['data'][:]

    columns = ['Residence Time (seconds)', 'Temperature (K)'] + cantera_species
    columns = [col.decode('utf-8') if isinstance(col, bytes) else col for col in columns]
    # Convert newcantera_species to a list of strings
    cantera_species = [species.decode('utf-8') for species in cantera_species]

    tplot = sol[:, 0]
    Tplot = sol[:, 1]

    # List to store the species to plot
    species_to_plot = ['H', 'CL', 'CCL4','HCL','CLO','CCLO','CL2']
    # Calculate the minimum and maximum concentrations for each species
    concentrations_glob = {species: sol[:, columns.index(species)] for species in species_to_plot}

def labelLine(line,x,label=None,align=True,**kwargs):

    ax = line.axes
    xdata = line.get_xdata()
    ydata = line.get_ydata()
    # print(f'x: {x}')
    # print(f'x type: {type(x)}')
    # print(f' xdata type: {type(xdata[-1])}')
    if (x < xdata[0]) or (x > xdata[-1]):
        print('x label location is outside data range!')
        return

    #Find corresponding y co-ordinate and angle of the line
    ip = 1
    for i in range(len(xdata)):
        if x < xdata[i]:
            ip = i
            break

    y = ydata[ip-1] + (ydata[ip]-ydata[ip-1])*(x-xdata[ip-1])/(xdata[ip]-xdata[ip-1])

    if not label:
        label = line.get_label()

    if align:
        #Compute the slope
        dx = xdata[ip] - xdata[ip-1]
        dy = ydata[ip] - ydata[ip-1]
        ang = degrees(atan2(dy,dx))

        #Transform to screen co-ordinates
        pt = np.array([x,y]).reshape((1,2))
        trans_angle = ax.transData.transform_angles(np.array((ang,)),pt)[0]

    else:
        trans_angle = 0

    #Set a bunch of keyword arguments
    if 'color' not in kwargs:
        kwargs['color'] = line.get_color()

    if ('horizontalalignment' not in kwargs) and ('ha' not in kwargs):
        kwargs['ha'] = 'center'

    if ('verticalalignment' not in kwargs) and ('va' not in kwargs):
        kwargs['va'] = 'center'

    if 'backgroundcolor' not in kwargs:
        kwargs['backgroundcolor'] = ax.get_facecolor()

    if 'clip_on' not in kwargs:
        kwargs['clip_on'] = True

    if 'zorder' not in kwargs:
        kwargs['zorder'] = 2.5

    ax.text(x,y,label,rotation=trans_angle,**kwargs)

def labelLines(lines,align=True,xvals=None,**kwargs):
    ax = lines[0].axes
    labLines = []
    labels = []

    #Take only the lines which have labels other than the default ones
    for line in lines:
        label = line.get_label()
        if "_line" not in label:
            labLines.append(line)
            labels.append(label)

    if xvals is None:
        xmin,xmax = ax.get_xlim()
        xvals = np.linspace(xmin,xmax,len(labLines)+2)[1:-1]

    for line,x,label in zip(labLines,xvals,labels):
        labelLine(line,x,label,align,**kwargs)

def update_plot(change=None):
    plt.close('all')
    global species_to_plot
    global concentrations_glob
    xlim=(0, 0.001)
    ylim=0.00794
    concentrations_glob = {species: sol[:, columns.index(species)] for species in species_to_plot}
    if not isinstance(species_to_plot, (list, tuple)):
        species_to_plot = [species_to_plot]
    

    pixel_x = 800
    pixel_y = 800
    inch_x = pixel_x / plt.rcParams["figure.dpi"]
    inch_y = pixel_y / plt.rcParams["figure.dpi"]

    _, ax = plt.subplots(figsize=(inch_x, inch_y))
    global color_dict
    color_dict = {'H': (0.0, 0.0, 0.0, 1.0), 'CL': (0.0, 0.0, 0.7255235294117647, 1.0), 'CCL4': (0.0, 0.6444666666666666, 0.7333666666666667, 1.0), 'HCL': (0.0, 0.7385313725490196, 0.0, 1.0), 'CLO': (0.7999666666666666, 0.9777666666666667, 0.0, 1.0), 'CCLO': (1.0, 0.1764705882352941, 0.0, 1.0), 'CL2': (0.8, 0.8, 0.8, 1.0)}
    for i, spec in enumerate(species_to_plot):
        mask = (tplot >= xlim[0]) & (tplot <= xlim[1])
        concentrations = sol[mask, columns.index(spec)]
        ax.plot(tplot[mask], concentrations, label=spec, color=color_dict[spec])
    #make dictionary of colors for each species
    label_plot_lines(ax)
    ax.set_xlabel('Residence Time (seconds)')
    ax.set_ylabel('Concentration (mol/m^3)')
    ax.set_xlim(xlim)
    ax.set_ylim([-0.05*ylim, ylim])  # Set the lower limit of the y-axis to 0
    ax.set_title('Concentration (<{:.3e}) vs. Residence Time ({} s)'.format(ylim, xlim[1]))
    plt.show()
    # Update the maximum of the ylim slider
    

def find_visible_segment(line, xlim, ylim):
    xdata = line.get_xdata()
    ydata = line.get_ydata()
    mask = (xdata >= xlim[0]) & (xdata <= xlim[1]) & (ydata >= ylim[0]) & (ydata <= ylim[1])
    
    if xdata[mask].size == 0 or ydata[mask].size == 0:
        return None, None
    return xdata[mask], ydata[mask]

def calculate_midpoints(lines, xlim, ylim):
    midpoints = []
    for line in lines:
        xdata, ydata = find_visible_segment(line, xlim, ylim)
        
        if xdata is None or ydata is None:
            continue
        
        y_mid = (max(ydata) + min(ydata)) / 2
        idx = np.abs(ydata - y_mid).argmin()
        midpoints.append(xdata[idx])
        print(f'{line.get_label()} midpoint: {xdata[idx]}')
    return midpoints

def distribute_midpoints(midpoints, xlim):
    unique_midpoints = sorted(set(midpoints))
    # Create a dictionary to map each unique midpoint to its duplicates
    midpoint_groups = {m: [] for m in unique_midpoints}
    for i, m in enumerate(midpoints):
        midpoint_groups[m].append(i)

    # Prepare a list to hold the new distributed x-values
    distributed_xvals = [None] * len(midpoints)

    for m in unique_midpoints:
        indices = midpoint_groups[m]
        if len(indices) > 1: # If there are duplicates
            # Find neighboring unique midpoints or use plot boundaries
            left_bound = unique_midpoints[unique_midpoints.index(m) - 1] if unique_midpoints.index(m) > 0 else xlim[0]
            right_bound = unique_midpoints[unique_midpoints.index(m) + 1] if unique_midpoints.index(m) < len(unique_midpoints) - 1 else xlim[1]

            # Distribute x-values evenly between the bounds
            new_xvals = np.linspace(left_bound, right_bound, len(indices) + 2)[1:-1]

            # Assign new x-values to the original indices
            for orig_idx, new_x in zip(indices, new_xvals):
                distributed_xvals[orig_idx] = new_x
        else:
            # If no duplicates, keep the original midpoint
            distributed_xvals[indices[0]] = m

    return distributed_xvals

def find_valid_x_for_label(line, proposed_x, xlim, ylim, max_attempts=100):
    # Calculate the 5% margin for x and y limits
    x_margin = 0.05 * (xlim[1] - xlim[0])
    y_margin = 0.05 * (ylim[1] - ylim[0])
    x_min_limit = xlim[0] + x_margin
    x_max_limit = xlim[1] - x_margin
    y_min_limit = ylim[0] + y_margin
    y_max_limit = ylim[1] - y_margin

    for attempt in range(max_attempts):
        y = line.get_ydata()[np.abs(line.get_xdata() - proposed_x).argmin()]
        if x_min_limit <= proposed_x <= x_max_limit and y_min_limit <= y <= y_max_limit:
            return proposed_x
        else:
            proposed_x += (x_max_limit - x_min_limit) / max_attempts
    return None

def label_plot_lines(ax):
    '''Labels the lines in the provided Axes object, avoiding edges and overlaps'''
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    lines = ax.get_lines()
    midpoints = calculate_midpoints(lines, xlim, ylim)
    # print(f"midpoints before distribute: {midpoints}")
    xvals = distribute_midpoints(midpoints, xlim)
    # print(f'xvals after distribute: {xvals}')
    # print(f"midpoints before find_valid_x_for_label: {midpoints}")
    adjusted_xvals=[]
    for line, val in zip(lines, xvals):
        adjusted_xvals.append(find_valid_x_for_label(line, val, xlim, ylim))
    # print(f"xvals after find_valid_x_for_label: {adjusted_xvals}")
    #remove any None values from adjusted_xvals and their corresponding line from lines
    
    adjusted_xvals = [x for x in adjusted_xvals if x is not None]
    lines = [line for line, x in zip(lines, adjusted_xvals) if x is not None]
    # for label, midpoint, xval in zip(labels, midpoints, xvals):
    #     print(f"{label}:")
    #     print(f" xval - {xval}")
    #     print(f" midpoints - {midpoint}")
        # Calculate and print Adjusted Value here
    labelLines(lines, xvals=adjusted_xvals, align=True)
init()
update_plot()


# %% example of label_plot_lines, to make sure functions work in normal cases
plt.figure()
#make a bunch of lines, using linear, polynomial, exponential, and trigonometric functions
x = np.linspace(0, 10, 100)
y1 = x
y2 = (x/2)**2
y3 = np.exp(x/2)
y4 = np.sin(x) +5


plt.plot(x ,y1, label='Line 1')
plt.plot(x, y2, label='Line 2')
plt.plot(x, y3, label='Line 3')
plt.plot(x, y4, label='Line 4')
plt.xlim(2, 8)
plt.ylim(0, 10)

ax = plt.gca()
label_plot_lines(ax)



