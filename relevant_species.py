#import graphviz and necessary libraries to get the names of the species from the labels of a dot file
import pathlib
import graphviz
import re

#function to get the names of the species from the labels of a dot file
def get_species_names(dot_file):
    #read the dot file
    dot_file = graphviz.Source.from_file(dot_file)
    #make regex to find the labels, returning only the species names. The regex looks for the letters and numbers between label=" and ", while ignoring values that don't have a letter in them
    regex = r'(?<=label=")[A-Za-z0-9]+(?=")'

    #use regex to get labels from the source
    labels = dot_file.source
    #get the labels from the source using regex
    return(re.findall(regex, labels))

dot_file = "pseudo_PFR\\Output\\38.45_45kW_C2F6_port8\\dotfile.dot"
species_names = get_species_names(dot_file)
#save species_names to a file
with open("path_species.txt", "w") as f:
    for name in species_names:
        f.write(name + "\n")

# #read species names, save back to variable
# with open("path_species.txt", "r") as f:
#     species_names = f.read().splitlines()