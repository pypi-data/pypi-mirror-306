#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc
import ctypes
import os
from datetime import datetime
from typing import List, Union, Optional, Any

import ROOT
import numpy

import wagascianpy.analysis.spill as spill
import wagascianpy.database.bsddb as bsddb
import wagascianpy.database.wagascidb as wagascidb
import wagascianpy.plotting as pl
import wagascianpy.plotting.colors as colors
import wagascianpy.plotting.graph as graph
import wagascianpy.plotting.harvest as harvest
import wagascianpy.plotting.marker as marker
import wagascianpy.plotting.topology as topol

ROOT.PyConfig.IgnoreCommandLineOptions = True

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

# compatible with Python 2 *and* 3
try:
    # noinspection PyUnresolvedReferences
    IntTypes = (int, long)  # Python2
except NameError:
    IntTypes = int  # Python3


class Plotter(ABC):

    def __init__(self,
                 output_file_path="./plot.pdf",
                 save_tfile=False,
                 markers=marker.MarkerTuple(run=False, maintenance=False, trouble=False, bsd=False)):
        # type: (str, bool, marker.MarkerTuple) -> None
        ROOT.PyConfig.IgnoreCommandLineOptions = True
        ROOT.gROOT.IsBatch()
        self._canvas = ROOT.TCanvas("canvas", "canvas", 1280, 720)
        self._title = ""
        self._graphs = []
        self._markers = []
        self._multi_graph = None
        self._1d_draw_options = "AL"
        self._2d_draw_options = "ZCOLPCOL"
        self._output_file_path = output_file_path
        self._enabled_markers = markers
        self._save_tfile = save_tfile
        self._plot_legend_flag = False
        self._xdata_is_datetime = True
        self._yrange = (None, None)
        self._logscale = False

    def template_plotter(self):
        # type: (...) -> None
        self._graphs = self.setup_graphs()
        self.set_title()
        for gr in self._graphs:
            self.gather_data(gr)
        self.change_graph_titles(self._graphs)
        self.build_multigraph()
        self.change_yaxis_title(self._multi_graph)
        self.add_run_markers()
        self.add_maintenance_day_markers()
        self.add_trouble_markers()
        self.add_bsd_markers()
        self.plot()
        if self._save_tfile:
            self.save()
        self._canvas.Close()

    @property
    def plot_legend_flag(self):
        # type: (...) -> bool
        return self._plot_legend_flag

    @plot_legend_flag.setter
    def plot_legend_flag(self, plot_legend_flag):
        # type: (bool) -> None
        if not isinstance(plot_legend_flag, bool):
            raise TypeError("Plot legend flag must be a boolean")
        self._plot_legend_flag = plot_legend_flag

    @property
    def draw_options_1d(self):
        # type: (...) -> str
        return self._1d_draw_options

    @draw_options_1d.setter
    def draw_options_1d(self, draw_options):
        # type: (str) -> None
        self._1d_draw_options = draw_options

    @property
    def draw_options_2d(self):
        # type: (...) -> str
        return self._2d_draw_options

    @draw_options_2d.setter
    def draw_options_2d(self, draw_options):
        # type: (str) -> None
        self._2d_draw_options = draw_options

    @property
    def xdata_is_datetime(self):
        # type: (...) -> bool
        return self._xdata_is_datetime

    @xdata_is_datetime.setter
    def xdata_is_datetime(self, xdata_is_datetime):
        # type: (bool) -> None
        assert isinstance(xdata_is_datetime, bool), "xdata_is_datetime only accept a boolean value"
        self._xdata_is_datetime = xdata_is_datetime

    @property
    def logscale(self):
        # type: (...) -> bool
        return self._logscale

    @logscale.setter
    def logscale(self, logscale):
        # type: (bool) -> None
        self._logscale = logscale

    @abc.abstractmethod
    def set_title(self):
        # type: (...) -> None
        if self._topology.how_many_enabled() == 1:
            self._title += " for {}".format(self._topology.get_enabled()[0].name)
        elif self._topology.how_many_enabled() == 2:
            self._title += " for {} and {}".format(self._topology.get_enabled()[0].name,
                                                   self._topology.get_enabled()[1].name)

    @abc.abstractmethod
    def setup_graphs(self):
        # type: (...) -> None
        pass

    @abc.abstractmethod
    def gather_data(self, gr):
        # type: (pl.graph.Graph) -> None
        pass

    def build_multigraph(self):
        # type: (...) -> None
        self._multi_graph = ROOT.TMultiGraph()
        self._multi_graph.SetName("multi_graph")
        ROOT.TGaxis.SetMaxDigits(3)
        for gr in self._graphs:
            if not gr.is_empty() and not isinstance(gr, graph.Graph2D):
                self._multi_graph.Add(gr.make_tgraph())
                if gr.yaxis_color != colors.Colors.Black.value:
                    self._multi_graph.GetYaxis().SetTitleColor(gr.yaxis_color)
                    self._multi_graph.GetYaxis().SetLabelColor(gr.yaxis_color)
                    self._multi_graph.GetYaxis().SetAxisColor(gr.yaxis_color)
        self._multi_graph.SetTitle(self._title)
        if self._xdata_is_datetime:
            self._multi_graph.GetXaxis().SetNdivisions(9, 3, 0, ROOT.kTRUE)
            self._multi_graph.GetXaxis().SetTimeDisplay(1)
            self._multi_graph.GetXaxis().SetTimeFormat("#splitline{%d %b}{%H:%M}%F1970-01-01 00:00:00")
            self._multi_graph.GetXaxis().SetLabelOffset(0.03)
        if self._yrange[0] is not None and self._yrange[1] is not None:
            self._multi_graph.GetYaxis().SetRangeUser(self._yrange[0], self._yrange[1])

    def add_maintenance_day_markers(self):
        # type: (...) -> None
        if self._enabled_markers.maintenance and hasattr(self, "_start") and hasattr(self, "_stop"):
            self.make_maintenance_day_markers(start=self._start, stop=self._stop,
                                              wagasci_database=self._patron.wagasci_database)

    def add_run_markers(self):
        # type: (...) -> None
        if self._enabled_markers.run and hasattr(self, "_start") and hasattr(self, "_stop"):
            self.make_run_markers(start=self._start, stop=self._stop,
                                  wagasci_database=self._patron.wagasci_database)

    def add_bsd_markers(self):
        # type: (...) -> None
        if self._enabled_markers.bsd and hasattr(self, "_start") and hasattr(self, "_stop"):
            self.make_bsd_markers(start=self._start, stop=self._stop,
                                  bsd_database=self._bsd_database if hasattr(self, "_bsd_database") else None)

    def add_trouble_markers(self):
        # type: (...) -> None
        if self._enabled_markers.trouble and hasattr(self, "_start") and hasattr(self, "_stop"):
            self.make_trouble_markers(start=self._start, stop=self._stop,
                                      wagasci_database=self._patron.wagasci_database)

    def change_graph_titles(self, graphs):
        # type: (List[graph.Graph]) -> None
        pass

    def change_yaxis_title(self, multigraph):
        # type: (ROOT.TMultiGraph) -> None
        pass

    def make_run_markers(self, wagasci_database, start, stop=None):
        # type: (str, Union[int, datetime], Optional[Union[int, datetime]]) -> None
        with wagascidb.WagasciDataBase(db_location=wagasci_database) as db:
            if isinstance(start, IntTypes):
                if not stop:
                    stop = db.get_last_run_number(only_good=False)
                records = db.get_run_interval(run_number_start=start, run_number_stop=stop, only_good=False)
            else:
                if not stop:
                    stop = datetime.now()
                records = db.get_time_interval(datetime_start=start, datetime_stop=stop, only_good=False,
                                               include_overlapping=False)
        counter = 0
        markers = []
        for record in records:
            mk = marker.DoubleMarker(left_position=record["start_time"],
                                     right_position=record["stop_time"],
                                     left_text="WAGASCI run %s" % record["run_number"],
                                     right_text="",
                                     line_color=colors.Colors.Blue)
            if counter % 2 == 0:
                mk.fill_color = colors.Colors.Azure.value
            else:
                mk.fill_color = colors.Colors.Orange.value
            mk.transparency = 0.1
            markers.append(mk)
            counter += 1
        self._markers += markers

    def make_bsd_markers(self, bsd_database, start, stop=None):
        # type: (str, datetime, Optional[datetime]) -> None
        with bsddb.BsdDataBase(bsd_database_location=bsd_database) as db:
            if not stop:
                stop = datetime.now()
            records = db.get_time_interval(datetime_start=start, datetime_stop=stop, only_good=False,
                                           include_overlapping=False)
        counter = 0
        markers = []
        for record in records:
            mk = marker.DoubleMarker(left_position=record["start_time"],
                                     right_position=record["stop_time"],
                                     left_text=record["name"],
                                     right_text="",
                                     line_color=colors.Colors.Blue)
            if counter % 2 == 0:
                mk.fill_color = colors.Colors.Azure.value
            else:
                mk.fill_color = colors.Colors.Orange.value
            mk.transparency = 0.1
            markers.append(mk)
            counter += 1
        self._markers += markers

    def make_maintenance_day_markers(self, wagasci_database, start, stop=None):
        # type: (str, Union[int, datetime], Optional[Union[int, datetime]]) -> None
        markers = marker.MaintenanceDays(
            start=start, stop=stop, wagasci_database=wagasci_database
        ).get_markers(include_overlapping=False)
        self._markers += markers

    def make_trouble_markers(self, wagasci_database, start, stop=None):
        # type: (str, Union[int, datetime], Optional[Union[int, datetime]]) -> None
        markers = marker.TroubleEvents(
            start=start, stop=stop, wagasci_database=wagasci_database
        ).get_markers(include_overlapping=False)
        self._markers += markers

    def _has_both_graph1d_and_graph2d(self):
        # type: (...) -> bool
        has_graph1d = self._how_many_graph1d() > 0
        has_graph2d = self._how_many_graph2d() > 0
        return has_graph2d and has_graph1d

    def _how_many_graph1d(self):
        # type: (...) -> int
        return sum(map(lambda g: not isinstance(g, graph.Graph2D) and not g.is_empty(),
                       self._graphs))

    def _how_many_graph2d(self):
        # type: (...) -> int
        return sum(map(lambda g: isinstance(g, graph.Graph2D) and not g.is_empty(),
                       self._graphs))

    def plot(self):
        # type: (...) -> None

        # PREPARE CANVAS
        ROOT.gStyle.Reset("Modern")
        ROOT.gStyle.SetTitleFontSize(0.035)
        pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
        pad2 = ROOT.TPad("pad2", "", 0, 0, 1, 1)
        self._canvas.cd()
        if self._has_both_graph1d_and_graph2d():
            self._canvas.SetFillColor(0)
            self._canvas.SetBorderMode(0)
            pad1.SetGrid()
            pad2.SetFillStyle(4000)
            pad2.SetFrameFillStyle(0)
            pad1.Draw()
            pad1.cd()

        # PLOT 2D HISTOGRAMS
        for gr in self._graphs:
            if isinstance(gr, pl.graph.Graph2D) and not gr.is_empty():
                tgraph = gr.make_tgraph(self.logscale)
                tgraph.SetTitle(self._title)
                tgraph.Draw(self.draw_options_2d)
                tgraph.GetYaxis().SetTitleOffset(0.75)
                if self.logscale:
                    self._canvas.SetLogy()
                    pad1.SetLogy()

        # PLOT 1D GRAPHS
        ROOT.gPad.Update()
        xmin = ctypes.c_double(0)
        ymin = ctypes.c_double(0)
        xmax = ctypes.c_double(0)
        ymax = ctypes.c_double(0)
        if self._has_both_graph1d_and_graph2d():
            pad1.GetRangeAxis(xmin, ymin, xmax, ymax)
            ymin = self._multi_graph.GetYaxis().GetXmin()
            ymax = self._multi_graph.GetYaxis().GetXmax()
            pad2.RangeAxis(xmin.value, ymin, xmax.value, ymax)
            pad2.Draw()
            pad2.cd()
        if self._how_many_graph1d() > 0:
            self._multi_graph.Draw(self.draw_options_1d)

        # PLOT MARKERS
        ROOT.gPad.Update()
        tobjects = []
        for mk in self._markers:
            tobjects += mk.make_tobjects()
        for tobj in tobjects:
            tobj.Draw()
        if self._plot_legend_flag:
            tlegend = ROOT.TLegend(0.13, 0.7, 0.4, 0.89)
            tlegend.SetFillColorAlpha(ROOT.kWhite, 1.)
            for gr in [gr for gr in self._graphs if not gr.is_empty()]:
                opt = "f"
                if "l" in self.draw_options_1d.lower():
                    opt += "l"
                if "p" in self.draw_options_1d.lower():
                    opt += "p"
                tlegend.AddEntry(gr.id, gr.title, opt)
            tlegend.Draw()

        # PRINT TO FILE
        ROOT.gPad.Update()
        self._canvas.Print(self._output_file_path)

    def save(self):
        # type: (...) -> None
        output_path = os.path.splitext(self._output_file_path)[0] + ".root"
        output_tfile = ROOT.TFile(output_path, "RECREATE")
        output_tfile.cd()
        self._canvas.Write()
        self._multi_graph.Write()
        output_tfile.Write()
        output_tfile.Close()


