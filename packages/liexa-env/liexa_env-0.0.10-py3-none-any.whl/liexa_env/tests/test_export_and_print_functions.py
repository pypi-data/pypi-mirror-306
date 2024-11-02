import unittest
from unittest.mock import patch, mock_open
import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from liexa_env._env import Env


class TestEnvExportAndPrint(unittest.TestCase):

    def setUp(self):
        """Set up an instance of Env for testing."""
        self.env = Env()
        self.env.env_vars = {
            "BASE_URL": "https://example.com",
            "API_KEY": "12345",
            "PASSWORD": "supersecret",
        }
        self.env.file_env_keys = {"BASE_URL", "API_KEY", "PASSWORD"}

    @patch("pathlib.Path.glob", return_value=[Path("test.env")])
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="BASE_URL=https://example.com\nAPI_KEY=12345\nPASSWORD=supersecret\n",
    )
    @patch.dict(os.environ, {}, clear=True)
    def test_load_file_based(self, mock_file, mock_is_file, mock_access, mock_glob):
        """Test loading file-based environment variables."""
        # Load file-based environment variables
        self.env.load(files="test.env")

        # Expected environment variables after loading
        expected_env_vars = {
            "BASE_URL": "https://example.com",
            "API_KEY": "12345",
            "PASSWORD": "supersecret",
        }

        # Validate loaded environment variables and keys
        self.assertEqual(self.env.env_vars, expected_env_vars)
        self.assertSetEqual(self.env.file_env_keys, {"BASE_URL", "API_KEY", "PASSWORD"})

    @patch("pathlib.Path.glob", return_value=[Path("test.env")])
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_export_to_file_after_load(
        self, mock_file, mock_is_file, mock_access, mock_glob
    ):
        """Test exporting environment variables to a file after loading from a file."""
        # Mock file content for "test.env"
        file_content = (
            "BASE_URL=https://example.com\nAPI_KEY=12345\nPASSWORD=supersecret\n"
        )

        # Load environment variables from a mock file
        with patch("builtins.open", mock_open(read_data=file_content)):
            self.env.load(files="test.env", overwrite_system=True)

        # Mock additional system environment variables
        system_vars = {"SYSTEM_VAR": "system_value"}
        with patch.dict("os.environ", system_vars, clear=False):
            # Update `env_vars` with system variables for this test case
            self.env.env_vars.update(system_vars)

            # Export to file (system and file-based variables included)
            self.env.export_to_file(file_path="output.env", include_system=True)

        # Verify file write content
        handle = mock_file()
        written_lines = [call.args[0].strip() for call in handle.write.call_args_list]

        # Expected lines to be written (include file-based vars and system vars)
        expected_lines = [
            "BASE_URL=https://example.com",
            "API_KEY=12345",
            "PASSWORD=supersecret",
            "SYSTEM_VAR=system_value",
        ]

        # Filter out any unrelated system environment variables from the written lines
        filtered_lines = [
            line
            for line in written_lines
            if line.split("=")[0] in {"BASE_URL", "API_KEY", "PASSWORD", "SYSTEM_VAR"}
        ]

        # Assert that each expected line is present in the filtered lines
        for line in expected_lines:
            self.assertIn(line, filtered_lines)

    @patch("builtins.print")
    def test_print_include_system_with_masking(self, mock_print):
        """Test printing both file-based and system environment variables with sensitive values masked."""
        # Simulate environment variables including system vars
        system_env_vars = {"SYSTEM_VAR": "system_value"}
        with patch.dict(self.env.env_vars, system_env_vars, clear=False):
            # Call print to display both file-based and system variables
            self.env.print(show_sensitive=False, include_system=True)

        # Ensure that system and file-based variables are printed
        printed_calls = [call.args[0] for call in mock_print.call_args_list]

        expected_calls = [
            "BASE_URL=https://example.com",
            "API_KEY=********",
            "PASSWORD=********",
            "SYSTEM_VAR=system_value",
        ]

        for expected_call in expected_calls:
            self.assertIn(expected_call, printed_calls)

    @patch("builtins.print")
    def test_print_include_system_show_sensitive(self, mock_print):
        """Test printing both file-based and system environment variables with sensitive values shown."""
        # Simulate environment variables including system vars
        system_env_vars = {"SYSTEM_VAR": "system_value"}
        with patch.dict(self.env.env_vars, system_env_vars, clear=False):
            # Call print to display both file-based and system variables
            self.env.print(show_sensitive=True, include_system=True)

        # Ensure that system and file-based variables are printed without masking
        printed_calls = [call.args[0] for call in mock_print.call_args_list]

        expected_calls = [
            "BASE_URL=https://example.com",
            "API_KEY=12345",
            "PASSWORD=supersecret",
            "SYSTEM_VAR=system_value",
        ]

        for expected_call in expected_calls:
            self.assertIn(expected_call, printed_calls)


if __name__ == "__main__":
    unittest.main()
