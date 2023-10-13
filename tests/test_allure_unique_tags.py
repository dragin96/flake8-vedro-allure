from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro_allure.config import DefaultConfig
from flake8_vedro_allure.errors import AllureTagIsNotUnique
from flake8_vedro_allure.visitors import ScenarioVisitor
from flake8_vedro_allure.visitors.scenario_allure_checkers import (
    AllureUniqueTagsChecker
)


def test_unique_tags_twice():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureUniqueTagsChecker)
    code = """
    @allure_labels(Feature.One, Feature.Two)
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, AllureTagIsNotUnique,
                 config=DefaultConfig(unique_allure_labels=['Feature']),
                 allure_tag='Feature')


def test_unique_tag():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureUniqueTagsChecker)
    code = """
    @allure_labels(Feature.One)
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(unique_allure_labels=['Feature']))


def test_one_of_two_tags_not_unique():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureUniqueTagsChecker)
    code = """
    @allure_labels(Story.A, Feature.One, Feature.Two)
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, AllureTagIsNotUnique,
                 config=DefaultConfig(unique_allure_labels=['Feature', 'Story']),
                 allure_tag='Feature')
