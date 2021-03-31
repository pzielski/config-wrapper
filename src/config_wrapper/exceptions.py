class ConfigWrapperException(Exception):
    """Base exception for config_wrapper errors"""


class InvalidFieldTypeException(ConfigWrapperException):
    """Configuration field has invalid type"""


class EmptyConfigurationException(ConfigWrapperException):
    """Configuration manager has zero linked sections"""
