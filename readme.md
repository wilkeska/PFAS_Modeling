# TODOp

1. Find how garrett made charts in his manuscript
2. Make charts better or change input data
3. Do comparisons of Cl species with F species

   1. Garrett seems to have started doing that in lagrangian hi res
      mass frac.ipynb, but he doesn’t include measured Cl data.

### cfs2canteraPD

1. Get injected_species from netj_file
2. Get conc_cutoff from netj_file (inject conc)
3. Make it run PFRTP-Garrett and cfs_post if needed

### cfs_post

1. Make trajectory selection faster
2. Make it run PFRTP-Garrett if needed

### PFRTP-Garrett

1. Make interactive widget to choose run conditions
2. Fix thing with flame temperature estimate
3. Temperatures shouldn’t go down then back up

# Instructions

1. Run [netj_generate.ipynb](netj_generate.ipynb) to generate input
   files from lists of run conditions
2. Run [cfs_batchrun.ipynb](cfs_batchrun.ipynb) to send the generated
   .netj files to CFS and run the simulations
3. Run [PFRTP-Garrett.ipynb](PFRTP-Garrett.ipynb) to use Cantera to
   perform the same simulations.
4. Run [cfs_post.ipynb](cfs_post.ipynb), and select .netj files.
5. Run [cfs2canteraPD.ipynb](cfs2canteraPD.ipynb) to generate path
   diagrams using Cantera.

# Problems

1. There are many many .ipynb files in Modeling_GPD, many of which are
   near duplicates of each other, scattered across folders. It is
   difficult to tell which ones are the most up to date and which ones
   are obsolete.
2. Residence Time column from cantera has no duplicate times. CFS will
   have 3-7 rows of identical times
3. Cantera increases time steps constantly, CFS has variable time steps
4. Concentrations of non-major species in cantera are around 1e-100, in
   CFS they are around 1e-15

   1. Produces problems for reaction path diagrams because cantera
      can’t tell which is the major species
   2. Concentrations are all 0 until injection, then they all
      instantly increase

      1. This is probably because the transient solution solves from
         the injection point and then tries to work backwards to the
         flame. Injecting at the flame may fix this.
5. CF3Or has  15 reactions, CF2s has  74, CF4  15, C2F6  6. C2F6
   behavior in path diagrams may be caused by incomplete reactions

   1. C2F6 may just not have that many reactions because it is a
      larger molecule, and the C-C bond is the most likely to break
6. Several reactions are “ambiguous” and cantera will use the
   designated default reaction

   1. Default reaction may not be conducive for simulating C2F6
7. Some reactions are not parsed (they may just not be relevant)

# Notes

1. CF4 will never be destroyed at temps below 1200K, 100% DE for temps
   \>1600 C
2. Higher values of MAXIT seem to produce more residence time steps

