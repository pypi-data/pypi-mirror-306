from typing import overload
from ninja_bear import GeneratorBase, PropertyType, NamingConventionType, DumpInfo


class Generator(GeneratorBase):
    """
    Shell specific generator. For more information about the generator methods, refer to GeneratorBase.
    """

    def _default_type_naming_convention(self) -> NamingConventionType:
        """
        Specifies the default type naming convention. This is necessary because some languages (e.g. Java)
        require the classes/structs/etc. to have a specific kind of naming format.

        :return: Default naming convention.
        :rtype:  NamingConventionType
        """
        return NamingConventionType.SCREAMING_SNAKE_CASE
    
    @overload
    def _default_property_naming_convention(self) -> NamingConventionType:
        return NamingConventionType.SCREAMING_SNAKE_CASE
    
    def _line_comment(self, string: str) -> str:
        """
        Turns a string into a line comment.

        :param string: String to turn into a line comment.
        :type string:  str

        :return: Commented string.
        :rtype:  str
        """
        return f'# {string}'
    
    def _dump(self, info: DumpInfo) -> str:
        """
        This is where the code gets created. TODO: Make sure to also handle indent and comments
        as this is in the implementer's responsibility. For an example implementation, please
        have a look at the ExampleScriptGenerator class in the ninja-bear test.py file.

        :param type_name:  Contains to required information to dump language specific code.
        :type type_name:   DumpInfo

        :return: Dumped type string.
        :rtype:  str
        """
        lines = ['#!/bin/sh', '']

        for property in info.properties:
            type = property.type
            value = property.value

            if type == PropertyType.BOOL:
                value = 1 if value else 0
            elif type in [PropertyType.STRING, PropertyType.REGEX]:
                value = f'"{value}"'.replace('\\', '\\\\')  # Replace backslash with double backslash to escape it.

            comment = f' {self._line_comment(property.comment)}' if property.comment else ''
            lines.append(f'{info.type_name}_{property.name}={value}{comment}')

        return '\n'.join(lines)
