import unittest
import numpy.testing

from wagascianpy.analysis.spill import *


class TestWagasciSpillCreation(unittest.TestCase):
    def test_wagasci_spill_constructor(self):
        WagasciSpill()

    def test_wagasci_spill_setters(self):
        spill = WagasciSpill()
        spill.converted_spill_number = 1
        spill.good_spill_flag = True
        spill.spill_mode = WAGASCI_SPILL_BEAM_MODE
        spill.spill_count = 1
        spill.spill_number = 1
        spill.temperature = 1.
        spill.humidity = 1.
        spill.wagasci_run = 1

        self.assertEqual(spill.converted_spill_number, 1)
        self.assertEqual(spill.good_spill_flag, True)
        self.assertEqual(spill.spill_mode, WAGASCI_SPILL_BEAM_MODE)
        self.assertEqual(spill.spill_count, 1)
        self.assertEqual(spill.spill_number, 1)
        self.assertAlmostEqual(spill.temperature, 1, delta=0.0001)
        self.assertAlmostEqual(spill.humidity, 1, delta=0.0001)
        self.assertEqual(spill.wagasci_run, 1)

        self.assertIsInstance(spill.converted_spill_number, int)
        self.assertIsInstance(spill.good_spill_flag, bool)
        self.assertIsInstance(spill.spill_mode, int)
        self.assertIsInstance(spill.spill_count, int)
        self.assertIsInstance(spill.spill_number, int)
        self.assertIsInstance(spill.temperature, float)
        self.assertIsInstance(spill.humidity, float)
        self.assertIsInstance(spill.wagasci_run, int)


