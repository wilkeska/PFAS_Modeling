# TODOp {#todop .unnumbered}

1.  Find how garrett made charts in his manuscript

2.  Make charts better or change input data

3.  Do comparisons of Cl species with F species

    1.  Garrett seems to have started doing that in lagrangian hi res
        mass frac.ipynb, but he doesn't include measured Cl data.

### cfs2canteraPD {#cfs2canterapd .unnumbered}

1.  Get injected_species from netj_file

2.  Get conc_cutoff from netj_file (inject conc)

3.  Make it run PFRTP-Garrett and cfs_post if needed

### cfs_post {#cfs_post .unnumbered}

1.  Make trajectory selection faster

2.  Make it run PFRTP-Garrett if needed

### PFRTP-Garrett {#pfrtp-garrett .unnumbered}

1.  Make interactive widget to choose run conditions

2.  Fix thing with flame temperature estimate

3.  Temperatures shouldn't go down then back up

# Instructions {#instructions .unnumbered}

1.  Run [netj_generate.ipynb](netj_generate.ipynb) to generate input
    files from lists of run conditions

2.  Run [cfs_batchrun.ipynb](cfs_batchrun.ipynb) to send the generated
    .netj files to CFS and run the simulations

3.  Run [PFRTP-Garrett.ipynb](PFRTP-Garrett.ipynb) to use Cantera to
    perform the same simulations.

4.  Run [cfs_post.ipynb](cfs_post.ipynb), and select .netj files.

5.  Run [cfs2canteraPD.ipynb](cfs2canteraPD.ipynb) to generate path
    diagrams using Cantera.

# Problems {#problems .unnumbered}

1.  There are many many .ipynb files in Modeling_GPD, many of which are
    near duplicates of each other, scattered across folders. It is
    difficult to tell which ones are the most up to date and which ones
    are obsolete.

2.  Residence Time column from cantera has no duplicate times. CFS will
    have 3-7 rows of identical times

3.  Cantera increases time steps constantly, CFS has variable time steps

4.  Concentrations of non-major species in cantera are around 1e-100, in
    CFS they are around 1e-15

    1.  Produces problems for reaction path diagrams because cantera
        can't tell which is the major species

    2.  Concentrations are all 0 until injection, then they all
        instantly increase

        1.  This is probably because the transient solution solves from
            the injection point and then tries to work backwards to the
            flame. Injecting at the flame may fix this.

5.  CF3Or has  15 reactions, CF2s has  74, CF4  15, C2F6  6. C2F6
    behavior in path diagrams may be caused by incomplete reactions

    1.  C2F6 may just not have that many reactions because it is a
        larger molecule, and the C-C bond is the most likely to break

6.  Several reactions are "ambiguous" and cantera will use the
    designated default reaction

    1.  Default reaction may not be conducive for simulating C2F6

7.  Some reactions are not parsed (they may just not be relevant)

# Notes {#notes .unnumbered}

1.  CF4 will never be destroyed at temps below 1200K, 100% DE for temps
    \>1600 C

2.  Higher values of MAXIT seem to produce more residence time steps

