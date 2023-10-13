import ast
from typing import List

from flake8_plugin_utils import Error

from flake8_vedro_allure.abstract_checkers import ScenarioChecker
from flake8_vedro_allure.config import Config
from flake8_vedro_allure.errors import AllureTagIsNotUnique
from flake8_vedro_allure.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor
)


@ScenarioVisitor.register_scenario_checker
class AllureUniqueTagsChecker(ScenarioChecker):

    def check_scenario(self, context: Context, config: Config) -> List[Error]:

        allure_decorator = self.get_allure_decorator(context.scenario_node)

        if not allure_decorator:
            return []

        tags_names = self.get_allure_tag_names(allure_decorator)

        errors = []
        for tag in config.unique_allure_labels:
            if tags_names.count(tag) > 1:
                errors.append(
                    AllureTagIsNotUnique(allure_decorator.lineno, allure_decorator.col_offset,
                                         allure_tag=tag)
                )

        return errors
