from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro_allure.config import DefaultConfig
from flake8_vedro_allure.errors import NoAllureIdError
from flake8_vedro_allure.visitors import ScenarioVisitor
from flake8_vedro_allure.visitors.scenario_allure_checkers import (
    AllureIdRequiredChecker
)


def test_with_simple_id_decorator():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
    @id(123)
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=True))


def test_with_simple_id_decorator_and_other_decorators():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
    @allure_labels(Feature.House)
    @id(123)
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=True))


def test_with_simple_id_decorator_when_not_required():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
    @id(123)
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=False)) 