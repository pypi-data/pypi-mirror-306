import sys
import time
import unittest
from enum import Enum

import pyfakefs.fake_filesystem_unittest
from six import string_types

from wagascianpy.utils.classproperty import classproperty
from wagascianpy.utils.configuration import WagasciConfigParser, VirtualConfiguration, conf_setter, conf_getter, \
    Configuration, create_sections


class TestEnum(Enum):
    Foo = 1
    Bar = 2


# noinspection PyMethodParameters,PyPropertyDefinition
class CustomVolatileConfiguration(VirtualConfiguration):
    _test_str = 'test_volatile'

    @classmethod
    def reset(cls):
        cls._test_str = 'test_volatile'

    @classmethod
    def is_volatile(cls):
        return True

    @classproperty
    def test_str(cls):
        return cls._test_str

    @test_str.setter
    def test_str(cls, value):
        conf_setter(cls=cls, name='_test_str', value=value)


# noinspection PyMethodParameters,PyPropertyDefinition
class CustomConfiguration(VirtualConfiguration):
    _test_str = 'test'
    _test_int = 1
    _test_float = 3.14
    _test_bool = False
    _test_enum = TestEnum.Foo
    _test_none_str = ''
    _test_none_int = 0
    _test_none_float = 0.

    @classmethod
    def reset(cls):
        cls._test_str = 'test'
        cls._test_int = 1
        cls._test_float = 3.14
        cls._test_bool = False
        cls._test_enum = TestEnum.Foo
        cls._test_none_str = ''
        cls._test_none_int = 0
        cls._test_none_float = 0.

    @classmethod
    def is_volatile(cls):
        return False

    @classproperty
    def test_str(cls):
        return cls._test_str

    @test_str.setter
    def test_str(cls, value):
        conf_setter(cls=cls, name='_test_str', value=value)

    @classproperty
    def test_int(cls):
        return cls._test_int

    @test_int.setter
    def test_int(cls, value):
        conf_setter(cls=cls, name='_test_int', value=value)

    @classproperty
    def test_float(cls):
        return cls._test_float

    @test_float.setter
    def test_float(cls, value):
        conf_setter(cls=cls, name='_test_float', value=value)

    @classproperty
    def test_bool(cls):
        return cls._test_bool

    @test_bool.setter
    def test_bool(cls, value):
        conf_setter(cls=cls, name='_test_bool', value=value)

    @classproperty
    def test_enum(cls):
        return cls._test_enum

    @test_enum.setter
    def test_enum(cls, value):
        conf_setter(cls=cls, name='_test_enum', value=value)

    @classproperty
    def test_none_str(cls):
        return cls._test_none_str

    @test_none_str.setter
    def test_none_str(cls, value):
        conf_setter(cls=cls, name='_test_none_str', value=value)

    @classproperty
    def test_none_int(cls):
        return cls._test_none_int

    @test_none_int.setter
    def test_none_int(cls, value):
        conf_setter(cls=cls, name='_test_none_int', value=value)

    @classproperty
    def test_none_float(cls):
        return cls._test_none_float

    @test_none_float.setter
    def test_none_float(cls, value):
        conf_setter(cls=cls, name='_test_none_float', value=value)


class CustomConfigParser1(WagasciConfigParser, CustomConfiguration, CustomVolatileConfiguration):
    pass