class BsdPlotter(Plotter, ABC):

    def __init__(self,
                 bsd_database,  # type: str
                 bsd_repository,  # type: str
                 start,  # type: Union[int, str, datetime]
                 stop=None,  # type: Optional[int, str, datetime]
                 wagasci_database=None,  # type: Optional[str]
                 t2krun=10,  # type: int
                 only_good=False,  # type: bool
                 *args, **kwargs):
        super(BsdPlotter, self).__init__(*args, **kwargs)
        self._bsd_database = bsd_database
        self._bsd_repository = bsd_repository
        self._t2krun = t2krun
        self._only_good = only_good
        self._start = start
        self._stop = stop
        self._patron = harvest.Patron(start=start, stop=stop, wagasci_database=wagasci_database)
        self._bsd_harvester_class = None

    @abc.abstractmethod
    def set_title(self):
        # type: (...) -> None
        pass

    @abc.abstractmethod
    def setup_graphs(self):
        # type: (...) -> None
        pass

    def gather_data(self, gr):
        # type: (pl.graph.Graph) -> None
        assert self._bsd_harvester_class is not None, "Derived class must set the _bsd_harvester_class attribute"
        if gr.id != "BSD":
            raise ValueError("Wrong graph with title {} and ID {}".format(gr.title, gr.id))
        self._patron.harvester = self._bsd_harvester_class(database=self._bsd_database, repository=self._bsd_repository,
                                                           t2krun=self._t2krun)
        gr.xdata, gr.ydata = self._patron.gather_data(only_good=self._only_good)


