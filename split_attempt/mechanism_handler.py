
import os
import cantera as ct
from utilities import myprint
from utilities import myprint
from settings import mechanism, yaml, kinetics, thermo, output
import os
import cantera as ct

if yaml == False and os.path.exists(output) == True:
    myprint('output mechanism yaml file already exists -> no mechanism file format conversion necessary...')
    mechanism = output
elif yaml == False:
    myprint('converting chemkin mechanism files to yaml file...')
    args = f' python -m cantera.ck2yaml --input={kinetics} --thermo={thermo} --output={output} --permissive'
    os.system(args)
    mechanism = output
else:
    ...



myprint(' ')
gri_names = list(ct.Solution('pfas\\files\\gri3.0.yaml').species_names)
mech_names = list(ct.Solution(mechanism).species_names)
notin = []
for species in gri_names:
    if species in mech_names:
        ...
    else:
        notin.append(species)

if notin:
    myprint('WARNING! PFRTP uses the GRI-Mech 3.0 kinetic mechanism to estimate the composition of flame off-gas given the input stoichiometric ratio. '+
            'The subsequent evolution of that gas in the PFR system is based on the input kinetic mechanism.'+
            ' GRI-Mech 3.0 contains '+str(len(notin))+' species that were not identified in the input mechanism: '+" ".join(notin))
    myprint('You may wish to (a) check if any of the listed species are included in the input mechanism using a different name and rename them accordingly and/or (b) confirm that the listed species are not relevant in this case.')
    myprint('The GRI-Mech 3.0 file used by PFRTP can be found at files')
    myprint(' ')
    myprint(' ')
else:
    ...

