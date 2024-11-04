Analysis sequence
=================

To extrapolate the pedestal we need at least to measure the 1 PEU and
2 PEU peaks. We chose to measure those peaks in two different
acquisitions. We first set the threshold at 0.5 PEU level and measure
the 1 PEU peak and the set the threashold at 1.5 PEU level and measure
the 2 PEU peak. Then we combine these measurements to extrapolate the
pedestal.

#. `wgDecoder` : Decode the data into a tree.root file
#. `wgMakeHist` : Fill various histograms into the hist.root file
#. `wgAnaHist` : Fit the histograms and save the result into xml
   files. In particular the 1 PEU peak and 2 PEU peak positions are
   fitted.
#. `wgAnaHistSummary` : Organize and put in order the xml files from
   the previous step.
#. `wgAnaPedestal` : Extrapolate the pedestal as shown in the previous
   section.

.. figure:: ../images/pedestal_run_folder_tree.png
            :width: 1200px

            Folder tree of the pedestal_run script