class BsdPotPlotter(BsdPlotter):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(BsdPotPlotter, self).__init__(*args, **kwargs)
        self._bsd_harvester_class = harvest.BsdPotHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "Delivered POT during run {};;POT".format(self._t2krun)

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = False
        self.xdata_is_datetime = True
        bsd_pot = graph.Graph("Delivered POT", "BSD")
        bsd_pot.color = colors.Colors.Red.value
        return [bsd_pot]


class BsdSpillPlotter(BsdPlotter):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(BsdSpillPlotter, self).__init__(*args, **kwargs)
        self._bsd_harvester_class = harvest.BsdSpillHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "BSD spill history during run {};;spill number".format(self._t2krun)

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = False
        self.xdata_is_datetime = True
        bsd = graph.Graph("BSD spill history", "BSD")
        bsd.color = colors.Colors.Red.value
        return [bsd]


class WagasciPlotter(Plotter, ABC):

    def __init__(self,
                 bsd_database,  # type: str
                 bsd_repository,  # type: str
                 wagasci_database,  # type: str
                 wagasci_repository,  # type: str
                 start,  # type: Union[str, int]
                 stop=None,  # type: Optional[Union[str, int]]
                 topology=None,  # type: Optional[pl.topology.Topology]
                 t2krun=10,  # type: int
                 only_good=False,  # type: bool
                 *args, **kwargs):
        # type: (...) -> None
        super(WagasciPlotter, self).__init__(*args, **kwargs)
        self._bsd_database = bsd_database
        self._bsd_repository = bsd_repository
        self._wagasci_repository = wagasci_repository
        self._t2krun = t2krun
        self._start = start
        self._stop = stop
        self._patron = harvest.Patron(start=start, stop=stop, wagasci_database=wagasci_database)
        self._wagasci_harvester_class = None
        self._bsd_harvester_class = None
        self._topology = topology if topology is not None else pl.topology.Topology()
        self._only_good = only_good

    @abc.abstractmethod
    def set_title(self):
        # type: (...) -> None
        super(WagasciPlotter, self).set_title()

    @abc.abstractmethod
    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        graphs = []
        for enabled_detector in self._topology.get_enabled():
            gr = graph.Graph(enabled_detector.name)
            gr.color = enabled_detector.name
            graphs.append(gr)
        return graphs

    def gather_data(self, gr):
        # type: (pl.graph.Graph) -> None
        if gr.id == "BSD":
            assert self._bsd_harvester_class is not None, \
                "Derived class must set the _bsd_harvester_class attribute"
            if not self._patron.is_harvester_ready() or \
                    not isinstance(self._patron.harvester, self._bsd_harvester_class):
                self._patron.harvester = self._bsd_harvester_class(
                    database=self._bsd_database,
                    repository=self._bsd_repository,
                    t2krun=self._t2krun)
            gr.xdata, gr.ydata = self._patron.gather_data(only_good=self._only_good)
        else:
            for enabled_detector in self._topology.get_enabled():
                if gr.id == str(enabled_detector.name):
                    assert self._wagasci_harvester_class is not None, \
                        "Derived class must set the _wagasci_harvester_class attribute"
                    if not self._patron.is_harvester_ready() or \
                            not isinstance(self._patron.harvester, self._wagasci_harvester_class):
                        self._patron.harvester = self._wagasci_harvester_class(
                            database=self._patron.wagasci_database,
                            repository=self._wagasci_repository,
                            t2krun=self._t2krun,
                            topology=self._topology)
                    gr.xdata, gr.ydata = self._patron.gather_data(detector_name=enabled_detector.name,
                                                                  only_good=self._only_good)


