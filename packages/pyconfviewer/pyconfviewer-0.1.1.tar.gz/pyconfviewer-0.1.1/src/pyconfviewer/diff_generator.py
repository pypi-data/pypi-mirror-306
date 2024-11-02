import os
import json
import difflib
from jinja2 import Environment, FileSystemLoader


class DiffGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        template_path = os.path.join(self.base_dir, "templates")
        self.env = Environment(loader=FileSystemLoader(template_path))

    def generate_diff(self, configs_a, configs_b):
        diffs = {}
        for key in configs_a.keys() | configs_b.keys():
            config_a = configs_a.get(key, "")
            config_b = configs_b.get(key, "")

            # Convert dictionaries to JSON strings for line-by-line comparison
            config_a_str = json.dumps(config_a, indent=4).splitlines()
            config_b_str = json.dumps(config_b, indent=4).splitlines()

            # Generate unified diff
            diff = "\n".join(
                difflib.unified_diff(
                    config_a_str,
                    config_b_str,
                    fromfile=key + " (A)",
                    tofile=key + " (B)",
                    lineterm="",
                )
            )
            if diff:
                diffs[key] = diff
        return diffs

    def generate_diff_html(
        self, diffs, output_dir="output", output_html_path="output/diff_report.html"
    ):
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Convert diffs to a JSON string and escape special characters for JavaScript
        diffs_json = (
            json.dumps(diffs)
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
        )

        # Render HTML with embedded JSON data
        template = self.env.get_template("config_diff_viewer.html")
        rendered_html = template.render(diffs_json=diffs_json)

        # Write the rendered HTML to the output path
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)
