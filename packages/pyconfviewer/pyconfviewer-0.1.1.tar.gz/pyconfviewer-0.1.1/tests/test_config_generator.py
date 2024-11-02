import unittest
import os
import shutil
from src.pyconfviewer.config_generator import ConfigGenerator
from src.pyconfviewer.diff_generator import DiffGenerator


class TestConfigAndDiffGenerator(unittest.TestCase):
    def setUp(self):
        # Define paths for mock configs and output files
        self.config_a_dir = "tests/mock_configs/config_a"
        self.config_b_dir = "tests/mock_configs/config_b"
        self.output_dir = "tests/output"
        self.config_html = os.path.join(self.output_dir, "config_report.html")
        self.diff_html = os.path.join(self.output_dir, "diff_report.html")

        # Ensure output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Initialize generators
        self.config_generator = ConfigGenerator()
        self.diff_generator = DiffGenerator()

    def test_generate_config_html(self):
        # Load mock configs from config_a directory
        configs_a = self.config_generator.load_configs(self.config_a_dir)

        # Generate HTML report for config_a
        self.config_generator.generate_config_html(
            configs_a, output_dir=self.output_dir, output_html_path=self.config_html
        )

        # Assert HTML report is generated
        self.assertTrue(os.path.exists(self.config_html))

        # Check if HTML contains expected elements
        with open(self.config_html, "r") as f:
            html_content = f.read()
            self.assertIn("<title>Configuration Viewer</title>", html_content)

    def test_generate_diff_html(self):
        # Load mock configs from config_a and config_b directories
        configs_a = self.config_generator.load_configs(self.config_a_dir)
        configs_b = self.config_generator.load_configs(self.config_b_dir)

        # Generate diff and HTML diff report
        diffs = self.diff_generator.generate_diff(configs_a, configs_b)
        self.diff_generator.generate_diff_html(
            diffs, output_dir=self.output_dir, output_html_path=self.diff_html
        )

        # Assert HTML diff report is generated
        self.assertTrue(os.path.exists(self.diff_html))

        # Check if HTML contains expected elements
        with open(self.diff_html, "r") as f:
            html_content = f.read()
            self.assertIn("<title>Configuration Diff Viewer</title>", html_content)

    def tearDown(self):
        # Cleanup generated files and output directory
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)


if __name__ == "__main__":
    unittest.main()
