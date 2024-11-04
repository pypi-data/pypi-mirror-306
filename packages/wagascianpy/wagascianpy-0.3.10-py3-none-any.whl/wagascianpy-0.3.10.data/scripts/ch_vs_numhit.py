#!python
# -*- coding: utf-8 -*-

import ROOT

if __name__ == "__main__":
    # Path to the ROOT file
    # input_root_file = "/Users/akihiro/SynologyDrive/研究/WAGASCI/片山/analysis/data/physics_run_2020-02-11_22-23-18_106_ecal_dif_0_tree.root";
    input_root_file = "/Users/akihiro/SynologyDrive/研究/WAGASCI/片山/analysis/data/physics_run_2020-02-11_22-23-18_106_ecal_dif_4_tree.root";
    # TFile object
    tfile = ROOT.TFile(input_root_file, "READ")
    # get TTree from TFile
    ttree = tfile.Get("raw")
    # create canvas

    # Print image to file
    # create TCanvas of 1280x720 pixels
    tcanvas = ROOT.TCanvas("c1", "c1", 1280, 720)
    # ttree.Draw("charge[0][0][0]")
    # ttree.Draw("hit[0][0][0]")
    # tcanvas.Print("/Users/akihiro/Desktop/test2.png")

    # Loop example
    NCOLUMNS = 16
    NCHANNELS = 36
    NCHIPS = 20

    counter = 0
    
    histo = ROOT.TH1D("ch_vs_numhit", "ch vs num hit", 720, 0, 720)
    for event in ttree:
        print(counter)
        for chip in range(int(NCHIPS)):
            for channel in range(int(NCHANNELS)):
                for column in range(int(NCOLUMNS)):
                    chipid = event.chipid[chip]
                    channelid = event.chanid[channel]
                    columnid = event.colid[column]
                    # columnid = 0
                    if event.hit[columnid + NCOLUMNS * channelid + NCOLUMNS * NCHANNELS * chipid] == 1:
                        histo.AddBinContent(channelid + NCHANNELS * chipid)

        # break after 10 spills to not have too long output
        counter += 1
        # if counter == 1:
        #     break

    histo.Draw();
    tcanvas.Print("/Users/akihiro/Desktop/test3.png")