class TestWagasciSpillMethods(unittest.TestCase):
    def setUp(self):
        self.spill = WagasciSpill()
        self.spill.converted_spill_number = 1
        self.spill.good_spill_flag = True
        self.spill.spill_mode = WAGASCI_SPILL_BEAM_MODE
        self.spill.spill_count = 1
        self.spill.spill_number = 1
        self.spill.temperature = 1.
        self.spill.humidity = 1.
        self.spill.wagasci_run = 1

    def test_are_all_defined(self):
        self.assertTrue(self.spill.are_all_defined())

    def test_get_type_char(self):
        self.assertEqual(self.spill._get_type_char("converted_spill_number"), 'i')
        self.assertEqual(self.spill._get_type_char("good_spill_flag"), 'o')
        self.assertEqual(self.spill._get_type_char("spill_mode"), 'i')
        self.assertEqual(self.spill._get_type_char("spill_count"), 'i')
        self.assertEqual(self.spill._get_type_char("spill_number"), 'i')
        self.assertEqual(self.spill._get_type_char("temperature"), 'd')
        self.assertEqual(self.spill._get_type_char("humidity"), 'd')
        self.assertEqual(self.spill._get_type_char("wagasci_run"), 'i')

    def test_get_numpy_type(self):
        self.assertEqual(self.spill._get_numpy_type("converted_spill_number"), numpy.int32)
        self.assertEqual(self.spill._get_numpy_type("good_spill_flag"), numpy.bool)
        self.assertEqual(self.spill._get_numpy_type("spill_mode"), numpy.int32)
        self.assertEqual(self.spill._get_numpy_type("spill_count"), numpy.int32)
        self.assertEqual(self.spill._get_numpy_type("spill_number"), numpy.int32)
        self.assertEqual(self.spill._get_numpy_type("temperature"), numpy.float64)
        self.assertEqual(self.spill._get_numpy_type("humidity"), numpy.float64)
        self.assertEqual(self.spill._get_numpy_type("wagasci_run"), numpy.int32)

    def test_get_type_str(self):
        self.assertEqual(self.spill._get_type_str("converted_spill_number"), 'converted_spill_number/I')
        self.assertEqual(self.spill._get_type_str("good_spill_flag"), 'good_spill_flag/O')
        self.assertEqual(self.spill._get_type_str("spill_mode"), 'spill_mode/I')
        self.assertEqual(self.spill._get_type_str("spill_count"), 'spill_count/I')
        self.assertEqual(self.spill._get_type_str("spill_number"), 'spill_number/I')
        self.assertEqual(self.spill._get_type_str("temperature"), 'temperature/D')
        self.assertEqual(self.spill._get_type_str("humidity"), 'humidity/D')
        self.assertEqual(self.spill._get_type_str("wagasci_run"), 'wagasci_run/I')

    def test_get_array(self):
        self.assertEqual(self.spill._get_array("converted_spill_number"), numpy.array([1], dtype=numpy.int32))
        self.assertEqual(self.spill._get_array("good_spill_flag"), numpy.array([True], dtype=numpy.bool))
        self.assertEqual(self.spill._get_array("spill_mode"), numpy.array([WAGASCI_SPILL_BEAM_MODE], dtype=numpy.int32))
        self.assertEqual(self.spill._get_array("spill_count"), numpy.array([1], dtype=numpy.int32))
        self.assertEqual(self.spill._get_array("spill_number"), numpy.array([1], dtype=numpy.int32))
        self.assertEqual(self.spill._get_array("temperature"), numpy.array([1.], dtype=numpy.float64))
        self.assertEqual(self.spill._get_array("humidity"), numpy.array([1.], dtype=numpy.float64))
        self.assertEqual(self.spill._get_array("wagasci_run"), numpy.array([1], dtype=numpy.int32))

    def test_get_array_list(self):
        expected_array_list = [
            SpillArrayInfo(
                name='spill_count',
                array=numpy.array([1], dtype=numpy.int32),
                type_char='i',
                type_str='spill_count/I'),
            SpillArrayInfo(
                name='spill_number',
                array=numpy.array([1], dtype=numpy.int32),
                type_char='i',
                type_str='spill_number/I'),
            SpillArrayInfo(
                name='converted_spill_number',
                array=numpy.array([1], dtype=numpy.int32),
                type_char='i',
                type_str='converted_spill_number/I'),
            SpillArrayInfo(
                name='spill_mode',
                array=numpy.array([WAGASCI_SPILL_BEAM_MODE], dtype=numpy.int32),
                type_char='i',
                type_str='spill_mode/I'),
            SpillArrayInfo(
                name='good_spill_flag',
                array=numpy.array([True], dtype=numpy.bool),
                type_char='o',
                type_str='good_spill_flag/O'),
            SpillArrayInfo(
                name='temperature',
                array=numpy.array([1.], dtype=numpy.float64),
                type_char='d',
                type_str='temperature/D'),
            SpillArrayInfo(
                name='humidity',
                array=numpy.array([1.], dtype=numpy.float64),
                type_char='d',
                type_str='humidity/D'),
            SpillArrayInfo(
                name='wagasci_run',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='i',
                type_str='wagasci_run/I'),
        ]
        self.assertEqual(sorted(expected_array_list), sorted(self.spill.get_array_list()))

    def test_set_array_list(self):
        expected_array_list = [
            SpillArrayInfo(
                name='spill_count',
                array=numpy.array([2], dtype=numpy.int32),
                type_char='i',
                type_str='spill_count/I'),
            SpillArrayInfo(
                name='spill_number',
                array=numpy.array([2], dtype=numpy.int32),
                type_char='i',
                type_str='spill_number/I'),
            SpillArrayInfo(
                name='converted_spill_number',
                array=numpy.array([2], dtype=numpy.int32),
                type_char='i',
                type_str='converted_spill_number/I'),
            SpillArrayInfo(
                name='spill_mode',
                array=numpy.array([WAGASCI_SPILL_NO_BEAM_MODE], dtype=numpy.int32),
                type_char='i',
                type_str='spill_mode/I'),
            SpillArrayInfo(
                name='good_spill_flag',
                array=numpy.array([False], dtype=numpy.bool),
                type_char='o',
                type_str='good_spill_flag/O'),
            SpillArrayInfo(
                name='temperature',
                array=numpy.array([2], dtype=numpy.float64),
                type_char='d',
                type_str='temperature/D'),
            SpillArrayInfo(
                name='humidity',
                array=numpy.array([2], dtype=numpy.float64),
                type_char='d',
                type_str='humidity/D'),
            SpillArrayInfo(
                name='wagasci_run',
                array=numpy.array([2], dtype=numpy.float64),
                type_char='i',
                type_str='wagasci_run/I'),
        ]
        self.spill.set_array_list(expected_array_list)
        self.assertEqual(sorted(expected_array_list), sorted(self.spill.get_array_list()))


