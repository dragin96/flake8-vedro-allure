from flake8_plugin_utils import assert_error, assert_not_error
from unittest.mock import patch, Mock

from flake8_vedro_allure.config import DefaultConfig
from flake8_vedro_allure.errors import DuplicateAllureIdError
from flake8_vedro_allure.visitors import ScenarioVisitor
from flake8_vedro_allure.visitors.scenario_allure_checkers import (
    DuplicateAllureIdChecker
)


def test_unique_allure_id():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(DuplicateAllureIdChecker)
    
    # Reset allure id cache between tests
    DuplicateAllureIdChecker.reset_checker()
    
    # Create code with two scenarios with different allure.id
    code = """
    class Scenario1:
        def __init__(self):
            allure.id(12345)
            
    class Scenario2:
        def __init__(self):
            allure.id(67890)
    """
    
    # Both scenarios should pass the check
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=True))


def test_no_duplicate_with_disabled_check():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(DuplicateAllureIdChecker)
    
    # Reset allure id cache between tests
    DuplicateAllureIdChecker.reset_checker()
    
    # Create code with two scenarios with the same allure.id
    code = """
    @allure.id(12345)
    class Scenario1: pass
    
    @allure.id(12345)
    class Scenario2: pass
    """
    
    # If is_allure_id_required=False, the check should not be performed
    assert_not_error(ScenarioVisitor, code,
                     config=DefaultConfig(is_allure_id_required=False))


def test_duplicate_detection():
    """
    Unit test for duplicate detection
    """
    # Initialize the checker
    DuplicateAllureIdChecker.reset_checker()
    checker = DuplicateAllureIdChecker()
    
    with patch.object(checker, 'extract_allure_id', return_value='12345'):
        class MockNode:
            def __init__(self, name, lineno=1, col_offset=0):
                self.name = name
                self.lineno = lineno
                self.col_offset = col_offset
    
        class MockContext:
            def __init__(self, filename, scenario_name, lineno=1, col_offset=0):
                self.filename = filename
                self.scenario_node = MockNode(scenario_name, lineno, col_offset)
        
        # First scenario should be added without errors
        context1 = MockContext('file1.py', 'Scenario1')
        errors1 = checker.check_scenario(context1, DefaultConfig(is_allure_id_required=True))
        assert len(errors1) == 0, "First scenario should not cause an error"
        
        # Second scenario with the same ID should cause an error
        context2 = MockContext('file2.py', 'Scenario2', 10, 5)
        errors2 = checker.check_scenario(context2, DefaultConfig(is_allure_id_required=True))
        
        assert len(errors2) == 1, "Second scenario should cause an error"
        assert isinstance(errors2[0], DuplicateAllureIdError), "Error should be of type DuplicateAllureIdError"


def test_same_filename_different_scenarios():
    """
    Test for duplicate detection in the same file with different scenario names
    """
    # Initialize the checker
    DuplicateAllureIdChecker.reset_checker()
    checker = DuplicateAllureIdChecker()
    
    with patch.object(checker, 'extract_allure_id', return_value='12345'):
        class MockNode:
            def __init__(self, name, lineno=1, col_offset=0):
                self.name = name
                self.lineno = lineno
                self.col_offset = col_offset
    
        class MockContext:
            def __init__(self, filename, scenario_name, lineno=1, col_offset=0):
                self.filename = filename
                self.scenario_node = MockNode(scenario_name, lineno, col_offset)
        
        # First scenario in the file
        context1 = MockContext('file1.py', 'Scenario1')
        errors1 = checker.check_scenario(context1, DefaultConfig(is_allure_id_required=True))
        assert len(errors1) == 0, "First scenario should not cause an error"
        
        # Second scenario in the same file but with a different name
        context2 = MockContext('file1.py', 'Scenario2', 10, 5)
        errors2 = checker.check_scenario(context2, DefaultConfig(is_allure_id_required=True))
        
        assert len(errors2) == 1, "Second scenario should cause an error"
        assert isinstance(errors2[0], DuplicateAllureIdError), "Error should be of type DuplicateAllureIdError"


def test_same_class_name_no_error():
    """
    Test that identical class names in different files should not cause an error
    if they have different IDs
    """
    # Initialize the checker
    DuplicateAllureIdChecker.reset_checker()
    checker = DuplicateAllureIdChecker()
    
    class MockNode:
        def __init__(self, name, lineno=1, col_offset=0):
            self.name = name
            self.lineno = lineno
            self.col_offset = col_offset

    class MockContext:
        def __init__(self, filename, scenario_name, lineno=1, col_offset=0):
            self.filename = filename
            self.scenario_node = MockNode(scenario_name, lineno, col_offset)
    
    # Scenario in the first file with ID 12345
    with patch.object(checker, 'extract_allure_id', return_value='12345'):
        context1 = MockContext('file1.py', 'Scenario')
        errors1 = checker.check_scenario(context1, DefaultConfig(is_allure_id_required=True))
        assert len(errors1) == 0, "First scenario should not cause an error"
    
    # Scenario in the second file with the same name but different ID
    with patch.object(checker, 'extract_allure_id', return_value='67890'):
        context2 = MockContext('file2.py', 'Scenario', 10, 5)
        errors2 = checker.check_scenario(context2, DefaultConfig(is_allure_id_required=True))
        assert len(errors2) == 0, "Second scenario should not cause an error with a different ID" 