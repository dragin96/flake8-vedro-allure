from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro_allure.config import DefaultConfig
from flake8_vedro_allure.errors import NoAllureIdError
from flake8_vedro_allure.visitors import ScenarioVisitor
from flake8_vedro_allure.visitors.scenario_allure_checkers import (
    AllureIdRequiredChecker
)


def test_no_allure_id_decorator():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, NoAllureIdError,
                 config=DefaultConfig(is_allure_id_required=True))


def test_no_allure_id_decorator_with_other_decorators():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
    @allure_labels(Feature.House)
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, NoAllureIdError,
                 config=DefaultConfig(is_allure_id_required=True))


def test_with_allure_id_decorator():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
    @allure.id(12345)
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=True))


def test_with_allure_id_and_other_decorators():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
    @allure_labels(Feature.House)
    @allure.id(12345)
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=True))


def test_allure_id_not_required():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=False))


def test_with_allure_id_method():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
    class Scenario:
        def setup(self):
            allure.id(12345)
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=True))


def test_with_allure_dynamic_id_method():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
    class Scenario:
        def setup(self):
            allure.dynamic.id(12345)
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=True))


def test_with_allure_id_in_parameterized_scenario():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(AllureIdRequiredChecker)
    code = """
    class Scenario:
        @classmethod
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
            
        def given_parameter(self, param):
            self.param = param
            allure.id(f"12345-{param}")
            
        def when_action(self):
            pass
    """
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=True)) 