+----------------------+----------------------+----------------------+
| **File**             | **Path**             | **Description**      |
+:=====================+:=====================+:=====================+
| (lr)2-2(l)3-3        | path                 | Takes a set of       |
|                      |                      | varying run          |
| netj_generate.ipynb  |                      | conditions and       |
|                      |                      | produces netj files  |
|                      |                      | to do all iterations |
+----------------------+----------------------+----------------------+
| cfs_batchrun.ipynb   | path1                | Uses CFS batch       |
|                      |                      | method to run        |
|                      |                      | generated netj       |
|                      |                      | files, prompts user  |
|                      |                      | for inputs to        |
|                      |                      | determine simulation |
|                      |                      | duration             |
+----------------------+----------------------+----------------------+
| PFRTP-Garrett.ipynb  | path2                | Uses a PFR           |
|                      |                      | simulation in        |
|                      |                      | Cantera to make      |
|                      |                      | similar results as   |
|                      |                      | CFS                  |
+----------------------+----------------------+----------------------+
| cfs_post.ipynb       | path3                | Runs CFS in GUI mode |
|                      |                      | to automate          |
|                      |                      | post-processing of   |
|                      |                      | vtk files to include |
|                      |                      | species              |
|                      |                      | concentration        |
+----------------------+----------------------+----------------------+
| cfs2canteraPD.ipynb  | path4                | Converts vtk to csv  |
|                      |                      | data, then produces  |
|                      |                      | a path diagram using |
|                      |                      | Cantera for a        |
|                      |                      | specified            |
|                      |                      | trajectory,          |
|                      |                      | residence time, and  |
|                      |                      | threshold.           |
+----------------------+----------------------+----------------------+
| lagrangian hi res    | L:/                  | Makes plots of       |
| mass frac.ipynb      | Lab/AMCD_PFAS_Incine | multiple species DE% |
|                      | ration/Modeling_GPD/ | vs Temperature       |
|                      | Cantera/PFR DE S     |                      |
|                      | Curves/              |                      |
+----------------------+----------------------+----------------------+
| eulerian             | L:/                  | Make                 |
| $                    | Lab/AMCD_PFAS_Incine | multidimensional     |
| <$injectant$>$.ipynb | ration/Modeling_GPD/ | color plots for      |
|                      | Cantera/inf          | conc. vs Temperature |
|                      | luent concentration/ | vs DE%. Also         |
|                      |                      | absolute and         |
|                      |                      | relative yield vs    |
|                      |                      | conc.                |
+----------------------+----------------------+----------------------+
| paths $<$SR$>$.ipynb | L:/                  | Makes path diagrams  |
|                      | Lab/AMCD_PFAS_Incine | for several species  |
|                      | ration/Modeling_GPD/ | at specified SR      |
|                      | Cantera/paths/       |                      |
+----------------------+----------------------+----------------------+
| T99.ipynb            | L:/                  | Makes T99 plots of   |
|                      | Lab/AMCD_PFAS_Incine | multiple species     |
|                      | ration/Modeling_GPD/ |                      |
|                      | Cantera/T99/         |                      |
+----------------------+----------------------+----------------------+
| lagrangian.ipynb     | L:/                  | Makes plots of       |
|                      | Lab/AMCD_PFAS_Incine | species DE vs        |
|                      | ration/Modeling_GPD/ | Temperature. Plots   |
|                      | Cantera/PFR          | from this script     |
|                      | DE S Curves/archive/ | don't look the same  |
|                      |                      | as plots in the doc, |
|                      |                      | so it is probably    |
|                      |                      | outdated.            |
+----------------------+----------------------+----------------------+

: Files, Paths, and Descriptions

              CF4                CHF3                C2F6           
  --------- ------- --- --- --- ------- --- --- --- ------- --- --- ---
             Ports               Ports               Ports          
               1     4   6   8     1     4   6   8     1     4   6   8
   27.5 kW                                                          
    45 kW                                                           

  : Validated Path Diagrams - CFS

              CF4                CHF3                C2F6           
  --------- ------- --- --- --- ------- --- --- --- ------- --- --- ---
             Ports               Ports               Ports          
               1     4   6   8     1     4   6   8     1     4   6   8
   27.5 kW                                                          
    45 kW                                                           

  : Validated Path Diagrams - Cantera

              CF4                CHF3                C2F6           
  --------- ------- --- --- --- ------- --- --- --- ------- --- --- ---
             Ports               Ports               Ports          
               1     4   6   8     1     4   6   8     1     4   6   8
   27.5 kW                                                          
    45 kW                                                           

  : CFS Executed Simulations

              CF4                CHF3                C2F6           
  --------- ------- --- --- --- ------- --- --- --- ------- --- --- ---
             Ports               Ports               Ports          
               1     4   6   8     1     4   6   8     1     4   6   8
   27.5 kW                                                          
    45 kW                                                           

  : Cantera Executed Simulations
