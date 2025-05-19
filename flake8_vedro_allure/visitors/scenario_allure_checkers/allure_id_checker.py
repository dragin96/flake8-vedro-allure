import ast
from typing import List, Union

from flake8_plugin_utils import Error

from flake8_vedro_allure.abstract_checkers import ScenarioChecker
from flake8_vedro_allure.config import Config
from flake8_vedro_allure.errors import NoAllureIdError
from flake8_vedro_allure.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor
)


@ScenarioVisitor.register_scenario_checker
class AllureIdRequiredChecker(ScenarioChecker):

    def has_allure_id_method(self, scenario_node: ast.ClassDef) -> bool:
        for node in scenario_node.body:
            if isinstance(node, ast.FunctionDef):
                for stmt in node.body:
                    if self._is_allure_id_assignment(stmt):
                        return True
        return False

    def _is_allure_id_assignment(self, node: ast.stmt) -> bool:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute):
                if node.value.func.attr == 'id':
                    if (isinstance(node.value.func.value, ast.Name) and 
                        node.value.func.value.id == 'allure'):
                        return True
                    elif (isinstance(node.value.func.value, ast.Attribute) and 
                          node.value.func.value.attr == 'dynamic' and
                          isinstance(node.value.func.value.value, ast.Name) and
                          node.value.func.value.value.id == 'allure'):
                        return True
        return False

    def check_scenario(self, context: Context, config: Config) -> List[Error]:
        if not config.is_allure_id_required:
            return []

        allure_id_decorator = self.get_allure_id_decorator(context.scenario_node)
        
        has_allure_id_method = self.has_allure_id_method(context.scenario_node)

        if not allure_id_decorator and not has_allure_id_method:
            return [NoAllureIdError(context.scenario_node.lineno, 
                                    context.scenario_node.col_offset)]

        return [] 