class WagasciPotPlotter(WagasciPlotter):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(WagasciPotPlotter, self).__init__(*args, **kwargs)
        self._wagasci_harvester_class = harvest.WagasciPotHarvester
        self._bsd_harvester_class = harvest.BsdPotHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "#splitline{Accumulated POT for each subdetector during run %s}" \
                      "{after spill matching but before ADC calibration};;POT" % str(self._t2krun)

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = True
        self.xdata_is_datetime = True
        graphs = super(WagasciPotPlotter, self).setup_graphs()
        bsd_graph = graph.Graph("Delivered POT", "BSD")
        bsd_graph.color = colors.Colors.Red.value
        graphs.append(bsd_graph)
        return graphs

    # noinspection PyUnresolvedReferences
    def change_graph_titles(self, graphs):
        # type: (List[pl.graph.Graph]) -> None
        bsd_graph = next((bsd_graph for bsd_graph in graphs if bsd_graph.id == "BSD"), None)
        if bsd_graph is None:
            return
        if bsd_graph.ydata.size == 0:
            bsd_pot = 0
        else:
            bsd_pot = numpy.amax(bsd_graph.ydata)
        bsd_graph.title += " = {:.2e} POT".format(bsd_pot)
        for igraph in [gr for gr in graphs if gr.id != "BSD"]:
            if igraph.ydata.size == 0:
                max_pot = 0
            else:
                max_pot = numpy.amax(igraph.ydata)
            percent = 100 * float(max_pot) / float(bsd_pot) if bsd_pot != 0 else 0
            igraph.title += " {:.1f}%".format(percent)


