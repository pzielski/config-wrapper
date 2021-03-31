import configparser
import dataclasses

from config_wrapper.exceptions import InvalidFieldTypeException, EmptyConfigurationException


class ConfigManager:
    """Base class for configuration managers

    This class should be used only as a base for real
        configuration manager class. These real classes
        should have defined attributes of a dataclasses.dataclass type

        Mentioned dataclass attributes are configuration sections
        and their types are section templates.
    """
    _valid_field_types = [str, bool, int, float, list]

    @classmethod
    def load(cls, file_path: str, encoding: str = 'utf-8', list_sep: str = ';'):
        """Loads configuration from file_path using configparser.ConfigParser.read()

         If the argument `sound` isn't passed in, the default Animal
        sound is used.

        Parameters
        ----------
        file_path : str
            path to configuration file

        encoding: str, optional
            encoding of config file (default is 'utf-8')

        list_sep: str optional
            list separator character (default ';')

        Raises
        ------
        EmptyConfigurationException
            If 'cls' class does not have any attributes
                of dataclasses.dataclass type
        InvalidFieldTypeException
            If any attribute type of section template
                is not one of ConfigManager._valid_field_types
        """
        config = configparser.ConfigParser()
        config.read(file_path, encoding=encoding)
        if '__annotations__' not in cls.__dict__:
            raise EmptyConfigurationException('Configuration class has zero linked sections')
        for section_name, section in cls.__annotations__.items():
            if dataclasses.is_dataclass(section):
                section_values = dict()
                for field in dataclasses.fields(section):
                    if not any([issubclass(field.type, t) for t in ConfigManager._valid_field_types]):
                        raise InvalidFieldTypeException(f'Field {field.name} in section {section_name} '
                                                        f'has invalid type; '
                                                        f'valid types are: {ConfigManager._valid_field_types}')
                    if issubclass(field.type, bool):
                        section_values[field.name] = config.getboolean(section_name, field.name)
                    elif issubclass(field.type, int):
                        section_values[field.name] = config.getint(section_name, field.name)
                    elif issubclass(field.type, float):
                        section_values[field.name] = config.getfloat(section_name, field.name)
                    elif issubclass(field.type, list):
                        value = config.get(section_name, field.name)
                        if value:
                            section_values[field.name] = config.get(section_name, field.name).split(list_sep)
                        else:
                            section_values[field.name] = []
                    else:
                        section_values[field.name] = config.get(section_name, field.name)
                setattr(cls, section_name, section(**section_values))

    @classmethod
    def generate_file(cls, file_path: str, encoding: str = 'utf-8'):
        """Generates configuration file based on attributes in 'cls' class

         Only attributes of dataclasses.dataclass are taken into account.

        Parameters
        ----------
        file_path : str
            path to configuration file that will be generated

        encoding: str, optional
            encoding of config file (default is 'utf-8')
        """

        file_string = ''
        for section_name, section in cls.__annotations__.items():
            if dataclasses.is_dataclass(section):
                file_string += f'[{section_name}]\n'
                for field in dataclasses.fields(section):
                    file_string += f'{field.name} = \n'
                file_string += '\n'
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(file_string)
