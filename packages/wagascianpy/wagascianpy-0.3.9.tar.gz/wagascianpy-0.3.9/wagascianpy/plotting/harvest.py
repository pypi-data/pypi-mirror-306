#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

""" Module to retrieve the data to plot (both X axis and Y axis). The data source can be a BSD file or a WAGASCI file
or a slow device data. The module is implemented using the Strategy design pattern. Each way of collecting the data
is generically called harvester and corresponds to a different strategy. """

import abc
import collections
import operator
import os
import re
from typing import Optional, List, Any, Union, Tuple, Dict

import numpy
from six import string_types

import wagascianpy.analysis.analysis
import wagascianpy.analysis.beam_summary_data
import wagascianpy.analysis.spill as sp
import wagascianpy.database.db_record
import wagascianpy.database.wagascidb as wgdb
import wagascianpy.plotting.detector as detect
import wagascianpy.plotting.topology as topol
import wagascianpy.utils.treenames as treenames
import wagascianpy.utils.utils as utils
from wagascianpy.analysis.analysis import SPIROC2D_NCHANNELS, WAGASCI_NCHIPS, WALLMRD_NCHIPS

# import ROOT
try:
    import ROOT

    ROOT.PyConfig.IgnoreCommandLineOptions = True
except ImportError as err:
    if "ROOT" in repr(err):
        ROOT = None
    else:
        raise

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

# value of the hit TBranch in the raw data TTree when a hit is found
_HIT = 1
# number of columns in a channel
_NCOLUMNS = 16
# number of active channels in a chip
_NCHANNELS = 32
# number of chips in WAGASCI
_NCHIPS_WAGASCI = 20
# number of chips in WallMRD
_CHIPS_WALLMRD = 3


class Patron(object):
    """
    The Patron defines the interface of interest to clients.
    """

    def __init__(self, start=None, stop=None, wagasci_database=None, harvester=None):
        """
        Usually, the Patron accepts a harvester through the constructor, but
        also provides a setter to change it at runtime.
        :param start: start run or start time
        :param stop: stop run or stop time
        :param wagasci_database: wagasci database location
        :param harvester: harvester class
        """
        # type: (Optional[Union[str, int]], Optional[Union[str, int]], Optional[str], Optional[Harvester])
        self._start = start  # type: Optional[Union[str, int]]
        self._stop = stop  # type: Optional[Union[str, int]]
        self._wagasci_database = wagasci_database if wagasci_database else None  # type: Optional[str]
        self._xdata = []
        self._ydata = []
        self._check_arguments()

        self.harvester = harvester

    @property
    def wagasci_database(self):
        # type: (...) -> str
        return self._wagasci_database

    # noinspection PyTypeChecker
    def _check_arguments(self):
        # type: (...) -> None
        """
        Check that the constructor arguments are sane
        """
        if isinstance(self._start, string_types):
            try:
                self._start = wagascianpy.database.db_record.DBRecord.str2datetime(self._start)
            except ValueError as exception:
                print('Start string must be in the format "%Y/%m/%d %H:%M:%S" or a '
                      'run number (int) : ' + self._start)
                raise exception
        if isinstance(self._stop, string_types):
            try:
                self._stop = wagascianpy.database.db_record.DBRecord.str2datetime(self._stop)
            except ValueError as exception:
                print('Stop string must be in the format "%Y/%m/%d %H:%M:%S" or a '
                      'run number (int) : ' + self._stop)
                raise exception

    def is_harvester_ready(self):
        # type: (...) -> bool
        """
        Check if the harvester class has been set
        :return: true if set false otherwise
        """
        return bool(self._harvester)

    @property
    def harvester(self):
        """
        The Patron maintains a reference to one of the Harvester objects. The
        Patron does not know the concrete class of a harvester. It should work
        with all strategies via the Harvester interface.
        """
        assert self._harvester is not None, "Set data harvester before using it"
        return self._harvester

    @harvester.setter
    def harvester(self, harvester):
        """
        Usually, the Patron allows replacing a Harvester object at runtime.
        """
        self._harvester = harvester
        if None not in [self._harvester, self._start, self._wagasci_database]:
            self._harvester.set_time_interval(start=self._start, stop=self._stop,
                                              wagasci_database=self._wagasci_database)

    def gather_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[List[float], List[Any]]
        """
        Call the harvest_data method of the harvester object to gather the data to plot
        :param detector_name: name of the detector if any
        :param only_good: only gather data and runs flagged as good
        :return: two lists of equal length with X axis data and Y axis data
        """
        return self._harvester.harvest_data(detector_name=detector_name, only_good=only_good)


