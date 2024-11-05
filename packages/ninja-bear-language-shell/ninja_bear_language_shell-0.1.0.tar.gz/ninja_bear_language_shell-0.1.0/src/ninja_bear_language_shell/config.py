from typing import Type

from .generator import Generator
from ninja_bear import LanguageConfigBase, NamingConventionType


class Config(LanguageConfigBase):
    """
    Shell specific config. For more information about the config methods, refer to LanguageConfigBase.
    """

    def _file_extension(self) -> str:
        """
        Specifies which extension to use for the generated config file. For Shell the
        file-extension '.sh' gets used.

        :return: Config file extension.
        :rtype:  str
        """
        return 'sh'

    def _generator_type(self) -> Type[Generator]:
        """
        Specifies which GeneratorBase deriving class to use to actually generate the config file.
        In this case the Generator class from generator.py gets used. If you want to use a different
        Generator class or you want to rename the Generator class, make sure to update the return
        value accordingly.

        :return: GeneratorBase derivative class to generate the config file.
        :rtype:  Type[Generator]
        """
        return Generator

    def _default_file_naming_convention(self) -> NamingConventionType:
        """
        Specifies the default file naming convention. This is necessary because some languages (e.g. Java)
        require files to have a specific kind of naming format.

        :return: Default naming convention.
        :rtype:  NamingConventionType
        """
        raise NamingConventionType.SNAKE_CASE

    def _allowed_file_name_pattern(self) -> str:
        """
        Specifies the allowed file name pattern for the generated config file. This is necessary
        because some languages (e.g. Java) require the file to have a specific kind of naming format.

        :return: File naming regex.
        :rtype:  str
        """
        return r'.+'