# noinspection PyUnresolvedReferences,PyPropertyAccess
class TestDefaultParser(unittest.TestCase):

    def setUp(self):
        self.default_parser = WagasciConfigParser()
        self.custom_parser = CustomConfigParser1()

    def tearDown(self):
        self.custom_parser.custom_configuration.reset()

    def test_property_value(self):
        self.assertEqual(CustomConfiguration.test_str, self.custom_parser.custom_configuration.test_str)
        self.assertEqual(CustomConfiguration.test_int, self.custom_parser.custom_configuration.test_int)
        self.assertEqual(CustomConfiguration.test_float, self.custom_parser.custom_configuration.test_float)
        self.assertEqual(CustomConfiguration.test_bool, self.custom_parser.custom_configuration.test_bool)
        self.assertEqual(CustomConfiguration.test_enum, self.custom_parser.custom_configuration.test_enum)

    def test_propery_type(self):
        self.assertIsInstance(self.custom_parser.custom_configuration.test_str, string_types)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_int, int)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_float, float)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_bool, bool)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_enum, TestEnum)

    def test_bool_propery_setter(self):
        self.custom_parser.custom_configuration.test_bool = 'True'
        self.assertTrue(self.custom_parser.custom_configuration.test_bool)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_bool, bool)
        self.custom_parser.custom_configuration.test_bool = 'False'
        self.assertFalse(self.custom_parser.custom_configuration.test_bool)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_bool, bool)

    def test_int_propery_setter(self):
        self.custom_parser.custom_configuration.test_int = '42'
        self.assertEqual(42, self.custom_parser.custom_configuration.test_int)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_int, int)
        self.custom_parser.custom_configuration.test_int = 42.1
        self.assertEqual(42, self.custom_parser.custom_configuration.test_int)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_int, int)

    def test_float_propery_setter(self):
        self.custom_parser.custom_configuration.test_float = '3.14'
        self.assertEqual(3.14, self.custom_parser.custom_configuration.test_float)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_float, float)
        self.custom_parser.custom_configuration.test_float = 3
        self.assertEqual(3., self.custom_parser.custom_configuration.test_float)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_float, float)

    def test_enum_propery_setter(self):
        self.custom_parser.custom_configuration.test_enum = 1
        self.assertEqual(TestEnum.Foo, self.custom_parser.custom_configuration.test_enum)
        self.custom_parser.custom_configuration.test_enum = 'bar'
        self.assertEqual(TestEnum.Bar, self.custom_parser.custom_configuration.test_enum)

    def test_none_str_propery_setter(self):
        self.custom_parser.custom_configuration.test_none_str = None
        self.assertEqual('', self.custom_parser.custom_configuration.test_none_str)

    def test_none_int_propery_setter(self):
        self.custom_parser.custom_configuration.test_none_int = None
        self.assertEqual(0, self.custom_parser.custom_configuration.test_none_int)

    def test_none_float_propery_setter(self):
        self.custom_parser.custom_configuration.test_none_float = None
        self.assertEqual(0.0, self.custom_parser.custom_configuration.test_none_float)

    def test_setter_exceptions(self):
        with self.assertRaises(ValueError):
            self.custom_parser.custom_configuration.test_float = 'aregareg'
        with self.assertRaises(ValueError):
            self.custom_parser.custom_configuration.test_int = 'aregareg'
        with self.assertRaises(ValueError):
            self.custom_parser.custom_configuration.test_bool = 'aregareg'
        with self.assertRaises(ValueError):
            self.custom_parser.custom_configuration.test_enum = 'aregareg'

    def test_get_section(self):
        self.assertEqual(self.custom_parser.get_section('custom_configuration'), CustomConfiguration)
        self.assertEqual(self.custom_parser.custom_configuration.test_str, 'test')
        self.assertRaises(AttributeError, self.default_parser.get_section, 'fdanviounvdafivb')

    def test_get_sections(self):
        self.assertIsInstance(self.default_parser.get_sections(), list)
        self.assertIsInstance(self.custom_parser.get_sections(), list)
        self.assertIn('custom_configuration', self.custom_parser.get_sections())

    def test_prettyprint(self):
        self.custom_parser = CustomConfigParser1()
        self.custom_parser.prettyprint()
        sys.stdout.flush()


###########################################################################################################

# noinspection PyUnresolvedReferences
class TestConfigFile(pyfakefs.fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        self.config_file_path_write = '/tmp/test_write.ini'
        self.config_file_path_read = '/tmp/test_read.ini'

    def test_write_default(self):
        self.custom_parser = CustomConfigParser1()
        self.custom_parser.custom_configuration.test_int = 42
        self.custom_parser.custom_configuration.test_enum = TestEnum.Bar
        self.custom_parser.custom_configuration.test_bool = True
        self.custom_parser.custom_configuration.test_float = 1.62
        self.custom_parser.custom_configuration.test_str = 'abu'
        self.custom_parser.custom_configuration.test_none_str = None
        self.custom_parser.custom_configuration.test_none_int = None
        self.custom_parser.custom_configuration.test_none_float = None
        self.custom_parser.write(self.config_file_path_write)
        with open(self.config_file_path_write, 'r') as fin:
            content = fin.read()
            self.assertIn('test_str = abu', content)
            self.assertIn('test_int = 42', content)
            self.assertIn('test_float = 1.62', content)
            self.assertIn('test_bool = True', content)
            self.assertIn('test_enum = Bar', content)
            self.assertIn('test_none_str = ', content)
            self.assertIn('test_none_int = 0', content)
            self.assertIn('test_none_float = 0.0', content)
        self.custom_parser.custom_configuration.reset()

    def test_read(self):
        with open(self.config_file_path_read, 'w') as fout:
            fout.writelines(['[custom_configuration]\n',
                             'test_str = abu\n',
                             'test_int = 42\n',
                             'test_bool = True\n',
                             'test_float = 1.62\n',
                             'test_enum = Bar'])

        self.custom_parser = CustomConfigParser1(self.config_file_path_read)
        self.assertEqual('abu', self.custom_parser.custom_configuration.test_str)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_str, str)
        self.assertEqual(42, self.custom_parser.custom_configuration.test_int)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_int, int)
        self.assertEqual(1.62, self.custom_parser.custom_configuration.test_float)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_float, float)
        self.assertEqual(True, self.custom_parser.custom_configuration.test_bool)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_bool, bool)
        self.assertEqual(TestEnum.Bar, self.custom_parser.custom_configuration.test_enum)
        self.assertIsInstance(self.custom_parser.custom_configuration.test_enum, TestEnum)
        self.custom_parser.custom_configuration.reset()

    def test_volatile(self):
        self.custom_parser = CustomConfigParser1(self.config_file_path_write)
        with open(self.config_file_path_write, 'r') as fin:
            content = fin.read()
            self.assertNotIn('test_str = test_volatile', content)
        self.assertEqual('test_volatile', self.custom_parser.custom_volatile_configuration.test_str)


