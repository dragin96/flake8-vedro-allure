import ast
from typing import List, Optional, Type

from flake8_vedro_allure.abstract_checkers import ScenarioChecker
from flake8_vedro_allure.config import Config
from flake8_vedro_allure.visitors._visitor_with_filename import (
    VisitorWithFilename
)


class Context:
    def __init__(self, scenario_node: ast.ClassDef,
                 filename: str):
        self.scenario_node = scenario_node
        self.filename = filename


class ScenarioVisitor(VisitorWithFilename):
    scenarios_checkers: List[ScenarioChecker] = []

    def __init__(self, config: Optional[Config] = None,
                 filename: Optional[str] = None) -> None:
        super().__init__(config, filename)
        self.import_from_nodes = []

    @property
    def config(self):
        return self._config

    @classmethod
    def register_scenario_checker(cls, checker: Type[ScenarioChecker]):
        cls.scenarios_checkers.append(checker())
        return checker

    @classmethod
    def deregister_all(cls):
        cls.scenarios_checkers = []

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == 'Scenario':
            context = Context(scenario_node=node,
                              filename=self.filename)
            try:
                for checker in self.scenarios_checkers:
                    self.errors.extend(checker.check_scenario(context, self.config))
            except Exception as e:
                print(f'Linter failed: checking {context.filename} with {checker.__class__}.\n'
                      f'Exception: {e}')
