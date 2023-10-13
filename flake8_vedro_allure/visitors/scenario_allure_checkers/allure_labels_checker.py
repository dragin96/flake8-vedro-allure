from typing import List

from flake8_plugin_utils import Error

from flake8_vedro_allure.abstract_checkers import ScenarioChecker
from flake8_vedro_allure.config import Config
from flake8_vedro_allure.errors import NoAllureLabelsDecorator
from flake8_vedro_allure.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor
)


@ScenarioVisitor.register_scenario_checker
class AllureLabelsChecker(ScenarioChecker):

    def check_scenario(self, context: Context, config: Config) -> List[Error]:
        if config.is_allure_labels_optional:
            return []

        allure_decorator = self.get_allure_decorator(context.scenario_node)

        if not allure_decorator:
            return [NoAllureLabelsDecorator(context.scenario_node.lineno,
                                            context.scenario_node.col_offset)]

        return []