class Harvester(ABC):
    """
    The Harvester interface declares operations common to all supported versions of some algorithm.
    The Patron uses this interface to call the algorithm defined by the concrete Harvester.
    """

    def __init__(self, database, repository, t2krun):
        # type: (str, str, int) -> None
        """
        :param database: location of the BSD or WAGASCI database
        :param repository: location of the BSD or WAGASCI repository
        :param t2krun: number of T2K run
        """
        self._database = database if database else None  # type: Optional[str]
        self._repository = repository if repository else None  # type: Optional[str]
        self._t2krun = t2krun  # type: int
        self._start_time = None
        self._stop_time = None
        self._trees_have_been_planted = False  # type: bool
        self._active_branches = None  # type: Optional[List[str]]
        if self._repository is not None and not os.path.exists(self._repository):
            raise OSError("Repository directory does not exist : %s" % self._repository)
        if self._database is not None and ':' not in self._database and not os.path.exists(self._database):
            raise OSError("Database file does not exist : %s" % self._database)

    def set_time_interval(self, start, stop, wagasci_database=None):
        # type: (Union[str, int], Union[str, int], Optional[str]) -> None
        """
        Set the time or run interval where to look for data
        :param start: start time or start run
        :param stop: stop time or stop run
        :param wagasci_database: location of the WAGASCI database file
        :return: None
        """
        if start is not None:
            database = wagasci_database if wagasci_database is not None else self._database
            self._start_time, self._stop_time = wgdb.run_to_interval(start=start, stop=stop, database=database)

    @abc.abstractmethod
    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[List[float], List[Any]]
        """
        Gather the data to plot
        :param detector_name: name of the detector if any
        :param only_good: only gather data and runs flagged as good
        :return: two lists of equal length with X axis data and Y axis data
        """
        pass

    @staticmethod
    def _list_root_files(run_root_dir, recursive=True):
        # type: (str, bool) -> List[Tuple[str, int]]
        """
        List all the files with .root extension and extract the DIF number
        :param run_root_dir: directory to list
        :return: list of tuples where the first element is the file name and the second is the DIF number
        """
        return [(filename, utils.extract_dif_id(filename))
                for filename in utils.find_files(path=run_root_dir, extension='root', recursive=recursive)
                if utils.extract_dif_id(filename) is not None]


################################################################
#                      Concrete Harvesters                     #
################################################################


class BsdHarvester(Harvester, ABC):

    def _get_spills(self):
        # type: (...) -> List[sp.BsdSpill]
        """
        Read the input files and extract the info about the BSD spills
        :return: list of BsdSpill objects
        """
        return wagascianpy.analysis.beam_summary_data.get_bsd_spills(bsd_database=self._database,
                                                                     bsd_repository=self._repository,
                                                                     t2krun=self._t2krun,
                                                                     start_time=self._start_time,
                                                                     stop_time=self._stop_time)

    @abc.abstractmethod
    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[List[float], List[Any]]
        """
        Gather the data to plot
        :param detector_name: ignored
        :param only_good: only good BSD spills
        :return: two lists of equal length with X axis data and Y axis data
        """
        pass


class BsdPotHarvester(BsdHarvester):

    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[List[float], List[float]]
        """
        Gather the data to plot. X axis is time, Y axis is POT delivered by neutrino beam line
        :param detector_name: ignored
        :param only_good: only good BSD spills
        :return: two lists of equal length with X axis data and Y axis data
        """
        bsd_spills = self._get_spills()
        accumulated_pot_list = []
        accumulated_pot = 0
        timestamp_list = []
        for spill in bsd_spills:
            if not only_good or spill.bsd_good_spill_flag == sp.IS_GOOD_SPILL:
                accumulated_pot += spill.pot
                accumulated_pot_list.append(accumulated_pot)
                timestamp_list.append(spill.timestamp)

        return timestamp_list, accumulated_pot_list


