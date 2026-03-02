import ast
from typing import List, Union, Optional

SCENARIOS_FOLDER = 'scenarios'


class ScenarioHelper:

    def get_decorator_by_name_or_attr(
        self,
        scenario_node: ast.ClassDef,
        name: Optional[str] = None,
        attr: Optional[str] = None,
        parent_name: Optional[str] = None
    ) -> Union[ast.Call, None]:
        for decorator in scenario_node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue

            if name is not None:
                if isinstance(decorator.func, ast.Name) and decorator.func.id == name:
                    return decorator

            if attr is not None:
                if parent_name is not None:
                    if (isinstance(decorator.func, ast.Attribute) and
                        decorator.func.attr == attr and
                        isinstance(decorator.func.value, ast.Name) and
                        decorator.func.value.id == parent_name):
                        return decorator
                else:
                    if isinstance(decorator.func, ast.Name) and decorator.func.id == attr:
                        return decorator

        return None

    def get_allure_decorator(self, scenario_node: ast.ClassDef) -> Union[ast.Call, None]:
        return self.get_decorator_by_name_or_attr(scenario_node, name='allure_labels')

    def _is_id_imported_from_allure(self, import_from_nodes: List[ast.ImportFrom]) -> bool:
        for import_from in import_from_nodes:
            if import_from.module == 'allure':
                for name in import_from.names:
                    if name.name == 'id':
                        return True
        return False

    def get_allure_id_decorator(
        self,
        scenario_node: ast.ClassDef,
        import_from_nodes: Optional[List[ast.ImportFrom]] = None
    ) -> Union[ast.Call, None]:
        allure_id = self.get_decorator_by_name_or_attr(
            scenario_node,
            attr='id',
            parent_name='allure'
        )
        if allure_id:
            return allure_id

        id_decorator = self.get_decorator_by_name_or_attr(
            scenario_node,
            name='id'
        )
        if id_decorator and import_from_nodes and self._is_id_imported_from_allure(import_from_nodes):
            return id_decorator

        return None

    def get_allure_tag_names(self, allure_decorator: ast.Call) -> List[str]:

        def get_tag_first_name(arg: ast.Attribute) -> str:
            if isinstance(arg.value, ast.Attribute):
                return get_tag_first_name(arg.value)
            if isinstance(arg.value, ast.Name):
                return arg.value.id
            return arg.attr

        tags_names = []
        for arg in allure_decorator.args:
            if isinstance(arg, ast.Attribute):
                tags_names.append(get_tag_first_name(arg))
        return tags_names