<table>
<caption>Files, Folders, and Descriptions</caption>
<tbody>
<tr class="odd">
<td style="text-align: left;"><span><strong>File</strong></span></td>
<td style="text-align: left;"><span><strong>Folder</strong></span></td>
<td style="text-align: left;"><span><strong>Description</strong></span></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>(r)<span>1-1</span>(lr)<span>2-2</span>(l)<span>3-3</span></p>
<p>flow_convert.ipynb</p></td>
<td style="text-align: left;">PFAS_Modeling/</td>
<td style="text-align: left;">Converts liters per minute to kilograms per second for air and for CH4 using cantera</td>
</tr>
<tr class="odd">
<td style="text-align: left;">netj_generate.ipynb</td>
<td style="text-align: left;">PFAS_Modeling/</td>
<td style="text-align: left;">Takes a set of varying run conditions and produces netj files to do all iterations</td>
</tr>
<tr class="even">
<td style="text-align: left;">cfs_batchrun.ipynb</td>
<td style="text-align: left;">PFAS_Modeling/</td>
<td style="text-align: left;">Uses CFS batch method to run generated netj files, prompts user for inputs to determine simulation duration</td>
</tr>
<tr class="odd">
<td style="text-align: left;">PFRTP-Garrett.ipynb</td>
<td style="text-align: left;">PFAS_Modeling/Pseudo_PFR</td>
<td style="text-align: left;">Uses a PFR simulation in Cantera to make similar results as CFS</td>
</tr>
<tr class="even">
<td style="text-align: left;">cfs_post.ipynb</td>
<td style="text-align: left;">PFAS_Modeling/</td>
<td style="text-align: left;">Runs CFS in GUI mode to automate post-processing of vtk files to include species concentration</td>
</tr>
<tr class="odd">
<td style="text-align: left;">cfs2canteraPD.ipynb</td>
<td style="text-align: left;">PFAS_Modeling/</td>
<td style="text-align: left;">Converts vtk to csv data, then produces a path diagram using Cantera for a specified trajectory, residence time, and threshold.</td>
</tr>
<tr class="even">
<td style="text-align: left;">pfr.ipynb</td>
<td style="text-align: left;">PFAS_Modeling/</td>
<td style="text-align: left;">Example PFR that came with Cantera</td>
</tr>
<tr class="odd">
<td style="text-align: left;">pfr2.ipynb</td>
<td style="text-align: left;">PFAS_Modeling/</td>
<td style="text-align: left;">Example Cantera PFR that includes heat loss</td>
</tr>
<tr class="even">
<td style="text-align: left;">vtk2csv.py</td>
<td style="text-align: left;">PFAS_Modeling/</td>
<td style="text-align: left;">Stand alone script for converting a specific vtk to a csv</td>
</tr>
<tr class="odd">
<td style="text-align: left;">lagrangian hi res mass frac.ipynb</td>
<td style="text-align: left;">L:/Lab/AMCD_PFAS_Incineration/Modeling_GPD/ Cantera/PFR DE S Curves/</td>
<td style="text-align: left;">Makes plots of multiple species DE% vs Temperature</td>
</tr>
<tr class="even">
<td style="text-align: left;">eulerian <span class="math inline"><</span>injectant<span class="math inline">></span>.ipynb</td>
<td style="text-align: left;">L:/Lab/AMCD_PFAS_Incineration/Modeling_GPD/ Cantera/influent concentration/</td>
<td style="text-align: left;">Make multidimensional color plots for conc. vs Temperature vs DE%. Also absolute and relative yield vs conc.</td>
</tr>
<tr class="odd">
<td style="text-align: left;">paths <span class="math inline"><</span>SR<span class="math inline">></span>.ipynb</td>
<td style="text-align: left;">L:/Lab/AMCD_PFAS_Incineration/Modeling_GPD/ Cantera/paths/</td>
<td style="text-align: left;">Makes path diagrams for several species at specified SR</td>
</tr>
<tr class="even">
<td style="text-align: left;">T99.ipynb</td>
<td style="text-align: left;">L:/Lab/AMCD_PFAS_Incineration/Modeling_GPD/ Cantera/T99/</td>
<td style="text-align: left;">Makes T99 plots of multiple species</td>
</tr>
<tr class="odd">
<td style="text-align: left;">lagrangian.ipynb</td>
<td style="text-align: left;">L:/Lab/AMCD_PFAS_Incineration/Modeling_GPD/ Cantera/PFR DE S Curves/archive/</td>
<td style="text-align: left;">Makes plots of species DE vs Temperature. Plots from this script don’t look the same as plots in the doc, so it is probably outdated.</td>
</tr>
</tbody>
</table>

Validated Path Diagrams - CFS

|        |  CF4  |  |  |  | CHF3 |  |  |  | C2F6 |  |  |  |
| :-----: | :---: | :-: | :-: | :-: | :---: | :-: | :-: | :-: | :---: | :-: | :-: | :-: |
|        | Ports |  |  |  | Ports |  |  |  | Ports |  |  |  |
|        |   1   | 4 | 6 | 8 |   1   | 4 | 6 | 8 |   1   | 4 | 6 | 8 |
| 27.5 kW |      |  |  |  |      |  |  |  |   x   |  |  | x |
|  45 kW  |   x   | y |  |  |      |  |  |  |   x   | x |  | x |

Validated Path Diagrams - Cantera

|        |  CF4  |  |  |  | CHF3 |  |  |  | C2F6 |  |  |  |
| :-----: | :---: | :-: | :-: | :-: | :---: | :-: | :-: | :-: | :---: | :-: | :-: | :-: |
|        | Ports |  |  |  | Ports |  |  |  | Ports |  |  |  |
|        |   1   | 4 | 6 | 8 |   1   | 4 | 6 | 8 |   1   | 4 | 6 | 8 |
| 27.5 kW |   x   | x | x | x |      |  |  |  |   y   | y | y | y |
|  45 kW  |   y   | y | y | y |      |  |  |  |   y   | y | y | y |

CFS Executed Simulations

|        |  CF4  |  |  |  | CHF3 |  |  |  | C2F6 |  |  |  |
| :-----: | :---: | :-: | :-: | :-: | :---: | :-: | :-: | :-: | :---: | :-: | :-: | :-: |
|        | Ports |  |  |  | Ports |  |  |  | Ports |  |  |  |
|        |   1   | 4 | 6 | 8 |   1   | 4 | 6 | 8 |   1   | 4 | 6 | 8 |
| 27.5 kW |      | y |  |  |      |  |  |  |   y   | y | y | y |
|  45 kW  |   y   | y |  |  |   y   | y | y |  |   y   | y | y | y |

Cantera Executed Simulations

|        |  CF4  |  |  |  | CHF3 |  |  |  | C2F6 |  |  |  |
| :-----: | :---: | :-: | :-: | :-: | :---: | :-: | :-: | :-: | :---: | :-: | :-: | :-: |
|        | Ports |  |  |  | Ports |  |  |  | Ports |  |  |  |
|        |   1   | 4 | 6 | 8 |   1   | 4 | 6 | 8 |   1   | 4 | 6 | 8 |
| 27.5 kW |   y   | y | y | y |      |  |  |  |   y   | y | y | y |
|  45 kW  |   y   | y | y | y |      |  |  |  |   y   | y | y | y |
