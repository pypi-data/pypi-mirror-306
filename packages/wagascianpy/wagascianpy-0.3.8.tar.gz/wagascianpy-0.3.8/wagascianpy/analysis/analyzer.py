#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc
import inspect
import json
import os
import shutil
import time
from collections import OrderedDict
from enum import Enum
from typing import Any, List, Dict, Optional, Union

from bitarray import bitarray
from recordclass import recordclass

import wagascianpy.analysis.analysis as analysis
import wagascianpy.analysis.apply_detector_flags as apply_detector_flags
import wagascianpy.analysis.beam_summary_data as beam_summary_data
import wagascianpy.analysis.sanity_check as sanity_check
import wagascianpy.utils.environment as environment
import wagascianpy.utils.utils as utils
from wagascianpy.utils.acq_config_xml import acqconfigxml_file_finder

try:
    from shutil import SameFileError
except ImportError:
    shutil.SameFileError = OSError

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})
# Chain mutable tuple
Chain = recordclass('Chain', ['link', 'thread'])


class AnalyzerInputType(Enum):
    """
    Type of input of the analyzer. single_run means that the analyzer accepts a single run at a time. multiple_runs
    means that the analyzer combine the information from multiple runs.
    """
    single_run = 1,
    multiple_runs = 2


class AnalyzerThreadingType(Enum):
    """
    Multithreading capabilities of an analyzer. multi_threaded means that the analyzer can act on the input files
    concurrently. single_threaded means that it should not be more than one active thread of the analyzer at a time.
    """
    multi_threaded = 1,
    single_threaded = 2


class Analyzer(ABC):
    """
    virtual class that represents an analizer program. It is assumed that the analyzer program acts on one or
    more WAGASCI runs. The output can be a series of plots, a new ROOT file or just to modify the input ROOT file or
    a combination of those.
    """
    depends = None

    def __init__(self,
                 analyzer_name,  # type: str
                 run_name,  # type: str
                 run_root_dir,  # type: str
                 output_dir,  # type: str
                 wagasci_libdir=None,  # type: Optional[str]
                 run_number=None,  # type: Optional[int]
                 default_args=None,  # type: Optional[Dict]
                 **kwargs):

        """
        :param analyzer_name: arbitrary name of the analyzer program
        :param run_name: name of the run to analyze
        :param run_root_dir: directory where the run files are located
        :param output_dir: directory where the output files are to be saved
        :param wagasci_libdir: directory where the WAGASCI library is
        :param run_number: run number
        :param default_args: default arguments of the analyzer program
        :param kwargs: variable arguments of the analyzer program
        """
        self.name = analyzer_name
        self.run_name = run_name
        self.run_number = run_number
        self.run_root_dir = run_root_dir
        self.output_dir = output_dir
        self._wagasci_libdir = wagasci_libdir
        if self._wagasci_libdir is None:
            try:
                env = environment.WagasciEnvironment()
                self._wagasci_libdir = env['WAGASCI_LIBDIR']
            except KeyError:
                raise KeyError("WAGASCI_LIBDIR variable not found in the shell environment")
        if default_args:
            self.args = default_args
        else:
            self.args = OrderedDict()
        self.set_init_arguments(**kwargs)

    @abc.abstractmethod
    def _set_runtime_arguments(self, input_files, dif_id):
        # type: (List[str], Optional[int]) -> None
        pass

    @abc.abstractmethod
    def spawn(self, chains):
        pass

    def get_topology(self, acq_config_xml):
        """
        Get the detector topology (DIF - CHIP - CHAN) from the XML configuration file
        :rtype: dict
        :param acq_config_xml: path to XML file containing the acquisition configuration
        :return: Detector topology dictionary
        """
        chain = analysis.WagasciAnalysis(self._wagasci_libdir)
        topology_string, pointer = chain.get_dif_topology(acq_config_xml)
        chain.free_topology(pointer)
        return json.loads(topology_string)

    def multiple_input_loop(self, input_files, chains):
        # type: (Dict[int, List[str]], Dict[int, Chain]) -> None
        """
        Analyze the input files concurrently  using the analyzer whose name is self.name and arguments are self.args
        :param input_files: input files
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        """
        # sanity checks
        print("Input files [DIF, input files path] : {}".format(input_files))
        if chains is None:
            raise ValueError("Chain recordclass objects not found")
        if not isinstance(chains, dict):
            raise TypeError("The chains dictionary must be initialized outside of the multiple_input_loop method")
        if len(chains) != 0 and len(chains) != len(input_files):
            raise ValueError("The number of chains ({}) must be the same as the number of "
                             "DIFs ({})".format(len(chains), len(input_files)))
        # DIF loop
        for dif_id, input_file in input_files.items():
            self._set_runtime_arguments(input_files=input_file, dif_id=utils.extract_dif_id(input_file))
            if dif_id not in chains:
                chain = Chain
                chain.link = analysis.WagasciAnalysis(self._wagasci_libdir)
                chain.thread = chain.link.spawn(self.name, **self.args)
                chains[dif_id] = chain
                time.sleep(1)
            else:
                chains[dif_id].thread = chains[dif_id].link.spawn(self.name, **self.args)
            print("Spawn thread with DIF {} : LINK ID {} : THREAD ID {}".format(dif_id, id(chains[dif_id].link),
                                                                                id(chains[dif_id].thread)))

    def single_input_loop(self, input_file, chains):
        # type: (str, Dict[int, Chain]) -> None
        """
        Analyze the input file using the analyzer whose name is self.name and arguments are self.args
        :param input_file: input file
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        """
        if chains and len(chains) > 1:
            raise IndexError("The method %s does not support more than one chain" %
                             inspect.currentframe().f_code.co_name)
        self._set_runtime_arguments(input_files=input_file, dif_id=utils.extract_dif_id(input_file))
        dummy_id = 0
        if not isinstance(chains, dict):
            raise TypeError("The chains dictionary must be initialized upstream")
        if dummy_id not in chains:
            chain = Chain
            chain.link = analysis.WagasciAnalysis(self._wagasci_libdir)
            chain.thread = chain.link.spawn(self.name, **self.args)
            chains[dummy_id] = chain
        else:
            chains[dummy_id].thread = chains[dummy_id].link.spawn(self.name, **self.args)
        print("Spawn thread with DIF {} : LINK ID {} : THREAD ID {}".format(dummy_id, id(chains[dummy_id].link),
                                                                            id(chains[dummy_id].thread)))

    def set_init_arguments(self, **kwargs):
        """
        Set the default value of some of the analyzer program arguments
        :param kwargs: default arguments
        """
        for key, value in kwargs.items():
            if key not in self.args:
                raise KeyError("Analyzer %s does not accept argument %s" % (self.name, key))
            self.args[key] = value


