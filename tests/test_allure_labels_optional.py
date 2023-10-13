from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro_allure.config import DefaultConfig
from flake8_vedro_allure.errors import NoAllureLabelsDecorator
from flake8_vedro_allure.visitors import ScenarioVisitor
from flake8_vedro_allure.visitors.scenario_allure_checkers import (
    AllureLabelsChecker
)


def test_no_allure_decorator_when_not_optional():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureLabelsChecker)
    code = """
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, NoAllureLabelsDecorator,
                 config=DefaultConfig(required_allure_labels=['Feature'],
                                      is_allure_labels_optional=False))


def test_no_allure_decorator_when_optional():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureLabelsChecker)
    code = """
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_labels_optional=True))


def test_allure_decorator_when_not_optional():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureLabelsChecker)
    code = """
    @allure_labels(Feature.House)
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_labels_optional=False))


def test_allure_decorator_when_optional():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureLabelsChecker)
    code = """
    @allure_labels(Feature.House)
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_labels_optional=True))
