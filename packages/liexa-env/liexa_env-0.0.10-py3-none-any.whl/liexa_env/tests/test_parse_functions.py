import unittest
from liexa_env._env import Env


class TestParseLines(unittest.TestCase):

    def setUp(self):
        """Set up an instance of Env for testing."""
        self.env = Env()

    # Test simple key-value pairs
    def test_parse_lines_simple(self):
        """Test parsing of simple key-value pairs."""
        lines = [
            "KEY1=value1",
            "KEY2=value2",
        ]
        result = self.env._parse_lines(lines)
        expected = {"KEY1": "value1", "KEY2": "value2"}
        self.assertEqual(result, expected)

    # Test multiline key-value pairs
    def test_parse_lines_multiline(self):
        """Test parsing of multiline key-value pairs with triple quotes."""
        lines = [
            'KEY1="""',
            "This is a multiline",
            "value that spans",
            "multiple lines",
            '"""',
            "KEY2=value2",
        ]
        result = self.env._parse_lines(lines)
        expected = {
            "KEY1": "\nThis is a multiline\nvalue that spans\nmultiple lines\n",
            "KEY2": "value2",
        }
        self.assertEqual(result, expected)

    # Test handling comments and empty lines
    def test_parse_lines_comments_and_empty_lines(self):
        """Test that comments and empty lines are ignored."""
        lines = [
            "# This is a comment",
            "",
            "KEY1=value1",
            "",
            "# Another comment",
            "KEY2=value2",
        ]
        result = self.env._parse_lines(lines)
        expected = {"KEY1": "value1", "KEY2": "value2"}
        self.assertEqual(result, expected)

    # Test unclosed multiline error
    def test_parse_lines_unclosed_multiline(self):
        """Test that an error is raised for unclosed multiline values."""
        lines = [
            'KEY1="""',
            "This is a multiline",
            "value that is not closed",
        ]
        with self.assertRaises(ValueError) as context:
            self.env._parse_lines(lines)
        self.assertEqual(
            str(context.exception), "Unclosed multiline value for key 'KEY1'"
        )

    # Test invalid format (missing '=')
    def test_parse_lines_invalid_format(self):
        """Test that an error is raised for lines without '='."""
        lines = [
            "KEY1=value1",
            "This is an invalid line",
        ]
        with self.assertRaises(ValueError) as context:
            self.env._parse_lines(lines)
        self.assertEqual(
            str(context.exception), "Invalid format: 'This is an invalid line'"
        )

    # Test multiline starting and ending on the same line
    def test_parse_lines_multiline_single_line(self):
        """Test parsing of a multiline value that starts and ends on the same line."""
        lines = [
            'KEY1="""This is a multiline value"""',
            "KEY2=value2",
        ]
        result = self.env._parse_lines(lines)
        expected = {"KEY1": "This is a multiline value", "KEY2": "value2"}
        self.assertEqual(result, expected)

    # Test multiline value with some comments and empty lines in between
    def test_parse_lines_multiline_with_comments_and_empty_lines(self):
        """Test that multiline values include comments and empty lines in between."""
        lines = [
            'KEY1="""',
            "This is a multiline value",
            "# This is a comment inside multiline",
            '"""',
            "KEY2=value2",
        ]
        result = self.env._parse_lines(lines)
        expected = {
            "KEY1": "\nThis is a multiline value\n# This is a comment inside multiline\n",
            "KEY2": "value2",
        }
        self.assertEqual(result, expected)

    # Test keeping empty lines inside a multiline value
    def test_parse_lines_multiline_with_empty_lines(self):
        """Test that empty lines inside multiline values are preserved."""
        lines = [
            'KEY1="""',
            "This is a multiline value",
            "",
            "with empty lines",
            '"""',
            "KEY2=value2",
        ]
        result = self.env._parse_lines(lines)
        expected = {
            "KEY1": "\nThis is a multiline value\n\nwith empty lines\n",
            "KEY2": "value2",
        }
        self.assertEqual(result, expected)

    def test_parse_lines_duplicate_keys(self):
        """Test that duplicate keys override previous values."""
        lines = [
            "KEY1=value1",
            "KEY1=value2",  # Duplicate key with a new value
        ]
        result = self.env._parse_lines(lines)
        expected = {"KEY1": "value2"}  # The second value should override the first one
        self.assertEqual(result, expected)

    def test_parse_lines_value_without_key(self):
        """Test that a value without a key raises an error."""
        lines = [
            "=value1",  # No key, only value
        ]
        with self.assertRaises(ValueError) as context:
            self.env._parse_lines(lines)
        self.assertEqual(str(context.exception), "Key cannot be empty")

    def test_parse_lines_whitespace_only(self):
        """Test that lines with only whitespace are ignored."""
        lines = [
            "   ",  # Line with spaces only
            "\t",  # Line with a tab character
            "KEY1=value1",
        ]
        result = self.env._parse_lines(lines)
        expected = {"KEY1": "value1"}
        self.assertEqual(result, expected)

    def test_parse_lines_key_value_with_whitespace(self):
        """Test that leading and trailing whitespace in keys and values are trimmed."""
        lines = [
            "  KEY1  =  value1  ",  # Extra spaces around key and value
            "  KEY2  =  value2",
        ]
        result = self.env._parse_lines(lines)
        expected = {"KEY1": "value1", "KEY2": "value2"}  # Whitespace should be trimmed
        self.assertEqual(result, expected)

    def test_parse_lines_multiline_with_trailing_whitespace(self):
        """Test that trailing whitespace inside multiline values is preserved."""
        lines = [
            'KEY1="""',
            "This is a multiline value with trailing spaces    ",
            "   And some leading spaces on this line",
            '"""',
            "KEY2=value2",
        ]
        result = self.env._parse_lines(lines)
        expected = {
            "KEY1": "\nThis is a multiline value with trailing spaces    \n   And some leading spaces on this line\n",
            "KEY2": "value2",
        }
        self.assertEqual(result, expected)

    def test_parse_lines_missing_closing_triple_quote(self):
        """Test that a missing closing triple quote raises an error."""
        lines = [
            'KEY1="""This is an unclosed multiline value',
            "KEY2=value2",
        ]
        with self.assertRaises(ValueError) as context:
            self.env._parse_lines(lines)
        self.assertEqual(
            str(context.exception), "Unclosed multiline value for key 'KEY1'"
        )

    def test_parse_lines_empty_multiline_value(self):
        """Test that a multiline value with no content is parsed as an empty string."""
        lines = [
            'KEY1=""""""',
            "KEY2=value2",
        ]
        result = self.env._parse_lines(lines)
        expected = {"KEY1": "", "KEY2": "value2"}  # Should be an empty string
        self.assertEqual(result, expected)

    def test_parse_lines_empty_multiline_with_whitespace(self):
        """Test that an empty multiline value with only whitespace is parsed as empty."""
        lines = [
            'KEY1="""   """',  # Multiline with spaces only
            "KEY2=value2",
        ]
        result = self.env._parse_lines(lines)
        expected = {"KEY1": "   ", "KEY2": "value2"}  # Preserve the whitespace inside
        self.assertEqual(result, expected)

    def test_parse_lines_multiple_equals_in_value(self):
        """Test that values with multiple equals signs are parsed correctly."""
        lines = [
            "DB_CONNECTION_STRING=host=localhost;user=test;password=test==password",
        ]
        result = self.env._parse_lines(lines)
        expected = {
            "DB_CONNECTION_STRING": "host=localhost;user=test;password=test==password"
        }
        self.assertEqual(result, expected)

    def test_parse_lines_special_characters_in_keys(self):
        """Test that special characters in keys are handled correctly."""
        lines = [
            "KEY-1=value1",
            "SPECIAL@KEY=value_with_special@#$",
        ]
        result = self.env._parse_lines(lines)
        expected = {"KEY-1": "value1", "SPECIAL@KEY": "value_with_special@#$"}
        self.assertEqual(result, expected)

    def test_parse_lines_key_with_spaces(self):
        """Test that keys with spaces raise an error."""
        lines = [
            "KEY 1=value1",  # Invalid key with a space
        ]
        with self.assertRaises(ValueError) as context:
            self.env._parse_lines(lines)
        # Check if the error message contains the correct key and error message
        self.assertIn(
            "Invalid key format: 'KEY 1' contains spaces", str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