class WagasciSpillHistoryPlotter(WagasciPlotter):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(WagasciSpillHistoryPlotter, self).__init__(*args, **kwargs)
        self._wagasci_harvester_class = harvest.WagasciSpillHistoryHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "#splitline{WAGASCI spill history during run %s}" \
                      "{before bit flip fixing};;spill number" % str(self._t2krun)

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = False
        self.xdata_is_datetime = True
        self.draw_options_1d = "AP"
        graphs = super(WagasciSpillHistoryPlotter, self).setup_graphs()
        for gr in graphs:
            gr.yrange = graph.Range(lower_bound=spill.WAGASCI_MINIMUM_SPILL, upper_bound=spill.WAGASCI_MAXIMUM_SPILL)
        return graphs


class WagasciFixedSpillPlotter(WagasciPlotter):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(WagasciFixedSpillPlotter, self).__init__(*args, **kwargs)
        self._wagasci_harvester_class = harvest.WagasciFixedSpillHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "#splitline{WAGASCI fixed spill history during run %s}" \
                      "{after bit flip fixing but before ADC calibration};;spill number" % str(self._t2krun)

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = False
        self.xdata_is_datetime = True
        self.draw_options_1d = "AP"
        return super(WagasciFixedSpillPlotter, self).setup_graphs()


