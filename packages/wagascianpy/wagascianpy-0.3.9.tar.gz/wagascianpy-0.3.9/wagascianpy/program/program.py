#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import os
import re

from six import string_types
from typing import Optional, Dict, Tuple, List

# Tries to guess the number of cores of the machine to correctly extimate the maximum number of threads to spawn
try:
    from multiprocessing import cpu_count
except ImportError as err:
    if "multiprocessing" in repr(err):
        # noinspection PyUnresolvedReferences
        from os import cpu_count
    else:
        raise

import wagascianpy.analysis.analysis as analysis
import wagascianpy.analysis.analyzer as analyzer
import wagascianpy.utils.environment as environment
import wagascianpy.utils.utils as utils

MAX_THREADS = 8


class Program(object):
    """
    Class to analyze a list of runs as an uninterrupted job. The usage scenario is when
    you need to analyze multiple runs in one batch and do not want to monitor the chain
    continuously.
    """

    def __init__(self, wagasci_libdir=None):
        # type: (Optional[str]) -> None
        """
        :param wagasci_libdir: path to the directory containing the WAGASCI library
        """

        global MAX_THREADS
        self._stop_on_exception = True
        self._enforce_dependencies = True
        self._run_dict = {}
        self._output_dir_same_as_input = True
        self._save_dict = {}
        self._multiple_run_analyzer_save_location = None
        self._analyzer_factories = []
        self._wagasci_libdir = wagasci_libdir

        # Enable thread safety
        env = environment.WagasciEnvironment()
        if self._wagasci_libdir is None:
            try:
                self._wagasci_libdir = env['WAGASCI_LIBDIR']
            except KeyError as error:
                raise KeyError("Could not find WAGASCI library directory : %s" % error)
        wagascilib_call = analysis.WagasciAnalysis(self._wagasci_libdir)
        wagascilib_call.enable_thread_safety()
        nproc = cpu_count()
        if not nproc:
            MAX_THREADS = 1
        elif 1 <= nproc <= MAX_THREADS:
            MAX_THREADS = nproc

    def _set_input_output(self, is_first_analyzer, run_name, run_root_dir):
        # type: (bool, str, str) -> Tuple[str, str]
        """setup the input directory and output directory for each analyzer"""
        if is_first_analyzer:
            if self._output_dir_same_as_input:
                output_dir = run_root_dir
            else:
                output_dir = self._save_dict[run_name]
        else:
            if self._output_dir_same_as_input:
                output_dir = run_root_dir
            else:
                output_dir = self._save_dict[run_name]
                run_root_dir = self._save_dict[run_name]
        return output_dir, run_root_dir

    # noinspection PyMethodMayBeStatic
    def _get_run_number(self, run_name):
        # type: (str) -> int
        """Parse run name for the run number"""
        match = re.search(r'.*_([\d]+)$', run_name)
        run_number = None if match is None else int(match.group(1))
        return run_number

    def _get_run_numbers(self):
        # type: (...) -> List[int]
        """Parse run names for the run numbers"""
        run_numbers = []
        for run_name in self._run_dict:
            run_numbers.append(self._get_run_number(run_name))
        return run_numbers

    def start(self):
        # type: (...) -> None
        """
        Start the program execution. For each analyzer that is to be applied to the input runs, there are two
        possibilities. One is that the analyzer accepts as input a single run. In such a case, the runs are looped
        over and fed one by one to the analyzer. The other one is that the analyzer accepts as input multiple runs.
        In such a case, all the runs in the selected interval are directly passed to the analyzer.

        It is assumed that for all the analyzers (but the raw data decoder) the input files are the same as the
        output files. In other words, the output information is appended to the ROOT input files or included in the
        same directory.

        Depending on the analyzer, multiple threads might be spawn, one for each input run. By design not all parts
        of ROOT are thread-safe, so it is not possible to run some analyzers in a multithreaded environment.

        :return: None
        """

        # setup first analyzer flags
        is_first_analyzer = {}
        for run_name in self._run_dict.keys():
            is_first_analyzer[run_name] = True
        # setup WagasciAnalysis thread chains
        run_chains = {}
        for run_name in self._run_dict.keys():
            run_chains[run_name] = {}
        # loop over the analyzers
        for analyzer_factory in self._analyzer_factories:
            print('Found analyzer {}'.format(analyzer_factory.name))
            if analyzer_factory.input_type == analyzer.AnalyzerInputType.single_run:
                # loop over the single runs
                for run_name, run_root_dir in sorted(self._run_dict.items()):
                    try:
                        # setup the input directory and output directory for each analyzer
                        output_dir, run_root_dir = self._set_input_output(is_first_analyzer=is_first_analyzer[run_name],
                                                                          run_name=run_name, run_root_dir=run_root_dir)
                        is_first_analyzer[run_name] = False
                        # get the run number from the run name
                        run_number = self._get_run_number(run_name)
                        # Get the analyzer from the factory
                        run_analyzer = analyzer_factory.get_analyzer(run_root_dir=run_root_dir, run_name=run_name,
                                                                     run_number=run_number, output_dir=output_dir)
                        # Spawn run analyzer
                        print('Applying "{}" analyzer on run "{}"'.format(run_analyzer.name, run_name))
                        run_analyzer.spawn(run_chains[run_name])
                        print("Total number of thread chains : {}".format(utils.count_threads(run_chains)))
                        # Limit number of threads
                        if analyzer_factory.threading_type == analyzer.AnalyzerThreadingType.multi_threaded:
                            utils.limit_chains(run_chains, MAX_THREADS)
                        else:
                            utils.join_single_chain(run_chains[run_name])
                    except Exception as exception:
                        if self._stop_on_exception:
                            raise exception
                        else:
                            print("Run {} failed with exception : {}".format(run_name, str(exception)))
            elif analyzer_factory.input_type == analyzer.AnalyzerInputType.multiple_runs:
                chain = {}
                # set the name for the multirun analyzer
                run_name = analyzer_factory.name
                run_numbers = self._get_run_numbers()
                min_run_number = min(run_numbers)
                max_run_number = max(run_numbers)
                if min_run_number is not None and max_run_number is not None:
                    run_name = "{}_from_{}_to_{}".format(run_name, min_run_number, max_run_number)
                try:
                    # set input and output directories
                    if all(is_first_analyzer.values()) or not self._save_dict:
                        run_root_dir = sorted(list(self._run_dict.values()))
                    else:
                        run_root_dir = sorted(list(self._save_dict.values()))
                    if self._multiple_run_analyzer_save_location is None:
                        raise ValueError("To use a multiple run analyzer you must set its save location first")
                    output_dir = self._multiple_run_analyzer_save_location
                    # Get analyzer from factory
                    ana = analyzer_factory.get_analyzer(run_root_dir=run_root_dir, run_name=run_name,
                                                        run_number=None, output_dir=output_dir)
                    print("Applying %s analyzer on runs from %s to %s"
                          % (ana.name, min_run_number, max_run_number))
                    # Spawn all the threads and join them rightaway
                    ana.spawn(chain)
                    utils.join_single_chain(chain)
                except Exception as exception:
                    if self._stop_on_exception:
                        raise exception
                    else:
                        print("{} failed with exception : {}".format(run_name, str(exception)))
            else:
                raise NotImplementedError("Analyzer type not recognized %s" % analyzer_factory.input_type)
            utils.join_chains(run_chains)
            for run_name in self._run_dict.keys():
                run_chains[run_name] = {}

    @property
    def multiple_runs_analyzer_save_location(self):
        # type: (...) -> str
        """
        In case of analyzers which need to analyze multiple runs at once and store the results in another directory,
        the user needs to specify it. One example is the wgAdcCalib program that needs to store the gain and dark
        noise history TTrees in some external directory.
        :return: output directory for analyzers that process multiple runs
        """
        return self._multiple_run_analyzer_save_location

    @multiple_runs_analyzer_save_location.setter
    def multiple_runs_analyzer_save_location(self, location):
        # type: (str) -> None
        """
        In case of analyzers which need to analyze multiple runs at once and store the results in another directory,
        the user needs to specify it. One example is the wgAdcCalib program that needs to store the gain and dark
        noise history TTrees in some external directory.
        :param location: output directory for analyzers that process multiple runs
        :return: None
        """
        if not isinstance(location, string_types):
            raise TypeError("multiple run analyzersave location must be a string path")
        if not os.path.exists(location):
            utils.mkdir_p(location)
        self._multiple_run_analyzer_save_location = location

    def set_run_location(self, run_dict):
        # type: (Dict[str, str]) -> None
        """
        Set the input runs dictionary
        :param run_dict: input runs dictionary (key: run name, value: run path)
        :return: None
        """
        self._run_dict = run_dict

    def get_run_location(self):
        # type: (...) -> Dict[str, str]
        """
        Get the input runs dictionary
        :return: input runs dictionary (key: run name, value: run path)
        """
        return self._run_dict

    def get_save_location(self):
        # type: (...) -> Dict[str, str]
        """
        Get a custom location where to store each run decoded data.
        :return: Dictionary where the key is the run name and the value is the path of the folder where the decoded
                 data is to be stored

        """
        return self._save_dict

    def set_save_location(self, save_dict):
        # type: (Dict[str, str]) -> None
        """
        Set a custom location where to store each run decoded data.
        :param save_dict: Dictionary where the key is the run name and the value is the path of the folder where the
                          decoded data is to be stored
        :rtype: None
        """
        self._save_dict = save_dict
        for run_name in self._run_dict:
            if run_name not in save_dict:
                raise KeyError("The save location dictionary does not contain the run named '%s'" % run_name)
        self._output_dir_same_as_input = False

    def output_dir_same_as_input(self):
        # type: (...) -> None
        """
        Set the output directory as the same as the input directory
        :return: None
        """
        self._save_dict.clear()
        self._output_dir_same_as_input = True

    def _check_dependencies(self, factory):
        # type: (analyzer.AnalyzerFactory) -> analyzer.AnalyzerFactory
        """
        Check that the order in which the analyzers are called is correct (that each analyzer dependency is satisfied)
        :param factory: factory
        :return: same factory
        """
        if factory.depends and factory.depends not in [f.name for f in self._analyzer_factories]:
            raise RuntimeError("{} depends on {} but not found".format(factory.name, factory.depends))
        return factory

    def add_step(self, name, **kwargs):
        # type: (str, ...) -> None
        """
        Add an analyzer to the list of analyzers of the program
        :param name: analyzer name
        :param kwargs: arguments to pass to the analyzer
        :return: None
        """
        producer = analyzer.AnalyzerFactoryProducer(self._wagasci_libdir)
        factory = producer.get_factory(name, **kwargs)
        if self._enforce_dependencies:
            analyzer_factory = self._check_dependencies(factory)
        else:
            analyzer_factory = factory
        self._analyzer_factories.append(analyzer_factory)

    def do_not_stop_on_exception(self):
        # type: (...) -> None
        """
        Do not stop the program execution if an analyzer fails
        :return: None
        """
        self._stop_on_exception = False

    def stop_on_exception(self):
        # type: (...) -> None
        """
        Stop the program execution if an analyzer fails
        :return: None
        """
        self._stop_on_exception = True

    def enforce_dependencies(self):
        # type: (...) -> None
        """
        Make sure that each analyzer is called in the right order
        :return: None
        """
        self._enforce_dependencies = True

    def do_not_enforce_dependencies(self):
        # type: (...) -> None
        """
        Allow an analyzer to be called even if the previous one is not present
        :return: None
        """
        self._enforce_dependencies = False
