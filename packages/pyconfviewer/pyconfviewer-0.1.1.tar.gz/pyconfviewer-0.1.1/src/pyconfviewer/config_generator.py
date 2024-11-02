import os
import json
import yaml
import toml
import configparser
from dotenv import dotenv_values
from jinja2 import Environment, FileSystemLoader


class ConfigGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        template_path = os.path.join(self.base_dir, "templates")
        self.env = Environment(loader=FileSystemLoader(template_path))

    def load_configs(self, config_dir):
        """Load configurations from various file formats."""
        configs = {}
        for file_name in os.listdir(config_dir):
            file_path = os.path.join(config_dir, file_name)
            if file_name.endswith(".yaml"):
                with open(file_path, "r") as f:
                    configs[file_name] = yaml.safe_load(f)
            elif file_name.endswith(".json"):
                with open(file_path, "r") as f:
                    configs[file_name] = json.load(f)
            elif file_name.endswith(".ini"):
                config = configparser.ConfigParser()
                config.read(file_path)

                # Create a dictionary with all sections, including DEFAULT
                ini_dict = {}
                for section in config.sections():
                    ini_dict[section] = {
                        **config.defaults(),
                        **dict(config.items(section)),
                    }

                # Include DEFAULT section explicitly
                if config.defaults():
                    ini_dict["DEFAULT"] = dict(config.defaults())

                configs[file_name] = ini_dict
            elif file_name == ".env":
                configs[file_name] = dotenv_values(file_path)
            elif file_name.endswith(".toml"):
                with open(file_path, "r") as f:
                    configs[file_name] = toml.load(f)
        return configs

    def generate_config_html(
        self, configs, output_dir="output", output_html_path="output/config_report.html"
    ):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        configs_json = json.dumps(configs).replace('"', '\\"')
        template = self.env.get_template("config_viewer.html")
        rendered_html = template.render(configs_json=configs_json)

        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)