class BsdSpillHarvester(BsdHarvester):

    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[List[float], List[int]]
        """
        Gather the data to plot. X axis is time, Y axis is BSD 32 bit spill number
        :param detector_name: ignored
        :param only_good: only good BSD spills
        :return: two lists of equal length with X axis data and Y axis data
        """
        bsd_spills = self._get_spills()
        spill_number_list = []
        timestamp_list = []
        for spill in bsd_spills:
            if not only_good or spill.bsd_good_spill_flag == sp.IS_GOOD_SPILL:
                spill_number_list.append(spill.bsd_spill_number)
                timestamp_list.append(spill.timestamp)

        return timestamp_list, spill_number_list


class WagasciHarvester(Harvester, ABC):

    def __init__(self, topology=None, *args, **kwargs):
        # type: (Optional[topol.Topology], *Any, **Any) -> None
        super(WagasciHarvester, self).__init__(*args, **kwargs)
        self._detectors = detect.Detectors(enabled_detectors=topology)

    @property
    def active_branches(self):
        # type: (...) -> List[str]
        """
        :return: list of active branches names
        """
        return self._active_branches

    @active_branches.setter
    def active_branches(self, active_branches):
        # type: (List[str]) -> None
        """
        :param active_branches: list of active branches names
        :return: None
        """
        self._active_branches = active_branches

    @staticmethod
    def _is_dif_good(record, dif_id):
        # type: (Dict[str, Any], int) -> bool
        """
        :param record: WAGASCI run record
        :param dif_id: DIF index
        :return: True if the good data flag of the DIF is set to 1, False if it set to 0
        """
        if topol.DifIndex.is_wallmrd_north(dif_id):
            if not record["wallmrd_north_good_data_flag"]:
                return False
        elif topol.DifIndex.is_wallmrd_south(dif_id):
            if not record["wallmrd_south_good_data_flag"]:
                return False
        elif topol.DifIndex.is_wagasci_upstream(dif_id):
            if not record["wagasci_upstream_good_data_flag"]:
                return False
        elif topol.DifIndex.is_wagasci_downstream(dif_id):
            if not record["wagasci_downstream_good_data_flag"]:
                return False
        return True

    def _plant_trees(self, only_good=False):
        # type: (bool) -> None
        """
        Open the input TFiles and assign a TTree object to each enabled DIF object
        :param only_good: only runs or detectors flagged as good
        :return: None
        """
        if not self._trees_have_been_planted:
            # Assign a TTree to each DIF
            with wgdb.WagasciDataBase(db_location=self._database) as db:
                records = db.get_time_interval(datetime_start=self._start_time, datetime_stop=self._stop_time,
                                               include_overlapping=False, only_good=only_good)
                for record in sorted(records, key=operator.itemgetter("run_number")):
                    for root_file, dif_id in self._list_root_files(os.path.join(self._repository, record["name"]),
                                                                   recursive=False):
                        if not only_good or self._is_dif_good(record=record, dif_id=dif_id):
                            tree_name = utils.extract_raw_tree_name(root_file)
                            self._detectors.get_dif(dif_id).add_tree(root_file=root_file, tree_name=tree_name)
            # Set the active branches of the TTree
            self._detectors.activate_branches(self._active_branches)
        self._trees_have_been_planted = True

    def _get_wagasci_spills_from_ttree(self, raw_tree):
        # type: (Any) -> List[sp.WagasciBsdSpill]
        """
        Read all the WAGASCI spills of the input TTree into a list of WagasciBsdSpill objects
        :param raw_tree: ROOT.TTree object
        :return: list of WAGASCI spills
        """
        assert raw_tree is not None, "Raw tree should be set before trying to read it"
        wagasci_spills = []
        for event in raw_tree:
            if event.spill_mode != sp.WAGASCI_SPILL_BEAM_MODE:
                continue
            wagasci_spill = sp.SpillFactory.get_spill("wagascibsd")
            for variable in self._active_branches:
                if not hasattr(event, variable):
                    raise AttributeError("Variable {} not found in TTree {}".format(variable,
                                                                                    raw_tree.GetFile().GetName()))
                setattr(wagasci_spill, variable, getattr(event, variable))
            wagasci_spills.append(wagasci_spill)
        return wagasci_spills

    @abc.abstractmethod
    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> None
        """
        Open the input TTrees and read the spill information from them
        :param detector_name: name of the detector to gather data from
        :param only_good: only gather data and runs flagged as good
        """
        self._plant_trees(only_good)
        assert detector_name is not None, "You must specify a detector where to harvest data from"
        dif = self._detectors.get_detector(detector_name)
        assert isinstance(dif, detect.Dif), "You should select a DIF and not a whole subdetector"
        if dif.has_tree():
            print("Extracting spills from DIF {} of detector {}".format(dif.name, detector_name))
            dif.set_spills(self._get_wagasci_spills_from_ttree(dif.get_tree()))