class Decoder(Analyzer):
    """
    Wrapper around the wgDecoder program
    """
    name = "decoder"
    depends = None
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.multi_threaded

    _default_args = utils.get_arguments_ordered_dict(analysis.WagasciAnalysis.decoder)
    _default_args.update({'calibration_dir': "",
                          'overwrite_flag': False,
                          'compatibility_mode': False})

    def __init__(self, **kwargs):
        super(Decoder, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)

        self.acq_config_xml = acqconfigxml_file_finder(self.run_root_dir, self.run_name)
        if not os.path.exists(self.acq_config_xml):
            raise OSError("Acquisition configuration XML file not found : %s" % self.acq_config_xml)
        self._topology = self.get_topology(self.acq_config_xml)
        utils.renametree(run_root_dir=self.run_root_dir, run_name=self.run_name, dif_topology=self._topology)

    def _set_runtime_arguments(self, input_files, dif_id):
        # type: (List[str], Optional[int]) -> None
        """
        Set arguments at execution time. By execution time I mean the moment the wgDecoder program is launched
        through the spawn method.
        :param dif_id: 
        :param input_files: input file
        :return: None
        """
        self.args["input_file"] = input_files
        self.args["output_dir"] = self.output_dir
        self.args["dif"] = dif_id
        self.args["n_chips"] = len(self._topology[str(dif_id)])

    def spawn(self, chains):
        # type: (Dict[int, Chain]) -> None
        """
        Spawn the wgDecoder threads contained in the chains dict
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        :return: None
        """
        if os.path.isfile(self.run_root_dir) and self.run_root_dir.endswith('.raw'):
            input_files = [utils.extract_dif_id(self.run_root_dir), [self.run_root_dir]]
        else:
            input_files = {utils.extract_dif_id(f): f for f in utils.find_files(self.run_root_dir, 'raw') if
                           utils.extract_dif_id(f) is not None}
        if not os.path.exists(self.output_dir):
            utils.mkdir_p(self.output_dir)
        for xml_file in utils.find_files(self.run_root_dir, 'xml'):
            dst = os.path.join(self.output_dir, os.path.basename(xml_file))
            if not os.path.exists(dst):
                shutil.copy2(src=xml_file, dst=dst)
        for log_file in utils.find_files(self.run_root_dir, 'log'):
            dst = os.path.join(self.output_dir, os.path.basename(log_file))
            if not os.path.exists(dst):
                shutil.copy2(src=log_file, dst=dst)
        self.multiple_input_loop(input_files, chains)


