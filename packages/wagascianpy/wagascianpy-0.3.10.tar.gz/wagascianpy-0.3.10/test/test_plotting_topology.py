import unittest

import wagascianpy.plotting.topology


class TestTopologyIterateByDetector(unittest.TestCase):

    def setUp(self):
        self.topology = wagascianpy.plotting.topology.Topology(iterate_by_dif=False)

    def test_are_all_enabled(self):
        self.assertTrue(self.topology.are_all_enabled())
        self.topology.wagasci_downstream.disable()
        self.assertFalse(self.topology.are_all_enabled())

    def test_disable_all(self):
        self.assertTrue(self.topology.are_all_enabled())
        self.topology.disable_all()
        self.assertFalse(self.topology.are_all_enabled())
        self.topology.wallmrd_north.enable()
        self.assertTrue(self.topology.wallmrd_north.is_enabled())
        self.assertFalse(self.topology.wallmrd_south.is_enabled())
        self.assertFalse(self.topology.wagasci_upstream.is_enabled())
        self.assertFalse(self.topology.wagasci_downstream.is_enabled())

    def test_disable_all_but_one(self):
        self.assertTrue(self.topology.are_all_enabled())
        self.topology.disable_all_but("WAGASCI downstream")
        self.assertFalse(self.topology.are_all_enabled())
        self.assertTrue(self.topology.wagasci_downstream.is_enabled())
        self.assertFalse(self.topology.wagasci_upstream.is_enabled())
        self.assertFalse(self.topology.wallmrd_south.is_enabled())
        self.assertFalse(self.topology.wallmrd_north.is_enabled())

    def test_get_all(self):
        self.assertEqual(4, len(self.topology.get_all()))
        self.assertIn(self.topology.wagasci_upstream, self.topology.get_all())
        self.assertIn(self.topology.wagasci_downstream, self.topology.get_all())
        self.assertIn(self.topology.wallmrd_north, self.topology.get_all())
        self.assertIn(self.topology.wallmrd_south, self.topology.get_all())

    def test_get_disabled(self):
        self.topology.wagasci_downstream.disable()
        self.assertEqual(1, len(self.topology.get_disabled()))
        self.assertIn(self.topology.wagasci_downstream, self.topology.get_disabled())

    def test_get_enabled(self):
        self.topology.wagasci_downstream.disable()
        self.assertEqual(3, len(self.topology.get_enabled()))
        self.assertIn(self.topology.wagasci_upstream, self.topology.get_enabled())
        self.assertIn(self.topology.wallmrd_north, self.topology.get_enabled())
        self.assertIn(self.topology.wallmrd_south, self.topology.get_enabled())

    def test_import_topology(self):
        topology = wagascianpy.plotting.topology.Topology(iterate_by_dif=True)
        topology.wagasci_downstream_top.disable()
        topology.wagasci_downstream_side.disable()
        self.topology.import_topology(topology)
        self.assertFalse(self.topology.wagasci_downstream.is_enabled())