class WagasciPotHarvester(WagasciHarvester):

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(WagasciPotHarvester, self).__init__(*args, **kwargs)
        self._active_branches = ["spill_number", "spill_mode", "fixed_spill_number", "good_spill_flag",
                                 "bsd_good_spill_flag", "pot", "timestamp"]

    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[Optional[List[float]], Optional[List[float]]]
        """
        Return a couple of lists of equal length. The first is the X axis timestamp, the second is the Y axis POTs.
        :param detector_name: name of the detector to gather data from
        :param only_good: only gather data and runs flagged as good
        :return: two lists of equal length with X axis data and Y axis data
        """
        if "top" not in detector_name and "bottom" not in detector_name and "side" not in detector_name:
            detector_name += " top"
        super(WagasciPotHarvester, self).harvest_data(detector_name=detector_name, only_good=only_good)
        top_dif = self._detectors.get_detector(detector_name)
        if top_dif.is_enabled():
            accumulated_pot_list = []
            accumulated_pot = 0
            timestamp_list = []
            for spill in top_dif.get_spills():
                if ((not only_good or spill.bsd_good_spill_flag == sp.IS_GOOD_SPILL) and
                        spill.good_spill_flag == sp.IS_GOOD_SPILL):
                    if spill.timestamp < 0 or spill.pot < 0:
                        print("Huston there was a problem!")
                        spill.pretty_print()
                        continue
                    timestamp_list.append(spill.timestamp)
                    accumulated_pot += spill.pot
                    accumulated_pot_list.append(accumulated_pot)
            return timestamp_list, accumulated_pot_list
        return None, None


class WagasciSpillHistoryHarvester(WagasciHarvester):

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(WagasciSpillHistoryHarvester, self).__init__(*args, **kwargs)
        self._active_branches = ["spill_mode", "spill_number", "timestamp"]

    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[Optional[List[float]], Optional[List[int]]]
        """
        Return a couple of lists: the first is the X axis timestamp, the second is the Y axis (non fixed) spill number.
        :param detector_name: name of the detector to gather data from
        :param only_good: only gather data and runs flagged as good
        :return: two lists of equal length with X axis data and Y axis data
        """
        if "top" not in detector_name and "bottom" not in detector_name and "side" not in detector_name:
            detector_name += " top"
        super(WagasciSpillHistoryHarvester, self).harvest_data(detector_name=detector_name, only_good=only_good)
        top_dif = self._detectors.get_detector(detector_name)
        if top_dif.is_enabled():
            spill_number_list = []
            timestamp_list = []
            for spill in top_dif.get_spills():
                if spill.timestamp > 0:
                    spill_number_list.append(spill.spill_number)
                    timestamp_list.append(spill.timestamp)
            return timestamp_list, spill_number_list
        return None, None


