
import sys
from utilities import myprint
from settings import run_with_dialog
import time

from ipywidgets import widgets, interact
from ipywidgets import SelectionSlider




plt.rcParams["figure.dpi"] = 200
gas = ct.Solution(mechanism)

t_min = 0.0
t_max = post_injection_duration #max(tplot)
t_step = post_injection_res_time_step #elsewhere_res_time_step

thresh_min = 0.0
thresh_max = 1.0
thresh_step = 1e-2

def format_float(num):
    return np.format_float_positional(num, trim='-')

@interact(
    res_time=SelectionSlider(value=t_min+t_step,
                             options=[("%g"%i,i) for i in np.arange(t_min,t_max,t_step)]),
    threshold=SelectionSlider(value=thresh_min+thresh_step,
                              options=[("%g"%i,i) for i in np.arange(thresh_min,thresh_max,thresh_step)]),
    details=widgets.ToggleButton(),
    species=widgets.Dropdown(
        options=gas.element_names,
        value=path_element,
        description="Element",
        disabled=False,
    ),
)
def plot_reaction_path_diagrams(res_time, threshold, details, species):
    plot_step = np.abs(tplot - res_time).argmin()
    P = ct.one_atm
    T = Tplot[plot_step]
    X = sim_data[plot_step]
    gas.TPX = T, P, X

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