class MakeHist(Analyzer):
    """
    Wrapper around the wgMakeHist program
    """
    name = "make_hist"
    depends = Decoder.name
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.single_threaded

    _default_args = utils.get_arguments_ordered_dict(analysis.WagasciAnalysis.make_hist)

    def __init__(self, **kwargs):
        super(MakeHist, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)
        self.acq_config_xml = acqconfigxml_file_finder(self.run_root_dir, self.run_name)
        if not os.path.exists(self.acq_config_xml):
            raise OSError("Acquisition configuration XML file not found : %s" % self.acq_config_xml)
        self.args["config_file"] = self.acq_config_xml

    def _set_runtime_arguments(self, input_files, dif_id):
        # type: (List[str], Optional[int]) -> None
        """
        Set arguments at execution time. By execution time I mean the moment the wgMakeHist program is launched
        through the spawn method.
        :param dif_id: 
        :param input_files: input file
        :return: None
        """
        flags = bitarray('0' * 9, endian='big')
        flags[7] = True  # dark noise
        flags[4] = True  # charge hit HG
        flags[0] = False  # overwrite
        ul_flags = int(flags.to01(), 2)
        self.args["ul_flags"] = ul_flags
        self.args["input_file"] = input_files
        self.args["output_dir"] = os.path.join(self.output_dir, self.name)
        self.args["dif"] = dif_id

    def spawn(self, chains):
        # type: (Dict[int, Chain]) -> None
        """
        Spawn the wgMakeHist threads contained in the chains dict
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        :return: None
        """
        if os.path.isfile(self.run_root_dir) and self.run_root_dir.endswith('tree.root'):
            input_files = [self.run_root_dir]
        elif os.path.isdir(self.run_root_dir):
            input_files = filter(lambda f: f.endswith('tree.root'), utils.find_files(self.run_root_dir, 'root'))
        else:
            raise OSError("Input file or directory is invalid : {}".format(self.run_root_dir))
        if not os.path.exists(self.output_dir):
            utils.mkdir_p(self.output_dir)
        for inputfile in input_files:
            self.single_input_loop(inputfile, chains)


class TdcCalibration(Analyzer):
    """
    Wrapper around the wgTDC program
    """
    name = "tdc_calibration"
    depends = Decoder.name
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.multi_threaded

    _default_args = utils.get_arguments_ordered_dict(analysis.WagasciAnalysis.tdc_calibration)

    def __init__(self, **kwargs):
        super(TdcCalibration, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)
        self.acq_config_xml = acqconfigxml_file_finder(self.run_root_dir, self.run_name)
        if not os.path.exists(self.acq_config_xml):
            raise OSError("Acquisition configuration XML file not found : %s" % self.acq_config_xml)
        self.args["config_file"] = self.acq_config_xml

    def _set_runtime_arguments(self, input_files, dif_id):
        # type: (List[str], Optional[int]) -> None
        """
        Set arguments at execution time. By execution time I mean the moment the wgTDC program is launched
        through the spawn method.
        :param dif_id: 
        :param input_files: input file
        :return: None
        """
        self.args["input_file"] = input_files
        self.args["dif"] = dif_id

    def spawn(self, chains):
        # type: (Dict[int, Chain]) -> None
        """
        Spawn the wgTdcCalibration threads contained in the chains dict
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        :return: None
        """
        if os.path.isfile(self.run_root_dir) and self.run_root_dir.endswith('tree.root'):
            input_files = [self.run_root_dir]
        elif os.path.isdir(self.run_root_dir):
            input_files = filter(lambda f: f.endswith('tree.root'), utils.find_files(self.run_root_dir, 'root'))
            input_files = {utils.extract_dif_id(input_file): input_file for input_file in input_files}
        else:
            raise OSError("Input file or directory is invalid : {}".format(self.run_root_dir))
        self.multiple_input_loop(input_files, chains)


