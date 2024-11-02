import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from liexa_env._env import Env
import os


class TestEnvLoading(unittest.TestCase):

    def setUp(self):
        """Set up an instance of Env for testing."""
        self.env = Env()

    @patch("pathlib.Path.glob", return_value=[Path(".env.production")])
    @patch("os.getenv", return_value="production")
    @patch("builtins.open", new_callable=mock_open, read_data="API_KEY=prod_key\n")
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    @patch(
        "pathlib.Path.is_dir", return_value=True
    )  # Mock is_dir to avoid directory check errors
    def test_auto_load_environment_with_env(
        self,
        mock_is_dir,
        mock_is_file,
        mock_access,
        mock_open_func,
        mock_getenv,
        mock_glob,
    ):
        """Test _auto_load_environment when ENV is set."""
        # Run auto-load to simulate environment variable-based loading
        self.env._auto_load_environment()

        # Verify that the variable from the file was loaded
        self.assertEqual(self.env.env_vars.get("API_KEY"), "prod_key")

    @patch("pathlib.Path.glob", return_value=[Path(".env")])
    @patch("os.getenv", return_value=None)
    @patch("builtins.open", new_callable=mock_open, read_data="API_KEY=default_key\n")
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    @patch(
        "pathlib.Path.is_dir", return_value=True
    )  # Mock is_dir to avoid directory check errors
    def test_auto_load_environment_without_env(
        self,
        mock_is_dir,
        mock_is_file,
        mock_access,
        mock_open_func,
        mock_getenv,
        mock_glob,
    ):
        """Test _auto_load_environment when ENV is not set and a single default .env file exists."""
        # Run auto-load to simulate default environment loading
        self.env._auto_load_environment()

        # Verify that the default .env variable was loaded
        self.assertEqual(self.env.env_vars.get("API_KEY"), "default_key")

    @patch("pathlib.Path.glob", return_value=[Path("test.env")])
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    @patch(
        "pathlib.Path.is_dir", return_value=True
    )  # Mock is_dir to avoid directory check errors
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="BASE_URL=https://example.com\nAPI_KEY=12345\nPASSWORD=supersecret\n",
    )
    @patch.dict(os.environ, {}, clear=True)
    def test_load_file_based(
        self, mock_file, mock_is_file, mock_access, mock_is_dir, mock_glob
    ):
        """Test loading file-based environment variables."""
        # Clear any previous data to isolate test
        self.env.env_vars.clear()
        self.env.file_env_keys.clear()

        # Load environment variables from a mock file
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
    @patch(
        "pathlib.Path.is_dir", return_value=True
    )  # Mock is_dir to avoid directory check errors
    def test_get_matching_env_files(
        self, mock_is_dir, mock_is_file, mock_access, mock_glob
    ):
        """Test _get_matching_env_files to ensure file matching logic works."""
        directory = "/fake/directory"
        pattern = "test.env"

        # Invoke _get_matching_env_files
        matching_files = self.env._get_matching_env_files(directory, pattern)

        # Assert that the correct mock file was returned
        self.assertEqual(matching_files, [Path("test.env")])

    @patch("pathlib.Path.glob", return_value=[])
    @patch(
        "pathlib.Path.is_dir", return_value=True
    )  # Mock is_dir to avoid directory check errors
    def test_no_matching_env_files(self, mock_is_dir, mock_glob):
        """Test _get_matching_env_files when no files match the pattern."""
        directory = "/fake/directory"
        pattern = "nonexistent.env"

        # Invoke _get_matching_env_files and expect an empty list
        matching_files = self.env._get_matching_env_files(directory, pattern)
        self.assertEqual(matching_files, [])


if __name__ == "__main__":
    unittest.main()
