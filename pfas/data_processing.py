
import os
import numpy as np
import pandas as pd
from settings import *
from utilities import *


# generate excel files
myprint(' ')
if run_with_dialog == True:
    time.sleep(2)
    myinput('press enter to generate output')
else:
    ...
myprint('generating and saving output to output folder...')




cantera_species = ct.Solution(mechanism).species_names
tplot = np.concatenate(([0],np.cumsum(tinj),np.cumsum(tgap2)+sum(tinj)))[:-1]
Tplot = Tnew[len(tnew)-len(sim_data):]

sim_data_new = list(np.array(sim_data).T)
sim_data_new.insert(0,Tplot)
sim_data_new.insert(0,tplot)
sol = np.array(sim_data_new).T
columns = ['Residence Time (seconds)','Temperature (K)'] + cantera_species
pd.DataFrame(sol,columns=columns).to_excel(output_folder+"\\solution_concentrations.xlsx")




eff_c = [] # effluent concentrations

for species in np.arange(len(cantera_species)):
    name = cantera_species[species]
    eff_c.append([name, np.array(sim_data)[:,species][-1]])

c = np.array(eff_c)
c_sorted = c[(c[:,1]).astype(float).argsort()[::-1]]
df = pd.DataFrame(c_sorted, columns=['Species','Effluent Concentration (mol fraction)'])
df.to_excel(output_folder+"\\solution_effluent_concentrations.xlsx")




cantera_reactions = list(ct.Solution(mechanism).reaction_equations())
if save_rates_solution == False:
    ...
else:
    nrp_new = list(np.array(nrp).T)
    nrp_new.insert(0,Tnew[len(tnew)-len(nrp):])
    nrp_new.insert(0,tplot)
    sol = np.array(nrp_new).T
    columns = ['Residence Time (seconds)','Temperature (K)'] + cantera_reactions
    pd.DataFrame(sol,columns=columns).to_excel(output_folder+"\\solution_reactions.xlsx")

