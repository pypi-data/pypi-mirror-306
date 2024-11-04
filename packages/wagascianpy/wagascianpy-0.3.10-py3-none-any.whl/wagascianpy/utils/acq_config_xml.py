#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio, Eguchi Aoi

import json
import os
import re
import subprocess

from six import string_types
from typing import Tuple

import wagascianpy.utils
from wagascianpy.pyrmod.pyrmod import PyrameSlowModule
from wagascianpy.utils.environment import WagasciEnvironment


###############################################################################
#                              WagasciConfig                                  #
###############################################################################

class WagasciConfig(PyrameSlowModule):
    _wg_config_module_name = "wg_config"

    def __init__(self, *arg, **kwargs):
        super(WagasciConfig, self).__init__(module_name=self._wg_config_module_name, *arg, **kwargs)


###############################################################################
#                          create_acq_config_xml                              #
###############################################################################

def create_acq_config_xml(topology, acq_config_path=None, acq_config_xml=None, running_dir=None, run_top_dir=None,
                          dif_mapping_file=None, mac_mapping_file=None, simulate=False, use_rundb=False):
    # type: (...) -> Tuple[int, str]
    """ Create Pyrame configuration XML file for the data taking acquisition
            :param topology: topology string
            :param acq_config_path: directory where to create the Pyrame XML configuration file
            :param acq_config_xml: file name of the Pyrame XML configuration file
            :param running_dir: directory were the data is temporarily stored during data acquisition
            :param run_top_dir: directory were the data is copied after data acquisition
            :param dif_mapping_file: JSON file containing the mapping between DIF ID number and GDCC port number
            :param mac_mapping_file: JSON file containing the mapping between GDCC ID number and GDCC MAC address
            :param simulate: in the configuration file set the simulation fields to true.
             Different from the Pyrame module call simulation.
            :param use_rundb: If set the Pyrame rundb module is activated

    """

    _conf_string = r'wg_config('
    for var_name, var_value in locals().items():
        if var_value not in [None, ""] and not var_name.startswith('_'):
            if isinstance(var_value, string_types):
                var_value = var_value.replace(',', r'\,')
            _conf_string += r'{}={},'.format(var_name, var_value)
    _conf_string.rstrip(',')
    _conf_string += r')'

    try:
        WagasciConfig(conf_string=_conf_string)
    except RuntimeError as err:
        return 0, str(err)

    return 1, "ok"


###############################################################################
#                                 get_net_if                                  #
###############################################################################

def get_net_if():
    # type: (...) -> str
    """Return the name of the network interface connected to the 192.168.10.0/24 LAN"""
    gdcc_pc_dev = None
    get_dev_command = "ip -o addr show"
    process = subprocess.Popen(get_dev_command.split(), stdout=subprocess.PIPE)
    ps_output, error = process.communicate()
    if error:
        raise ValueError("Error when looking for network interface : %s" % error)
    for line in ps_output.strip().decode().splitlines():
        if re.search("192.168.10", line):
            fields = line.strip().split()
            gdcc_pc_dev = fields[1]
            break
    if gdcc_pc_dev is None:
        print("could not find a network interface connected "
              "to the 192.168.10.0 LAN")
        gdcc_pc_dev = "eth0"
    return gdcc_pc_dev


###############################################################################
#                          acqconfigxml_file_finder                           #
###############################################################################

def acqconfigxml_file_finder(run_root_dir, run_name):
    # type: (str, str) -> str
    env = wagascianpy.utils.environment.WagasciEnvironment()
    path1 = os.path.join(run_root_dir, run_name + ".xml")
    path2 = os.path.join(run_root_dir, os.path.basename(env['WAGASCI_ACQCONFIGDIR']), env['WAGASCI_ACQCONFIGXML'])
    path3 = os.path.join(run_root_dir, env['WAGASCI_ACQCONFIGXML'])
    if os.path.exists(path1):
        acqconfigxml = path1
    elif os.path.exists(path2):
        acqconfigxml = path2
    elif os.path.exists(path3):
        acqconfigxml = path3
    else:
        raise EnvironmentError("XML acquisition configuration file not found. "
                               "Run root dir : {}, Run name : {}".format(run_root_dir, run_name))
    return acqconfigxml
