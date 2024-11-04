#!python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import os
import sys

import wagascianpy.plotting.detector
import wagascianpy.plotting.marker
import wagascianpy.plotting.parse_args
import wagascianpy.plotting.plotter
import wagascianpy.utils.utils
from wagascianpy.plotting.configuration import Configuration


def history_plotter(plotter):
    plotter.template_plotter()


if __name__ == "__main__":

    # Parse shell arguments
    args = wagascianpy.plotting.parse_args.parse_args(sys.argv[1:])

    # Edit the initial configuration
    wagascianpy.plotting.configuration.fill_configuration(args)

    if not os.path.exists(Configuration.plotter.output_path()):
        wagascianpy.utils.utils.mkdir_p(Configuration.plotter.output_path())

    markers = wagascianpy.plotting.marker.MarkerTuple(
        run=Configuration.plotter.run_markers(),
        maintenance=Configuration.plotter.maintenance_markers(),
        trouble=Configuration.plotter.trouble_markers(),
        bsd=Configuration.plotter.bsd_markers())

    output_file_format = os.path.join(Configuration.plotter.output_path(),
                                      "%s_{name}.pdf" % Configuration.plotter.output_string())

    topology_str = Configuration.plotter.topology()
    topology = wagascianpy.plotting.parse_args.parse_plotting_topology(topology_str) if topology_str else None

    if Configuration.bsddb.bsd_download_location():
        bsd_location = Configuration.bsddb.bsd_download_location()
    else:
        bsd_location = Configuration.bsddb.bsd_repository()

    if Configuration.plotter.delivered_pot():
        history_plotter(
            wagascianpy.plotting.plotter.BsdPotPlotter(
                output_file_path=output_file_format.format(name='bsd_pot_history'),
                bsd_database=Configuration.bsddb.bsd_database(),
                bsd_repository=bsd_location,
                wagasci_database=Configuration.wagascidb.wagasci_database(),
                t2krun=Configuration.global_configuration.t2krun(),
                start=Configuration.run_select.start(),
                stop=Configuration.run_select.stop(),
                markers=markers,
                save_tfile=Configuration.run_select.save_tfile()))

    if Configuration.plotter.accumulated_pot():
        history_plotter(wagascianpy.plotting.plotter.WagasciPotPlotter(
            output_file_path=output_file_format.format(name='pot_history'),
            bsd_database=Configuration.bsddb.bsd_database(),
            bsd_repository=bsd_location,
            wagasci_database=Configuration.wagascidb.wagasci_database(),
            wagasci_repository=Configuration.wagascidb.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            only_good=Configuration.plotter.only_good(),
            start=Configuration.run_select.start(),
            stop=Configuration.run_select.stop(),
            markers=markers,
            save_tfile=Configuration.run_select.save_tfile()))

    if Configuration.plotter.bsd_spill_history():
        history_plotter(wagascianpy.plotting.plotter.BsdSpillPlotter(
            output_file_path=output_file_format.format(name='bsd_spill_history'),
            bsd_database=Configuration.bsddb.bsd_database(),
            bsd_repository=bsd_location,
            wagasci_database=Configuration.wagascidb.wagasci_database(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select.start(),
            stop=Configuration.run_select.stop(),
            markers=markers,
            save_tfile=Configuration.run_select.save_tfile()))

    if Configuration.plotter.wagasci_spill_history():
        history_plotter(wagascianpy.plotting.plotter.WagasciSpillHistoryPlotter(
            output_file_path=output_file_format.format(name='wg_spill_history'),
            bsd_database=Configuration.bsddb.bsd_database(),
            bsd_repository=bsd_location,
            wagasci_database=Configuration.wagascidb.wagasci_database(),
            wagasci_repository=Configuration.wagascidb.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select.start(),
            stop=Configuration.run_select.stop(),
            markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select.save_tfile()))

    if Configuration.plotter.wagasci_fixed_spill():
        history_plotter(wagascianpy.plotting.plotter.WagasciFixedSpillPlotter(
            output_file_path=output_file_format.format(name='wg_fixed_spill_history'),
            bsd_database=Configuration.bsddb.bsd_database(),
            bsd_repository=bsd_location,
            wagasci_database=Configuration.wagascidb.wagasci_database(),
            wagasci_repository=Configuration.wagascidb.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select.start(),
            stop=Configuration.run_select.stop(),
            markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select.save_tfile()))

    if Configuration.plotter.wagasci_spill_number():
        history_plotter(wagascianpy.plotting.plotter.WagasciSpillNumberPlotter(
            output_file_path=output_file_format.format(name='wg_spill_number'),
            bsd_database=Configuration.bsddb.bsd_database(),
            bsd_repository=bsd_location,
            wagasci_database=Configuration.wagascidb.wagasci_database(),
            wagasci_repository=Configuration.wagascidb.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select.start(),
            stop=Configuration.run_select.stop(),
            markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select.save_tfile()))

    if Configuration.plotter.temperature():
        history_plotter(wagascianpy.plotting.plotter.TemperaturePlotter(
            output_file_path=output_file_format.format(name='temperature_history'),
            bsd_database=Configuration.bsddb.bsd_database(),
            bsd_repository=bsd_location,
            wagasci_database=Configuration.wagascidb.wagasci_database(),
            wagasci_repository=Configuration.wagascidb.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select.start(),
            stop=Configuration.run_select.stop(),
            markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select.save_tfile()))

    if Configuration.plotter.humidity():
        history_plotter(wagascianpy.plotting.plotter.HumidityPlotter(
            output_file_path=output_file_format.format(name='humidity_history'),
            bsd_database=Configuration.bsddb.bsd_database(),
            bsd_repository=bsd_location,
            wagasci_database=Configuration.wagascidb.wagasci_database(),
            wagasci_repository=Configuration.wagascidb.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select.start(),
            stop=Configuration.run_select.stop(),
            markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select.save_tfile()))

    if Configuration.plotter.bcid_history():
        history_plotter(wagascianpy.plotting.plotter.BcidPlotter(
            output_file_path=output_file_format.format(name='bcid_history'),
            bsd_database=Configuration.bsddb.bsd_database(),
            bsd_repository=bsd_location,
            wagasci_database=Configuration.wagascidb.wagasci_database(),
            wagasci_repository=Configuration.wagascidb.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select.start(),
            stop=Configuration.run_select.stop(),
            markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select.save_tfile()))

    if Configuration.plotter.gain_history() and not Configuration.plotter.randomize_channels() > 0 \
            and Configuration.plotter.channel() == -1:
        history_plotter(wagascianpy.plotting.plotter.GainHistoryPlotterDif(
            output_file_path=output_file_format.format(name='gain_dif_history'),
            history_location=Configuration.global_configuration.history_location(),
            markers=markers,
            start=Configuration.run_select.start(),
            stop=Configuration.run_select.stop(),
            wagasci_database=Configuration.wagascidb.wagasci_database(),
            topology=topology,
            save_tfile=Configuration.run_select.save_tfile()))

    if Configuration.plotter.dark_noise_history() and not Configuration.plotter.randomize_channels() > 0 \
            and Configuration.plotter.channel() == -1:
        history_plotter(wagascianpy.plotting.plotter.DarkNoiseHistoryPlotterDif(
            output_file_path=output_file_format.format(name='dark_noise_dif_history'),
            history_location=Configuration.global_configuration.history_location(),
            markers=markers,
            start=Configuration.run_select.start(),
            stop=Configuration.run_select.stop(),
            wagasci_database=Configuration.wagascidb.wagasci_database(),
            topology=topology,
            save_tfile=Configuration.run_select.save_tfile()))

    if Configuration.plotter.threshold_history() and not Configuration.plotter.randomize_channels() > 0 \
            and Configuration.plotter.channel() == -1:
        history_plotter(wagascianpy.plotting.plotter.ThresholdHistoryPlotterDif(
            output_file_path=output_file_format.format(name='threshold_dif_history'),
            history_location=Configuration.global_configuration.history_location(),
            markers=markers,
            start=Configuration.run_select.start(),
            stop=Configuration.run_select.stop(),
            wagasci_database=Configuration.wagascidb.wagasci_database(),
            topology=topology,
            save_tfile=Configuration.run_select.save_tfile()))

    nentries = Configuration.plotter.randomize_channels()
    if nentries <= 0 and Configuration.plotter.dif() >= 0 and Configuration.plotter.chip() >= 0 and \
            Configuration.plotter.channel() >= 0:
        difs = [Configuration.plotter.dif()]
        chips = [Configuration.plotter.chip()]
        channels = [Configuration.plotter.channel()]
    elif nentries > 0:
        difs = wagascianpy.utils.utils.randomize(nentries, 0, 8)
        chips = wagascianpy.utils.utils.randomize(nentries, 0, 20)
        channels = wagascianpy.utils.utils.randomize(nentries, 0, 32)
    else:
        difs = chips = channels = []
    random_channels = zip(difs, chips, channels)
    for random_channel in random_channels:
        dif = random_channel[0]
        chip = random_channel[1]
        channel = random_channel[2]
        if wagascianpy.plotting.detector.DifIndex.is_wallmrd(dif):
            chip = chip % 3
        name = "{{}}_history_dif{}_chip{}_chan{}".format(dif, chip, channel)
        if Configuration.plotter.gain_history():
            history_plotter(wagascianpy.plotting.plotter.GainHistoryPlotterChannel(
                output_file_path=output_file_format.format(name=name.format("gain")),
                history_location=Configuration.global_configuration.history_location(),
                markers=markers,
                start=Configuration.run_select.start(),
                stop=Configuration.run_select.stop(),
                wagasci_database=Configuration.wagascidb.wagasci_database(),
                dif=dif,
                chip=chip,
                channel=channel,
                save_tfile=Configuration.run_select.save_tfile()))

        if Configuration.plotter.dark_noise_history():
            history_plotter(wagascianpy.plotting.plotter.DarkNoiseHistoryPlotterChannel(
                output_file_path=output_file_format.format(name=name.format("dark_noise")),
                history_location=Configuration.global_configuration.history_location(),
                markers=markers,
                start=Configuration.run_select.start(),
                stop=Configuration.run_select.stop(),
                wagasci_database=Configuration.wagascidb.wagasci_database(),
                dif=dif,
                chip=chip,
                channel=channel,
                save_tfile=Configuration.run_select.save_tfile()))

        if Configuration.plotter.threshold_history():
            history_plotter(wagascianpy.plotting.plotter.ThresholdHistoryPlotterChannel(
                output_file_path=output_file_format.format(name=name.format("hit_threshold")),
                history_location=Configuration.global_configuration.history_location(),
                markers=markers,
                start=Configuration.run_select.start(),
                stop=Configuration.run_select.stop(),
                wagasci_database=Configuration.wagascidb.wagasci_database(),
                dif=dif,
                chip=chip,
                channel=channel,
                save_tfile=Configuration.run_select.save_tfile()))