class SpillNumberFixer(Analyzer):
    """
    Wrapper around the wgSpillNumberFixer program
    """
    name = "spill_number_fixer"
    depends = Decoder.name
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.single_threaded

    _default_args = utils.get_arguments_ordered_dict(analysis.WagasciAnalysis.spill_number_fixer)
    _default_args.update({'output_filename': "", 'passes': "", 'offset': 0, 'enable_graphics': False})

    def _set_runtime_arguments(self, input_files, dif_id):
        # type: (List[str], Optional[int]) -> None
        """
        Set arguments at execution time. By execution time I mean the moment the wgSpillNumberFixer program is launched
        through the spawn method.
        :param dif_id: 
        :return: None
        """
        self.args["output_filename"] = self.run_name
        self.args["passes"] = utils.spill_number_fixer_passes_calculator(self.run_number)
        if self.run_number >= 110:
            self.args["offset"] = 1

    def __init__(self, **kwargs):
        super(SpillNumberFixer, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)
        self.args["input_dir"] = self.run_root_dir
        self.args["output_dir"] = self.output_dir

    def spawn(self, chains):
        """
        Spawn the wgSpillNumberFixer threads contained in the chains dict
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        :return: None
        """
        if not os.path.exists(self.output_dir):
            utils.mkdir_p(self.output_dir)
        self.single_input_loop(self.run_root_dir, chains)


class BeamSummaryData(Analyzer):
    """
    Wrapper around the wgBeamSummaryData program
    """
    name = "beam_summary_data"
    depends = SpillNumberFixer.name
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.single_threaded

    _default_args = utils.get_arguments_ordered_dict(beam_summary_data.beam_summary_data)
    _default_args.update({'t2krun': 10, 'recursive': True})

    def __init__(self, **kwargs):
        super(BeamSummaryData, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)

    def _set_runtime_arguments(self, input_files, dif_id):
        # type: (List[str], Optional[int]) -> None
        """
        Set arguments at execution time. By execution time I mean the moment the wgBeamSummaryData program is launched
        through the spawn method.
        :param dif_id: 
        :return: None
        """
        self.args["input_path"] = input_files
        if os.path.isdir(input_files):
            self.args["recursive"] = True
        else:
            self.args["recursive"] = False

    def spawn(self, chains):
        # type: (Dict[int, Chain]) -> None
        """
        Spawn the wgBeamSummaryData threads contained in the chains dict
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        :return: None
        """
        self.single_input_loop(self.run_root_dir, chains)


class ApplyDetectorFlags(Analyzer):
    """
    Wrapper around the wgApplyDetectorFlags program
    """
    name = "apply_detector_flags"
    depends = SpillNumberFixer.name
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.single_threaded

    _default_args = utils.get_arguments_ordered_dict(apply_detector_flags.apply_detector_flags)

    def __init__(self, **kwargs):
        super(ApplyDetectorFlags, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)

    def _set_runtime_arguments(self, input_files, dif_id):
        # type: (List[str], Optional[int]) -> None
        """
        Set arguments at execution time. By execution time I mean the moment the program is launched
        through the spawn method.
        :param dif_id: 
        :return: None
        """
        self.args["input_path"] = input_files

    def spawn(self, chains):
        # type: (Dict[int, Chain]) -> None
        """
        Spawn the threads contained in the chains dict
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        :return: None
        """
        self.single_input_loop(self.run_root_dir, chains)


