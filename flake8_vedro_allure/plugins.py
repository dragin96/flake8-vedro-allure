import argparse
import ast
from typing import Callable, List, Optional

from flake8.options.manager import OptionManager
from flake8_plugin_utils import Plugin, Visitor

from flake8_vedro_allure.visitors import ScenarioVisitor

from .config import Config


def str_to_bool(string):
    return string.lower() in ('true', 'yes', 't', '1')


class PluginWithFilename(Plugin):
    def __init__(self, tree: ast.AST, filename: str, *args, **kwargs):
        super().__init__(tree)
        self.filename = filename

    def run(self):
        for visitor_cls in self.visitors:
            visitor = self._create_visitor(visitor_cls, filename=self.filename)
            visitor.visit(self._tree)
            for error in visitor.errors:
                yield self._error(error)

    @classmethod
    def _create_visitor(cls, visitor_cls: Callable, filename: Optional[str] = None) -> Visitor:
        if cls.config is None:
            return visitor_cls(filename=filename)
        return visitor_cls(config=cls.config, filename=filename)


class VedroAllurePlugin(PluginWithFilename):
    name = 'flake8_vedro_allure'
    version = '1.0.0'
    visitors = [
        ScenarioVisitor,
    ]

    def __init__(self, tree: ast.AST, filename: str,  *args, **kwargs):
        super().__init__(tree, filename)

    @classmethod
    def add_options(cls, option_manager: OptionManager):
        option_manager.add_option(
            '--is-allure-labels-optional',
            type=str,
            default='true',
            parse_from_config=True,
            help='If allure labels decorator is required for every test',
        )
        option_manager.add_option(
            '--required-allure-labels',
            comma_separated_list=True,
            parse_from_config=True,
            help='List of required allure labels for every tests',
        )
        option_manager.add_option(
            '--unique-allure-labels',
            comma_separated_list=True,
            parse_from_config=True,
            help='List of allure labels that should not be used twice per one test',
        )
        option_manager.add_option(
            '--is-allure-id-required',
            type=str,
            default='false',
            parse_from_config=True,
            help='If allure.id() decorator is required for every test',
        )


    @classmethod
    def parse_options_to_config(
        cls, option_manager: OptionManager, options: argparse.Namespace, args: List[str]
    ) -> Config:
        return Config(
            is_allure_labels_optional=str_to_bool(options.is_allure_labels_optional),
            required_allure_labels=options.required_allure_labels,
            unique_allure_labels=options.unique_allure_labels,
            is_allure_id_required=str_to_bool(options.is_allure_id_required)
        )
