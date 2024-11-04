#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio

import json
import os
import unittest

import wagascianpy.analysis.analysis
import wagascianpy.utils.environment


class TestTopology(unittest.TestCase):

    def setUp(self):
        env = wagascianpy.utils.environment.WagasciEnvironment()
        self.wagasci_lib = env["WAGASCI_LIBDIR"]

        self.topology_source = os.path.abspath(
            './test_simple_repo/physics_run_2020-01-15_14-49-32_60/physics_run_2020-01-15_14-49-32_60.xml')

    def test_get_dif_topology(self):
        expected_topology_json = {
            "2": {
                "0": "32", "1": "32", "2": "32"},
            "3": {
                "0": "32", "1": "32", "2": "32"},
            "4": {
                "0": "32", "1": "32", "10": "32", "11": "32", "12": "32", "13": "32", "14": "32", "15": "32",
                "16": "32", "17": "32", "18": "32", "19": "32", "2": "32", "3": "32", "4": "32", "5": "32",
                "6": "32", "7": "32", "8": "32", "9": "32"},
            "5": {
                "0": "32", "1": "32", "10": "32", "11": "32", "12": "32", "13": "32", "14": "32", "15": "32",
                "16": "32", "17": "32", "18": "32", "19": "32", "2": "32", "3": "32", "4": "32", "5": "32",
                "6": "32", "7": "32", "8": "32", "9": "32"},
            "6": {
                "0": "32", "1": "32", "10": "32", "11": "32", "12": "32", "13": "32", "14": "32", "15": "32",
                "16": "32", "17": "32", "18": "32", "19": "32", "2": "32", "3": "32", "4": "32", "5": "32",
                "6": "32", "7": "32", "8": "32", "9": "32"},
            "7": {
                "0": "32", "1": "32", "10": "32", "11": "32", "12": "32", "13": "32", "14": "32", "15": "32",
                "16": "32", "17": "32", "18": "32", "19": "32", "2": "32", "3": "32", "4": "32", "5": "32",
                "6": "32", "7": "32", "8": "32", "9": "32"}
        }
        process = wagascianpy.analysis.analysis.WagasciAnalysis(lib_dir=self.wagasci_lib)
        dif_topology_string, dif_topology_pointer = process.get_dif_topology(self.topology_source, "", "")
        topology_json = json.loads(dif_topology_string)
        process.free_topology(dif_topology_pointer)
        self.assertEqual(expected_topology_json, topology_json)


if __name__ == '__main__':
    unittest.main()
