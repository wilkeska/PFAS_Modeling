# Instructions

1. Run [netj_generate.ipynb](netj_generate.ipynb "netj_generate.ipynb") to generate input files from lists of run conditions
2. Run [cfs_batchrun.ipynb](cfs_batchrun.ipynb) to send the generated .netj files to CFS and run the simulations
3. Run [PFRTP-Garrett.ipynb](PFRTP-Garrett.ipynb) to use Cantera to perform the same simulations. This will generate dot files for the path diagram created by the Cantera simulation, which will be used to select which species are relevant for the CFS path diagram. (Not all species available should be chosen, as CFS *will* crash)
4. Run [cfs_post.ipynb](cfs_post.ipynb), and select .netj files. The program will run the GUI form of CFS, and use the dot file from PFRTP-Garrett Cantera simulation of the same conditions to choose which species data to include in the vtk file. The program can handle multiple files, and will go through them in sequence. `<font color=red>` **IMPORTANT** `</font>` DO NOT MOVE THE MOUSE UNTIL THE SCRIPT COMPLETES!
5. Run [cfs2canteraPD_stable.ipynb](cfs2canteraPD_stable.ipynb) to generate path diagrams using Cantera from the streamline_pp.vtk file. Path diagrams are specific to trajectory, residence time, and the threshold for the minimum relative flux to qualify as a major species.

# Problems

1. Residence Time column from cantera has no duplicate times. CFS will have 3-7 rows of identical times
2. Concentrations of non-major species in cantera are around 1e-100, in CFS they are around 1e-15
   1. Produces problems for reaction path diagrams because cantera can’t tell which is the major species
   2. Concentrations are all 0 until injection, then they all instantly increase
   3. CFS spray settings may introduce significant concentrations from transient phase?
3. CF3Or has ~15 reactions, CF2s has ~74, CF4 ~15, C2F6 ~6. C2F6 behavior in path diagrams may be caused by incomplete reactions
4. Several reactions are “ambiguous” and cantera will use the designated default reaction
   1. Default reaction may not be conducive for simulating C2F6
5. Some reactions are not parsed (they may just not be relevant)
6. cfs2canteraPD will create a valid path diagram for CF4 at 45kW injected at port 4. Tolerance = 0.0001, cutoff = 1e-20, threshold = 0.01. Will not create valid diagram for CF3CF3 in any condition, or CF4 in conditons:
7. PFRTP-Garrett does not make valid diagrams for CF4 @ 27.5 kW

<table border="1">
<caption><h4>Validated Path Diagrams - CFS</h4></caption>
<thead>
  <tr><!-- headers -->
    <th ></th>
    <th colspan="4" style="border-right: 2px solid white; border-left: 2px solid white; text-align: center">CF4</th>
    <th colspan="4" style="border-right: 2px solid white; text-align: center">CHF3</th>
    <th colspan="4" style="border-right: 2px solid white; text-align: center">C2F6 ✗</th>
  </tr>
</thead>
  <tr>
    <td rowspan="2" style="border-right: 2px solid white; border-left: 2px solid white;"></td>
    <td colspan="4" style="border-right: 2px solid white; text-align: center">Ports</td>
    <td colspan="4" style="border-right: 2px solid white; text-align: center">Ports</td>
    <td colspan="4" style="border-right: 2px solid white; text-align: center">Ports</td>
  </tr>
  <tr>
    <td style="border-bottom: 2px solid white;">1</td>
    <td style="border-bottom: 2px solid white;">4</td>
    <td style="border-bottom: 2px solid white;">6</td>
    <td style="border-right: 2px solid white;border-bottom: 2px solid white;">8</td>
    <td style="border-bottom: 2px solid white;">1</td>
    <td style="border-bottom: 2px solid white;">4</td>
    <td style="border-bottom: 2px solid white;">6</td>
    <td style="border-right: 2px solid white;border-bottom: 2px solid white;">8</td>
    <td style="border-bottom: 2px solid white;">1</td>
    <td style="border-bottom: 2px solid white;">4</td>
    <td style="border-bottom: 2px solid white;">6</td>
    <td style="border-right: 2px solid white;border-bottom: 2px solid white;">8</td>
  </tr>
  <tr>
    <td style="border-right: 2px solid white; border-left: 2px solid white;">27.5 kW</td>
    <td colspan="1">    </td> <!-- CF4 1-->
    <td colspan="1">    </td> <!-- CF4 4-->
    <td colspan="1">    </td> <!-- CF4 6-->
    <td colspan="1"  style="border-right: 2px solid white;">      </td> <!-- CF4 8-->
    <td colspan="1">    </td><!-- CHF3 1-->
    <td colspan="1">    </td><!-- CHF3 4-->
    <td colspan="1">    </td><!-- CHF3 6-->
    <td colspan="1" style="border-right: 2px solid white;">    </td><!-- CHF3 8-->
    <td colspan="1">  ✗  </td><!-- C2F6 1-->
    <td colspan="1">    </td><!-- C2F6 4-->
    <td colspan="1">    </td><!-- C2F6 6-->
    <td colspan="1" style="border-right: 2px solid white;"> ✗   </td><!-- C2F6 8-->
  </tr>
  <tr>
    <td style="border-right: 2px solid white; border-left: 2px solid white; border-bottom: 2px solid white;">45 kW</td>
    <td colspan="1" style="border-bottom: 2px solid white;">   ✗   </td><!-- CF4 1-->
    <td colspan="1" style="border-bottom: 2px solid white;">   ✓   </td><!-- CF4 4-->
    <td colspan="1" style="border-bottom: 2px solid white;">      </td><!-- CF4 6-->
    <td colspan="1" style="border-right: 2px solid white; border-bottom: 2px solid white;">     </td> <!-- CF4 8-->
    <td colspan="1" style="border-bottom: 2px solid white;">      </td><!-- CHF3 1-->
    <td colspan="1" style="border-bottom: 2px solid white;">      </td><!-- CHF3 4-->
    <td colspan="1" style="border-bottom: 2px solid white;">      </td><!-- CHF3 6-->
    <td colspan="1" style="border-right: 2px solid white; border-bottom: 2px solid white;" >    </td> <!-- CHF3 8-->
    <td colspan="1" style="border-bottom: 2px solid white;">   ✗(?)   </td><!-- C2F6 1-->
    <td colspan="1" style="border-bottom: 2px solid white;">  ✗    </td><!-- C2F6 4-->
    <td colspan="1" style="border-bottom: 2px solid white;">      </td><!-- C2F6 6-->
    <td colspan="1" style="border-right: 2px solid white; border-bottom: 2px solid white;">   ✗  </td> <!-- C2F6 8-->
  </tr>
