import configparser
import dataclasses
import unittest
from dataclasses import dataclass
from unittest.mock import MagicMock

from src.config_wrapper import ConfigManager
from exceptions import InvalidFieldTypeException, EmptyConfigurationException


@dataclass
class SingleFieldStr:
    str_field: str


@dataclass
class SingleFieldBool:
    bool_field: bool


@dataclass
class SingleFieldInt:
    int_field: int


@dataclass
class SingleFieldFloat:
    float_field: float


@dataclass
class SingleFieldList:
    list_field: list


@dataclass
class MultipleField:
    str_field: str
    bool_field: bool
    int_field: int
    float_field: float
    list_field: list


@dataclass
class MultipleField2:
    str_field: str
    str_field_2: str
    bool_field: bool
    bool_field_2: bool
    int_field: int
    int_field_2: int
    float_field: float
    float_field_2: float
    list_field: list
    list_field_2: list


@dataclass
class EmptySection:
    pass


@dataclass
class InvalidFieldTypeSection:
    dict_field: dict


class ConfigManagerTestCase(unittest.TestCase):
    def setUp(self):
        configparser.ConfigParser.read = MagicMock()
        config_data = {
            'section_single_field_str': {
                'str_field': 'abcABCąśćżłÓŹq1 123 $@'
            },
            'section_single_field_bool': {
                'bool_field': False
            },
            'section_single_field_int': {
                'int_field': 1234567890
            },
            'section_single_field_float': {
                'float_field': 991.012
            },
            'section_single_field_list_one_element': {
                'list_field': '123'
            },
            'section_single_field_list_empty': {
                'list_field': ''
            },
            'section_single_field_list_multiple_elements': {
                'list_field': 'a;123; ą ę ź'
            },
            'section_multiple_fields_1': {
                'str_field': 'abcABCąśćżłÓŹq1 123 $@',
                'bool_field': False,
                'int_field': 1234567890,
                'float_field': 991.012,
                'list_field': '123'
            },
            'section_multiple_fields_2': {
                'str_field': '123',
                'bool_field': True,
                'int_field': -16,
                'float_field': -0.1,
                'list_field': ''
            },
            'section_multiple_fields_3': {
                'str_field': 'Żółte Tłoki śiorbią żółtka -1',
                'str_field_2': '',
                'bool_field': False,
                'bool_field_2': True,
                'int_field': 0,
                'int_field_2': 1001,
                'float_field': 12,
                'float_field_2': 0.0,
                'list_field': 'Poważne słowa;Zubehör Gehäuse',
                'list_field_2': '1;a;v;x'
            }
        }

        def mock_get(_, section_name, field_name):
            return config_data[section_name][field_name]

        configparser.ConfigParser.get = mock_get
        configparser.ConfigParser.getboolean = mock_get
        configparser.ConfigParser.getint = mock_get
        configparser.ConfigParser.getfloat = mock_get

    def test_load_singleSection_singleFieldStr_ok(self):
        # arrange
        class AppConfig(ConfigManager):
            section_single_field_str: SingleFieldStr
        expected_value = 'abcABCąśćżłÓŹq1 123 $@'

        # act
        AppConfig.load('_')

        # assert
        self.assertEqual(AppConfig.section_single_field_str.str_field, expected_value)

    def test_load_singleSection_singleFieldBool_ok(self):
        # arrange
        class AppConfig(ConfigManager):
            section_single_field_bool: SingleFieldBool
        expected_value = False

        # act
        AppConfig.load('_')

        # assert
        self.assertEqual(AppConfig.section_single_field_bool.bool_field, expected_value)

    def test_load_singleSection_singleFieldInt_ok(self):
        # arrange
        class AppConfig(ConfigManager):
            section_single_field_int: SingleFieldInt
        expected_value = 1234567890

        # act
        AppConfig.load('_')

        # assert
        self.assertEqual(AppConfig.section_single_field_int.int_field, expected_value)

    def test_load_singleSection_singleFieldFloat_ok(self):
        # arrange
        class AppConfig(ConfigManager):
            section_single_field_float: SingleFieldFloat
        expected_value = 991.012

        # act
        AppConfig.load('_')

        # assert
        self.assertEqual(AppConfig.section_single_field_float.float_field, expected_value)

    def test_load_singleSection_singleFieldList_oneElement_ok(self):
        # arrange
        class AppConfig(ConfigManager):
            section_single_field_list_one_element: SingleFieldList
        expected_value = ['123']

        # act
        AppConfig.load('_')

        # assert
        self.assertEqual(AppConfig.section_single_field_list_one_element.list_field, expected_value)

    def test_load_singleSection_singleFieldList_empty_ok(self):
        # arrange
        class AppConfig(ConfigManager):
            section_single_field_list_empty: SingleFieldList
        expected_value = []

        # act
        AppConfig.load('_')

        # assert
        self.assertEqual(AppConfig.section_single_field_list_empty.list_field, expected_value)

    def test_load_singleSection_singleFieldList_multipleElements_ok(self):
        # arrange
        class AppConfig(ConfigManager):
            section_single_field_list_multiple_elements: SingleFieldList
        expected_value = ['a', '123', ' ą ę ź']

        # act
        AppConfig.load('_')

        # assert
        self.assertEqual(AppConfig.section_single_field_list_multiple_elements.list_field, expected_value)

    def test_load_multipleSections_singleField_ok(self):
        # arrange
        class AppConfig(ConfigManager):
            section_single_field_str: SingleFieldStr
            section_single_field_bool: SingleFieldBool
            section_single_field_int: SingleFieldInt
            section_single_field_float: SingleFieldFloat
            section_single_field_list_one_element: SingleFieldList
        expected_values = ['abcABCąśćżłÓŹq1 123 $@', False, 1234567890, 991.012, ['123']]

        # act
        AppConfig.load('_')

        # assert
        self.assertEqual(AppConfig.section_single_field_str.str_field, expected_values[0])
        self.assertEqual(AppConfig.section_single_field_bool.bool_field, expected_values[1])
        self.assertEqual(AppConfig.section_single_field_int.int_field, expected_values[2])
        self.assertEqual(AppConfig.section_single_field_float.float_field, expected_values[3])
        self.assertEqual(AppConfig.section_single_field_list_one_element.list_field, expected_values[4])

    def test_load_multipleSections_multipleFields_ok(self):
        # arrange
        class AppConfig(ConfigManager):
            section_multiple_fields_1: MultipleField
            section_multiple_fields_2: MultipleField
            section_multiple_fields_3: MultipleField2
        expected_values = [
            ['abcABCąśćżłÓŹq1 123 $@', False, 1234567890, 991.012, ['123']],
            ['123', True, -16, -0.1, []],
            ['Żółte Tłoki śiorbią żółtka -1', '', False, True, 0, 1001, 12.0, 0,
             ['Poważne słowa', 'Zubehör Gehäuse'], ['1', 'a', 'v', 'x']]
        ]

        # act
        AppConfig.load('_')

        # assert
        self.assertEqual(AppConfig.section_multiple_fields_1.str_field, expected_values[0][0])
        self.assertEqual(AppConfig.section_multiple_fields_1.bool_field, expected_values[0][1])
        self.assertEqual(AppConfig.section_multiple_fields_1.int_field, expected_values[0][2])
        self.assertEqual(AppConfig.section_multiple_fields_1.float_field, expected_values[0][3])
        self.assertEqual(AppConfig.section_multiple_fields_1.list_field, expected_values[0][4])

        self.assertEqual(AppConfig.section_multiple_fields_2.str_field, expected_values[1][0])
        self.assertEqual(AppConfig.section_multiple_fields_2.bool_field, expected_values[1][1])
        self.assertEqual(AppConfig.section_multiple_fields_2.int_field, expected_values[1][2])
        self.assertEqual(AppConfig.section_multiple_fields_2.float_field, expected_values[1][3])
        self.assertEqual(AppConfig.section_multiple_fields_2.list_field, expected_values[1][4])

        self.assertEqual(AppConfig.section_multiple_fields_3.str_field, expected_values[2][0])
        self.assertEqual(AppConfig.section_multiple_fields_3.str_field_2, expected_values[2][1])
        self.assertEqual(AppConfig.section_multiple_fields_3.bool_field, expected_values[2][2])
        self.assertEqual(AppConfig.section_multiple_fields_3.bool_field_2, expected_values[2][3])
        self.assertEqual(AppConfig.section_multiple_fields_3.int_field, expected_values[2][4])
        self.assertEqual(AppConfig.section_multiple_fields_3.int_field_2, expected_values[2][5])
        self.assertEqual(AppConfig.section_multiple_fields_3.float_field, expected_values[2][6])
        self.assertEqual(AppConfig.section_multiple_fields_3.float_field_2, expected_values[2][7])
        self.assertEqual(AppConfig.section_multiple_fields_3.list_field, expected_values[2][8])
        self.assertEqual(AppConfig.section_multiple_fields_3.list_field_2, expected_values[2][9])

    def test_load_emptySection_ok(self):
        # arrange
        class AppConfig(ConfigManager):
            empty_section: EmptySection

        # act
        AppConfig.load('_')

        # assert
        self.assertTrue(dataclasses.is_dataclass(AppConfig.empty_section))

    def test_load_invalidFieldType_raiseInvalidFieldTypeException(self):
        # arrange
        class AppConfig(ConfigManager):
            invalid_field_type_section: InvalidFieldTypeSection

        # act & assert
        self.assertRaises(InvalidFieldTypeException, AppConfig.load, '-')

    def test_load_noSections_raiseEmptyConfigurationException(self):
        # arrange
        class AppConfig(ConfigManager):
            pass

        # act & assert
        self.assertRaises(EmptyConfigurationException, AppConfig.load, '-')


if __name__ == '__main__':
    unittest.main()