class WagasciSpillNumberPlotter(WagasciPlotter):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(WagasciSpillNumberPlotter, self).__init__(*args, **kwargs)
        self._wagasci_harvester_class = harvest.WagasciSpillNumberHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "#splitline{WAGASCI spill number during run %s}" \
                      "{before bit flip fixing and BSD spill matching};event number (increasing in time);spill number" \
                      % str(self._t2krun)

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = False
        self.xdata_is_datetime = False
        self.draw_options_1d = "AP"
        graphs = super(WagasciSpillNumberPlotter, self).setup_graphs()
        for gr in graphs:
            gr.yrange = graph.Range(lower_bound=spill.WAGASCI_MINIMUM_SPILL, upper_bound=spill.WAGASCI_MAXIMUM_SPILL)
        return graphs


class TemperaturePlotter(WagasciPlotter):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(TemperaturePlotter, self).__init__(*args, **kwargs)
        self._wagasci_harvester_class = harvest.TemperatureHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "WAGASCI temperature history during run %s};;Temperature (C°)" % str(self._t2krun)

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = True
        self.xdata_is_datetime = True
        return super(TemperaturePlotter, self).setup_graphs()


class HumidityPlotter(WagasciPlotter):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(HumidityPlotter, self).__init__(*args, **kwargs)
        self._wagasci_harvester_class = harvest.HumidityHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "WAGASCI humidity history during run %s};;Humidity (%%)" % str(self._t2krun)

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = True
        self.xdata_is_datetime = True
        return super(HumidityPlotter, self).setup_graphs()


class AdcCalibrationPlotterDif(Plotter, ABC):

    def __init__(self,
                 start,  # type: Union[str, int]
                 stop=None,  # type: Optional[Union[str, int]]
                 wagasci_database=None,  # type: Optional[str]
                 history_location=None,  # type: Optional[str]
                 topology=None,  # type: Optional[pl.topology.Topology]
                 *args, **kwargs):
        # type: (...) -> None
        super(AdcCalibrationPlotterDif, self).__init__(*args, **kwargs)
        self._start = start
        self._stop = stop
        self._history_location = history_location
        self._topology = topology
        self._data_harvester_class = None
        self._temperature_harvester_class = None
        self._patron = harvest.Patron(start=start, stop=stop, wagasci_database=wagasci_database)

    @abc.abstractmethod
    def set_title(self):
        # type: (...) -> None
        super(AdcCalibrationPlotterDif, self).set_title()

    @abc.abstractmethod
    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        graphs = [graph.Graph2D(title="history", graph_id="data")]
        if self._topology.how_many_enabled() == 1:
            for enabled_detector in self._topology.get_enabled():
                gr = graph.Graph(title=enabled_detector.name, graph_id="temperature")
                gr.color = colors.Colors.Red
                gr.yaxis_color = colors.Colors.Red
                graphs.append(gr)
        return graphs

    def change_yaxis_title(self, multigraph):
        # type: (ROOT.TMultiGraph) -> None
        multigraph.GetYaxis().SetTitle("Temperature (Celsius Degrees)")

    def _set_harvester(self, harvester_class):
        assert harvester_class is not None, "Derived class must set the harvester class attribute"
        if not self._patron.is_harvester_ready() or not isinstance(self._patron.harvester, harvester_class):
            self._patron.harvester = harvester_class(database=self._patron.wagasci_database,
                                                     repository=self._history_location,
                                                     t2krun=None,
                                                     topology=self._topology)

    def gather_data(self, gr):
        # type: (pl.graph.Graph) -> None
        if not self._topology.iterate_by_dif:
            raise RuntimeError("You must iterate through the active detectors by DIF")
        if gr.id == "data":
            self._set_harvester(self._data_harvester_class)
            gr.xdata, gr.ydata = self._patron.gather_data()
        else:
            for enabled_detector in self._topology.get_enabled():
                if gr.id == str(enabled_detector.name):
                    self._set_harvester(self._temperature_harvester_class)
                    gr.xdata, gr.ydata = self._patron.gather_data(detector_name=enabled_detector.name)


class GainHistoryPlotterDif(AdcCalibrationPlotterDif):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(GainHistoryPlotterDif, self).__init__(*args, **kwargs)
        self._data_harvester_class = harvest.GainHarvesterDif
        self._temperature_harvester_class = harvest.AdcCalibrationTemperatureHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "Gain history"
        super(GainHistoryPlotterDif, self).set_title()
        self._title += ";;Gain (ADC counts)"

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = False
        self.xdata_is_datetime = True
        self.draw_options_2d = "COL"
        if self._topology.how_many_enabled() == 1:
            self.draw_options_2d += "Y+"
        else:
            self.draw_options_2d += "Z"
        self.draw_options_1d = "AL"
        return super(GainHistoryPlotterDif, self).setup_graphs()


