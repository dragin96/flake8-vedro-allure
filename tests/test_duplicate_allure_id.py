from flake8_plugin_utils import assert_error, assert_not_error
from unittest.mock import patch

from flake8_vedro_allure.config import DefaultConfig
from flake8_vedro_allure.errors import DuplicateAllureIdError
from flake8_vedro_allure.visitors import ScenarioVisitor
from flake8_vedro_allure.visitors.scenario_allure_checkers import (
    DuplicateAllureIdChecker
)


def test_no_duplicate_with_disabled_check():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(DuplicateAllureIdChecker)

    code = """
    @allure.id(12345)
    class Scenario: pass
    """

    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=False))


def test_duplicate_detection():
    checker = DuplicateAllureIdChecker()
    checker.reset_checker()

    with patch.object(checker, 'extract_allure_id', return_value='12345'):
        class MockNode:
            def __init__(self, name, lineno=1, col_offset=0):
                self.name = name
                self.lineno = lineno
                self.col_offset = col_offset

        class MockContext:
            def __init__(self, filename, lineno=1, col_offset=0):
                self.filename = filename
                self.scenario_node = MockNode('Scenario', lineno, col_offset)
                self.import_from_nodes = []

        context1 = MockContext('file1.py')
        errors1 = checker.check_scenario(context1, DefaultConfig(is_allure_id_required=True))
        assert len(errors1) == 0, "First scenario should not cause an error"

        context2 = MockContext('file2.py', 10, 5)
        errors2 = checker.check_scenario(context2, DefaultConfig(is_allure_id_required=True))

        assert len(errors2) == 1, "Second scenario should cause an error"
        assert isinstance(errors2[0], DuplicateAllureIdError)


def test_same_file_no_error():
    checker = DuplicateAllureIdChecker()
    checker.reset_checker()

    with patch.object(checker, 'extract_allure_id', return_value='12345'):
        class MockNode:
            def __init__(self, name, lineno=1, col_offset=0):
                self.name = name
                self.lineno = lineno
                self.col_offset = col_offset

        class MockContext:
            def __init__(self, filename, lineno=1, col_offset=0):
                self.filename = filename
                self.scenario_node = MockNode('Scenario', lineno, col_offset)
                self.import_from_nodes = []

        context1 = MockContext('file1.py')
        errors1 = checker.check_scenario(context1, DefaultConfig(is_allure_id_required=True))
        assert len(errors1) == 0

        context2 = MockContext('file1.py', 10, 5)
        errors2 = checker.check_scenario(context2, DefaultConfig(is_allure_id_required=True))
        assert len(errors2) == 0, "Same file should not cause a duplicate error"


def test_different_ids_no_error():
    checker = DuplicateAllureIdChecker()
    checker.reset_checker()

    class MockNode:
        def __init__(self, name, lineno=1, col_offset=0):
            self.name = name
            self.lineno = lineno
            self.col_offset = col_offset

    class MockContext:
        def __init__(self, filename, lineno=1, col_offset=0):
            self.filename = filename
            self.scenario_node = MockNode('Scenario', lineno, col_offset)
            self.import_from_nodes = []

    with patch.object(checker, 'extract_allure_id', return_value='12345'):
        context1 = MockContext('file1.py')
        errors1 = checker.check_scenario(context1, DefaultConfig(is_allure_id_required=True))
        assert len(errors1) == 0

    with patch.object(checker, 'extract_allure_id', return_value='67890'):
        context2 = MockContext('file2.py', 10, 5)
        errors2 = checker.check_scenario(context2, DefaultConfig(is_allure_id_required=True))
        assert len(errors2) == 0, "Different IDs should not cause an error"


def test_allure_id_keyword_arg():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(DuplicateAllureIdChecker)

    code = """
    @allure.id(id=12345)
    class Scenario: pass
    """

    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=True))
