# %%
import cantera as ct
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from ipywidgets import widgets, interact
from ipywidgets import SelectionSlider
import matplotlib.pyplot as plt
import matplotlib.image as mpimage
from IPython.display import Image


# %%
########## Path diagram ##########
path_res_time = 0.001 # seconds, precision will be limited by grid resolution settings
path_element = 'F' # case sensitive
path_species = 'all' # 'all' or individual species name to only display fluxes connected to that species
path_threshold = 0.1 # kmol/m3/sec
path_details = False # or True

########## Grid resolution ##########
post_injection_res_time_step = 1e-3 # residence time grid size (seconds)
post_injection_duration = 1e-1 # seconds
elsewhere_res_time_step = 1e-2 # residence time grid size (seconds)

########## Additional settings ##########
run_with_dialog = False # Running with dialog may be best for public distributions
print_info_every = 100 # print simulation info every n time steps
atol = 1e-15 # absolute error tolerance for reactor equations solver
rtol = 1e-9 # relative error tolerance for reactor equations solver
it0 = True # generate output with pre-injection data trimmed off (True) or not trimmed (False)
concentrations_interactive_plot_cutoff = 1e-7 # mol fraction
rates_interactive_plot_cutoff = 1e-8 # mol/m3/s
save_rates_solution = False # Generating the net rates excel spreadsheet adds a lot of wall time
individual_plots = False # Generating individual species concentration plots adds a lot of wall time
major_species_cutoff = 1e-6 # mol fraction
minor_species_cutoff = 1e-15 # mol fraction
output_folder = 'C:\\Users\\KWILKES\\Desktop\\PFAS_Modeling\\cfs_para_test_cond\\1430_45kW_CF4_port4\\reaction_paths'
spec_list = ['C', 'CF', 'CF2O', 'CF2s', 'CF3Or', 'CF3r', 'CF4', 'CFO', 'CHF3', 'CHFO', 'CHFs', 'CO', 'F', 'F2', 'H', 'H2', 'H2O', 'HF', 'O', 'O2', 'OHr']

# %%
data = pd.read_csv('C:\\Users\\KWILKES\\Desktop\\PFAS_Modeling\\cfs_para_test_cond\\1430_45kW_CF4_port4\\excel\\destruct.csv', sep = ',', header = 0, index_col = False)

time = data['time'].values
traj_numbers = data['traj_number'].unique()
temp = data['TEMPERATURE:'].values
mechanism = 'NCSU_PFASmech1.0.yaml'
avg_data = pd.DataFrame()
if not os.path.exists('C:\\Users\\KWILKES\\Desktop\\PFAS_Modeling\\cfs_para_test_cond\\1430_45kW_CF4_port4\\excel\\avg_data.csv'):
    print('no avg_data, Creating avg_data.csv')
#iterate through unique times, calculate concentration for each species at each time
    for time_point in data['time'].unique():
        traj_num = data[data['time'] == time_point]['traj_number'].values[0]
        concentrations = data.loc[data['time'] == time_point, spec_list].reset_index(drop=True)
        avg_data_row = pd.DataFrame({'time': time_point, 'temperature' : temp[np.where(data['time'] == time_point)[0][0]], 'traj_number': traj_num, 'C': concentrations['C'], 'CF': concentrations['CF'], 'CF2O': concentrations['CF2O'], 'CF2s': concentrations['CF2s'], 'CF3Or': concentrations['CF3Or'], 'CF3r': concentrations['CF3r'], 'CF4': concentrations['CF4'], 'CFO': concentrations['CFO'], 'CHF3': concentrations['CHF3'], 'CHFO': concentrations['CHFO'], 'CHFs': concentrations['CHFs'], 'CO': concentrations['CO'], 'F': concentrations['F'], 'F2': concentrations['F2'], 'H': concentrations['H'], 'H2': concentrations['H2'], 'H2O': concentrations['H2O'], 'HF': concentrations['HF'], 'O': concentrations['O'], 'O2': concentrations['O2'], 'OH': concentrations['OHr']}, index=[0])
        avg_data = pd.concat([avg_data, avg_data_row])
    avg_data.to_csv('C:\\Users\\KWILKES\\Desktop\\PFAS_Modeling\\cfs_para_test_cond\\1430_45kW_CF4_port4\\excel\\avg_data.csv', index = False)