class WagasciFixedSpillHarvester(WagasciHarvester):

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(WagasciFixedSpillHarvester, self).__init__(*args, **kwargs)
        self._active_branches = ["spill_mode", "fixed_spill_number", "good_spill_flag",
                                 "bsd_good_spill_flag", "timestamp"]

    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[Optional[List[float]], Optional[List[int]]]
        """
        Return a couple of lists: the first is the X axis timestamp, the second is the Y axis fixed spill number.
        :param detector_name: name of the detector to gather data from
        :param only_good: only gather data and runs flagged as good
        :return: two lists of equal length with X axis data and Y axis data
        """
        if "top" not in detector_name and "bottom" not in detector_name and "side" not in detector_name:
            detector_name += " top"
        super(WagasciFixedSpillHarvester, self).harvest_data(detector_name=detector_name, only_good=only_good)
        top_dif = self._detectors.get_detector(detector_name)
        if top_dif.is_enabled():
            fixed_spill_number_list = []
            timestamp_list = []
            for spill in top_dif.get_spills():
                if spill.good_spill_flag == sp.IS_GOOD_SPILL and spill.timestamp > 0:
                    if spill.fixed_spill_number < sp.WAGASCI_MINIMUM_SPILL or \
                            spill.fixed_spill_number > sp.WAGASCI_MAXIMUM_SPILL or \
                            spill.timestamp < 0:
                        print("WARNING! WAGASCI spill is out of range. Time {} : Spill {}".format(
                            spill.timestamp, spill.fixed_spill_number))
                    fixed_spill_number_list.append(spill.fixed_spill_number)
                    timestamp_list.append(spill.timestamp)
            return timestamp_list, fixed_spill_number_list
        return None, None


class WagasciSpillNumberHarvester(WagasciHarvester):

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(WagasciSpillNumberHarvester, self).__init__(*args, **kwargs)
        self._active_branches = ["spill_mode", "spill_number"]

    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[Optional[List[int]], Optional[List[int]]]
        """
        Return a couple of lists: the first is the X axis event number, the second is the Y axis (non fixed) spill
        number.
        :param detector_name: name of the detector to gather data from
        :param only_good: only gather data and runs flagged as good
        :return: two lists of equal length with X axis data and Y axis data
        """
        if "top" not in detector_name and "bottom" not in detector_name and "side" not in detector_name:
            detector_name += " top"
        super(WagasciSpillNumberHarvester, self).harvest_data(detector_name=detector_name, only_good=only_good)
        top_dif = self._detectors.get_detector(detector_name)
        if top_dif.is_enabled():
            spill_number_list = []
            event_list = []
            for counter, spill in enumerate(top_dif.get_spills()):
                spill_number_list.append(spill.spill_number)
                event_list.append(counter)
            return event_list, spill_number_list
        return None, None


class TemperatureHarvester(WagasciHarvester):

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(TemperatureHarvester, self).__init__(*args, **kwargs)
        self._active_branches = ["spill_mode", "good_spill_flag", "bsd_good_spill_flag",
                                 "timestamp", "temperature"]

    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[Optional[List[float]], Optional[List[float]]]
        """
        Return a couple of lists: the first is the X axis timestamp, the second is the Y axis temperature.
        :param detector_name: name of the detector to gather data from
        :param only_good: only gather data and runs flagged as good
        :return: two lists of equal length with X axis data and Y axis data
        """
        super(TemperatureHarvester, self).harvest_data(detector_name=detector_name, only_good=only_good)
        detector = self._detectors.get_detector(detector_name)
        if detector.is_enabled():
            temperature_list = []
            timestamp_list = []
            for spill in detector.get_spills():
                if ((not only_good or spill.bsd_good_spill_flag == sp.IS_GOOD_SPILL) and
                        spill.good_spill_flag == sp.IS_GOOD_SPILL and spill.timestamp > 0):
                    temperature_list.append(spill.temperature)
                    timestamp_list.append(spill.timestamp)
            return timestamp_list, temperature_list
        return None, None


