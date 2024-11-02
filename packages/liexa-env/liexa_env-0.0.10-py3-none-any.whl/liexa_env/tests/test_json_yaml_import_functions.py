import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import json
from liexa_env._env import Env


class TestEnvFileLoading(unittest.TestCase):

    def setUp(self):
        """Set up an instance of Env for testing."""
        self.env = Env()

    @patch("pathlib.Path.glob", return_value=[Path("config.json")])
    @patch(
        "builtins.open", new_callable=mock_open, read_data='{"db": {"name": "test_db"}}'
    )
    @patch("os.access", return_value=True)  # Ensure files are readable
    @patch("pathlib.Path.is_file", return_value=True)
    def test_load_json_file(self, mock_is_file, mock_access, mock_open_func, mock_glob):
        """Test loading and parsing of a JSON file."""
        self.env.load(["config.json"])
        self.assertEqual(self.env.env_vars.get("DB_NAME"), "test_db")

    @patch("pathlib.Path.glob", return_value=[Path("config.yaml")])
    @patch("builtins.open", new_callable=mock_open, read_data="db:\n  name: test_db\n")
    @patch("os.access", return_value=True)  # Ensure files are readable
    @patch("pathlib.Path.is_file", return_value=True)
    def test_load_yaml_file(self, mock_is_file, mock_access, mock_open_func, mock_glob):
        """Test loading and parsing of a YAML file."""
        self.env.load(["config.yaml"])
        self.assertEqual(self.env.env_vars.get("DB_NAME"), "test_db")

    @patch(
        "pathlib.Path.glob", side_effect=[[Path("config.yaml")], [Path("config.json")]]
    )
    @patch("builtins.open", new_callable=mock_open, read_data="db:\n  name: test_db\n")
    @patch("os.access", return_value=True)  # Ensure files are readable
    @patch("pathlib.Path.is_file", return_value=True)
    def test_load_multiple_files(
        self, mock_is_file, mock_access, mock_open_func, mock_glob
    ):
        """Test loading of both YAML and JSON files."""
        mock_open_func.side_effect = [
            mock_open(read_data="db:\n  name: test_db\n").return_value,
            mock_open(read_data='{"app": {"name": "test_app"}}').return_value,
        ]
        self.env.load(["config.yaml", "config.json"])
        expected_env_vars = {"DB_NAME": "test_db", "APP_NAME": "test_app"}
        for key, value in expected_env_vars.items():
            self.assertEqual(self.env.env_vars.get(key), value)

    @patch("pathlib.Path.glob", return_value=[Path("config.json")])
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"level1": {"level2": {"level3": {"key": "value"}}}}',
    )
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    def test_deeply_nested_json(
        self, mock_is_file, mock_access, mock_open_func, mock_glob
    ):
        """Test parsing a deeply nested JSON structure."""
        self.env.load(["config.json"])
        self.assertEqual(self.env.env_vars.get("LEVEL1_LEVEL2_LEVEL3_KEY"), "value")

    @patch("pathlib.Path.glob", return_value=[Path("config.yaml")])
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="databases:\n  - name: db1\n    port: 3306\n  - name: db2\n    port: 3307\n",
    )
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    def test_yaml_list_of_dictionaries(
        self, mock_is_file, mock_access, mock_open_func, mock_glob
    ):
        """Test YAML list of dictionaries."""
        self.env.load(["config.yaml"])
        expected_value = (
            '[{"name": "db1", "port": "3306"}, {"name": "db2", "port": "3307"}]'
        )
        self.assertEqual(self.env.env_vars.get("DATABASES"), expected_value)

    @patch("pathlib.Path.glob", return_value=[Path("malformed.json")])
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"')
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    def test_malformed_json(self, mock_is_file, mock_access, mock_open_func, mock_glob):
        """Test that a malformed JSON file raises an error."""
        with self.assertRaises(json.JSONDecodeError):
            self.env.load(["malformed.json"])

    @patch(
        "pathlib.Path.glob",
        side_effect=[[Path("config1.json")], [Path("config2.yaml")]],
    )
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"shared_key": "json_value"}',
    )
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    def test_overlapping_keys_multiple_files(
        self, mock_is_file, mock_access, mock_open_func, mock_glob
    ):
        """Test overlapping keys in JSON and YAML files with file load order priority."""
        mock_open_func.side_effect = [
            mock_open(read_data='{"shared_key": "json_value"}').return_value,
            mock_open(read_data="shared_key: yaml_value\n").return_value,
        ]
        self.env.load(["config1.json", "config2.yaml"])
        self.assertEqual(
            self.env.env_vars.get("SHARED_KEY"), "yaml_value"
        )  # YAML should override JSON


if __name__ == "__main__":
    unittest.main()
