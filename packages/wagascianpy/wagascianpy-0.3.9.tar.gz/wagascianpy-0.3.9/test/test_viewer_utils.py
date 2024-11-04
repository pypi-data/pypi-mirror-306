import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import pyfakefs.fake_filesystem_unittest

# noinspection PyProtectedMember
import wagascianpy.viewer.utils


class TestCheckers(pyfakefs.fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        self.fs.create_dir('/testdir')
        self.fs.create_file('/testdir/libwagasci.so')
        self.fs.create_dir('/testdir/run1')
        self.fs.create_dir('/testdir/run2')
        self.fs.create_dir('/testdir/run3')
        self.records = [{"name": "run1", "run_folder": "/testdir/run1"},
                        {"name": "run2", "run_folder": "/testdir/run2"},
                        {"name": "run3", "run_folder": "/testdir/run3"}]
        self.run_dic = {"run1": "/testdir/run1", "run2": "/testdir/run2", "run3": "/testdir/run3"}

    def test_check_repository_and_database_sanity_1(self):
        # should not throw
        repository = '/testdir'
        database = '/testdir/database.db'
        wagascianpy.viewer.utils.check_repository_and_database_sanity(repository=repository, database=database)
        repository = 'kekcc:/testdir'
        database = 'kekcc:/testdir/database.db'
        wagascianpy.viewer.utils.check_repository_and_database_sanity(repository=repository, database=database)
        repository = '/testdir'
        database = 'kekcc:/testdir/database.db'
        wagascianpy.viewer.utils.check_repository_and_database_sanity(repository=repository, database=database)
        repository = 'giorgio@kekcc:/testdir'
        database = 'giorgio@kekcc:/testdir/database.db'
        wagascianpy.viewer.utils.check_repository_and_database_sanity(repository=repository, database=database)

    def test_check_repository_and_database_sanity_2(self):
        repository = 'kekcc::/testdir'
        database = 'kekcc:/testdir/database.db'
        self.assertRaises(ValueError, wagascianpy.viewer.utils.check_repository_and_database_sanity,
                          repository=repository, database=database)

    def test_check_repository_and_database_sanity_3(self):
        repository = '/testdir'
        database = '/testdir/database.txt'
        self.assertRaises(ValueError, wagascianpy.viewer.utils.check_repository_and_database_sanity,
                          repository=repository, database=database)

    def test_check_repository_and_database_sanity_4(self):
        repository = ''
        database = '/testdir/database.db'
        self.assertRaises(ValueError, wagascianpy.viewer.utils.check_repository_and_database_sanity,
                          repository=repository, database=database)

    def test_check_repository_and_database_sanity_5(self):
        repository = '/testdir'
        database = ''
        self.assertRaises(ValueError, wagascianpy.viewer.utils.check_repository_and_database_sanity,
                          repository=repository, database=database)

    def test_check_repository_and_database_sanity_6(self):
        repository = ':/testdir'
        database = '/testdir/database.txt'
        self.assertRaises(ValueError, wagascianpy.viewer.utils.check_repository_and_database_sanity,
                          repository=repository, database=database)

    def test_check_wagasci_libdir_1(self):
        wagasci_libdir = '/testdir'
        self.assertEqual(wagasci_libdir, wagascianpy.viewer.utils.check_wagasci_libdir(wagasci_libdir))

    def test_check_wagasci_libdir_2(self):
        wagasci_libdir = ''
        self.assertIsNone(wagascianpy.viewer.utils.check_wagasci_libdir(wagasci_libdir))

    def test_check_wagasci_libdir_3(self):
        wagasci_libdir = None
        self.assertIsNone(wagascianpy.viewer.utils.check_wagasci_libdir(wagasci_libdir))

    def test_check_wagasci_libdir_4(self):
        wagasci_libdir = '/sdfaoigqpsaoJAADG'
        self.assertIsNone(wagascianpy.viewer.utils.check_wagasci_libdir(wagasci_libdir))

    def test_check_wagasci_libdir_5(self):
        wagasci_libdir = '/testdir/libwagasci.so'
        self.assertRaises(ValueError, wagascianpy.viewer.utils.check_wagasci_libdir, wagasci_libdir)

    def test_check_input_folder_1(self):
        self.assertRaises(OSError, wagascianpy.viewer.utils.check_input_folder,
                          input_folder='/asidsagjpoasdgopj', records=[], batch_mode=True)

    def test_check_input_folder_2(self):
        self.assertEqual(self.run_dic, wagascianpy.viewer.utils.check_input_folder(input_folder='/testdir',
                                                                                   records=self.records,
                                                                                   batch_mode=True))

    # noinspection PyUnusedLocal,PyShadowingBuiltins
    @mock.patch('wagascianpy.viewer.utils._get_input', return_value='/testdir')
    def test_check_input_folder_3(self, input):
        self.assertEqual(self.run_dic, wagascianpy.viewer.utils.check_input_folder(input_folder='',
                                                                                   records=self.records,
                                                                                   batch_mode=True))

    def test_check_input_folder_4(self):
        self.records.append({'name': 'run4', 'run_folder': '/testdir/run4'})
        self.assertEqual(self.run_dic, wagascianpy.viewer.utils.check_input_folder(input_folder='/testdir',
                                                                                   records=self.records,
                                                                                   batch_mode=True))

    def test_check_input_folder_5(self):
        del self.records[0]
        del self.run_dic["run1"]
        self.assertEqual(self.run_dic, wagascianpy.viewer.utils.check_input_folder(input_folder='/testdir',
                                                                                   records=self.records,
                                                                                   batch_mode=True))


if __name__ == '__main__':
    unittest.main()
