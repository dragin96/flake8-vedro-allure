# flake8-vedro-allure
Flake8 based linter for Vedro framework and allure

## Installation

```bash
pip inslall flake8-vedro-allure
```


## Rules

1. **ALR001**: missing @allure_labels for scenario
2. **ALR002**: missing required allure tag
3. **ALR003**: duplication of unique allure tag

**Rules configuration**
```editorconfig
[flake8]
is_allure_labels_optional = false                 ;ALR001
required_allure_labels = Feature,Story,Priority   ;ALR002
unique_allure_labels = Priority                   ;ALR003
```

## Configuration
Flake8-vedro-allure is flake8 plugin, so the configuration is the same as [flake8 configuration](https://flake8.pycqa.org/en/latest/user/configuration.html).

You can ignore rules via
- file `setup.cfg`: parameter `ignore`
```editorconfig
[flake8]
ignore = ALR001
```
- comment in code `#noqa: ALR001`