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

    def get_allure_id_decorator(self, scenario_node: ast.ClassDef) -> Union[ast.Call, None]:
        """Check if class has an @allure.id() decorator"""
        for decorator in scenario_node.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                if decorator.func.attr == 'id' and isinstance(decorator.func.value, ast.Name) and decorator.func.value.id == 'allure':
                    return decorator
        return None

    def has_allure_id_method(self, scenario_node: ast.ClassDef) -> bool:
        """Check if class has a method that sets allure.id"""
        for node in scenario_node.body:
            # Check for a function definition
            if isinstance(node, ast.FunctionDef):
                # Check function body for assignment like allure.dynamic.id(...)
                for stmt in node.body:
                    if self._is_allure_id_assignment(stmt):
                        return True
        return False

    def _is_allure_id_assignment(self, node: ast.stmt) -> bool:
        """Check if a statement is setting an allure ID"""
        # Check for expressions like allure.dynamic.id(...)
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute):
                # Check for allure.dynamic.id(...) pattern
                if node.value.func.attr == 'id':
                    # Direct allure.id(...) call
                    if (isinstance(node.value.func.value, ast.Name) and 
                        node.value.func.value.id == 'allure'):
                        return True
                    # allure.dynamic.id(...) call
                    elif (isinstance(node.value.func.value, ast.Attribute) and 
                          node.value.func.value.attr == 'dynamic' and
                          isinstance(node.value.func.value.value, ast.Name) and
                          node.value.func.value.value.id == 'allure'):
                        return True
        return False

    def check_scenario(self, context: Context, config: Config) -> List[Error]:
        if not config.is_allure_id_required:
            return []

        # Check for decorator
        allure_id_decorator = self.get_allure_id_decorator(context.scenario_node)
        
        # Check for method setting ID
        has_allure_id_method = self.has_allure_id_method(context.scenario_node)

        # If neither are found, report an error
        if not allure_id_decorator and not has_allure_id_method:
            return [NoAllureIdError(context.scenario_node.lineno, 
                                    context.scenario_node.col_offset)]

        return [] 