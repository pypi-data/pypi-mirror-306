from os import path
import pathlib
import unittest

from ninja_bear import Orchestrator, Plugin
from ninja_bear.base.generator_configuration import GeneratorConfiguration
from src.ninja_bear_language_shell.generator import Generator
from src.ninja_bear_language_shell.config import Config


# Desired code outcome when using ninja-bear-language-shell.
_COMPARE_FILE_CONTENT = """
#!/bin/sh

TEST_CONFIG_MY_BOOLEAN=1
TEST_CONFIG_MY_INTEGER=142
TEST_CONFIG_MY_FLOAT=322.0
TEST_CONFIG_MY_COMBINED_FLOAT=45724.0
TEST_CONFIG_MY_DOUBLE=233.9
TEST_CONFIG_MY_REGEX="Test Reg(E|e)x" # Just another RegEx.
TEST_CONFIG_MY_SUBSTITUTED_STRING="Sometimes I just want to scream Hello World!"
"""


class Test(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._test_path = pathlib.Path(__file__).parent.resolve()
        self._test_config_path = path.join(self._test_path, '..', 'example/test-config.yaml')
        self._plugins = [
            Plugin('ninja-bear-language-shell', Config)
        ]

    def test_run_generators(self):
        orchestrator = Orchestrator.read_config(self._test_config_path, plugins=self._plugins)
        language_configs = orchestrator.language_configs

        self.assertEqual(len(language_configs), 1)

        language_config = language_configs[0]
        config_generator = language_config.generator

        # This is required to use the local implementation of the generator. Otherwise, the
        # plugin would be executed by the ninja-bear module and the code coverage couldn't
        # be checked.
        local_generator = Generator(
            GeneratorConfiguration(
                indent=config_generator._indent,
                transformers=config_generator.transformers,
                naming_conventions=config_generator._naming_conventions,
                type_name=config_generator._type_name
            ),
            properties=config_generator._properties,
            additional_props=config_generator._additional_props,
        )

        self.maxDiff = None
        self.assertEqual(local_generator.dump().strip(), _COMPARE_FILE_CONTENT.strip())
