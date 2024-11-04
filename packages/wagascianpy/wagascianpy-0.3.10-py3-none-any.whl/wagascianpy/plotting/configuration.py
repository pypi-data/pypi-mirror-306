#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# copyright 2020 pintaudi giorgio
#

import argparse
import sys
import time

import wagascianpy.plotting.topology as topol
from wagascianpy.analysis.analysis import WAGASCI_NCHIPS, WALLMRD_NCHIPS
from wagascianpy.utils.configuration import *


def _check_topology_sanity(dif, chip, channel):
    elements = [dif, chip, channel]
    if any(i < 0 for i in elements) and not all(i >= 0 for i in elements):
        raise ValueError("Or all of dif, chip, channel are >= 0, or no one should be!")
    if topol.DifIndex.is_wagasci(dif):
        if chip >= WAGASCI_NCHIPS:
            raise ValueError("WAGASCI chip ID {} is out of boundary {}".format(dif, WAGASCI_NCHIPS))
    elif topol.DifIndex.is_wallmrd(dif):
        if chip >= WALLMRD_NCHIPS:
            raise ValueError("WallMRD chip ID {} is out of boundary {}".format(dif, WALLMRD_NCHIPS))
    else:
        ValueError("DIF ID {} not recognized".format(dif))


def fill_configuration(args=None):
    # type: (Optional[[argparse.Namespace, Dict[str, Any]]]) -> None
    """
    Take as input the parsed arguments from command line and return the Configuration object
    :param args: parsed arguments
    :return: Configuration object
    """

    if isinstance(args, argparse.Namespace):
        args = vars(args)

    # plotting configuration
    output_string = args["output_string"]
    output_path = args["output_path"]
    delivered_pot = args["delivered_pot"]
    accumulated_pot = args["accumulated_pot"]
    bsd_spill_history = args["bsd_spill_history"]
    wagasci_spill_history = args["wagasci_spill_history"]
    wagasci_spill_number = args["wagasci_spill_number"]
    wagasci_fixed_spill = args["wagasci_fixed_spill"]
    temperature = args["temperature"]
    humidity = args["humidity"]
    gain_history = args["gain_history"]
    dark_noise_history = args["dark_noise_history"]
    threshold_history = args["threshold_history"]
    bcid_history = args["bcid_history"]
    all_plotters = args["all"]
    run_markers = args["run_markers"]
    maintenance_markers = args["maintenance_markers"]
    trouble_markers = args["trouble_markers"]
    bsd_markers = args["bsd_markers"]
    topology = args["topology"]
    only_good = args["only_good"]
    save_tfile = args["save_tfile"]
    randomize_channels = args["randomize_channels"]
    dif = args["dif"]
    chip = args["chip"]
    channel = args["channel"]
    # WAGASCI database configuration
    wagasci_database = args["wagasci_database"]
    wagasci_decoded_location = args["wagasci_decoded_location"]
    # BSD database configuration
    bsd_database = args["bsd_database"]
    bsd_repository = args["bsd_repository"]
    bsd_download_location = args["bsd_download_location"]
    # global configuration
    t2krun = args["t2krun"]
    history_location = args["history_location"]
    # run selectors
    start_time = args["start_time"]
    stop_time = args["stop_time"]
    start_run = args["start_run"]
    stop_run = args["stop_run"]

    # wagasci database configuration
    if not wagasci_database:
        wagasci_database = Configuration.wagascidb.wagasci_database()
    if not wagasci_decoded_location:
        wagasci_decoded_location = Configuration.wagascidb.wagasci_decoded_location()

    # bsd database configuration
    if not bsd_database:
        bsd_database = Configuration.bsddb.bsd_database()
    if not bsd_download_location:
        bsd_download_location = Configuration.bsddb.bsd_download_location()
    if not bsd_repository:
        bsd_repository = Configuration.bsddb.bsd_repository()

    # global configuration
    if not t2krun:
        t2krun = Configuration.global_configuration.t2krun()
    if not history_location:
        history_location = Configuration.global_configuration.history_location()

    # sanity checks
    if all_plotters:
        delivered_pot = accumulated_pot = bsd_spill_history = wagasci_spill_history = True
        wagasci_spill_number = wagasci_fixed_spill = temperature = humidity = True
        gain_history = dark_noise_history = threshold_history = True

    if randomize_channels > 0:
        dif = chip = channel = -1
    elif dif >= 0 or chip >= 0 or channel >= 0:
        _check_topology_sanity(dif=dif, chip=chip, channel=channel)

    start = start_run if start_run else start_time
    stop = stop_run if stop_run else stop_time

    if start and stop and not wagasci_database:
        raise KeyError("WAGASCI database must also be specified if start and stop arguments are used")

    # WAGASCI database configuration
    Configuration.wagascidb.override({
        'wagasci_database': wagasci_database,
        'wagasci_decoded_location': wagasci_decoded_location
    })

    # BSD database configuration
    Configuration.bsddb.override({
        'bsd_database': bsd_database,
        'bsd_download_location': bsd_download_location,
        'bsd_repository': bsd_repository
    })

    # global configuration
    Configuration.global_configuration.override({
        't2krun': t2krun,
        'history_location': history_location
    })

    # plotter configuration
    Configuration.create_section('plotter')
    Configuration.plotter.override({
        'output_string': output_string,
        'output_path': output_path,
        'delivered_pot': delivered_pot,
        'accumulated_pot': accumulated_pot,
        'bsd_spill_history': bsd_spill_history,
        'wagasci_spill_history': wagasci_spill_history,
        'wagasci_spill_number': wagasci_spill_number,
        'wagasci_fixed_spill': wagasci_fixed_spill,
        'temperature': temperature,
        'humidity': humidity,
        'gain_history': gain_history,
        'dark_noise_history': dark_noise_history,
        'threshold_history': threshold_history,
        'bcid_history': bcid_history,
        'run_markers': run_markers,
        'maintenance_markers': maintenance_markers,
        'trouble_markers': trouble_markers,
        'bsd_markers': bsd_markers,
        'save_tfile': save_tfile,
        'topology': topology,
        'randomize_channels': randomize_channels,
        'dif': dif,
        'chip': chip,
        'channel': channel,
        'only_good': only_good
    })

    # run selectors
    Configuration.create_section('run_select')
    Configuration.run_select.override({
        'start': start,
        'stop': stop,
    })

    print("CONFIGURATION:")
    Configuration.dump()
    sys.stdout.flush()
    time.sleep(1)