class DarkNoiseHistoryPlotterDif(AdcCalibrationPlotterDif):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(DarkNoiseHistoryPlotterDif, self).__init__(*args, **kwargs)
        self._data_harvester_class = harvest.DarkNoiseHarvesterDif
        self._temperature_harvester_class = harvest.AdcCalibrationTemperatureHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "Dark noise history"
        super(DarkNoiseHistoryPlotterDif, self).set_title()
        self._title += ";;Dark noise (Hz)"

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = False
        self.xdata_is_datetime = True
        self.draw_options_2d = "COL"

        if self._topology.how_many_enabled() == 1:
            self.draw_options_2d += "Y+"
        else:
            self.draw_options_2d += "Z"
        self.draw_options_1d = "AL"
        self.logscale = True

        return super(DarkNoiseHistoryPlotterDif, self).setup_graphs()


class ThresholdHistoryPlotterDif(AdcCalibrationPlotterDif):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(ThresholdHistoryPlotterDif, self).__init__(*args, **kwargs)
        self._data_harvester_class = harvest.ThresholdHarvesterDif
        self._temperature_harvester_class = harvest.AdcCalibrationTemperatureHarvester
        self._yrange = (1, 6)

    def set_title(self):
        # type: (...) -> None
        self._title = "Hit threshold level history"
        super(ThresholdHistoryPlotterDif, self).set_title()
        self._title += ";;Hit threshold (PEU)"

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = False
        self.xdata_is_datetime = True
        self.draw_options_2d = "COL"

        if self._topology.how_many_enabled() == 1:
            self.draw_options_2d += "Y+"
        else:
            self.draw_options_2d += "Z"
        self.draw_options_1d = "AL"
        self.logscale = False

        return super(ThresholdHistoryPlotterDif, self).setup_graphs()


class AdcCalibrationPlotterChannel(Plotter, ABC):

    def __init__(self,
                 start,  # type: Union[str, int]
                 stop=None,  # type: Optional[Union[str, int]]
                 wagasci_database=None,  # type: Optional[str]
                 history_location=None,  # type: Optional[str]
                 dif=0,  # type: int
                 chip=0,  # type: int
                 channel=0,  # type: int
                 *args, **kwargs):
        super(AdcCalibrationPlotterChannel, self).__init__(*args, **kwargs)
        self._data_harvester_class = None
        self._temperature_harvester_class = None
        self._start = start
        self._stop = stop
        self._history_location = history_location
        self._dif = dif
        self._chip = chip
        self._channel = channel
        self._topology = topol.Topology(iterate_by_dif=True)
        self._topology.disable_all_but(topol.DifIndex.get_name(index=dif))
        self._patron = harvest.Patron(start=start, stop=stop, wagasci_database=wagasci_database)

    @abc.abstractmethod
    def set_title(self):
        # type: (...) -> None
        pass

    def _make_data_graph_title(self):
        # type: (...) -> str
        return "{} : CHIP {} CHANNEL {}".format(pl.topology.DifIndex.get_name(self._dif), self._chip, self._channel)

    @abc.abstractmethod
    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        graphs = [graph.Graph(title=self._make_data_graph_title(), graph_id="data")]
        gr = graph.Graph(title=pl.topology.DifIndex.get_name(self._dif), graph_id="temperature")
        gr.color = colors.Colors.Red
        gr.yaxis_color = colors.Colors.Red
        graphs.append(gr)
        return graphs

    # def change_yaxis_title(self, multigraph):
    #     # type: (ROOT.TMultiGraph) -> None
    #     multigraph.GetYaxis().SetTitle("Temperature (Celsius Degrees)")

    def _set_data_harvester(self, harvester_class):
        assert harvester_class is not None, "Derived class must set the harvester class attribute"
        if not self._patron.is_harvester_ready() or not isinstance(self._patron.harvester, harvester_class):
            self._patron.harvester = harvester_class(database=self._patron.wagasci_database,
                                                     repository=self._history_location,
                                                     t2krun=None,
                                                     topology=self._topology,
                                                     chip=self._chip,
                                                     channel=self._channel)

    def _set_temp_harvester(self, harvester_class):
        assert harvester_class is not None, "Derived class must set the harvester class attribute"
        if not self._patron.is_harvester_ready() or not isinstance(self._patron.harvester, harvester_class):
            self._patron.harvester = harvester_class(database=self._patron.wagasci_database,
                                                     repository=self._history_location,
                                                     t2krun=None)

    def gather_data(self, gr):
        # type: (pl.graph.Graph) -> None
        if gr.id == "data":
            self._set_data_harvester(self._data_harvester_class)
            gr.xdata, gr.ydata = self._patron.gather_data()
        else:
            self._set_temp_harvester(self._temperature_harvester_class)
            gr.xdata, gr.ydata = self._patron.gather_data(detector_name=self._topology.get_enabled()[0].name)