class HumidityHarvester(WagasciHarvester):

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(HumidityHarvester, self).__init__(*args, **kwargs)
        self._active_branches = ["spill_mode", "good_spill_flag", "bsd_good_spill_flag",
                                 "timestamp", "humidity"]

    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[Optional[List[float]], Optional[List[float]]]
        """
        Return a couple of lists: the first is the X axis timestamp, the second is the Y axis humidity.
        :param detector_name: name of the detector to gather data from
        :param only_good: only gather data and runs flagged as good
        :return: two lists of equal length with X axis data and Y axis data
        """
        super(HumidityHarvester, self).harvest_data(detector_name=detector_name, only_good=only_good)
        detector = self._detectors.get_detector(detector_name)
        if detector.is_enabled():
            humidity_list = []
            timestamp_list = []
            for spill in detector.get_spills():
                if ((not only_good or spill.bsd_good_spill_flag == sp.IS_GOOD_SPILL) and
                        spill.good_spill_flag == sp.IS_GOOD_SPILL and spill.timestamp > 0):
                    humidity_list.append(spill.humidity)
                    timestamp_list.append(spill.timestamp)
            return timestamp_list, humidity_list
        return None, None


class AdcCalibrationHarvester(Harvester, ABC):

    def __init__(self, topology=None, *args, **kwargs):
        # type: (topol.Topology, Any, Any) -> None
        """
        :param topology: Topology object that specifies which are the enabled DIFs
        """
        super(AdcCalibrationHarvester, self).__init__(*args, **kwargs)
        self._detectors = detect.Detectors(enabled_detectors=topology)  # type: detect.Detectors

    def _list_adc_calibration_files(self):
        # type: (...) -> List[Tuple[int, int, int, str]]
        rootfiles = utils.find_files(self._repository, extension='root', recursive=False)
        nums_re = re.compile(r"from_(\d+)_to_(\d+)_ecal_dif_(\d+)")
        start_stop_run = collections.namedtuple('start_stop_run', 'start stop dif path')
        results = []
        for path in rootfiles:
            if bool(nums_re.search(path)):
                start = int(nums_re.search(path).group(1))
                stop = int(nums_re.search(path).group(2))
                dif = int(nums_re.search(path).group(3))
                results.append(start_stop_run(start, stop, dif, path))
        return sorted(results)

    @staticmethod
    def _select_run(run_number, start_stop_dirs):
        # type: (int, List[Tuple[int, int, int, str]]) -> List[Tuple[int, int, int, str]]
        return [start_stop_dir for start_stop_dir in start_stop_dirs
                if start_stop_dir.start <= run_number <= start_stop_dir.stop]

    def _plant_trees(self):
        # type: (...) -> None
        """
        Open the input TFiles and assign a TTree object to each enabled DIF object
        :return: None
        """

        if not self._trees_have_been_planted:
            if not self._active_branches:
                raise ValueError("Set active branches before planting trees")

            all_files = self._list_adc_calibration_files()
            selected_files = set()

            if self._database:
                print("[AdbCalibrationHarvester] Using WAGASCI run database to select runs from {} to {}".format(
                    self._start_time, self._stop_time))

                with wgdb.WagasciDataBase(db_location=self._database) as db:
                    records = db.get_time_interval(datetime_start=self._start_time, datetime_stop=self._stop_time,
                                                   include_overlapping=True, only_good=True)
                    for record in sorted(records, key=operator.itemgetter("run_number")):
                        selected_runs = self._select_run(record["run_number"], all_files)
                        for selected_run in selected_runs:
                            selected_files.add(selected_run)
                selected_files = sorted(list(selected_files))
            else:
                print("[AdbCalibrationHarvester] WARNING : WAGASCI run database not given so all runs will be "
                      "selected. The ordering of the runs cannot be guaranteed.")
                selected_files = all_files

            for selected_file in selected_files:
                if self._detectors.get_dif(selected_file.dif).is_enabled():
                    self._detectors.get_dif(selected_file.dif).add_tree(root_file=selected_file.path,
                                                                        tree_name=treenames.HISTORY_TREE_NAME,
                                                                        tree_friends=[treenames.THRESHOLD_TREE_NAME])
            self._detectors.activate_branches(self._active_branches)
        self._trees_have_been_planted = True

    @abc.abstractmethod
    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> None
        """
        Setup the TTrees where to gather data from
        :param detector_name: ignored
        :param only_good: ignored
        :return: None
        """
        self._plant_trees()


