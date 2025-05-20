from flake8_plugin_utils import Error


class NoAllureLabelsDecorator(Error):
    code = 'ALR001'
    message = 'scenario should has allure_labels decorator'


class NoRequiredAllureTag(Error):
    code = 'ALR002'
    message = 'scenario should has allure tags {allure_tags}'


class AllureTagIsNotUnique(Error):
    code = 'ALR003'
    message = 'scenario should has only one allure tag {allure_tag}'


class NoAllureIdError(Error):
    code = 'ALR004'
    message = 'scenario should have @allure.id() or @id() decorator'


class DuplicateAllureIdError(Error):
    code = 'ALR005'
    message = 'duplicate allure id {allure_id} was found in {scenario_path}'
    
    def __init__(self, lineno: int, col_offset: int, **kwargs):
        super().__init__(lineno, col_offset, **kwargs)
        
    @classmethod
    def formatted_message(cls, **kwargs) -> str:
        return cls.message.format(**kwargs)
