import ast
from typing import List, Dict, Tuple, Optional

from flake8_plugin_utils import Error

from flake8_vedro_allure.abstract_checkers import ScenarioChecker
from flake8_vedro_allure.config import Config
from flake8_vedro_allure.errors import DuplicateAllureIdError
from flake8_vedro_allure.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor
)


@ScenarioVisitor.register_scenario_checker
class DuplicateAllureIdChecker(ScenarioChecker):
    # Cache for tracking allure ids across different files
    # Format: allure_id -> (filename, class_name, lineno)
    _allure_ids: Dict[str, Tuple[str, str, int]] = {}

    def extract_allure_id(self, scenario_node: ast.ClassDef) -> Optional[str]:
        """
        Extracts the value of allure.id or id from the scenario decorator
        
        Args:
            scenario_node: The scenario class node
            
        Returns:
            String representation of the allure id or None
        """
        allure_id_decorator = self.get_allure_id_decorator(scenario_node)
        if not allure_id_decorator or not allure_id_decorator.args:
            return None

        arg = allure_id_decorator.args[0]

        if isinstance(arg, ast.Constant) and arg.value is not None:
            return str(arg.value)
        return None

    def check_scenario(self, context: Context, config: Config) -> List[Error]:
        errors: List[Error] = []

        allure_id = self.extract_allure_id(context.scenario_node)

        if not allure_id or not config.is_allure_id_required:
            return errors

        filename = context.filename or 'unknown_file.py'
        class_name = context.scenario_node.name

        if allure_id in self._allure_ids:
            stored_filename, stored_class, stored_lineno = self._allure_ids[allure_id]

            # consider it a duplicate
            if stored_filename != filename or stored_class != class_name:
                errors.append(
                    DuplicateAllureIdError(
                        context.scenario_node.lineno,
                        context.scenario_node.col_offset,
                        allure_id=allure_id,
                        scenario_path=f"{stored_filename}::{stored_class}"
                    )
                )
        else:
            self._allure_ids[allure_id] = (filename, class_name, context.scenario_node.lineno)
            
        return errors
        
    @classmethod
    def reset_checker(cls):
        """
        Resets the accumulated allure ids for a new check
        """
        cls._allure_ids = {} 