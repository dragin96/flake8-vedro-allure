from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro_allure.config import DefaultConfig
from flake8_vedro_allure.errors import NoRequiredAllureTag
from flake8_vedro_allure.visitors import ScenarioVisitor
from flake8_vedro_allure.visitors.scenario_allure_checkers import (
    AllureRequiredTagsChecker
)


def test_none_of_one_required_tag():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureRequiredTagsChecker)
    code = """
    @allure_labels(MANUAL)
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, NoRequiredAllureTag,
                 config=DefaultConfig(required_allure_labels=['Feature']),
                 allure_tags='Feature')


def test_none_of_one_required_tag_2():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureRequiredTagsChecker)
    code = """
    @allure_labels(MANUAL, OtherFeature.Page)
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, NoRequiredAllureTag,
                 config=DefaultConfig(required_allure_labels=['Feature']),
                 allure_tags='Feature')


def test_one_of_one_required_tag():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureRequiredTagsChecker)
    code = """
    @allure_labels(Feature.House)
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(required_allure_labels=['Feature']))


def test_one_of_two_required_tags():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureRequiredTagsChecker)
    code = """
    @allure_labels(Feature.House)
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, NoRequiredAllureTag,
                 config=DefaultConfig(required_allure_labels=['Feature', 'Story']),
                 allure_tags='Story')


def test_two_of_two_required_tags():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureRequiredTagsChecker)
    code = """
    @allure_labels(Story.New, Feature.House)
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(required_allure_labels=['Feature', 'Story']))


def test_none_of_two_required_tags():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureRequiredTagsChecker)
    code = """
    @allure_labels(Other.Tag)
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, NoRequiredAllureTag,
                 config=DefaultConfig(required_allure_labels=['Feature', 'Story']),
                 allure_tags='Feature,Story')


def test_required_tag_twice():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureRequiredTagsChecker)
    code = """
    @allure_labels(Feature.One, Feature.Two)
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(required_allure_labels=['Feature']))