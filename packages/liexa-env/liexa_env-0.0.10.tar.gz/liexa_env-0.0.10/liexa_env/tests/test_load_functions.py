import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from liexa_env._env import Env
import os


class TestEnv(unittest.TestCase):

    def setUp(self):
        """Set up an instance of Env for testing."""
        self.env = Env()

    # Tests for _file_names_valid
    def test_file_names_valid_empty_list(self):
        """Test _file_names_valid raises ValueError for empty list."""
        with self.assertRaises(ValueError):
            self.env._file_names_valid([])

    def test_file_names_valid_empty_string(self):
        """Test _file_names_valid raises ValueError for empty string in list."""
        with self.assertRaises(ValueError):
            self.env._file_names_valid(["file1.txt", ""])

    def test_file_names_valid_valid_names(self):
        """Test _file_names_valid with valid file names."""
        try:
            self.env._file_names_valid(["file1.txt", "file2.txt"])
        except ValueError:
            self.fail("_file_names_valid raised ValueError unexpectedly")

    # Tests for _files_exist_and_readable
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    def test_files_exist_and_readable_valid(self, mock_is_file, mock_access):
        """Test _files_exist_and_readable when files exist and are readable."""
        try:
            self.env._files_exist_and_readable(["file1.txt"])
        except (FileNotFoundError, PermissionError):
            self.fail("_files_exist_and_readable raised an error unexpectedly")

    @patch("os.access", return_value=False)
    @patch("pathlib.Path.is_file", return_value=True)
    def test_files_exist_and_readable_permission_error(self, mock_is_file, mock_access):
        """Test _files_exist_and_readable raises PermissionError when file isn't readable."""
        with self.assertRaises(PermissionError):
            self.env._files_exist_and_readable(["file1.txt"])

    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=False)
    def test_files_exist_and_readable_file_not_found(self, mock_is_file, mock_access):
        """Test _files_exist_and_readable raises FileNotFoundError when file doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            self.env._files_exist_and_readable(["file1.txt"])

    # Tests for _read_files
    @patch(
        "builtins.open", new_callable=mock_open, read_data="KEY1=value1\nKEY2=value2"
    )
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    def test_read_files_valid(self, mock_is_file, mock_access, mock_open_func):
        """Test _read_files reads files correctly."""
        files = ["file1.txt"]
        result = self.env._read_files(files)
        self.assertEqual(result, ["KEY1=value1", "KEY2=value2"])

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    def test_read_files_error_handling(self, mock_is_file, mock_access, mock_open_func):
        """Test _read_files raises IOError when file read fails."""
        mock_open_func.side_effect = OSError("File read error")
        files = ["file1.txt"]

        with self.assertRaises(IOError) as context:
            self.env._read_files(files)

        self.assertEqual(
            str(context.exception), "Error reading file file1.txt: File read error"
        )

    @patch("pathlib.Path.glob", return_value=[Path("file1.txt")])
    @patch("builtins.open", new_callable=mock_open, read_data="KEY1=value1")
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    def test_load_valid(self, mock_is_file, mock_access, mock_open_func, mock_glob):
        """Test load method with valid files."""
        try:
            self.env.load(["file1.txt"])
        except Exception as e:
            self.fail(f"load raised an error unexpectedly: {e}")

    def test_load_invalid_type(self):
        """Test load raises ValueError for invalid input type."""
        with self.assertRaises(ValueError):
            self.env.load(123)  # Not a string or list of strings

        with self.assertRaises(ValueError):
            self.env.load([123, "file.txt"])  # List contains non-string item

    @patch("pathlib.Path.glob", return_value=[Path("file1.txt"), Path("file2.txt")])
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_load_multiple_files(
        self, mock_open_func, mock_is_file, mock_access, mock_glob
    ):
        """Test load method with multiple valid files."""

        # Define file-specific content
        mock_files = {"file1.txt": "KEY1=value1", "file2.txt": "KEY2=value2"}

        # Custom side effect function to simulate reading from specific files
        def open_side_effect(file, *args, **kwargs):
            filename = Path(file).name  # Extract just the filename
            if filename in mock_files:
                return mock_open(read_data=mock_files[filename]).return_value
            raise FileNotFoundError(f"File {filename} not found")

        mock_open_func.side_effect = open_side_effect

        # Run the load method with both files
        self.env.load(["file1.txt", "file2.txt"])

        # Verify that both environment variables were correctly loaded
        self.assertEqual(self.env.env_vars.get("KEY1"), "value1")
        self.assertEqual(self.env.env_vars.get("KEY2"), "value2")

    @patch("pathlib.Path.glob", return_value=[Path("file1.txt")])
    @patch.dict(os.environ, {"KEY1": "system_value1"}, clear=True)
    @patch("builtins.open", new_callable=mock_open, read_data="KEY1=file_value1")
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    def test_load_overwrite_system(
        self, mock_is_file, mock_access, mock_open_func, mock_glob
    ):
        """Test load method with overwrite_system=True."""
        self.env.load(["file1.txt"], overwrite_system=True)

        # Ensure that the system variable was overwritten
        self.assertEqual(self.env.env_vars["KEY1"], "file_value1")
        self.assertEqual(os.environ["KEY1"], "file_value1")

    @patch("pathlib.Path.glob", return_value=[Path("file1.txt")])
    @patch.dict(os.environ, {"KEY1": "system_value1"}, clear=True)
    @patch("builtins.open", new_callable=mock_open, read_data="KEY1=file_value1")
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    def test_load_no_overwrite_system(
        self, mock_is_file, mock_access, mock_open_func, mock_glob
    ):
        """Test load method with overwrite_system=False."""
        # Call the load method with overwrite_system set to False
        self.env.load(["file1.txt"], overwrite_system=False)

        # Ensure that the system variable was not overwritten by the file value
        self.assertEqual(self.env.env_vars["KEY1"], "system_value1")
        self.assertEqual(os.environ["KEY1"], "system_value1")

    @patch("pathlib.Path.glob", return_value=[Path("file1.txt")])
    @patch("builtins.open", new_callable=mock_open, read_data="INVALID_LINE")
    @patch("os.access", return_value=True)
    @patch("pathlib.Path.is_file", return_value=True)
    def test_load_invalid_file_format(
        self, mock_is_file, mock_access, mock_open_func, mock_glob
    ):
        """Test load method raises an error for invalid file format."""
        with self.assertRaises(ValueError) as context:
            self.env.load(["file1.txt"])

        self.assertIn("Invalid format", str(context.exception))


if __name__ == "__main__":
    unittest.main()