class AdcCalibrationHarvesterDif(AdcCalibrationHarvester, ABC):

    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[Optional[List[float]], Optional[List[List[float]]]]
        """
        Return a couple of lists: the first is the timestamp (X axis), the second is the list of gain for all the
        channels (Y axis).
        :param detector_name: name of the detector to gather data from
        :param only_good: ignored
        :return: two lists of equal length with X axis data and Y axis data
        """
        super(AdcCalibrationHarvesterDif, self).harvest_data(detector_name=detector_name, only_good=only_good)
        time = []  # type: List[float]
        data = []  # type: List[List[float]]
        for detector in self._detectors:
            for dif in [dif for dif in detector if dif.has_tree()]:
                print("Extracting data from DIF {} {}".format(detector.name, dif.name))
                for event in dif.get_tree():
                    if getattr(event, self._active_branches[0]) > 0.:
                        yarray = numpy.frombuffer(getattr(event, self._active_branches[1]), dtype="float64")
                        ylist = yarray[~numpy.isnan(yarray)].tolist()
                        ylist = [i for i in ylist if i >= 0.]
                        if ylist:
                            time.append(getattr(event, self._active_branches[0]))
                            data.append(ylist)
        return time, data


class GainHarvesterDif(AdcCalibrationHarvesterDif):

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(GainHarvesterDif, self).__init__(*args, **kwargs)
        self._active_branches = ["average_timestamp", "gain"]


class DarkNoiseHarvesterDif(AdcCalibrationHarvesterDif):

    def __init__(self, *args, **kwargs):
        # type: (Any, Any) -> None
        super(DarkNoiseHarvesterDif, self).__init__(*args, **kwargs)
        self._active_branches = ["average_timestamp", "dark_noise"]


class ThresholdHarvesterDif(AdcCalibrationHarvesterDif):

    def __init__(self, *args, **kwargs):
        # type: (Any, Any) -> None
        super(ThresholdHarvesterDif, self).__init__(*args, **kwargs)
        self._active_branches = ["average_timestamp", "hit_threshold"]


class AdcCalibrationTemperatureHarvester(AdcCalibrationHarvester):

    def __init__(self, *args, **kwargs):
        # type: (Any, Any) -> None
        super(AdcCalibrationTemperatureHarvester, self).__init__(*args, **kwargs)
        self._active_branches = ["average_timestamp", "average_temperature"]

    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[Optional[List[float]], Optional[List[float]]]
        """
        Return a couple of lists: the first is the timestamp (X axis), the second is the temperature (Y axis).
        :param detector_name: name of the detector to gather data from
        :param only_good: ignored
        :return: two lists of equal length with X axis data and Y axis data
        """
        super(AdcCalibrationTemperatureHarvester, self).harvest_data(detector_name=detector_name, only_good=only_good)
        time = []
        data = []
        dif = self._detectors.get_dif(detector_name)
        print("Extracting data from DIF {}".format(detector_name))
        for event in dif.get_tree():
            if getattr(event, self._active_branches[0]) > 0. and getattr(event, self._active_branches[1]) > 0.:
                time.append(getattr(event, self._active_branches[0]))
                data.append(getattr(event, self._active_branches[1]))
        return time, data


class AdcCalibrationHarvesterChannel(AdcCalibrationHarvester, ABC):

    def __init__(self, chip=0, channel=0, *args, **kwargs):
        # type: (int, int, Any, Any) -> None
        """
        :param chip: chip ID
        :param channel: channel ID
        """
        super(AdcCalibrationHarvesterChannel, self).__init__(*args, **kwargs)
        self._chip = chip  # type: int
        self._channel = channel  # type: int

    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[Optional[List[float]], Optional[List[float]]]
        """
        Return a couple of lists: the first is the timestamp (X axis), the second is the gain (Y axis).
        :param detector_name: ignored
        :param only_good: ignored
        :return: two lists of equal length with X axis data and Y axis data
        """
        super(AdcCalibrationHarvesterChannel, self).harvest_data(detector_name=detector_name, only_good=only_good)
        time = []
        data = []
        for detector in self._detectors:
            for dif in [dif for dif in detector if dif.has_tree()]:
                print("Extracting data from DIF {} {}".format(detector.name, dif.name))
                for event in dif.get_tree():
                    if getattr(event, self._active_branches[0]) > 0.:
                        yarray = numpy.frombuffer(getattr(event, self._active_branches[1]), dtype="float64")
                        reshaped_array = numpy.reshape(yarray, (WAGASCI_NCHIPS if topol.DifIndex.is_wagasci(dif.dif_id)
                                                                else WALLMRD_NCHIPS, SPIROC2D_NCHANNELS))
                        ydata = reshaped_array[self._chip][self._channel]
                        if ydata >= 0:
                            time.append(getattr(event, self._active_branches[0]))
                            data.append(ydata)
        return time, data


