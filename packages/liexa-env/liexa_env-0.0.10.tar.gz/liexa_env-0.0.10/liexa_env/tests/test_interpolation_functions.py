import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from liexa_env._env import Env
import os


class TestInterpolation(unittest.TestCase):

    def setUp(self):
        """Set up an instance of Env for testing."""
        self.env = Env()

    # Test simple interpolation of variables
    def test_interpolation_simple(self):
        """Test simple variable interpolation."""
        lines = ["BASE_URL=https://example.com", "API_URL=${BASE_URL}/api"]
        self.env.env_vars = self.env._parse_lines(lines)
        for key in self.env.env_vars:
            self.env.env_vars[key] = self.env._interpolate_value(
                self.env.env_vars[key], self.env.env_vars
            )

        expected = {
            "BASE_URL": "https://example.com",
            "API_URL": "https://example.com/api",
        }
        self.assertEqual(self.env.env_vars, expected)

    # Test nested interpolation (one variable references another with interpolation)
    def test_interpolation_nested(self):
        """Test nested variable interpolation."""
        lines = [
            "BASE_URL=https://example.com",
            "API_VERSION=v1",
            "FULL_API_URL=${BASE_URL}/api/${API_VERSION}",
        ]
        self.env.env_vars = self.env._parse_lines(lines)
        for key in self.env.env_vars:
            self.env.env_vars[key] = self.env._interpolate_value(
                self.env.env_vars[key], self.env.env_vars
            )

        expected = {
            "BASE_URL": "https://example.com",
            "API_VERSION": "v1",
            "FULL_API_URL": "https://example.com/api/v1",
        }
        self.assertEqual(self.env.env_vars, expected)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="BASE_URL=https://example.com\n",
    )
    def test_interpolation_multiple_files(self, mock_file):
        """Test interpolation across multiple files."""
        # Clear any existing environment variables
        self.env.env_vars.clear()

        # Simulate reading from two separate files with dependencies
        lines_file_1 = ["BASE_URL=https://example.com"]
        lines_file_2 = ["API_KEY=12345", "API_URL=${BASE_URL}/api?key=${API_KEY}"]

        # Update env_vars with parsed lines
        self.env.env_vars.update(self.env._parse_lines(lines_file_1))
        self.env.env_vars.update(self.env._parse_lines(lines_file_2))

        # Interpolate values
        for key in self.env.env_vars:
            self.env.env_vars[key] = self.env._interpolate_value(
                self.env.env_vars[key], self.env.env_vars
            )

        # Expected result after interpolation
        expected = {
            "BASE_URL": "https://example.com",
            "API_KEY": "12345",
            "API_URL": "https://example.com/api?key=12345",
        }

        # Check if the interpolated values match the expected output
        self.assertEqual(self.env.env_vars, expected)

    # Test escaping interpolation using \${}
    def test_interpolation_escaped(self):
        r"""Test escaping interpolation using \${}."""
        lines = ["BASE_URL=https://example.com", "API_URL=\\${BASE_URL}/api"]
        self.env.env_vars = self.env._parse_lines(lines)
        for key in self.env.env_vars:
            self.env.env_vars[key] = self.env._interpolate_value(
                self.env.env_vars[key], self.env.env_vars
            )

        expected = {
            "BASE_URL": "https://example.com",
            "API_URL": "${BASE_URL}/api",  # This is expected to be a literal string
        }
        self.assertEqual(self.env.env_vars, expected)

    # Test missing variable in interpolation
    def test_interpolation_missing_variable(self):
        """Test that interpolation raises an error for a missing variable."""
        lines = ["API_URL=https://example.com/api/${MISSING_VAR}"]
        self.env.env_vars = self.env._parse_lines(lines)

        with self.assertRaises(ValueError) as context:
            for key in self.env.env_vars:
                self.env.env_vars[key] = self.env._interpolate_value(
                    self.env.env_vars[key], self.env.env_vars
                )

        self.assertEqual(
            str(context.exception), "Variable 'MISSING_VAR' is not defined."
        )

    # Test multiline values that include interpolations
    def test_interpolation_multiline(self):
        """Test interpolation within multiline values."""
        lines = [
            'MULTILINE="""This is a multiline value',
            'with an interpolated value: ${BASE_URL}"""',
            "BASE_URL=https://example.com",
        ]
        self.env.env_vars = self.env._parse_lines(lines)
        for key in self.env.env_vars:
            self.env.env_vars[key] = self.env._interpolate_value(
                self.env.env_vars[key], self.env.env_vars
            )

        expected = {
            "MULTILINE": "This is a multiline value\nwith an interpolated value: https://example.com",
            "BASE_URL": "https://example.com",
        }
        self.assertEqual(self.env.env_vars, expected)

        # Test direct circular reference

    def test_interpolation_direct_circular_reference(self):
        """Test that direct circular references raise an error."""
        lines = ["VAR1=${VAR1}"]
        self.env.env_vars = self.env._parse_lines(lines)

        with self.assertRaises(ValueError) as context:
            for key in self.env.env_vars:
                self.env.env_vars[key] = self.env._interpolate_value(
                    self.env.env_vars[key], self.env.env_vars
                )

        self.assertIn("Circular reference detected", str(context.exception))

    # Test indirect circular reference (VAR1 -> VAR2 -> VAR3 -> VAR1)
    def test_interpolation_indirect_circular_reference(self):
        """Test that indirect circular references raise an error."""
        lines = ["VAR1=${VAR2}", "VAR2=${VAR3}", "VAR3=${VAR1}"]
        self.env.env_vars = self.env._parse_lines(lines)

        with self.assertRaises(ValueError) as context:
            for key in self.env.env_vars:
                self.env.env_vars[key] = self.env._interpolate_value(
                    self.env.env_vars[key], self.env.env_vars
                )

        self.assertIn("Circular reference detected", str(context.exception))

    # Test more complex circular reference (VAR1 -> VAR2 -> VAR3 -> VAR4 -> VAR1)
    def test_interpolation_complex_circular_reference(self):
        """Test that more complex circular references raise an error."""
        lines = ["VAR1=${VAR2}", "VAR2=${VAR3}", "VAR3=${VAR4}", "VAR4=${VAR1}"]
        self.env.env_vars = self.env._parse_lines(lines)

        with self.assertRaises(ValueError) as context:
            for key in self.env.env_vars:
                self.env.env_vars[key] = self.env._interpolate_value(
                    self.env.env_vars[key], self.env.env_vars
                )

        self.assertIn("Circular reference detected", str(context.exception))

        # Test interpolation where a variable is empty

    def test_interpolation_empty_value(self):
        """Test interpolation where a variable is set to an empty value."""
        lines = ["BASE_URL=", "API_URL=${BASE_URL}/api"]
        self.env.env_vars = self.env._parse_lines(lines)
        for key in self.env.env_vars:
            self.env.env_vars[key] = self.env._interpolate_value(
                self.env.env_vars[key], self.env.env_vars
            )

        expected = {
            "BASE_URL": "",
            "API_URL": "/api",  # Empty BASE_URL results in just "/api"
        }
        self.assertEqual(self.env.env_vars, expected)

        # Test interpolation with system environment variables

    @patch.dict(os.environ, {"HOME": "/home/user"})
    def test_interpolation_system_variable(self):
        """Test interpolation with system environment variables."""
        lines = ["USER_HOME=${SYS:HOME}/myapp"]
        self.env.env_vars = self.env._parse_lines(lines)
        for key in self.env.env_vars:
            self.env.env_vars[key] = self.env._interpolate_value(
                self.env.env_vars[key], self.env.env_vars
            )

        expected = {"USER_HOME": "/home/user/myapp"}
        self.assertEqual(self.env.env_vars, expected)

        # Test no interpolation for non-matching patterns

    def test_interpolation_no_pattern(self):
        """Test when no interpolation patterns exist."""
        lines = ["BASE_URL=https://example.com", "API_URL=https://another-url.com/api"]
        self.env.env_vars = self.env._parse_lines(lines)
        for key in self.env.env_vars:
            self.env.env_vars[key] = self.env._interpolate_value(
                self.env.env_vars[key], self.env.env_vars
            )

        expected = {
            "BASE_URL": "https://example.com",
            "API_URL": "https://another-url.com/api",  # No interpolation needed
        }
        self.assertEqual(self.env.env_vars, expected)

    def test_interpolation_partially_missing_variables(self):
        """Test that interpolation partially succeeds when some variables are missing."""
        lines = [
            "BASE_URL=https://example.com",
            "API_URL=${BASE_URL}/api/${MISSING_VAR}",
        ]
        self.env.env_vars = self.env._parse_lines(lines)

        with self.assertRaises(ValueError) as context:
            for key in self.env.env_vars:
                self.env.env_vars[key] = self.env._interpolate_value(
                    self.env.env_vars[key], self.env.env_vars
                )

        self.assertIn("Variable 'MISSING_VAR' is not defined.", str(context.exception))

    def test_interpolation_non_existing_system_variable(self):
        """Test that interpolation raises an error for non-existing system variables."""
        lines = ["USER_HOME=${SYS:NON_EXISTENT_VAR}"]
        self.env.env_vars = self.env._parse_lines(lines)

        with self.assertRaises(ValueError) as context:
            for key in self.env.env_vars:
                self.env.env_vars[key] = self.env._interpolate_value(
                    self.env.env_vars[key], self.env.env_vars
                )

        self.assertIn(
            "System variable 'NON_EXISTENT_VAR' is not defined", str(context.exception)
        )

    def test_interpolation_empty_pattern(self):
        """Test that an empty interpolation pattern raises an error with context."""
        lines = ["API_URL=https://example.com/api/${}"]
        self.env.env_vars = self.env._parse_lines(lines)

        with self.assertRaises(ValueError) as context:
            for key in self.env.env_vars:
                self.env.env_vars[key] = self.env._interpolate_value(
                    self.env.env_vars[key], self.env.env_vars
                )

        # Check if the error message includes the expected message with the escaped '${}' pattern
        self.assertIn("Invalid empty interpolation pattern.", str(context.exception))


if __name__ == "__main__":
    unittest.main()
