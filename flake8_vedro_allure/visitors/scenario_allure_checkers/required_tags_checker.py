import ast
from typing import List

from flake8_plugin_utils import Error

from flake8_vedro_allure.abstract_checkers import ScenarioChecker
from flake8_vedro_allure.config import Config
from flake8_vedro_allure.errors import NoRequiredAllureTag
from flake8_vedro_allure.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor
)


@ScenarioVisitor.register_scenario_checker
class AllureRequiredTagsChecker(ScenarioChecker):

    def check_scenario(self, context: Context, config: Config) -> List[Error]:
        allure_decorator = self.get_allure_decorator(context.scenario_node)

        if not allure_decorator:
            return []

        tags_names = self.get_allure_tag_names(allure_decorator)

        errors = []
        if config.required_allure_labels:
            missing_tags = [
                tag for tag in config.required_allure_labels if tag not in tags_names
            ]
            if len(missing_tags) > 0:
                errors.append(
                    NoRequiredAllureTag(allure_decorator.lineno, allure_decorator.col_offset,
                                        allure_tags=",".join(missing_tags)))

        return errors
