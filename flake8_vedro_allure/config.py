from typing import List, Optional


class Config:
    def __init__(
            self,
            is_allure_labels_optional: bool,
            required_allure_labels: Optional[List],
            unique_allure_labels: Optional[List],
            is_allure_id_required: bool = False
    ):
        self.is_allure_labels_optional = is_allure_labels_optional
        self.required_allure_labels = required_allure_labels if required_allure_labels else []
        self.unique_allure_labels = unique_allure_labels if unique_allure_labels else []
        self.is_allure_id_required = is_allure_id_required


class DefaultConfig(Config):
    def __init__(
            self,
            is_allure_labels_optional: bool = True,
            required_allure_labels: Optional[List] = None,
            unique_allure_labels: Optional[List] = None,
            is_allure_id_required: bool = False
    ):

        super().__init__(
            is_allure_labels_optional=is_allure_labels_optional,
            required_allure_labels=required_allure_labels,
            unique_allure_labels=unique_allure_labels,
            is_allure_id_required=is_allure_id_required
        )
