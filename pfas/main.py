
import os

# 1. Initialization and importing packages


# 2. Setting system conditions
from settings import *

# 3. Utilizing utility functions and setting up output folders
from utilities import *

# 4. Mechanism handling and species mapping
from mechanism_handler import *

# 5. Running the main simulation
from simulation import sim

# Execute the main simulation
sim_data, nrp = sim(Tnew, tnew)

# 6. Data processing for output and plotting
from data_processing import *

# 7. Plotting data
from plotting import *

# 8. Handling interactive widgets
from interactive_widgets import *