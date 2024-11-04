import unittest
import numpy
import ROOT

import wagascianpy.plotting.colors
import wagascianpy.plotting.graph


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.xdata_list = [0, 1, 2]
        self.ydata_list = [10, 20, 30]
        self.xdata_array = numpy.array(self.xdata_list, dtype=numpy.float64)
        self.ydata_array = numpy.array(self.ydata_list, dtype=numpy.float64)
        self.xrange = wagascianpy.plotting.graph.Range(lower_bound=0, upper_bound=2)
        self.yrange = wagascianpy.plotting.graph.Range(lower_bound=10, upper_bound=30)
        self.title = "test title"
        self.graph_id = "test_id"
        self.color = wagascianpy.plotting.colors.Colors.Azure.value

    def test_constructor(self):
        graph = wagascianpy.plotting.graph.Graph(title=self.title, graph_id=self.graph_id)
        self.assertEqual(graph.title, self.title)
        self.assertEqual(graph.id, self.graph_id)
        graph = wagascianpy.plotting.graph.Graph(title=self.title)
        self.assertEqual(graph.id, self.title)
        self.assertRaises(TypeError, wagascianpy.plotting.graph.Graph)
        self.assertIsNone(graph.xdata)
        self.assertIsNone(graph.ydata)
        self.assertEqual(wagascianpy.plotting.graph.Range(None, None), graph.xrange)
        self.assertEqual(wagascianpy.plotting.graph.Range(None, None), graph.yrange)
        self.assertEqual(wagascianpy.plotting.colors.Colors.Black.value, graph.color)
        self.assertTrue(graph.is_empty())

    def test_getter_setter(self):
        graph = wagascianpy.plotting.graph.Graph(title=self.title, graph_id=self.graph_id)
        graph.xdata = self.xdata_array
        graph.ydata = self.ydata_array
        graph.color = self.color
        graph.xrange = self.xrange
        graph.yrange = self.yrange
        self.assertListEqual(self.xdata_list, list(graph.xdata))
        self.assertListEqual(self.ydata_list, list(graph.ydata))
        graph.xdata = self.xdata_list
        graph.ydata = self.ydata_list
        self.assertListEqual(self.xdata_list, list(graph.xdata))
        self.assertListEqual(self.ydata_list, list(graph.ydata))
        self.assertEqual(self.color, graph.color)
        self.assertEqual(self.xrange, graph.xrange)
        self.assertEqual(self.yrange, graph.yrange)
        self.assertFalse(graph.is_empty())

    def test_make_tgraph(self):
        graph = wagascianpy.plotting.graph.Graph(title=self.title, graph_id=self.graph_id)
        graph.xdata = self.xdata_array
        graph.ydata = self.ydata_array
        graph.color = self.color
        graph.xrange = self.xrange
        graph.yrange = self.yrange
        tgraph = graph.make_tgraph()
        self.assertIsInstance(tgraph, ROOT.TGraph)
        self.assertEqual(len(self.xdata_array), tgraph.GetN())
        for i in range(len(self.xdata_array)):
            x = numpy.array([0], dtype=numpy.float64)
            y = numpy.array([0], dtype=numpy.float64)
            tgraph.GetPoint(i, x, y)
            self.assertEqual(self.xdata_array[i], x[0])
            self.assertEqual(self.ydata_array[i], y[0])


class TestGraph2D(unittest.TestCase):

    def setUp(self):
        self.xdata = [0, 1, 2]
        self.ydata = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
        self.title = "test title"
        self.graph_id = "test_id"
        self.graph = wagascianpy.plotting.graph.Graph2D(title=self.title, graph_id=self.graph_id)
        self.graph.xdata = self.xdata
        self.graph.ydata = self.ydata

    def test_make_tgraph(self):
        th2d = self.graph.make_tgraph()
        self.assertIsInstance(th2d, ROOT.TH2D)
        self.assertEqual(len(self.xdata), th2d.GetNbinsX())


if __name__ == '__main__':
    unittest.main()
