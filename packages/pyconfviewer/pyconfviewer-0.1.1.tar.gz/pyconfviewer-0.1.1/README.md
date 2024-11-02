# pyconfviewer

`pyconfviewer` is a Python library designed for viewing and comparing configuration files in various formats such as YAML, JSON, INI, and .env. It simplifies the management and review of configuration files by generating visual HTML reports.

Please let me know if you use the other configuration files as issues or pull requests. I will try to add support for them.

## Features

- Supports loading configurations in multiple formats: YAML, JSON, INI, and .env
- Generates HTML reports for easy visualization of configurations
- Compares configurations between two directories, highlighting differences in HTML format
- Easily installable and runnable with simple command examples

## Requirements

- Python 3.8 or higher(latest version is 3.13 as of now)

## Installation

`pyconfviewer` is available on PyPI. Install it with:

```bash
pip install pyconfviewer
```

## Usage

After installation, use `pyconfviewer` in your own scripts to generate configuration reports or compare configuration files.
Please see the example/run_generator.py script below for a demonstration.

### 1. Generate an HTML report of configuration files

The following example script, `rungenerator.py`, reads configuration files from a specified directory and generates an HTML report at `config_report.html`.

```python
import os
from pyconfviewer.config_generator import ConfigGenerator

# Define the configuration directory
config_dir = "path/to/config_a"
output_dir = "output"
config_html = os.path.join(output_dir, "config_report.html")

# Create an instance of ConfigGenerator and generate the HTML report
config_generator = ConfigGenerator()
configs = config_generator.load_configs(config_dir)
config_generator.generate_config_html(configs, output_dir=output_dir, output_html_path=config_html)

print(f"Configuration HTML generated at {config_html}")
```

Example output:

![config_report.html](https://github.com/pkaiy81/pyconfviewer/blob/main/examples/images/image.png)

### 2. Generate an HTML diff report comparing two configuration directories

Compare configuration files in two directories and generate an HTML report at `diff_report.html`.

```python
from pyconfviewer.diff_generator import DiffGenerator

# Define the configuration directories to compare
config_a_dir = "path/to/config_a"
config_b_dir = "path/to/config_b"
diff_html = os.path.join(output_dir, "diff_report.html")

# Create an instance of DiffGenerator and generate the HTML diff report
diff_generator = DiffGenerator()
configs_a = config_generator.load_configs(config_a_dir)
configs_b = config_generator.load_configs(config_b_dir)
diffs = diff_generator.generate_diff(configs_a, configs_b)
diff_generator.generate_diff_html(diffs, output_dir=output_dir, output_html_path=diff_html)

print(f"Diff HTML generated at {diff_html}")
```

Example output:
![diif_report.html](https://github.com/pkaiy81/pyconfviewer/blob/develop/examples/images/image-1.png)

## Contributing

`pyconfviewer` is an open-source project, and contributions are welcome!
If you have ideas for improvements or would like to fix bugs, please feel free to submit a pull request.

For more details, see [CONTRIBUTION.md](CONTRIBUTION.md).

## License

This project is licensed under the [MIT License](LICENSE).