class TestBsdSpillCreation(unittest.TestCase):
    def test_bsd_spill_constructor(self):
        BsdSpill()

    def test_bsd_spill_setters(self):
        spill = BsdSpill()
        spill.converted_spill_number = 1
        spill.bsd_good_spill_flag = 1
        spill.timestamp = 1
        spill.pot = 1
        spill.bsd_spill_number = 1
        spill.bunch_pot = list(range(0, 8))

        self.assertEqual(spill.converted_spill_number, 1)
        self.assertEqual(spill.bsd_good_spill_flag, 1)
        self.assertEqual(spill.pot, 1)
        self.assertEqual(spill.timestamp, 1)
        self.assertEqual(spill.bsd_spill_number, 1)
        self.assertIsNone(numpy.testing.assert_almost_equal(spill.bunch_pot,
                                                            numpy.array(list(range(0, 8)), dtype=numpy.float64)))

        self.assertIsInstance(spill.converted_spill_number, int)
        self.assertIsInstance(spill.bsd_good_spill_flag, int)
        self.assertIsInstance(spill.pot, float)
        self.assertIsInstance(spill.timestamp, float)
        self.assertIsInstance(spill.bsd_spill_number, int)
        self.assertIsInstance(spill.bunch_pot, numpy.ndarray)


