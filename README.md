# Config wrapper

Simple package that wraps `configparser` module. It loads configuration file and keeps it in singleton object. 

Main requirements are:
* have type hints in IDE (like PyCharm)
* easy to add new sections and fields
* automatic type casting based on on dataclass attribute type

Currently only following field types are supported: `str`, `bool`, `ini`, `float`, `list`.


## Simple example
Preparing config manager:
```
# define config section templates
from dataclasses import dataclass

@dataclass
class ExampleSection1:
    field_1: str
    field_2: int

@dataclass
class ExampleSection2:
    field_1: bool
    field_2: float
    field_3: list

# prepare config manager
from config_wrapper import ConfigManager

class AppConfig(ConfigManager):
    section_1: ExampleSection1
    section_2: ExampleSection2
``` 

Prepare `config.ini` file:

```
[section_1]
field_1 = value 123
field_2 = 42

[section_2]
field_1 = no
field_2 = 3.14
field_3 = item1;item2;item3
```

Load configuration & access to values loaded from `config.ini` file:
```
AppConfig.load('config.ini', list_sep=';')

print(AppConfig.section_1.field_1)
# value 123

print(AppConfig.section_2.field_1)
# False

print(AppConfig.section_2.field_3)
# ['item1', 'item2', 'item3']
```

## Config section template
Config section template is simple dataclass. It's attributes represents fields in configuration in section.  

To point type of field one must pass type hint to dataclass attribute (e.g. `field_name: int`).

Section example:
```
from dataclasses import dataclass

@dataclass
class MySection:
    field_1: str  # name of field in config file
    field_2: int    
``` 

Attention! Default values of attributes are ignored and overwritten by values from configuration file!

## Passing sections to config manager
Having config sections class one can create class that inherits from `ConfigManager` class and add class attribute of section template type.
This attribute name is associated with section name from configuration file.

Simple example:
```
from dataclasses import dataclass

from config_wrapper import ConfigManager

@dataclass
class MySection:
    field_1: str  # name of field in config file
    field_2: int


class AppConfig(ConfigManager):
    my_section_name: MySection    
```

Above example corresponds to following configuration structure:

```
[my_section_name]
field_1 =
field_2 =
```

## TODO

1. Add unit tests for generating raw config file from ConfigManager.
1. Generating config file from ConfigManager using default values from template sections.
1. While generating config file if file exist and field has value it will be copied to newly generated file.
1. Maybe support for JSON and YAML files.
1. Maybe support for more types. 