###########################################################################################################

# noinspection PyUnresolvedReferences
class TestConfigurationProvider(pyfakefs.fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_default_configuration(self):
        parser = WagasciConfigParser()
        self.assertEqual(parser.global_configuration.t2krun, Configuration.global_configuration.t2krun())

    def test_create_section(self):
        Configuration.create_section("test_section")
        Configuration.test_section.override({'foo': 42})
        self.assertEqual(42, Configuration.test_section.foo())
        Configuration.create_section("test_section")  # should not raise
        Configuration.delete_section("test_section")

    def test_get_sections(self):
        Configuration.create_section("test_section")
        Configuration.test_section.override({'foo': 42})
        self.assertIn("test_section", Configuration.get_sections())
        Configuration.delete_section("test_section")


###########################################################################################################

# noinspection PyMethodParameters,PyPropertyDefinition
class CustomVolatileConfiguration(VirtualConfiguration):
    _test_str = "buyaka"
    _test_bool = True

    @classmethod
    def reset(cls):
        cls._test_str = "buyaka"
        cls._test_bool = True

    @classmethod
    def is_volatile(cls):
        return True

    @classproperty
    def test_str(cls):
        return conf_getter(cls=cls, name='_test_str')

    @test_str.setter
    def test_str(cls, value):
        conf_setter(cls=cls, name='_test_str', value=value)

    @classproperty
    def test_bool(cls):
        return conf_getter(cls=cls, name='_test_bool')

    @test_bool.setter
    def test_bool(cls, value):
        conf_setter(cls=cls, name='_test_bool', value=value)


class CustomConfigParser2(WagasciConfigParser, CustomVolatileConfiguration):
    pass


@create_sections(parser_class=CustomConfigParser2)
class CustomConfigurationProvider(Configuration):
    pass


class TestCustomConfigurationProvider(pyfakefs.fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_default_configuration(self):
        parser = CustomConfigParser2()
        self.assertEqual(parser.custom_volatile_configuration.test_str,
                         CustomConfigurationProvider.custom_volatile_configuration.test_str())
        self.assertEqual(parser.custom_volatile_configuration.test_bool,
                         CustomConfigurationProvider.custom_volatile_configuration.test_bool())
        self.assertEqual(parser.global_configuration.t2krun,
                         CustomConfigurationProvider.global_configuration.t2krun())

    def test_create_section(self):
        CustomConfigurationProvider.create_section("test_section")
        CustomConfigurationProvider.test_section.override({'foo': 42})
        self.assertEqual(42, CustomConfigurationProvider.test_section.foo())
        CustomConfigurationProvider.create_section("test_section")  # should not raise
        CustomConfigurationProvider.delete_section("test_section")

    def test_get_sections(self):
        CustomConfigurationProvider.create_section("test_section")
        CustomConfigurationProvider.test_section.override({'foo': 42})
        self.assertIn("test_section", CustomConfigurationProvider.get_sections())
        CustomConfigurationProvider.delete_section("test_section")

    def test_dump(self):
        # Normal configuration
        print("NORMAL CONFIGURATION")
        Configuration.dump()
        print("CUSTOM CONFIGURATION")
        # Custom configuration
        CustomConfigurationProvider.dump()
        sys.stdout.flush()
        time.sleep(1)


if __name__ == '__main__':
    unittest.main()
