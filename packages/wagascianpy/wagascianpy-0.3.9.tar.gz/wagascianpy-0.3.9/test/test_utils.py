import os
import time
import unittest
from random import randint

import pyfakefs.fake_filesystem_unittest
from recordclass import recordclass

import wagascianpy.analysis.analysis
import wagascianpy.utils.acq_config_xml
import wagascianpy.utils.utils


# noinspection PyPep8Naming
class TestFileSystemUtils(pyfakefs.fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.topology = {"1": {"0": 32}, "3": {"0": 32}, "5": {"0": 32}, "7": {"0": 32}}
        self.setUpPyfakefs()

    def test_renametree_1(self):
        self.fs.create_file('/test_renametree/test_ecal_dif_0.raw')
        self.fs.create_file('/test_renametree/test_ecal_dif_1.raw')
        self.fs.create_file('/test_renametree/test_ecal_dif_2.raw')
        self.fs.create_file('/test_renametree/test_ecal_dif_3.raw')

        wagascianpy.utils.utils.renametree(run_root_dir='/test_renametree', run_name='test', dif_topology=self.topology)
        self.check_paths()

    def test_renametree_2(self):
        self.fs.create_file('/test_renametree/test_ecal_dif_0.raw')
        self.fs.create_file('/test_renametree/test_ecal_dif_3.raw')
        self.fs.create_file('/test_renametree/test_ecal_dif_5.raw')
        self.fs.create_file('/test_renametree/test_ecal_dif_7.raw')

        wagascianpy.utils.utils.renametree(run_root_dir='/test_renametree', run_name='test', dif_topology=self.topology)
        self.check_paths()

    def test_renametree_3(self):
        self.fs.create_file('/test_renametree/test_ecal_dif_0.raw')
        self.fs.create_file('/test_renametree/test_ecal_dif_4.raw')
        self.fs.create_file('/test_renametree/test_ecal_dif_6.raw')
        self.fs.create_file('/test_renametree/test_ecal_dif_7.raw')

        wagascianpy.utils.utils.renametree(run_root_dir='/test_renametree', run_name='test', dif_topology=self.topology)
        self.check_paths()

    def test_renametree_4(self):
        self.fs.create_file('/test_renametree/test_ecal_dif_0.raw')
        self.fs.create_file('/test_renametree/test_ecal_dif_4.raw')
        self.fs.create_file('/test_renametree/test_ecal_dif_7.raw')

        self.assertRaises(ValueError, wagascianpy.utils.utils.renametree, run_root_dir='/test_renametree',
                          run_name='test', dif_topology=self.topology)

    def check_paths(self):
        self.assertFalse(os.path.exists('/test_renametree/test_ecal_dif_0.raw'))
        self.assertTrue(os.path.exists('/test_renametree/test_ecal_dif_1.raw'))
        self.assertFalse(os.path.exists('/test_renametree/test_ecal_dif_2.raw'))
        self.assertTrue(os.path.exists('/test_renametree/test_ecal_dif_3.raw'))
        self.assertFalse(os.path.exists('/test_renametree/test_ecal_dif_4.raw'))
        self.assertTrue(os.path.exists('/test_renametree/test_ecal_dif_5.raw'))
        self.assertFalse(os.path.exists('/test_renametree/test_ecal_dif_6.raw'))
        self.assertTrue(os.path.exists('/test_renametree/test_ecal_dif_7.raw'))


def my_test_function(run_name, dif_id, max_seconds=3):
    print("Run {} DIF {} : START".format(run_name, dif_id))
    time.sleep(randint(1, max_seconds))
    print("Run {} DIF {} : RETURN".format(run_name, dif_id))
    return 0


class TestThreadUtils(unittest.TestCase):

    def setUp(self):
        self.max_threads = 4
        self.run_chains = {"test1": {}, "test2": {}, "test3": {}}
        for run_name, chain in sorted(self.run_chains.items()):
            for dif_id in range(8):
                chain[dif_id] = recordclass('Chain', ['link', 'thread'])
                chain[dif_id].thread = wagascianpy.analysis.analysis.ThreadWithReturnValue(target=my_test_function,
                                                                                           args=(run_name, dif_id,))

    def test_limit_chains(self):
        for run_name, chain in sorted(self.run_chains.items()):
            for dif_id in range(8):
                chain[dif_id].thread.start()
                wagascianpy.utils.utils.limit_chains(self.run_chains, self.max_threads)

                num_active_threads = 0
                for dif_chains in self.run_chains.values():
                    for dif_chain in dif_chains.values():
                        if dif_chain.thread.is_alive():
                            num_active_threads += 1
                print("Number of active threads = {}".format(num_active_threads))
                self.assertLessEqual(num_active_threads, self.max_threads)

    def test_join_chains(self):
        for run_name, chain in sorted(self.run_chains.items()):
            for dif_id in range(8):
                chain[dif_id].thread.start()

        wagascianpy.utils.utils.join_chains(self.run_chains)

        num_active_threads = 0
        for dif_chains in self.run_chains.values():
            for dif_chain in dif_chains.values():
                if dif_chain.thread.is_alive():
                    num_active_threads += 1
        self.assertEqual(num_active_threads, 0)


if __name__ == '__main__':
    unittest.main()