class GainHistoryPlotterChannel(AdcCalibrationPlotterChannel):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(GainHistoryPlotterChannel, self).__init__(*args, **kwargs)
        self._data_harvester_class = harvest.GainHarvesterChannel
        self._temperature_harvester_class = harvest.AdcCalibrationTemperatureHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "Gain history of {};;Gain (ADC counts)".format(self._make_data_graph_title())

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = False
        self.xdata_is_datetime = True
        self.draw_options_1d = "ALP"
        return super(GainHistoryPlotterChannel, self).setup_graphs()


class DarkNoiseHistoryPlotterChannel(AdcCalibrationPlotterChannel):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(DarkNoiseHistoryPlotterChannel, self).__init__(*args, **kwargs)
        self._data_harvester_class = harvest.DarkNoiseHarvesterChannel
        self._temperature_harvester_class = harvest.AdcCalibrationTemperatureHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "Dark noise rate history of {};;Dark noise rate (Hz)".format(self._make_data_graph_title())

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = False
        self.xdata_is_datetime = True
        self.draw_options_1d = "ALP"
        return super(DarkNoiseHistoryPlotterChannel, self).setup_graphs()


class ThresholdHistoryPlotterChannel(AdcCalibrationPlotterChannel):

    def __init__(self, *args, **kwargs):
        # type: (...) -> None
        super(ThresholdHistoryPlotterChannel, self).__init__(*args, **kwargs)
        self._data_harvester_class = harvest.ThresholdHarvesterChannel
        self._temperature_harvester_class = harvest.AdcCalibrationTemperatureHarvester
        self._yrange = (0, 6)

    def set_title(self):
        # type: (...) -> None
        self._title = "Hit threshold level history of {};;Hit threshold (PEU)".format(self._make_data_graph_title())

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph]
        self.plot_legend_flag = False
        self.xdata_is_datetime = True
        self.draw_options_1d = "ALP"
        return super(ThresholdHistoryPlotterChannel, self).setup_graphs()


class BcidPlotter(WagasciPlotter, ABC):

    def __init__(self, topology=None, *args, **kwargs):
        # type: (Optional[pl.topology.Topology], *Any, **Any) -> None
        super(BcidPlotter, self).__init__(*args, **kwargs)
        self._topology = topology if topology is not None else pl.topology.Topology(iterate_by_dif=True)
        self._wagasci_harvester_class = harvest.BcidHarvester

    def set_title(self):
        # type: (...) -> None
        self._title = "BCID history"
        super(BcidPlotter, self).set_title()
        self._title += ";;BCID counts (1 BCID count = 580 ns)"

    def setup_graphs(self):
        # type: (...) -> List[pl.graph.Graph2D]
        graphs = [graph.Graph2D("BCID")]
        graphs[0].raw_ydata = False
        self.plot_legend_flag = False
        self.xdata_is_datetime = True
        self.draw_options_2d = "COL"
        self.draw_options_2d += "Z"
        self.logscale = False
        return graphs

    def gather_data(self, gr):
        # type: (pl.graph.Graph) -> None
        if not self._topology.iterate_by_dif:
            raise RuntimeError("You must iterate through the active detectors by DIF")
        assert self._wagasci_harvester_class is not None, \
            "Derived class must set the _data_harvester_class attribute"
        enabled_detector = self._topology.get_enabled()[0]
        self._patron.harvester = self._wagasci_harvester_class(database=self._patron.wagasci_database,
                                                               repository=self._wagasci_repository,
                                                               t2krun=self._t2krun,
                                                               topology=self._topology)
        gr.xdata, gr.ydata = self._patron.gather_data(detector_name=enabled_detector.name, only_good=self._only_good)
