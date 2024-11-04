#!python
# -*- coding: utf-8 -*-

import ROOT

if __name__ == "__main__":
    # Path to the ROOT file
#    input_root_file = "/home/neo/Desktop/test_ecal_dif_5_tree.root"
    input_root_file = "/Users/akihiro/SynologyDrive/研究/WAGASCI/片山/analysis/data/physics_run_2020-02-11_22-23-18_106_ecal_dif_0_tree.root";
    # TFile object
    tfile = ROOT.TFile(input_root_file, "READ")
    # get TTree from TFile
    ttree = tfile.Get("raw")
    # create canvas

    # Print image to file
    # create TCanvas of 1280x720 pixels
    tcanvas = ROOT.TCanvas("c1", "c1", 1280, 720)
    ttree.Draw("spill_number")
    tcanvas.Print("/Users/akihiro/Desktop/test.png")

    # Loop example
    counter = 0
    for event in ttree:
        print(event.spill_number)
        # break after 10 spills to not have too long output
        counter += 1
        if counter == 10:
            break