class BcidDistribution(Analyzer):
    """
    Wrapper around the bcid_distribution function
    """
    name = "bcid_distribution"
    depends = MakeHist.name
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.single_threaded

    _default_args = utils.get_arguments_ordered_dict(analysis.WagasciAnalysis.bcid_distribution)
    _default_args.update({'chip_by_chip': True})

    def __init__(self, **kwargs):
        super(BcidDistribution, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)

    def _set_runtime_arguments(self, input_files, dif_id):
        # type: (List[str], Optional[int]) -> None
        """
        Set arguments at execution time. By execution time I mean the moment the bcid distribution function  is
        executed through the spawn method.
        :param dif_id: 
        :return: None
        """
        self.args["input_file"] = input_files
        self.args["output_img_dir"] = os.path.join(self.output_dir, self.name)

    def spawn(self, chains):
        # type: (Dict[int, Chain]) -> None
        """
        Spawn the wgBCID threads contained in the chains dict
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        :return: None
        """
        if os.path.isfile(self.run_root_dir) and self.run_root_dir.endswith('hist.root'):
            input_files = [self.run_root_dir]
        else:
            make_hist_dir = os.path.join(self.run_root_dir, MakeHist.name)
            input_files = utils.find_files(make_hist_dir, 'root')

        self.args["topology_source"] = acqconfigxml_file_finder(self.run_root_dir, os.path.basename(self.run_root_dir))

        if not os.path.exists(self.output_dir):
            utils.mkdir_p(self.output_dir)
        for input_file in input_files:
            self._set_runtime_arguments(input_files=input_file, dif_id=None)
            link = analysis.WagasciAnalysis(self._wagasci_libdir)
            link.bcid_distribution(**self.args)


class AdcDistribution(Analyzer):
    """
    Wrapper around the adc_distribution function
    """
    name = "adc_distribution"
    depends = MakeHist.name
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.single_threaded

    _default_args = utils.get_arguments_ordered_dict(analysis.WagasciAnalysis.adc_distribution)
    _default_args.update({'chip_by_chip': True})

    def __init__(self, **kwargs):
        super(AdcDistribution, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)

    def _set_runtime_arguments(self, input_files, dif_id):
        # type: (List[str], Optional[int]) -> None
        """
        Set arguments at execution time. By execution time I mean the moment the adc distribution function  is
        executed through the spawn method.
        :param dif_id: 
        :return: None
        """
        self.args["input_file"] = input_files
        self.args["output_img_dir"] = os.path.join(self.output_dir, self.name)

    def spawn(self, chains):
        # type: (Dict[int, Chain]) -> None
        """
        Spawn the wgADC threads contained in the chains dict
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        :return: None
        """
        if os.path.isfile(self.run_root_dir) and self.run_root_dir.endswith('hist.root'):
            input_files = [self.run_root_dir]
        else:
            make_hist_dir = os.path.join(self.run_root_dir, MakeHist.name)
            input_files = utils.find_files(make_hist_dir, 'root')

        self.args["topology_source"] = acqconfigxml_file_finder(self.run_root_dir, os.path.basename(self.run_root_dir))

        if not os.path.exists(self.output_dir):
            utils.mkdir_p(self.output_dir)
        for input_file in input_files:
            self._set_runtime_arguments(input_files=input_file, dif_id=None)
            link = analysis.WagasciAnalysis(self._wagasci_libdir)
            link.adc_distribution(**self.args)


class Temperature(Analyzer):
    """
    Wrapper around the wgTemperature program
    """
    name = "temperature"
    depends = BeamSummaryData.name
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.multi_threaded

    _default_args = utils.get_arguments_ordered_dict(analysis.WagasciAnalysis.temperature)
    _default_args.update({'sqlite_database': "/hsm/nu/wagasci/data/temphum/mh_temperature_sensors_t2krun10.sqlite3"})

    def __init__(self, **kwargs):
        super(Temperature, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)

    def _set_runtime_arguments(self, input_files, dif_id):
        # type: (List[str], Optional[int]) -> None
        """
        Set arguments at execution time. By execution time I mean the moment the wgTemperature program is launched
        through the spawn method.
        :param dif_id: 
        :param input_files: input file
        :return: None
        """
        self.args["input_file"] = input_files

    def spawn(self, chains):
        # type: (Dict[int, Chain]) -> None
        """
        Spawn the wgTemperature threads contained in the chains dict
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        :return: None
        """
        if os.path.isfile(self.run_root_dir) and self.run_root_dir.endswith('.root'):
            input_files = [utils.extract_dif_id(self.run_root_dir), [self.run_root_dir]]
        else:
            input_files = {utils.extract_dif_id(f): f for f in utils.find_files(self.run_root_dir, 'root') if
                           utils.extract_dif_id(f) is not None}
        self.multiple_input_loop(input_files, chains)


