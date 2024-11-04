#!python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio, Eguchi Aoi

""" Script to analyze the S-curve data of the SPIROC2D ASIC """

# Python modules
import json
import argparse
import multiprocessing
import os

import ROOT
from bitarray import bitarray

# WAGASCI modules
from wagascianpy.analysis.analysis import WagasciAnalysis
from wagascianpy.utils.environment import WagasciEnvironment
from wagascianpy.utils.utils import list_dir_with_integer

MAX_NB_THREAD_CHAINS = 16


# ================================================================ #
#                                                                  #
#                        Analysis functions                        #
#                                                                  #
# ================================================================ #

def scurve_decoder(wagasci_lib, threshold_dir, acq_name, dif, n_chips, overwrite_flag=True):
    """ wgDecoder for the scurve_run.py script """
    wg_ana = WagasciAnalysis(wagasci_lib)
    dif = int(dif)
    n_chips = int(n_chips)
    input_raw_file = os.path.join(threshold_dir, "RawData", "%s_ecal_dif_%d.raw" % (acq_name, dif))
    output_dir = os.path.join(threshold_dir, "wgDecoder")
    compatibility_mode = False
    return wg_ana.decoder(input_raw_file, "", output_dir, overwrite_flag, compatibility_mode, dif, n_chips)


def scurve_make_hist(wg_ana, threshold_dir, acq_name, dif, acq_config_xml):
    """ wgMakeHist for the pedestal_run.py script """
    dif = int(dif)
    input_tree_file = os.path.join(threshold_dir, "wgDecoder", "%s_ecal_dif_%d_tree.root" % (acq_name, dif))
    output_dir = os.path.join(threshold_dir, "wgMakeHist")
    flags = bitarray('0' * 9, endian='big')
    flags[7] = True  # dark noise
    flags[0] = True  # overwrite
    ul_flags = int(flags.to01(), 2)
    return wg_ana.make_hist(input_tree_file, acq_config_xml, output_dir, ul_flags, dif)


def scurve_ana_hist(wg_ana, threshold_dir, acq_name, dif, acq_config_xml):
    """ wgAnaHist for the pedestal_run.py script """
    dif = int(dif)
    input_hist_file = os.path.join(threshold_dir, "wgMakeHist", "%s_ecal_dif_%d_hist.root" % (acq_name, dif))
    output_dir = os.path.join(threshold_dir, "wgAnaHist", "Xml", "dif%d" % dif)
    output_img_dir = os.path.join(threshold_dir, "wgAnaHist", "Images", "dif%d" % dif)
    flags = bitarray('0' * 8, endian='big')
    flags[7] = True  # overwrite
    flags[6] = bool(acq_config_xml)
    flags[5] = False  # print
    flags[4] = True  # Dark noise
    ul_flags = int(flags.to01(), 2)
    return wg_ana.ana_hist(input_hist_file, acq_config_xml, output_dir, output_img_dir, ul_flags, dif)


def scurve_ana_hist_summary(wg_ana, threshold_dir, dif):
    """ wgAnaHistSummary for the pedestal_run.py script """
    dif = int(dif)
    input_dir = os.path.join(threshold_dir, "wgAnaHist", "Xml", "dif%d" % dif)
    output_xml_dir = os.path.join(threshold_dir, "wgAnaHistSummary", "Xml", "dif%d" % dif)
    output_img_dir = os.path.join(threshold_dir, "wgAnaHistSummary", "Images", "dif%d" % dif)
    flags = bitarray('0' * 8, endian='big')
    flags[7] = True  # overwrite
    flags[5] = False  # print
    flags[4] = True  # Dark noise
    ul_flags = int(flags.to01(), 2)
    return wg_ana.ana_hist_summary(input_dir, output_xml_dir, output_img_dir, ul_flags)


def scurve_scurve(wg_ana, run_root_dir):
    """ wgScurve for the scurve_run.py script """
    output_dir = os.path.join(run_root_dir, "wgScurve", "Xml")
    output_img_dir = os.path.join(run_root_dir, "wgScurve", "Images")
    paranoid_mode = False
    return wg_ana.scurve(run_root_dir, output_dir, output_img_dir, paranoid_mode)


# ================================================================ #
#                                                                  #
#                          scurve_analysis                         #
#                                                                  #
# ================================================================ #

