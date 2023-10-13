import ast
from typing import List, Union

SCENARIOS_FOLDER = 'scenarios'


class ScenarioHelper:

    def get_allure_decorator(self, scenario_node: ast.ClassDef) -> Union[ast.Call, None]:
        for decorator in scenario_node.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                if decorator.func.id == 'allure_labels':
                    return decorator

    def get_allure_tag_names(self, allure_decorator: ast.Call) -> List[str]:

        def get_tag_first_name(arg: ast.Attribute) -> str:
            if isinstance(arg.value, ast.Attribute):
                return get_tag_first_name(arg.value)
            if isinstance(arg.value, ast.Name):
                return arg.value.id

        tags_names = []
        for arg in allure_decorator.args:
            if isinstance(arg, ast.Attribute):
                tags_names.append(get_tag_first_name(arg))
        return tags_names
