# shiertier_i18n
english | [中文](https://github.com/shiertier-utils/shiertier_i18n/blob/main/README_zh.md)

## Introduction

`shiertier_i18n` is a simple internationalization (i18n) library for Python, designed to help developers easily localize their applications into different languages. The library is based on the `gettext` module and supports automatic detection of language and localization directories from environment variables, providing a simple interface for translating strings.

## Installation

You can install `shiertier_i18n` via `pip`:

```bash
pip install git+https://github.com/shiertier/shiertier_i18n.git
```

Please note that this project is still under development.

## Usage

### Initialization

First, you need to initialize the `I18n` class:

```python
from shiertier_i18n import I18n

# Using default language and localization directory
i18n = I18n()

# Or specify the language and localization directory
i18n = I18n(language_str='zh_CN', locales_dir='/path/to/locales')
```

### Translating Strings

You can use the `translate` method to translate strings:

```python
translated_str = i18n.translate("Hello, world!")
print(translated_str)
```

You can also pass a dictionary to replace placeholders in the translated string:

```python
translated_str = i18n.translate("Hello, $$name$$!", replace_dict={'$$name$$': 'Alice'})
print(translated_str)
```

### Shortcut

If you only need to quickly translate a string, you can use the `easy_i18n` shortcut:

```python
from shiertier_i18n import easy_i18n

translated_str = easy_i18n("Hello, world!")
print(translated_str)
```

## Configuration

### Language

By default, the `I18n` class will get the language setting from the `LANGUAGE` environment variable. If `LANGUAGE` is not set, it defaults to `en_US`.

You can also specify the language when initializing the `I18n` class:

```python
i18n = I18n(language_str='zh_CN')
```

### Localization Directory

By default, the `I18n` class will get the localization directory from the `SHIERTIER_LOCALES_DIR` environment variable. If `SHIERTIER_LOCALES_DIR` is not set, it defaults to the `.shiertier/locales` directory under the user's home directory.

You can also specify the localization directory when initializing the `I18n` class:

```python
i18n = I18n(locales_dir='/path/to/locales')
```

## Dependencies

- `gettext`

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.