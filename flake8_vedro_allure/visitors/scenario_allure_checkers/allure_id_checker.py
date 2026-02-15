from typing import List

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

    def check_scenario(self, context: Context, config: Config) -> List[Error]:
        if not config.is_allure_id_required:
            return []

        allure_id_decorator = self.get_allure_id_decorator(
            context.scenario_node,
            context.import_from_nodes
        )

        if not allure_id_decorator:
            return [NoAllureIdError(context.scenario_node.lineno,
                                    context.scenario_node.col_offset)]

        return []
