# shiertier_logger

English | [中文](https://github.com/shiertier-utils/shiertier_logger/blob/main/README_zh.md)

## Introduction

`shiertier_logger` is a Python logging utility designed to simplify logging with internationalization (i18n) support. It integrates seamlessly with the `loguru` library and provides a straightforward interface for logging messages in different languages. The library also supports automatic log file rotation and configuration via environment variables.

## Installation

You can install `shiertier_logger` via `pip`:

```bash
pip install git+https://github.com/shiertier/shiertier_logger.git
```

Please note that this project is still under development.

## Usage

### Initialization

The logger is automatically initialized when you import the module. The log files are stored in the directory specified by the `LOG_DIR` environment variable, or in the `.shiertier/logs` directory under the user's home directory if `LOG_DIR` is not set.

```python
from shiertier_logger import logger

# or use Logger_I18n, need shiertier_i18n support
from shiertier_logger import easy_logger_i18n
```

### Logging Messages

You can use the `easy_logger_i18n` object to log messages with translation support:

```python
easy_logger_i18n.info("Hello, world!")
```

You can also pass a dictionary to replace placeholders in the logged message:

```python
easy_logger_i18n.info("Hello, $$name$$!", replace_dict={'$$name$$': 'Alice'})
```

### Available Methods

- `info(message: str, replace_dict: Dict[str, Any] = None) -> None`
- `debug(message: str, replace_dict: Dict[str, Any] = None) -> None`
- `warning(message: str, replace_dict: Dict[str, Any] = None) -> None`
- `error(message: str, replace_dict: Dict[str, Any] = None) -> None`

### Configuration

#### Log Directory

By default, the log files are stored in the directory specified by the `LOG_DIR` environment variable. If `LOG_DIR` is not set, it defaults to the `.shiertier/logs` directory under the user's home directory.

You can set the `LOG_DIR` environment variable to specify a different directory:

```bash
export LOG_DIR=/path/to/logs
```

#### Log Level

The log level can be configured via the `LOG_LEVEL` environment variable. The default log level is `INFO`.

You can set the `LOG_LEVEL` environment variable to specify a different log level:

```bash
export LOG_LEVEL=DEBUG
```

#### Log to System Output

By default, the logger logs to both a file and the system output (stdout). You can disable logging to the system output by setting the `LOG_SYS` environment variable to `False`.

```bash
export LOG_SYS=False
```

## Dependencies

- `loguru`
- `shiertier_i18n` (optional, for translation support)

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.