class TestTopologyIterateByDif(unittest.TestCase):

    def setUp(self):
        self.topology = wagascianpy.plotting.topology.Topology(iterate_by_dif=True)

    def test_are_all_enabled(self):
        self.assertTrue(self.topology.are_all_enabled())
        self.topology.wagasci_downstream_side.disable()
        self.assertFalse(self.topology.are_all_enabled())

    def test_disable_all(self):
        self.assertTrue(self.topology.are_all_enabled())
        self.topology.disable_all()
        self.assertFalse(self.topology.are_all_enabled())

    def test_disable_all_but_one(self):
        self.assertTrue(self.topology.are_all_enabled())
        self.topology.disable_all_but("WAGASCI downstream side")
        self.assertFalse(self.topology.are_all_enabled())
        self.assertFalse(self.topology.wagasci_downstream_top.is_enabled())
        self.assertTrue(self.topology.wagasci_downstream_side.is_enabled())

    def test_get_all(self):
        self.assertEqual(8, len(self.topology.get_all()))
        self.assertIn(self.topology.wagasci_upstream_top, self.topology.get_all())
        self.assertIn(self.topology.wagasci_downstream_top, self.topology.get_all())
        self.assertIn(self.topology.wallmrd_north_top, self.topology.get_all())
        self.assertIn(self.topology.wallmrd_south_top, self.topology.get_all())
        self.assertIn(self.topology.wagasci_upstream_side, self.topology.get_all())
        self.assertIn(self.topology.wagasci_downstream_side, self.topology.get_all())
        self.assertIn(self.topology.wallmrd_north_bottom, self.topology.get_all())
        self.assertIn(self.topology.wallmrd_south_bottom, self.topology.get_all())

    def test_get_disabled(self):
        self.topology.wagasci_downstream_side.disable()
        self.assertEqual(1, len(self.topology.get_disabled()))
        self.assertFalse(self.topology.wagasci_downstream_side.is_enabled())
        self.assertTrue(self.topology.wagasci_downstream_top.is_enabled())
        self.assertTrue(self.topology.wagasci_upstream_top.is_enabled())
        self.assertTrue(self.topology.wagasci_upstream_side.is_enabled())
        self.assertTrue(self.topology.wallmrd_north_top.is_enabled())
        self.assertTrue(self.topology.wallmrd_north_bottom.is_enabled())
        self.assertTrue(self.topology.wallmrd_south_top.is_enabled())
        self.assertTrue(self.topology.wallmrd_south_bottom.is_enabled())
        self.assertIn(self.topology.wagasci_downstream_side, self.topology.get_disabled())

    def test_get_enabled(self):
        self.topology.wagasci_downstream_side.disable()
        self.assertEqual(7, len(self.topology.get_enabled()))
        self.assertIn(self.topology.wagasci_upstream_top, self.topology.get_enabled())
        self.assertIn(self.topology.wagasci_downstream_top, self.topology.get_enabled())
        self.assertIn(self.topology.wallmrd_north_top, self.topology.get_enabled())
        self.assertIn(self.topology.wallmrd_south_top, self.topology.get_enabled())
        self.assertIn(self.topology.wagasci_upstream_side, self.topology.get_enabled())
        self.assertNotIn(self.topology.wagasci_downstream_side, self.topology.get_enabled())
        self.assertIn(self.topology.wallmrd_north_bottom, self.topology.get_enabled())
        self.assertIn(self.topology.wallmrd_south_bottom, self.topology.get_enabled())

    def test_import_topology(self):
        topology = wagascianpy.plotting.topology.Topology(iterate_by_dif=False)
        topology.wagasci_downstream.disable()
        self.topology.import_topology(topology)
        self.assertFalse(self.topology.wagasci_downstream_top.is_enabled())
        self.assertFalse(self.topology.wagasci_downstream_side.is_enabled())


class TestDifIndex(unittest.TestCase):

    def test_dif_index_true(self):
        self.assertTrue(wagascianpy.plotting.topology.DifIndex.is_wallmrd_north(0))
        self.assertTrue(wagascianpy.plotting.topology.DifIndex.is_wallmrd_south(3))
        self.assertTrue(wagascianpy.plotting.topology.DifIndex.is_wallmrd(2))
        self.assertTrue(wagascianpy.plotting.topology.DifIndex.is_wagasci_upstream(5))
        self.assertTrue(wagascianpy.plotting.topology.DifIndex.is_wagasci_downstream(6))
        self.assertTrue(wagascianpy.plotting.topology.DifIndex.is_wagasci(4))

    def test_dif_index_false(self):
        self.assertFalse(wagascianpy.plotting.topology.DifIndex.is_wallmrd_north(6))
        self.assertFalse(wagascianpy.plotting.topology.DifIndex.is_wallmrd_south(4))
        self.assertFalse(wagascianpy.plotting.topology.DifIndex.is_wallmrd(10))
        self.assertFalse(wagascianpy.plotting.topology.DifIndex.is_wagasci_upstream(2))
        self.assertFalse(wagascianpy.plotting.topology.DifIndex.is_wagasci_downstream(3))
        self.assertFalse(wagascianpy.plotting.topology.DifIndex.is_wagasci(1))


if __name__ == '__main__':
    unittest.main()