class TestBsdSpillMethods(unittest.TestCase):
    def setUp(self):
        self.spill = BsdSpill()
        self.spill.converted_spill_number = 1
        self.spill.bsd_good_spill_flag = 1
        self.spill.timestamp = 1
        self.spill.pot = 1
        self.spill.bsd_spill_number = 1
        self.spill.t2k_run = 1
        self.spill.main_ring_run = 1
        self.spill.neutrino_daq_run = 1
        self.spill.horn_current = 1
        self.spill.neutrino_mode = 1
        self.spill.bunch_pot = list(range(0, 8))

    def test_are_all_defined(self):
        self.assertTrue(self.spill.are_all_defined())

    def test_get_type_char(self):
        self.assertEqual(self.spill._get_type_char("converted_spill_number"), 'i')
        self.assertEqual(self.spill._get_type_char("bsd_good_spill_flag"), 'i')
        self.assertEqual(self.spill._get_type_char("pot"), 'd')
        self.assertEqual(self.spill._get_type_char("timestamp"), 'd')
        self.assertEqual(self.spill._get_type_char("bsd_spill_number"), 'i')
        self.assertEqual(self.spill._get_type_char("bunch_pot"), 'd')

    def test_get_numpy_type(self):
        self.assertEqual(self.spill._get_numpy_type("converted_spill_number"), numpy.int32)
        self.assertEqual(self.spill._get_numpy_type("bsd_good_spill_flag"), numpy.int32)
        self.assertEqual(self.spill._get_numpy_type("pot"), numpy.float64)
        self.assertEqual(self.spill._get_numpy_type("timestamp"), numpy.float64)
        self.assertEqual(self.spill._get_numpy_type("bsd_spill_number"), numpy.int32)
        self.assertEqual(self.spill._get_numpy_type("bunch_pot"), numpy.float64)

    def test_get_type_str(self):
        self.assertEqual(self.spill._get_type_str("converted_spill_number"), 'converted_spill_number/I')
        self.assertEqual(self.spill._get_type_str("bsd_good_spill_flag"), 'bsd_good_spill_flag/I')
        self.assertEqual(self.spill._get_type_str("pot"), 'pot/D')
        self.assertEqual(self.spill._get_type_str("timestamp"), 'timestamp/D')
        self.assertEqual(self.spill._get_type_str("bsd_spill_number"), 'bsd_spill_number/I')
        self.assertEqual(self.spill._get_type_str("bunch_pot"), 'bunch_pot[8]/D')

    def test_get_array(self):
        self.assertEqual(self.spill._get_array("converted_spill_number"), numpy.array([1], dtype=numpy.int32))
        self.assertEqual(self.spill._get_array("bsd_good_spill_flag"), numpy.array([1], dtype=numpy.int32))
        self.assertEqual(self.spill._get_array("pot"), numpy.array([1], dtype=numpy.float64))
        self.assertEqual(self.spill._get_array("timestamp"), numpy.array([1], dtype=numpy.float64))
        self.assertEqual(self.spill._get_array("bsd_spill_number"), numpy.array([1], dtype=numpy.int32))
        self.assertIsNone(numpy.testing.assert_almost_equal(self.spill._get_array("bunch_pot"),
                                                            numpy.array(list(range(0, 8)), dtype=numpy.float64)))

    def test_get_array_list(self):
        expected_array_list = [
            SpillArrayInfo(
                name='bsd_spill_number',
                array=numpy.array([1], dtype=numpy.int32),
                type_char='i',
                type_str='bsd_spill_number/I'),
            SpillArrayInfo(
                name='converted_spill_number',
                array=numpy.array([1], dtype=numpy.int32),
                type_char='i',
                type_str='converted_spill_number/I'),
            SpillArrayInfo(
                name='pot',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='d',
                type_str='pot/D'),
            SpillArrayInfo(
                name='timestamp',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='d',
                type_str='timestamp/D'),
            SpillArrayInfo(
                name='bsd_good_spill_flag',
                array=numpy.array([1], dtype=numpy.int32),
                type_char='i',
                type_str='bsd_good_spill_flag/I'),
            SpillArrayInfo(
                name='t2k_run',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='i',
                type_str='t2k_run/I'),
            SpillArrayInfo(
                name='main_ring_run',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='i',
                type_str='main_ring_run/I'),
            SpillArrayInfo(
                name='neutrino_daq_run',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='i',
                type_str='neutrino_daq_run/I'),
            SpillArrayInfo(
                name='horn_current',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='d',
                type_str='horn_current/D'),
            SpillArrayInfo(
                name='neutrino_mode',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='i',
                type_str='neutrino_mode/I'),
            SpillArrayInfo(
                name='bunch_pot',
                array=numpy.array(list(range(0, 8)), dtype=numpy.float64),
                type_char='d',
                type_str='bunch_pot[8]/D')
        ]
        sorted_array_list = [v for v in sorted(expected_array_list) if v.array.size == 1]
        for i, v in enumerate([v for v in sorted(self.spill.get_array_list()) if v.array.size == 1]):
            self.assertEqual(v, sorted_array_list[i])
        sorted_array_list = [v for v in sorted(expected_array_list) if v.array.size > 1]
        for i, v in enumerate([v for v in sorted(self.spill.get_array_list()) if v.array.size > 1]):
            self.assertIsNone(numpy.testing.assert_almost_equal(v.array, sorted_array_list[i].array))

    def test_set_array_list(self):
        expected_array_list = [
            SpillArrayInfo(
                name='bsd_spill_number',
                array=numpy.array([2], dtype=numpy.int32),
                type_char='i',
                type_str='bsd_spill_number/I'),
            SpillArrayInfo(
                name='converted_spill_number',
                array=numpy.array([2], dtype=numpy.int32),
                type_char='i',
                type_str='converted_spill_number/I'),
            SpillArrayInfo(
                name='pot',
                array=numpy.array([2], dtype=numpy.float64),
                type_char='d',
                type_str='pot/D'),
            SpillArrayInfo(
                name='timestamp',
                array=numpy.array([2], dtype=numpy.float64),
                type_char='d',
                type_str='timestamp/D'),
            SpillArrayInfo(
                name='bsd_good_spill_flag',
                array=numpy.array([2], dtype=numpy.int32),
                type_char='i',
                type_str='bsd_good_spill_flag/I'),
            SpillArrayInfo(
                name='t2k_run',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='i',
                type_str='t2k_run/I'),
            SpillArrayInfo(
                name='main_ring_run',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='i',
                type_str='main_ring_run/I'),
            SpillArrayInfo(
                name='neutrino_daq_run',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='i',
                type_str='neutrino_daq_run/I'),
            SpillArrayInfo(
                name='horn_current',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='d',
                type_str='horn_current/D'),
            SpillArrayInfo(
                name='neutrino_mode',
                array=numpy.array([1], dtype=numpy.float64),
                type_char='i',
                type_str='neutrino_mode/I'),
            SpillArrayInfo(
                name='bunch_pot',
                array=numpy.ones(8, dtype=numpy.float64),
                type_char='d',
                type_str='bunch_pot[8]/D')
        ]
        self.spill.set_array_list(expected_array_list)
        sorted_array_list = [v for v in sorted(expected_array_list) if v.array.size == 1]
        for i, v in enumerate([v for v in sorted(self.spill.get_array_list()) if v.array.size == 1]):
            self.assertEqual(v, sorted_array_list[i])
        sorted_array_list = [v for v in sorted(expected_array_list) if v.array.size > 1]
        for i, v in enumerate([v for v in sorted(self.spill.get_array_list()) if v.array.size > 1]):
            self.assertIsNone(numpy.testing.assert_almost_equal(v.array, sorted_array_list[i].array))


if __name__ == '__main__':
    unittest.main()
