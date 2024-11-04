#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import unittest

import numpy

import wagascianpy.plotting.colors
import wagascianpy.plotting.marker

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class TestMarkers(unittest.TestCase):

    def setUp(self):
        self.canvas = ROOT.TCanvas("c1", "c1", 1280, 720)
        self.graph = ROOT.TGraph(3, numpy.array([0, 1, 2], dtype=numpy.float64),
                                 numpy.array([0, 1, 2], dtype=numpy.float64))

    def test_single_marker(self):
        self.marker = wagascianpy.plotting.marker.Marker(1, "Hello World!")
        self.marker.line_color = wagascianpy.plotting.colors.Colors.Red
        self.output_filename = "./test_single_markers.png"

    def test_double_marker(self):
        self.marker = wagascianpy.plotting.marker.DoubleMarker(left_position=1,
                                                               left_text="Left text",
                                                               right_position=1.5,
                                                               right_text="Right text")
        self.marker.line_color = wagascianpy.plotting.colors.Colors.Blue
        self.marker.fill_color = wagascianpy.plotting.colors.Colors.Orange
        self.marker.transparency = 0.5
        self.output_filename = "./test_double_markers.pdf"

    def tearDown(self):
        self.graph.Draw()
        markers = self.marker.make_tobjects()
        for marker in markers:
            marker.Draw()
        self.canvas.Print(self.output_filename)


if __name__ == '__main__':
    unittest.main()
