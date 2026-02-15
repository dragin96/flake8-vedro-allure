import ast
from typing import List, Dict, Optional, NamedTuple

from flake8_plugin_utils import Error

from flake8_vedro_allure.abstract_checkers import ScenarioChecker
from flake8_vedro_allure.config import Config
from flake8_vedro_allure.errors import DuplicateAllureIdError
from flake8_vedro_allure.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor
)


class AllureIdInScenario(NamedTuple):
    scenario_path: str
    lineno: int


@ScenarioVisitor.register_scenario_checker
class DuplicateAllureIdChecker(ScenarioChecker):

    def __init__(self):
        self._allure_ids: Dict[str, AllureIdInScenario] = {}

    def extract_allure_id(self, scenario_node: ast.ClassDef,
                          import_from_nodes: Optional[List[ast.ImportFrom]] = None) -> Optional[str]:
        allure_id_decorator = self.get_allure_id_decorator(scenario_node, import_from_nodes)
        if not allure_id_decorator:
            return None

        if allure_id_decorator.args:
            arg = allure_id_decorator.args[0]
            if isinstance(arg, ast.Constant) and arg.value is not None:
                return str(arg.value)

        for keyword in allure_id_decorator.keywords:
            if keyword.arg == 'id':
                if isinstance(keyword.value, ast.Constant) and keyword.value is not None:
                    return str(keyword.value.value)

        return None

    def check_scenario(self, context: Context, config: Config) -> List[Error]:
        if not config.is_allure_id_required:
            return []

        allure_id = self.extract_allure_id(
            context.scenario_node,
            context.import_from_nodes
        )

        if not allure_id:
            return []

        filename = context.filename or 'unknown_file.py'

        if allure_id in self._allure_ids:
            stored = self._allure_ids[allure_id]
            if stored.scenario_path != filename:
                return [
                    DuplicateAllureIdError(
                        context.scenario_node.lineno,
                        context.scenario_node.col_offset,
                        allure_id=allure_id,
                        scenario_path=stored.scenario_path
                    )
                ]

        self._allure_ids[allure_id] = AllureIdInScenario(
            scenario_path=filename,
            lineno=context.scenario_node.lineno
        )

        return []

    def reset_checker(self):
        self._allure_ids = {}