class AdcCalibration(Analyzer):
    """
    Wrapper around the wgAdcCalib program (all passes)
    """
    name = "adc_calibration"
    depends = Temperature.name
    input_type = AnalyzerInputType.multiple_runs
    threading_type = AnalyzerThreadingType.multi_threaded

    _default_args = utils.get_arguments_ordered_dict(analysis.WagasciAnalysis.adc_calibration)
    _default_args.update({'passes': -1, 'enable_plotting': False, 'fixed_wallmrd_gain': False,
                          'fixed_wallmrd_input_dac': 121, 'silent_mode': True})

    def __init__(self, **kwargs):
        super(AdcCalibration, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)
        self.history_filename = self.run_name
        self.args["history_dir"] = self.output_dir
        if self.run_number is not None:
            self.history_filename = "{}_{}".format(self.history_filename, self.run_number)

    def _set_runtime_arguments(self, input_files, dif_id):
        # type: (List[str], Optional[int]) -> None
        """
        Set arguments at execution time. By execution time I mean the moment the wgAdcCalib program is launched
        through the spawn method.
        :param dif_id: 
        :param input_files: input file
        :return: None
        """
        self.args["tree_files"] = input_files
        self.args["history_file"] = "{}_ecal_dif_{}.root".format(self.history_filename, dif_id)
        self.args["dif_id"] = dif_id

    def spawn(self, chains):
        # type: (Dict[int, Chain]) -> None
        """
        Spawn the wgAdcCalib threads contained in the chains dict
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        :return: None
        """
        if not isinstance(self.run_root_dir, list):
            self.run_root_dir = [self.run_root_dir]
        input_files = {}
        self.args["topology_source"] = acqconfigxml_file_finder(self.run_root_dir[0],
                                                                os.path.basename(self.run_root_dir[0]))
        topology = self.get_topology(self.args["topology_source"])
        for dif_id in [int(dif_id) for dif_id in topology]:
            input_files[dif_id] = []
            for run_dir in sorted(self.run_root_dir):
                for root_file in utils.find_files(path=run_dir, extension='root', recursive=False):
                    if dif_id == utils.extract_dif_id(root_file):
                        input_files[dif_id].append(root_file)
                        break
        self.multiple_input_loop(input_files, chains)


class SanityCheck(Analyzer):
    """
    Wrapper around the sanity_check function
    """
    name = "sanity_check"
    depends = AdcCalibration.name
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.single_threaded

    _default_args = utils.get_arguments_ordered_dict(sanity_check.sanity_check)

    def __init__(self, **kwargs):
        super(SanityCheck, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)

    def _set_runtime_arguments(self, input_files, dif_id):
        # type: (List[str], Optional[int]) -> None
        """
        Set arguments at execution time. By execution time I mean the moment the program is launched
        through the spawn method.
        :param dif_id: 
        :return: None
        """
        self.args["input_path"] = input_files

    def spawn(self, chains):
        # type: (Dict[int, Chain]) -> None
        """
        Spawn the threads contained in the chains dict
        :param chains: dictionary where the key is the DIF ID and the value is a Chain recordclass object.
        :return: None
        """
        self.single_input_loop(self.run_root_dir, chains)


class AnalyzerFactory(ABC):
    """
    Abstract factory design patter to produce Analyzer objects.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs: arguments to pass to the analyzer object constructor
        """
        self._kwargs = kwargs

    @abc.abstractmethod
    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        # type: (str, str, **Any) -> None
        """
        Build analyzer (abstract method)
        :param run_root_dir: directory where the run files are stored
        :param output_dir: directory where to save the output files
        :param kwargs: additional arguments for the analyzer
        :return: None
        """
        self._kwargs.update(kwargs)