class GainHarvesterChannel(AdcCalibrationHarvesterChannel):

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(GainHarvesterChannel, self).__init__(*args, **kwargs)
        self._active_branches = ["average_timestamp", "gain"]


class DarkNoiseHarvesterChannel(AdcCalibrationHarvesterChannel):

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(DarkNoiseHarvesterChannel, self).__init__(*args, **kwargs)
        self._active_branches = ["average_timestamp", "dark_noise"]


class ThresholdHarvesterChannel(AdcCalibrationHarvesterChannel):

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(ThresholdHarvesterChannel, self).__init__(*args, **kwargs)
        self._active_branches = ["average_timestamp", "hit_threshold"]


class BcidHarvester(WagasciHarvester):

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        """
        :param args: positional arguments for the Harvester super class
        :param kwargs: keyword arguments for the Harvester super class
        """
        super(BcidHarvester, self).__init__(*args, **kwargs)
        self._active_branches = ["spill_mode", "timestamp", "bcid", "hit"]
        # Number of spills over which the BCID histogram is calculated
        self._spill_period = 5000
        # Maximum value of the BCID to be plotted
        self._max_bcid = 100

    def harvest_data(self, detector_name=None, only_good=False):
        # type: (Optional[str], bool) -> Tuple[Optional[List[float]], Optional[List[List[float]]]]
        """
        Setup the TTrees where to gather data from and read the data
        :param detector_name: name of the detector to gather data from
        :param only_good: only gather data and runs flagged as good
        :return: two lists of equal length with X axis data and Y axis data
        """
        super(BcidHarvester, self).harvest_data(detector_name=detector_name, only_good=only_good)
        time = []
        data = []
        for detector in self._detectors:
            for dif in [dif for dif in detector if dif.has_tree() and dif.is_enabled()]:

                if topol.DifIndex.is_wagasci(dif.dif_id):
                    num_chips = _NCHIPS_WAGASCI
                elif topol.DifIndex.is_wallmrd(dif.dif_id):
                    num_chips = _CHIPS_WALLMRD
                else:
                    raise ValueError("DIF ID not recognized : {}".format(dif.dif_id))

                print("Extracting BCID data from DIF {} {}".format(detector.name, dif.name))

                hist = ROOT.TH1I("DIF{}".format(dif.dif_id), "DIF{}".format(dif.dif_id),
                                 self._max_bcid, 0, self._max_bcid)

                average_timestamp = 0
                i = 0
                for event in dif.get_tree():
                    if event.spill_mode == sp.WAGASCI_SPILL_BEAM_MODE and event.timestamp > 0.:
                        i += 1
                        average_timestamp += event.timestamp
                        for chip in range(num_chips):
                            for channel in range(_NCHANNELS):
                                for column in range(_NCOLUMNS):
                                    if event.hit[column + _NCOLUMNS * channel + _NCOLUMNS * _NCHANNELS * chip] == _HIT:
                                        hist.Fill(event.bcid[column + _NCOLUMNS * chip])
                        if i != 0 and i % self._spill_period == 0:
                            print("{} {} : event {}".format(detector.name, dif.name, i))
                            average_timestamp /= self._spill_period
                            yarray = numpy.array(hist)[1:-1]
                            ylist = yarray[~numpy.isnan(yarray)].tolist()
                            ylist = [j for j in ylist if j >= 0.]
                            if ylist:
                                time.append(average_timestamp)
                                data.append(ylist)
                            hist.Reset("ICESM")
                            average_timestamp = 0
        return time, data