</table>

<table border="1">
<caption><h4>Validated Path Diagrams - Cantera</h4></caption>
<thead>
  <tr><!-- headers -->
    <th ></th>
    <th colspan="4" style="border-right: 2px solid white; border-left: 2px solid white; text-align: center">CF4</th>
    <th colspan="4" style="border-right: 2px solid white; text-align: center">CHF3</th>
    <th colspan="4" style="border-right: 2px solid white; text-align: center">C2F6</th>
  </tr>
</thead>
  <tr>
    <td rowspan="2" style="border-right: 2px solid white; border-left: 2px solid white;"></td>
    <td colspan="4" style="border-right: 2px solid white; text-align: center">Ports</td>
    <td colspan="4" style="border-right: 2px solid white; text-align: center">Ports</td>
    <td colspan="4" style="border-right: 2px solid white; text-align: center">Ports</td>
  </tr>
  <tr>
    <td style="border-bottom: 2px solid white;">1</td>
    <td style="border-bottom: 2px solid white;">4</td>
    <td style="border-bottom: 2px solid white;">6</td>
    <td style="border-right: 2px solid white;border-bottom: 2px solid white;">8</td>
    <td style="border-bottom: 2px solid white;">1</td>
    <td style="border-bottom: 2px solid white;">4</td>
    <td style="border-bottom: 2px solid white;">6</td>
    <td style="border-right: 2px solid white;border-bottom: 2px solid white;">8</td>
    <td style="border-bottom: 2px solid white;">1</td>
    <td style="border-bottom: 2px solid white;">4</td>
    <td style="border-bottom: 2px solid white;">6</td>
    <td style="border-right: 2px solid white;border-bottom: 2px solid white;">8</td>
  </tr>
  <tr>
    <td style="border-right: 2px solid white; border-left: 2px solid white;">27.5 kW</td>
    <td colspan="1"> ✗   </td> <!-- CF4 1-->
    <td colspan="1">  ✗  </td> <!-- CF4 4-->
    <td colspan="1">  ✗  </td> <!-- CF4 6-->
    <td colspan="1"  style="border-right: 2px solid white;">  ✗    </td> <!-- CF4 8-->
    <td colspan="1">    </td><!-- CHF3 1-->
    <td colspan="1">    </td><!-- CHF3 4-->
    <td colspan="1">    </td><!-- CHF3 6-->
    <td colspan="1" style="border-right: 2px solid white;">    </td><!-- CHF3 8-->
    <td colspan="1">  ✓  </td><!-- C2F6 1-->
    <td colspan="1">   ✓ </td><!-- C2F6 4-->
    <td colspan="1">  ✓  </td><!-- C2F6 6-->
    <td colspan="1" style="border-right: 2px solid white;">  ✓  </td><!-- C2F6 8-->
  </tr>
  <tr>
    <td style="border-right: 2px solid white; border-left: 2px solid white; border-bottom: 2px solid white;">45 kW</td>
    <td colspan="1" style="border-bottom: 2px solid white;"> ✓     </td><!-- CF4 1-->
    <td colspan="1" style="border-bottom: 2px solid white;"> ✓     </td><!-- CF4 4-->
    <td colspan="1" style="border-bottom: 2px solid white;">  ✓    </td><!-- CF4 6-->
    <td colspan="1" style="border-right: 2px solid white; border-bottom: 2px solid white;">  ✓   </td> <!-- CF4 8-->
    <td colspan="1" style="border-bottom: 2px solid white;">      </td><!-- CHF3 1-->
    <td colspan="1" style="border-bottom: 2px solid white;">      </td><!-- CHF3 4-->
    <td colspan="1" style="border-bottom: 2px solid white;">      </td><!-- CHF3 6-->
    <td colspan="1" style="border-right: 2px solid white; border-bottom: 2px solid white;" >    </td> <!-- CHF3 8-->
    <td colspan="1" style="border-bottom: 2px solid white;">  ✓    </td><!-- C2F6 1-->
    <td colspan="1" style="border-bottom: 2px solid white;">   ✓   </td><!-- C2F6 4-->
    <td colspan="1" style="border-bottom: 2px solid white;">   ✓   </td><!-- C2F6 6-->
    <td colspan="1" style="border-right: 2px solid white; border-bottom: 2px solid white;"> ✓    </td> <!-- C2F6 8-->
  </tr>
</table>
