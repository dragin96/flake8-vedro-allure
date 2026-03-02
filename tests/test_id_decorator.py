from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro_allure.config import DefaultConfig
from flake8_vedro_allure.errors import NoAllureIdError
from flake8_vedro_allure.visitors import ScenarioVisitor
from flake8_vedro_allure.visitors.scenario_allure_checkers import (
    AllureIdRequiredChecker
)


def test_with_id_from_allure_import():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
from allure import id

@id(123)
class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=True))


def test_with_id_from_allure_import_and_other_decorators():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
from allure import id

@allure_labels(Feature.House)
@id(123)
class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=True))


def test_with_id_from_non_allure_import():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
from any_other_lib import id

@id(1)
class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, NoAllureIdError,
                 config=DefaultConfig(is_allure_id_required=True))


def test_with_id_without_import():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
@id(123)
class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, NoAllureIdError,
                 config=DefaultConfig(is_allure_id_required=True))
