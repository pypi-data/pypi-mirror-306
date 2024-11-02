import unittest
import json
from datetime import date, time, datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from liexa_env._env import Env


class TestEnvCastingFunctions(unittest.TestCase):

    def setUp(self):
        """Set up an instance of Env for testing."""
        self.env = Env()

    # Test as_int function
    def test_as_int(self):
        self.env.API_TIMEOUT = "30000"
        self.assertEqual(self.env.as_int("API_TIMEOUT"), 30000)

        # Test invalid int value
        self.env.INVALID_INT = "abc"
        with self.assertRaises(ValueError):
            self.env.as_int("INVALID_INT")

    # Test as_bool function
    def test_as_bool(self):
        self.env.DEBUG_MODE = "true"
        self.assertTrue(self.env.as_bool("DEBUG_MODE"))

        self.env.DEBUG_MODE = "false"
        self.assertFalse(self.env.as_bool("DEBUG_MODE"))

        self.env.DEBUG_MODE = "1"
        self.assertTrue(self.env.as_bool("DEBUG_MODE"))

        self.env.DEBUG_MODE = "0"
        self.assertFalse(self.env.as_bool("DEBUG_MODE"))

        # Test invalid boolean value
        self.env.INVALID_BOOL = "maybe"
        with self.assertRaises(ValueError):
            self.env.as_bool("INVALID_BOOL")

    # Test as_float function
    def test_as_float(self):
        self.env.API_VERSION = "1.5"
        self.assertEqual(self.env.as_float("API_VERSION"), 1.5)

        # Test invalid float value
        self.env.INVALID_FLOAT = "abc"
        with self.assertRaises(ValueError):
            self.env.as_float("INVALID_FLOAT")

    # Test as_json function
    def test_as_json(self):
        self.env.SETTINGS_JSON = '{"debug": true, "version": 1}'
        expected = {"debug": True, "version": 1}
        self.assertEqual(self.env.as_json("SETTINGS_JSON"), expected)

        # Test invalid JSON
        self.env.INVALID_JSON = "not a json"
        with self.assertRaises(json.JSONDecodeError):
            self.env.as_json("INVALID_JSON")

    # Test as_list function
    def test_as_list(self):
        self.env.ALLOWED_HOSTS = "localhost,127.0.0.1,localhost"
        expected = ["localhost", "127.0.0.1", "localhost"]
        self.assertEqual(self.env.as_list("ALLOWED_HOSTS"), expected)

        # Test empty value in list
        self.env.EMPTY_LIST = ""
        with self.assertRaises(ValueError):
            self.env.as_list("EMPTY_LIST")

    # Test as_set function
    def test_as_set(self):
        self.env.ALLOWED_HOSTS = "localhost,127.0.0.1,localhost"
        expected = {"localhost", "127.0.0.1"}
        self.assertEqual(self.env.as_set("ALLOWED_HOSTS"), expected)

        # Test empty value in set
        self.env.EMPTY_SET = ""
        with self.assertRaises(ValueError):
            self.env.as_set("EMPTY_SET")

    # Test as_dict function
    def test_as_dict(self):
        self.env.CONFIG_PAIRS = "debug=true,version=1.5,enabled=yes"
        expected = {"debug": "true", "version": "1.5", "enabled": "yes"}
        self.assertEqual(self.env.as_dict("CONFIG_PAIRS"), expected)

        # Test invalid dictionary format
        self.env.INVALID_DICT = "invalid"
        with self.assertRaises(ValueError):
            self.env.as_dict("INVALID_DICT")

        # Test empty dictionary
        self.env.EMPTY_DICT = ""
        with self.assertRaises(ValueError):
            self.env.as_dict("EMPTY_DICT")

    # Test non-existent environment variable
    def test_non_existent_variable(self):
        with self.assertRaises(AttributeError):
            self.env.as_int("NON_EXISTENT_VAR")

    # Test whitespace handling in as_int
    def test_as_int_with_whitespace(self):
        self.env.API_TIMEOUT = "  30000  "
        self.assertEqual(self.env.as_int("API_TIMEOUT"), 30000)

    # Test whitespace handling in as_list
    def test_as_list_with_whitespace(self):
        self.env.ALLOWED_HOSTS = " localhost , 127.0.0.1 ,  "
        expected = ["localhost", "127.0.0.1"]
        self.assertEqual(self.env.as_list("ALLOWED_HOSTS"), expected)

    # Test delimiter handling in as_list
    def test_as_list_with_custom_delimiter(self):
        self.env.ALLOWED_HOSTS = "localhost|127.0.0.1|localhost"
        expected = ["localhost", "127.0.0.1", "localhost"]
        self.assertEqual(self.env.as_list("ALLOWED_HOSTS", delimiter="|"), expected)

    # Test as_json with mixed data types
    def test_as_json_with_mixed_data(self):
        self.env.SETTINGS_JSON = (
            '{"key1": 1, "key2": "value", "key3": true, "key4": null}'
        )
        expected = {"key1": 1, "key2": "value", "key3": True, "key4": None}
        self.assertEqual(self.env.as_json("SETTINGS_JSON"), expected)

    # Test invalid as_json (missing brackets)
    def test_as_json_invalid(self):
        self.env.INVALID_JSON = '{"key1": 1, "key2": "value"'
        with self.assertRaises(json.JSONDecodeError):
            self.env.as_json("INVALID_JSON")

    # Test as_bool with mixed-case strings
    def test_as_bool_with_mixed_case(self):
        self.env.FLAG = "True"
        self.assertTrue(self.env.as_bool("FLAG"))

        self.env.FLAG = "False"
        self.assertFalse(self.env.as_bool("FLAG"))

    # Test as_bool with unexpected values
    def test_as_bool_unexpected_values(self):
        self.env.FLAG = "on"
        self.assertTrue(self.env.as_bool("FLAG"))

        self.env.FLAG = "off"
        self.assertFalse(self.env.as_bool("FLAG"))

        # Invalid boolean string
        self.env.FLAG = "notabool"
        with self.assertRaises(ValueError):
            self.env.as_bool("FLAG")

    # Test as_dict with custom delimiters
    def test_as_dict_with_custom_delimiters(self):
        self.env.CONFIG_PAIRS = "debug:true|version:1.5|enabled:yes"
        expected = {"debug": "true", "version": "1.5", "enabled": "yes"}
        self.assertEqual(
            self.env.as_dict("CONFIG_PAIRS", pair_delimiter="|", kv_delimiter=":"),
            expected,
        )

    # Test as_list with empty values and only delimiters
    def test_as_list_empty_values(self):
        # Expecting a ValueError for invalid/empty list input
        self.env.EMPTY_LIST = ",,,"
        with self.assertRaises(ValueError):
            self.env.as_list("EMPTY_LIST")

        # Expecting a ValueError for a single delimiter with no values
        self.env.SINGLE_COMMA = ","
        with self.assertRaises(ValueError):
            self.env.as_list("SINGLE_COMMA")

            # Invalid date format
        self.env.INVALID_DATE = "25-10-2023"
        with self.assertRaises(ValueError):
            self.env.as_date("INVALID_DATE")

        # Custom date format
        self.env.CUSTOM_DATE = "25-10-2023"
        self.assertEqual(
            self.env.as_date("CUSTOM_DATE", date_format="%d-%m-%Y"), date(2023, 10, 25)
        )

    # Test as_time function
    def test_as_time(self):
        # Valid time
        self.env.CRON_TIME = "14:30:00"
        self.assertEqual(self.env.as_time("CRON_TIME"), time(14, 30, 0))

        # Invalid time format
        self.env.INVALID_TIME = "2 PM"
        with self.assertRaises(ValueError):
            self.env.as_time("INVALID_TIME")

        # Custom time format
        self.env.CUSTOM_TIME = "02:30 PM"
        self.assertEqual(
            self.env.as_time("CUSTOM_TIME", time_format="%I:%M %p"), time(14, 30)
        )

    # Test as_datetime function
    def test_as_datetime(self):
        # Valid datetime
        self.env.EVENT_TIMESTAMP = "2023-10-25 14:30:00"
        self.assertEqual(
            self.env.as_datetime("EVENT_TIMESTAMP"), datetime(2023, 10, 25, 14, 30, 0)
        )

        # Invalid datetime format
        self.env.INVALID_TIMESTAMP = "2023/10/25 14:30"
        with self.assertRaises(ValueError):
            self.env.as_datetime("INVALID_TIMESTAMP")

        # Custom datetime format
        self.env.CUSTOM_TIMESTAMP = "25-10-2023 02:30 PM"
        self.assertEqual(
            self.env.as_datetime(
                "CUSTOM_TIMESTAMP", datetime_format="%d-%m-%Y %I:%M %p"
            ),
            datetime(2023, 10, 25, 14, 30),
        )

    # Test handling of None values in date/time
    def test_as_date_none_value(self):
        self.env.NONE_DATE = "null"
        self.assertIsNone(self.env.as_date("NONE_DATE", date_format="null"))

    def test_as_time_none_value(self):
        self.env.NONE_TIME = "null"
        self.assertIsNone(self.env.as_time("NONE_TIME", time_format="null"))

    def test_as_datetime_none_value(self):
        self.env.NONE_DATETIME = "null"
        self.assertIsNone(self.env.as_datetime("NONE_DATETIME", datetime_format="null"))


if __name__ == "__main__":
    unittest.main()