class DecoderFactory(AnalyzerFactory):
    depends = Decoder.depends
    name = Decoder.name
    input_type = Decoder.input_type
    threading_type = Decoder.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        # type: (str, str, **Any) -> Decoder
        """
        Build wgDecoder analyzer
        :param run_root_dir: directory where the run files are stored
        :param output_dir: directory where to save the output files
        :param kwargs: additional arguments for the analyzer
        :return: Analyzer object
        """
        super(DecoderFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return Decoder(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class MakeHistFactory(AnalyzerFactory):
    depends = MakeHist.depends
    name = MakeHist.name
    input_type = MakeHist.input_type
    threading_type = MakeHist.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        # type: (str, str, **Any) -> MakeHist
        """
        Build wgMakeHist analyzer
        :param run_root_dir: directory where the run files are stored
        :param output_dir: directory where to save the output files
        :param kwargs: additional arguments for the analyzer
        :return: MakeHist object
        """
        super(MakeHistFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return MakeHist(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class TdcCalibrationFactory(AnalyzerFactory):
    depends = TdcCalibration.depends
    name = TdcCalibration.name
    input_type = TdcCalibration.input_type
    threading_type = TdcCalibration.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        # type: (str, str, **Any) -> TdcCalibration
        """
        Build wgTdcCalibration analyzer
        :param run_root_dir: directory where the run files are stored
        :param output_dir: directory where to save the output files
        :param kwargs: additional arguments for the analyzer
        :return: TdcCalibration object
        """
        super(TdcCalibrationFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return TdcCalibration(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class SpillNumberFixerFactory(AnalyzerFactory):
    depends = SpillNumberFixer.depends
    name = SpillNumberFixer.name
    input_type = SpillNumberFixer.input_type
    threading_type = SpillNumberFixer.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        # type: (str, str, **Any) -> SpillNumberFixer
        """
        Build wgSpillNumberFixer analyzer
        :param run_root_dir: directory where the run files are stored
        :param output_dir: directory where to save the output files
        :param kwargs: additional arguments for the analyzer
        :return: Analyzer object
        """
        super(SpillNumberFixerFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return SpillNumberFixer(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class BeamSummaryDataFactory(AnalyzerFactory):
    depends = BeamSummaryData.depends
    name = BeamSummaryData.name
    input_type = BeamSummaryData.input_type
    threading_type = BeamSummaryData.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        # type: (str, str, **Any) -> BeamSummaryData
        """
        Build beam_summary_data analyzer
        :param run_root_dir: directory where the run files are stored
        :param output_dir: directory where to save the output files
        :param kwargs: additional arguments for the analyzer
        :return: Analyzer object
        """
        super(BeamSummaryDataFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return BeamSummaryData(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class ApplyDetectorFlagsFactory(AnalyzerFactory):
    depends = ApplyDetectorFlags.depends
    name = ApplyDetectorFlags.name
    input_type = ApplyDetectorFlags.input_type
    threading_type = ApplyDetectorFlags.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        # type: (str, str, **Any) -> ApplyDetectorFlags
        """
        Build apply_detector_flags analyzer
        :param run_root_dir: directory where the run files are stored
        :param output_dir: directory where to save the output files
        :param kwargs: additional arguments for the analyzer
        :return: Analyzer object
        """
        super(ApplyDetectorFlagsFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return ApplyDetectorFlags(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class SanityCheckFactory(AnalyzerFactory):
    depends = SanityCheck.depends
    name = SanityCheck.name
    input_type = SanityCheck.input_type
    threading_type = SanityCheck.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        # type: (str, str, **Any) -> SanityCheck
        """
        Build sanity_check analyzer
        :param run_root_dir: directory where the run files are stored
        :param output_dir: directory where to save the output files
        :param kwargs: additional arguments for the analyzer
        :return: Analyzer object
        """
        super(SanityCheckFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return SanityCheck(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class BcidDistributionFactory(AnalyzerFactory):
    depends = BcidDistribution.depends
    name = BcidDistribution.name
    input_type = BcidDistribution.input_type
    threading_type = BcidDistribution.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        # type: (str, str, **Any) -> BcidDistribution
        """
        Build bcid_distribution analyzer
        :param run_root_dir: directory where the run files are stored
        :param output_dir: directory where to save the output files
        :param kwargs: additional arguments for the analyzer
        :return: Analyzer object
        """
        super(BcidDistributionFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return BcidDistribution(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class AdcDistributionFactory(AnalyzerFactory):
    depends = AdcDistribution.depends
    name = AdcDistribution.name
    input_type = AdcDistribution.input_type
    threading_type = AdcDistribution.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        # type: (str, str, **Any) -> AdcDistribution
        """
        Build adc_distribution analyzer
        :param run_root_dir: directory where the run files are stored
        :param output_dir: directory where to save the output files
        :param kwargs: additional arguments for the analyzer
        :return: Analyzer object
        """
        super(AdcDistributionFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return AdcDistribution(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class TemperatureFactory(AnalyzerFactory):
    depends = Temperature.depends
    name = Temperature.name
    input_type = Temperature.input_type
    threading_type = Temperature.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        # type: (str, str, **Any) -> Temperature
        """
        Build wgTemperature analyzer
        :param run_root_dir: directory where the run files are stored
        :param output_dir: directory where to save the output files
        :param kwargs: additional arguments for the analyzer
        :return: Analyzer object
        """
        super(TemperatureFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return Temperature(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class AdcCalibrationFactory(AnalyzerFactory):
    depends = AdcCalibration.depends
    name = AdcCalibration.name
    input_type = AdcCalibration.input_type
    threading_type = AdcCalibration.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        # type: (str, str, **Any) -> AdcCalibration
        """
        Build wgAdcCalib analyzer
        :param run_root_dir: directory where the run files are stored
        :param output_dir: directory where to save the output files
        :param kwargs: additional arguments for the analyzer
        :return: Analyzer object
        """
        super(AdcCalibrationFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return AdcCalibration(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class AnalyzerFactoryProducer:
    """
    Abstract factory design patter to produce Analyzer objects.
    """
    _ReturnType = Union[DecoderFactory, MakeHistFactory, TdcCalibrationFactory, SpillNumberFixerFactory,
                        BeamSummaryDataFactory, ApplyDetectorFlagsFactory, TemperatureFactory, AdcCalibrationFactory,
                        BcidDistributionFactory, AdcDistributionFactory, SanityCheckFactory]

    def __init__(self, wagasci_libdir=None):
        # type: (str) -> None
        """
        :param wagasci_libdir: WAGASCI library directory
        """
        self._wagasci_libdir = wagasci_libdir
        pass

    def get_factory(self, type_of_factory, **kwargs):
        # type: (str, **Any) -> _ReturnType
        """
        Return the analyzer factory of the desired type
        :param type_of_factory: name of the factory
        :param kwargs: arguments to pass to the factory constructor
        :return: AnalyzerFactory object
        """
        if type_of_factory == Decoder.name:
            return DecoderFactory(wagasci_libdir=self._wagasci_libdir, **kwargs)
        elif type_of_factory == MakeHist.name:
            return MakeHistFactory(wagasci_libdir=self._wagasci_libdir, **kwargs)
        elif type_of_factory == TdcCalibration.name:
            return TdcCalibrationFactory(wagasci_libdir=self._wagasci_libdir, **kwargs)
        elif type_of_factory == SpillNumberFixer.name:
            return SpillNumberFixerFactory(wagasci_libdir=self._wagasci_libdir, **kwargs)
        elif type_of_factory == BeamSummaryData.name:
            return BeamSummaryDataFactory(wagasci_libdir=self._wagasci_libdir, **kwargs)
        elif type_of_factory == ApplyDetectorFlags.name:
            return ApplyDetectorFlagsFactory(wagasci_libdir=self._wagasci_libdir, **kwargs)
        elif type_of_factory == Temperature.name:
            return TemperatureFactory(wagasci_libdir=self._wagasci_libdir, **kwargs)
        elif type_of_factory == AdcCalibration.name:
            return AdcCalibrationFactory(wagasci_libdir=self._wagasci_libdir, **kwargs)
        elif type_of_factory == BcidDistribution.name:
            return BcidDistributionFactory(wagasci_libdir=self._wagasci_libdir, **kwargs)
        elif type_of_factory == AdcDistribution.name:
            return AdcDistributionFactory(wagasci_libdir=self._wagasci_libdir, **kwargs)
        elif type_of_factory == SanityCheck.name:
            return SanityCheckFactory(wagasci_libdir=self._wagasci_libdir, **kwargs)
        raise NotImplementedError("Factory %s not implemented or not recognized" % type_of_factory)
