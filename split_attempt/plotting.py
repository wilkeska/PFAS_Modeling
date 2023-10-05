
import matplotlib.pyplot as plt
import matplotlib.image as mpimage
import plotly.graph_objects as go
from utilities import myprint
from settings import *
import matplotlib.pyplot as plt

data = np.array(sim_data).T
fig = go.Figure()
for i in np.arange(len(cantera_species)):
    if max(data[i])<concentrations_interactive_plot_cutoff:
        ...
    else:
        fig.add_trace(go.Scatter(x=tplot,y=data[i],name=cantera_species[i]))
fig.update_yaxes(title_text='Concentration (mol fraction)',type='log',exponentformat='power')
fig.update_xaxes(title_text='Residence Time (seconds)')
fig.update_layout(template='plotly_white')
fig.write_html(output_folder+"\\interactive_plot_concentrations.html")




data = np.array(nrp).T
fig = go.Figure()
for i in np.arange(len(cantera_reactions)):
    if max(data[i])<rates_interactive_plot_cutoff:
        ...
    else:
        fig.add_trace(go.Scatter(x=tplot,y=data[i],name=cantera_reactions[i]))
    
ylabel='Net Rate of Progress (kmol/m3/s)'
fig.update_yaxes(title_text=ylabel,type='log',exponentformat='power')
fig.update_xaxes(title_text='Residence Time (seconds)')
fig.update_layout(template='plotly_white')
fig.write_html(output_folder+"\\interactive_plot_net_rates.html")




# generate figures and excel files
# organize them based on maximum concentration across all slices

if individual_plots == True:
    if os.path.exists(output_folder+r"\\individual_major_species") == False:
        os.makedirs(output_folder+r"\\individual_major_species")
    if os.path.exists(output_folder+r"\\individual_minor_species") == False:
        os.makedirs(output_folder+r"\\individual_minor_species")
    neg_species = [] # negligible species
    eff_c = [] # effluent concentrations

    for species in np.arange(len(cantera_species)):
        name = cantera_species[species]
        eff_c.append([name, np.array(sim_data)[:,species][-1]])

        plt.plot(tplot,np.array(sim_data)[:,species])
        plt.xlabel('Residence time (seconds)')
        plt.ylabel('Concentration (mol fraction)')
        plt.title(name, fontsize=20,fontweight='bold')
        plt.yscale('log')
        if np.max(np.array(sim_data)[:,species]) > major_species_cutoff:
            plt.savefig(output_folder+'\\individual_major_species\\'+name+'.png',dpi=300,
                        bbox_inches='tight',facecolor='white');
        elif np.max(np.array(sim_data)[:,species]) > minor_species_cutoff:
            plt.savefig(output_folder+'\\individual_minor_species\\'+name+'.png',dpi=300,
                        bbox_inches='tight',facecolor='white');
        else:
            neg_species.append([name, np.max(np.array(sim_data)[:,species])])
        plt.close();

    df = pd.DataFrame(neg_species, columns=['Species', 'Maximum Concentration (mol fraction)'])
    df.to_excel(output_folder+"\\negligible_species.xlsx")
    
else:
    ...




plt.rcParams["figure.dpi"] = 200
gas = ct.Solution(mechanism)
retry = 'y'

while retry == 'y':
    plot_step = np.abs(tplot - path_res_time).argmin()
    P = ct.one_atm
    T = Tplot[plot_step]
    X = sim_data[plot_step]
    gas.TPX = T, P, X

    diagram = ct.ReactionPathDiagram(gas, path_element)
    diagram.threshold = path_threshold
    diagram.dot_options='node[shape="box"]'
    title = (
        (
            f'Path diagram for {path_element} at residence time of {str(path_res_time)}'
            + ' seconds \r scaled by maximum flux (kmol m-^3 s^-1) \r'
        )
        + ' with displayed threshold of '
    ) + str(path_threshold)
    diagram.title = title
    diagram.show_details = path_details
    diagram.display_only(-1 if path_species == 'all' else gas.species_index(path_species))
    dot_file = f"{output_folder}/dotfile.dot"
    png_file = f"{output_folder}/reaction_paths.png"
    diagram.write_dot(dot_file)
    os.system(f'dot {dot_file} -Tpng -o {png_file} -Gdpi=100')
    img = mpimage.imread(png_file)
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    if run_with_dialog == True:
        retry = myinput('path diagram saved to output folder...generate new path diagram? (y/n): ')
    else:
        retry = 'n'
    if retry == 'y':
        path_res_time = float(myinput('type path diagram residence time (in seconds) and press enter: '))
        path_element = myinput('type path diagram element symbol and press enter: ')
        path_species = myinput('type path diagram species and press enter (all/individual species name): ')
        path_threshold = float(myinput('type path diagram threshold and press enter: '))
        path_details = input('show path details? (y/n) and press enter: ').lower().strip() == 'y'
    else:
        ...