#save avg_data to csv
else:
    print('avg_data.csv exists, loading avg_data.csv')
    avg_data = pd.read_csv('C:\\Users\\KWILKES\\Desktop\\PFAS_Modeling\\cfs_para_test_cond\\1430_45kW_CF4_port4\\excel\\avg_data.csv', sep = ',', header = 0)

# %%
plt.rcParams["figure.dpi"] = 200
gas = ct.Solution(mechanism)

t_min = 0.0
t_max = post_injection_duration #max(tplot)
t_step = post_injection_res_time_step #elsewhere_res_time_step

thresh_min = 0.0
thresh_max = 1.0
thresh_step = 1e-2

def plot_reaction_path_diagrams(traj_num, res_time, threshold, details, species):
    #select only rows from avg_data with traj_num = traj_num
    plot_data = avg_data[avg_data['traj_number'] == traj_num] #select only rows from avg_data with traj_num = traj_num
    initial_row = plot_data[plot_data['time'] == res_time] #select row with residence time = res_time
    species_concentrations = initial_row.drop(['time', 'temperature', 'traj_number'], axis='columns')
    species_dict = species_concentrations.to_dict(orient='list')
    species_dict = {k: v[0] for k, v in species_dict.items()}

    P = ct.one_atm
    T = initial_row['temperature']
    X = species_dict
    gas.TP = float(T.iloc[0]), P
    gas.X = X

    diagram = ct.ReactionPathDiagram(gas, species)
    diagram.threshold = threshold
    diagram.dot_options='node[shape="box"]'
    diagram.show_details = details
    diagram.display_only(-1 if path_species == 'all' else gas.species_index(path_species))
    #diagram.display_only(gas.species_index('HOCL'))
    title = (
        (
            f'Path diagram for {species} at residence time of {str(res_time)}'
            + ' seconds \r scaled by maximum flux (kmol m-^3 s^-1) \r'
        )
        + ' with displayed threshold of '
    ) + str(threshold)
    diagram.title = title
    dot_file = f"{output_folder}/dotfile.dot"
    png_file = f"{output_folder}/reaction_paths.png"
    diagram.write_dot(dot_file)
    os.system(f'dot {dot_file} -Tpng -o {png_file} -Gdpi=300')
    img = mpimage.imread(png_file)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def format_float(num):
    return np.format_float_positional(num, trim='-')

def update_time_description(change):
    try:
        res_time = data['time'][change.new]
        res_time_slider.description = f"Residence Time: {res_time}"
    except IndexError:
        print(f"IndexError: {change.new} is not a valid index for the residence time slider. Valid indices are 0 to {len(data['time']) - 1}") 


resmax= len(data['time'])

#making interactive options
res_time_slider = widgets.IntSlider(min=0, max=resmax, step=1, description='Residence Time:')
res_time_slider.observe(update_time_description, names='value')
traj_dropdown = widgets.Dropdown(options = traj_numbers, value = traj_numbers[0], description = 'Trajectory:')
threshold_slider = widgets.FloatSlider(min = 0.1, max = 1.0, step = 0.1, value = 0.1, description = 'Threshold:')
details_toggle = widgets.ToggleButton(value = False, description = 'Details:')
species_dropdown = widgets.Dropdown(options = spec_list, value = path_element, description = 'Species:')

@interact(traj_num = traj_dropdown, res_time = res_time_slider, threshold = threshold_slider, details = details_toggle, species = species_dropdown)

def update_plot(traj_num, res_time, threshold, details, species):
    traj_data = data[data['traj_number'] == traj_num]
    res_time_slider.min = traj_data['time'].min()
    res_time_slider.max = traj_data['time'].max()
    if res_time_slider.value < res_time_slider.min or res_time_slider.value > res_time_slider.max:
        res_time_slider.value = res_time_slider.min

    actual_res_time = traj_data['time'].iloc[res_time]
    plot_reaction_path_diagrams(traj_num, actual_res_time, threshold, details, species)

# %%
# import os
# import matplotlib.image as mpimage

# os.system(f'dot C:\\Users\\KWILKES\\Desktop\\PFAS_Modeling\\cfs_para_test_cond\\1430_45kW_CF4_port4\\dot\\F.dot -Tpng -o {element_name}.png -Gdpi=100')
# png_file = 'F.png'
# img = mpimage.imread(png_file)
# plt.imshow(img)
# plt.axis('off')
# plt.show()


