import numpy as np

########## System conditions ##########
lengths = [36,13,133,97] # inches
diameters = [20.5,15.5,10.5,8] # inches
SR = 2.2 # stoichiometric ratio
exhaust_gas_q = 960 # total volumetric flow rate (L/min)
injection_loc = 55 # inches, see files\rainbow_ports.txt for list of port locations
injectant = 'PF8acid' # injected species, must be in quotations and match name in mechanism file
injectant_conc = 35e-6 # injected species concentration in furnace @ injection point (mol fraction)
output_folder = 'Output/PF8acid' # script will auto-generate the folder

########## Mechanism ##########
#mechanism = 'NCSU_PFASmech1.0.yaml' # mechanism file, irrelevant if 'yaml' = False
mechanism = 'pfas\\NCSU_PFASmech1.0.yaml' # mechanism file, irrelevant if 'yaml' = False
yaml = True # if False, below chemkin format files will be converted to a Cantera friendly yaml file
kinetics = 'NCSU_PFASmech1.0_Kinetics.inp'
thermo = 'NCSU_PFASmech1.0_Thermo.dat'
output = 'new_mech_file.yaml' # must have .yaml extension

########## Temperature fitting ##########
measured_temps = [927,864,819,753,711,655,501,449,399,364] # °C
measured_temps_locs = [18,55,79,103,127,151,201,225,249,273] # inches
ff = 0.9 # "fudge factor" for flame temp because Cantera's solution is adiabatic
spline = True # fit using scipy.interpolate.UnivariateSpline (True) or numpy.polyfit (False)
k = 3 # spline degree
s = None # spline smoothing factor, see scipy documentation for guidance
pdeg = 4 # polynomial degree, only appliciable if 'spline' is set to False

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