def scurve_analysis(run, decoder=True, makehist=True, anahist=True, overwrite=False):
    """ S-curve run """

    decoder = bool(decoder)
    makehist = bool(makehist)
    anahist = bool(anahist)
    overwrite = bool(overwrite)

    # Environmental variables
    env = WagasciEnvironment()
    wagasci_lib = env["WAGASCI_LIBDIR"]

    if not os.path.exists(run):
        run = os.path.join(env['WAGASCI_CALIBDATADIR'], run)

    run_name = os.path.basename(run)
    run_root_dir = run
    acq_config_path = os.path.join(run_root_dir, os.path.basename(env['WAGASCI_ACQCONFIGDIR']))
    acq_config_xml = os.path.join(acq_config_path, env['WAGASCI_ACQCONFIGXML'])
    if not os.path.exists(acq_config_xml):
        print("Acquisition configuration XML file not found : %s" % acq_config_xml)

    # =========================================================== #
    #                        ANALYZE DATA                         #
    # =========================================================== #

    wg_ana = WagasciAnalysis(wagasci_lib)
    topology_string, pointer = wg_ana.get_dif_topology(acq_config_xml)
    dif_topology = json.loads(topology_string)
    wg_ana.free_topology(pointer)
    wg_ana.enable_thread_safety()
    del wg_ana

    ###########################################################################
    #                                 decoder                                 #
    ###########################################################################

    if decoder:

        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        results = {}

        idac_dirs = list_dir_with_integer(run_root_dir)

        for idac, idac_dir in idac_dirs:
            threshold_dirs = list_dir_with_integer(os.path.join(run_root_dir, idac_dir))
            for threshold, threshold_dir in threshold_dirs:
                threshold_dir = os.path.join(run_root_dir, idac_dir, threshold_dir)
                acq_name = "%s_iDAC%s_threshold%s" % (run_name, idac, threshold)
                for dif in dif_topology:
                    filepath = os.path.join(threshold_dir, "wgDecoder", "%s_ecal_dif_%s_tree.root" % (acq_name, dif))
                    if not overwrite and os.path.exists(filepath):
                        tfile = ROOT.TFile(filepath, "READ")
                        if not tfile.IsZombie():
                            print("Skipping %s" % filepath)
                            continue
                        else:
                            print("Removing zombie file %s" % filepath)
                            os.remove(filepath)
                    n_chips = len(dif_topology[dif])
                    result = pool.apply_async(scurve_decoder,
                                              args=(wagasci_lib, threshold_dir, acq_name, dif, n_chips, overwrite))
                    results[filepath] = result
                # dif loop
            # threshold loop
        # idac loop

        # Wait until all the threads have returned
        have_errors = False
        for filepath, result in results.items():
            result = result.get()
            if result != 0:
                have_errors = True
                print("File {} returned error {}".format(filepath, result))

        if have_errors:
            choice = input("\nErrors happened during decoding : whould you like to continue? (yes, no) : ")
            if choice.lower() in ["n", "no"]:
                return -1

        pool.close()
        pool.terminate()
        pool.join()

    ###########################################################################
    #                                make_hist                                #
    ###########################################################################

    if makehist:

        idac_dirs = list_dir_with_integer(run_root_dir)

        for idac, idac_dir in idac_dirs:
            threshold_dirs = list_dir_with_integer(os.path.join(run_root_dir, idac_dir))
            for threshold, threshold_dir in threshold_dirs:
                threshold_dir = os.path.join(run_root_dir, idac_dir, threshold_dir)
                acq_name = "%s_iDAC%s_threshold%s" % (run_name, idac, threshold)
                actual_acq_config_xml = os.path.join(threshold_dir, "RawData", "%s.xml" % acq_name)
                for dif in dif_topology:
                    filepath = os.path.join(threshold_dir, "wgMakeHist", "%s_ecal_dif_%s_hist.root" % (acq_name, dif))
                    if not overwrite and os.path.exists(filepath):
                        tfile = ROOT.TFile(filepath, "READ")
                        if not tfile.IsZombie():
                            print("Skipping %s" % filepath)
                            continue
                        else:
                            print("Removing zombie file %s" % filepath)
                            os.remove(filepath)
                    wg_ana = WagasciAnalysis(wagasci_lib)
                    result = scurve_make_hist(wg_ana=wg_ana, threshold_dir=threshold_dir, acq_name=acq_name,
                                              dif=dif, acq_config_xml=actual_acq_config_xml)
                    if result != 0:
                        print("wgMakeHist returned error code %d" % result)
                        exit(result)
                    del wg_ana
                # dif loop
            # threshold loop
        # idac loop

    #############################################################################
    #                                   ana_hist                                #
    #############################################################################

    if anahist:

        idac_dirs = list_dir_with_integer(run_root_dir)

        for idac, idac_dir in idac_dirs:
            threshold_dirs = list_dir_with_integer(os.path.join(run_root_dir, idac_dir))
            for threshold, threshold_dir in threshold_dirs:
                threshold_dir = os.path.join(run_root_dir, idac_dir, threshold_dir)
                acq_name = "%s_iDAC%s_threshold%s" % (run_name, idac, threshold)
                actual_acq_config_xml = os.path.join(threshold_dir, "RawData", "%s.xml" % acq_name)
                for dif in dif_topology:
                    anahist_dirname = os.path.join(threshold_dir, "wgAnaHist", "Xml", "dif%s" % dif)
                    if not overwrite and os.path.exists(anahist_dirname):
                        print("Skipping %s" % anahist_dirname)
                        continue
                    wg_ana = WagasciAnalysis(wagasci_lib)
                    result = scurve_ana_hist(wg_ana=wg_ana, threshold_dir=threshold_dir, acq_name=acq_name,
                                             dif=dif, acq_config_xml=actual_acq_config_xml)
                    if result != 0:
                        print("wgAnaHist returned error code %d" % result)
                        exit(result)
                    del wg_ana
                # dif loop
            # peu loop
        # input_dac loop

    #############################################################################
    #                               ana_hist_summary                            #
    #############################################################################

    if anahist:

        idac_dirs = list_dir_with_integer(run_root_dir)

        for idac, idac_dir in idac_dirs:
            threshold_dirs = list_dir_with_integer(os.path.join(run_root_dir, idac_dir))
            for threshold, threshold_dir in threshold_dirs:
                threshold_dir = os.path.join(run_root_dir, idac_dir, threshold_dir)
                for dif in dif_topology:
                    anahist_dirname = os.path.join(threshold_dir, "wgAnaHistSummary", "Xml", "dif%s" % dif)
                    if not overwrite and os.path.exists(anahist_dirname):
                        print("Skipping %s" % anahist_dirname)
                        continue
                    wg_ana = WagasciAnalysis(wagasci_lib)
                    result = scurve_ana_hist_summary(wg_ana=wg_ana, threshold_dir=threshold_dir, dif=dif)
                    if result != 0:
                        print("wgAnaHistSummary returned error code %d" % result)
                        exit(result)
                    del wg_ana
                # dif loop
            # peu loop
        # input_dac loop

    #######################################################################
    #                           scurve analysis                           #
    #######################################################################

    wg_ana = WagasciAnalysis(wagasci_lib)
    result = scurve_scurve(wg_ana=wg_ana, run_root_dir=run_root_dir)
    del wg_ana
    if result != 0:
        print("wgScurve returned error code %d" % result)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description='Analyze the Scurve calibration data')

    PARSER.add_argument('-f', '--run', metavar='<run name or path>', type=str, required=True,
                        help='Name or path of the run to analyze. If only the run name is given the run must be inside '
                             'the ${WAGASCI_CALIBDATADIR} folder.')
    PARSER.add_argument('-d', '--disable-decoder', dest='decoder', action='store_false',
                        required=False, default=True, help="Disable the wgDecoder.")
    PARSER.add_argument('-m', '--disable-makehist', dest='makehist', action='store_false',
                        required=False, default=True, help="Disable the wgMakeHist.")
    PARSER.add_argument('-a', '--disable-anahist', dest='anahist', action='store_false',
                        required=False, default=True, help="Disable the wgAnaHist and wgAnaHistSummary.")
    PARSER.add_argument('-r', '--overwrite', dest='overwrite', action='store_true',
                        required=False, default=False, help="Overwrite flag.")

    ARGS = PARSER.parse_args()

    RUN = ARGS.run
    DECODER = ARGS.decoder
    MAKEHIST = ARGS.makehist
    ANAHIST = ARGS.anahist
    OVERWRITE = ARGS.overwrite

    scurve_analysis(RUN, DECODER, MAKEHIST, ANAHIST, OVERWRITE)
