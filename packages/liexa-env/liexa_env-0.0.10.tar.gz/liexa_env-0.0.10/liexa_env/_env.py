import os
from typing import Union, List
import sys
from pathlib import Path
import re
import json
from datetime import datetime, date, time


class Env:

    def __init__(self) -> None:
        """Initialize the Env class."""
        self.file_env_keys = (
            set()
        )  # To store the keys of environment variables from files
        self.env_vars = {}  # Dictionary to store environment variables
        self.INTERPOLATION_PATTERN = re.compile(
            r"\\?\$\{([^:}]*)?(?::([^}]+))?\}"
        )  # Matches ${VAR_NAME} and ${SYS:VAR_NAME}

        self._auto_load_environment()

    def __getattr__(self, var_name: str) -> str:
        """
        Dynamically access environment variables using env.VARNAME syntax.

        Args:
            var_name (str): The name of the environment variable to retrieve.

        Returns:
            str: The value of the environment variable.

        Raises:
            AttributeError: If the environment variable is not found in the loaded or system environment variables.
        """
        # First, try to get the variable from the loaded environment variables
        if var_name in self.env_vars:
            return self.env_vars[var_name]

        # If the variable is not found, raise an AttributeError with a debug message
        raise AttributeError(f"Environment variable '{var_name}' can't be found.")

    def __setattr__(self, var_name: str, value: any) -> None:
        """
        Dynamically set environment variables using env.VARNAME = "value" syntax.
        Automatically create new environment variables if they don't exist.

        Args:
            var_name (str): The name of the environment variable to set.
            value (any): The value of the environment variable.
        """

        value_str = str(value)  # Ensure the value is converted to a string

        # Prevent recursion when setting internal attributes
        if var_name in self.__dict__ or var_name in (
            "file_env_keys",
            "env_vars",
            "INTERPOLATION_PATTERN",
        ):
            super().__setattr__(var_name, value)
        else:
            # Set the variable in the loaded environment variables
            self.env_vars[var_name] = value_str

            # Also update the system environment variables
            os.environ[var_name] = value_str

    def _file_names_valid(self, files: List[str]) -> None:
        """
        Validate that the provided list of file names is not empty and does not contain invalid entries.

        Args:
            files (List[str]): List of file names to validate.

        Raises:
            ValueError: If the list is empty or contains an empty string.
        """
        if not files:
            raise ValueError("Empty list isn't a valid input for file names")
        for file in files:
            if not file.strip():
                raise ValueError("Empty string isn't a valid input for file names")

    def _files_exist_and_readable(self, files: List[str]) -> None:
        """
        Check if the specified files exist and are readable. If not, appropriate exceptions are raised.

        Args:
            files (List[str]): List of file names to check for existence and readability.

        Raises:
            FileNotFoundError: If any file does not exist.
            PermissionError: If any file cannot be read due to permission issues.
        """
        file_exist_error = []
        file_read_error = []
        entry_point = Path(
            sys.argv[0]
        ).parent  # Get the directory where the script is located

        for file in files:
            file_path = entry_point / file

            if not Path.is_file(file_path):
                file_exist_error.append(file)

            if not os.access(file_path, os.R_OK):
                file_read_error.append(file)

        if file_exist_error:
            raise FileNotFoundError(f"Files that do not exist: {file_exist_error}")

        if file_read_error:
            raise PermissionError(
                f"Files that cannot be read due to permission issues: {file_read_error}"
            )

    def _read_files(self, files: List[str]) -> List[str]:
        """Read and parse specified files, converting them to environment variable lines."""
        all_lines = []
        for file in files:
            path = Path(file)
            try:
                if path.suffix == ".json":
                    all_lines.extend(self._parse_json_to_lines(path))
                elif path.suffix in {".yaml", ".yml"}:
                    json_data = self._yaml_to_dict(path)
                    all_lines.extend(self._convert_dict_to_env_lines(json_data))
                else:
                    with open(path, "r") as f:
                        all_lines.extend(f.read().splitlines())
            except OSError as e:
                raise IOError(f"Error reading file {file}: {e}") from e
        return all_lines

    def _yaml_to_dict(self, filename: str) -> dict:
        """Parse a YAML file and convert it to a JSON-compatible dictionary."""

        def parse_block(start_index, current_indent, is_list=False):
            items = [] if is_list else {}
            index = start_index
            while index < len(lines):
                line = lines[index].rstrip("\n")
                if not line.strip() or line.strip().startswith("#"):
                    index += 1
                    continue
                stripped_line = line.lstrip(" ")
                indent = len(line) - len(stripped_line)
                if indent < current_indent:
                    break

                if is_list and not stripped_line.startswith("- "):
                    break
                elif is_list and stripped_line.startswith("- "):
                    item_line = stripped_line[2:].strip()
                    if ":" in item_line or item_line == "":
                        item_data = {}
                        if ":" in item_line:
                            key, value = map(str.strip, item_line.split(":", 1))
                            if value == "":
                                index += 1
                                nested_data, index = parse_block(index, indent + 2)
                                item_data[key] = nested_data
                            else:
                                item_data[key] = (
                                    "" if value.lower() == "null" else str(value)
                                )
                            index += 1
                        else:
                            index += 1
                        nested_data, index = parse_block(index, indent + 1)
                        item_data.update(nested_data)
                        items.append(item_data)
                    else:
                        items.append(
                            "" if item_line.lower() == "null" else str(item_line)
                        )
                        index += 1
                elif ":" in stripped_line:
                    key_value = stripped_line.split(":", 1)
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    if value == "":
                        index += 1
                        if index < len(lines) and lines[index].lstrip(" ").startswith(
                            "- "
                        ):
                            nested_data, index = parse_block(
                                index, indent + 1, is_list=True
                            )
                        else:
                            nested_data, index = parse_block(index, indent + 1)
                        items[key] = nested_data
                    else:
                        items[key] = "" if value.lower() == "null" else str(value)
                        index += 1
                else:
                    index += 1
            return (items, index) if is_list else (items, index)

        with open(filename, "r") as file:
            global lines
            lines = file.readlines()
        parsed_data, _ = parse_block(0, 0)
        return parsed_data

    def _convert_dict_to_env_lines(self, data: dict) -> List[str]:
        """Convert a dictionary to lines of KEY=value format for environment variables."""
        flattened_data = self._flatten_data(data)
        return [f"{key}={value}" for key, value in flattened_data.items()]

    def _parse_json_to_lines(self, file_path: Path) -> List[str]:
        """Parse JSON file and convert it to KEY=value lines."""
        with open(file_path, "r") as f:
            json_data = json.load(f)
        return self._convert_dict_to_env_lines(json_data)

    def _flatten_data(self, data: any, parent_key: str = "") -> dict[str, str]:
        """Flatten a nested dictionary into a flat dictionary with KEY=value format."""
        items = {}
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f"{parent_key}_{k}".upper() if parent_key else k.upper()
                items.update(self._flatten_data(v, new_key))
        elif isinstance(data, list):
            items[parent_key] = json.dumps(data)
        else:
            items[parent_key] = "" if data is None else str(data)
        return items

    def _parse_lines(self, all_lines: List[str]) -> dict:
        """Parse lines of environment variables, handling single-line and multiline values."""
        env_dict = {}
        current_key = None
        current_value = []
        in_multiline_value = False

        for line in all_lines:
            if in_multiline_value:
                if '"""' in line:
                    current_value.append(line.split('"""')[0])
                    env_dict[current_key] = "\n".join(current_value)
                    current_key = None
                    current_value = []
                    in_multiline_value = False
                else:
                    current_value.append(line)
                continue

            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = map(str.strip, line.split("=", 1))

                if " " in key:
                    raise ValueError(f"Invalid key format: '{key}' contains spaces")
                if not key:
                    raise ValueError("Key cannot be empty")

                if value.startswith('"""'):
                    current_key = key
                    value = value[3:]
                    if '"""' in value:
                        env_dict[current_key] = value.split('"""')[0]
                        current_key = None
                    else:
                        current_value.append(value)
                        in_multiline_value = True
                else:
                    env_dict[key] = value
            else:
                raise ValueError(f"Invalid format: '{line}'")

        if in_multiline_value:
            raise ValueError(f"Unclosed multiline value for key '{current_key}'")

        return env_dict

    def _interpolate_value(
        self, value: str, env_dict: dict, seen_vars: set = None
    ) -> str:
        r"""
        Interpolate environment variables using ${} syntax in the provided value.
        Supports escaping with \${} to avoid interpolation. System variables can be referenced using ${SYS:VAR_NAME}.

        Args:
            value (str): The value that may contain interpolation patterns.
            env_dict (dict): The dictionary of all environment variables from the .env file.
            seen_vars (set): A set of variables currently being interpolated to detect circular references.

        Returns:
            str: The interpolated value.

        Raises:
            ValueError: If a referenced variable is not defined or if a circular reference is detected.
        """
        if seen_vars is None:
            seen_vars = set()  # Initialize the set if not provided

        def replace_match(match):
            if match.group(0).startswith("\\"):
                # Handle escaped interpolation
                return f"${{{match.group(1)}}}"

            # Get the variable name
            var_type = match.group(1)
            var_name = match.group(2) if match.group(2) else match.group(1)

            if not var_name.strip():
                raise ValueError("Invalid empty interpolation pattern.")

            # Detect circular reference (either direct or indirect)
            if var_name in seen_vars:
                raise ValueError(
                    f"Circular reference detected involving variable '{var_name}'"
                )

            # Add the variable to the seen set
            seen_vars.add(var_name)

            # If the pattern is ${SYS:VAR_NAME}, look only in system environment variables
            if var_type == "SYS":
                if var_name not in os.environ:
                    raise ValueError(f"System variable '{var_name}' is not defined.")
                result = os.environ[var_name]  # Use system environment variable
            else:
                # Otherwise, fallback to the env_dict for file-based vars
                if var_name not in env_dict:
                    raise ValueError(f"Variable '{var_name}' is not defined.")

                # Recursively interpolate the value, passing the seen_vars set
                result = self._interpolate_value(
                    env_dict[var_name], env_dict, seen_vars
                )

            # Remove the variable from the seen set after successful interpolation
            seen_vars.remove(var_name)

            return result

        # Replace all patterns in the value
        return self.INTERPOLATION_PATTERN.sub(replace_match, value)

    def _auto_load_environment(self):
        """Auto-load environment variables with fallback logic."""
        app_env = os.getenv("ENV")

        entry_point = Path(sys.argv[0]).parent

        if app_env:
            files = self._get_matching_env_files(entry_point, f".env.{app_env}*")
            if files:
                self.load([str(file) for file in files], overwrite_system=True)
        else:
            default_env_files = self._get_matching_env_files(entry_point, ".env*")

            if len(default_env_files) == 1:
                self.load(str(default_env_files[0]), overwrite_system=True)

    def _get_matching_env_files(self, directory: str, pattern: str) -> List[Path]:
        """
        Return a list of all files in a specific directory that match the given pattern.

        Args:
            directory (str): The directory to search for files.
            pattern (str): The pattern to match files (e.g., 'env.*.db', 'env.prod.*').

        Returns:
            List[Path]: A list of Path objects that match the pattern within the specified directory.
        """
        # Create a Path object for the directory
        dir_path = Path(directory)

        # Ensure the directory exists
        if not dir_path.is_dir():
            raise ValueError(
                f"The specified directory '{directory}' does not exist or is not a directory."
            )

        # Use Path.glob to find files matching the pattern within the directory
        matching_files = sorted(dir_path.glob(pattern))
        return matching_files

    def load(self, files: Union[str, List[str]], overwrite_system: bool = True) -> None:
        """
        Load environment variables from the specified file(s). Ensures the files are valid and readable before loading.

        Args:
            files (Union[str, List[str]]): A single file name or a list of file names to load.

        Raises:
            ValueError: If the input is neither a string nor a list of strings.
        """
        input_file_names = []

        if isinstance(files, str):
            input_file_names.append(files)
        elif isinstance(files, list):
            if all(isinstance(file, str) for file in files):
                input_file_names = files
            else:
                raise ValueError("All elements in the list must be strings")
        else:
            raise ValueError("Invalid file name, must be a string or list of strings")

        self._file_names_valid(input_file_names)

        entry_point = Path(sys.argv[0]).parent

        file_names = []

        for input_file_name in input_file_names:
            file_names.append(
                self._get_matching_env_files(entry_point, input_file_name)
            )

        file_names = [str(item) for sublist in file_names for item in sublist]

        # Check if file_names list is empty and handle it before validation
        if not file_names:
            raise ValueError("No matching files found for provided patterns")

        self._files_exist_and_readable(file_names)

        env_files_content = self._read_files(file_names)
        raw_env_vars = self._parse_lines(env_files_content)

        self.file_env_keys.update(raw_env_vars.keys())

        for key in raw_env_vars:
            raw_env_vars[key] = self._interpolate_value(raw_env_vars[key], raw_env_vars)

        self.env_vars = raw_env_vars

        system_vars = dict(os.environ)

        if overwrite_system:
            self.env_vars = {**system_vars, **raw_env_vars}
        else:
            self.env_vars = {**raw_env_vars, **system_vars}

        # Reflect to system as env vars
        for key, value in self.env_vars.items():
            os.environ[key] = value

    def _export(self, include_system: bool = False) -> dict:
        """
        Export environment variables.

        If include_system is True, returns all variables in self.env_vars (both file-based and system).
        If include_system is False, returns only file-based environment variables (stored in self.file_env_keys).

        Args:
            include_system (bool): If True, exports both system and file-based variables.
                                   If False, exports only file-based variables.

        Returns:
            dict: A dictionary of environment variables to be exported.
        """
        if include_system:
            return self.env_vars
        else:
            return {
                key: self.env_vars[key]
                for key in self.file_env_keys
                if key in self.env_vars
            }

    def export_to_file(
        self, file_path: str = ".env.OUTPUT", include_system: bool = False
    ) -> None:
        """
        Export the environment variables to a specified file.

        If include_system is True, all variables in self.env_vars (both file-based and system) are exported to the file.
        If include_system is False, only file-based environment variables (stored in self.file_env_keys) are exported.

        Args:
            file_path (str): The path to the file where the variables will be exported. Defaults to '.env.OUTPUT'.
            include_system (bool): If True, exports both system and file-based variables to the file.
                                   If False, exports only file-based variables to the file.
        """
        env_vars_to_export = self._export(include_system)

        with open(file_path, "w") as f:
            for key, value in env_vars_to_export.items():
                f.write(f"{key}={value}\n")

    def print(self, show_sensitive: bool = False, include_system: bool = False) -> None:
        """
        Print the environment variables to the console.

        If show_sensitive is False, sensitive values like passwords will be masked.
        If include_system is True, both system and file-based variables are printed.
        If include_system is False, only file-based variables (stored in self.file_env_keys) are printed.

        Args:
            show_sensitive (bool): If False, sensitive values are masked.
            include_system (bool): If True, prints both system and file-based variables.
                                   If False, prints only file-based variables.
        """

        def mask_sensitive(key: str, value: str) -> str:
            """Mask sensitive information (e.g., password, secret) in environment variables."""
            sensitive_keywords = [
                "password",
                "secret",
                "token",
                "private",
                "key",
                "pass",
                "auth",
                "user",
                "certificate",
                "login",
                "gcp_service_account",
                "azure_tenant",
                "azure_client_id",
            ]

            if any(
                sensitive_word in key.lower() for sensitive_word in sensitive_keywords
            ):
                return "********"  # Mask sensitive values
            return value

        # Use the _export method to get the environment variables to print
        env_vars_to_print = self._export(include_system)

        for key, value in env_vars_to_print.items():
            if show_sensitive:
                print(f"{key}={value}")
            else:
                print(f"{key}={mask_sensitive(key, value)}")

    def as_int(self, var_name: str) -> int:
        """
        Retrieve the environment variable as an integer.

        Args:
            var_name (str): The name of the environment variable.

        Returns:
            int: The value of the environment variable as an integer.

        Raises:
            ValueError: If the conversion fails.
        """
        value = self.__getattr__(var_name)
        try:
            return int(value)
        except ValueError:
            raise ValueError(
                f"Cannot convert environment variable '{var_name}' to an integer."
            )

    def as_bool(self, var_name: str) -> bool:
        """
        Retrieve the environment variable as a boolean.

        Args:
            var_name (str): The name of the environment variable.

        Returns:
            bool: The value of the environment variable as a boolean.

        Raises:
            ValueError: If the conversion fails.
        """
        value = self.__getattr__(var_name).lower()
        if value in ["true", "1", "yes", "on"]:
            return True
        elif value in ["false", "0", "no", "off"]:
            return False
        else:
            raise ValueError(
                f"Cannot convert environment variable '{var_name}' to a boolean."
            )

    def as_float(self, var_name: str) -> float:
        """
        Retrieve the environment variable as a float.

        Args:
            var_name (str): The name of the environment variable.

        Returns:
            float: The value of the environment variable as a float.

        Raises:
            ValueError: If the conversion fails.
        """
        value = self.__getattr__(var_name)
        try:
            return float(value)
        except ValueError:
            raise ValueError(
                f"Cannot convert environment variable '{var_name}' to a float."
            )

    def as_json(self, var_name: str) -> any:
        """
        Retrieve the environment variable as a parsed JSON object.

        Args:
            var_name (str): The name of the environment variable.

        Returns:
            Any: The value of the environment variable as a parsed JSON object.

        Raises:
            json.JSONDecodeError: If the conversion fails.
        """
        value = self.__getattr__(var_name)
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            raise json.JSONDecodeError(
                f"Cannot convert environment variable '{var_name}' to a valid JSON object.",
                value,
                0,
            )

    def as_list(self, var_name: str, delimiter: str = ",") -> list:
        """
        Retrieve the environment variable as a list by splitting a string on the given delimiter.

        Args:
            var_name (str): The name of the environment variable.
            delimiter (str): The character to split the string on. Defaults to ','.

        Returns:
            list: The value of the environment variable as a list.

        Raises:
            ValueError: If the variable value is empty or cannot be split into a valid list.
        """
        value = self.__getattr__(var_name)

        if not value:
            raise ValueError(
                f"Cannot convert environment variable '{var_name}' to a list because it is empty."
            )

        # Split the string based on the delimiter, strip whitespace from each element, and filter out empty elements
        result_list = [item.strip() for item in value.split(delimiter) if item.strip()]

        if not result_list:
            raise ValueError(
                f"Cannot convert environment variable '{var_name}' to a valid list."
            )

        return result_list

    def as_set(self, var_name: str, delimiter: str = ",") -> set:
        """
        Retrieve the environment variable as a set of unique values.

        Args:
            var_name (str): The name of the environment variable.
            delimiter (str): The character to split the string on. Defaults to ','.

        Returns:
            set: The value of the environment variable as a set of unique items.

        Raises:
            ValueError: If the variable value is empty or cannot be split into a valid set.
        """
        value_list = self.as_list(var_name, delimiter)

        if not value_list:
            raise ValueError(
                f"Cannot convert environment variable '{var_name}' to a valid set."
            )

        return set(value_list)

    def as_dict(
        self, var_name: str, pair_delimiter: str = ",", kv_delimiter: str = "="
    ) -> dict[str, str]:
        """
        Retrieve the environment variable as a dictionary of key-value pairs.

        Args:
            var_name (str): The name of the environment variable.
            pair_delimiter (str): The delimiter between pairs (default ',').
            kv_delimiter (str): The delimiter between keys and values (default '=').

        Returns:
            dict: The value of the environment variable as a dictionary of key-value pairs.

        Raises:
            ValueError: If the conversion fails or the format is invalid.
        """
        value = self.__getattr__(var_name)
        try:
            pairs = [item.split(kv_delimiter) for item in value.split(pair_delimiter)]
            return {key.strip(): val.strip() for key, val in pairs if len(key) > 0}
        except Exception:
            raise ValueError(
                f"Cannot convert environment variable '{var_name}' to a dictionary."
            )

    def as_date(self, var_name: str, date_format: str = "%Y-%m-%d") -> date:
        """
        Retrieve the environment variable as a date.

        Args:
            var_name (str): The name of the environment variable.
            date_format (str): The format to interpret the date. Defaults to "%Y-%m-%d".

        Returns:
            date: The value of the environment variable as a date.
        """
        value = self.__getattr__(var_name)
        if value.lower() in ("null", ""):
            return None
        try:
            return datetime.strptime(value, date_format).date()
        except ValueError:
            raise ValueError(
                f"Cannot convert environment variable '{var_name}' to a date."
            )

    def as_time(self, var_name: str, time_format: str = "%H:%M:%S") -> time:
        """
        Retrieve the environment variable as a time.

        Args:
            var_name (str): The name of the environment variable.
            time_format (str): The format to interpret the time. Defaults to "%H:%M:%S".

        Returns:
            time: The value of the environment variable as a time.
        """
        value = self.__getattr__(var_name)
        if value.lower() in ("null", ""):
            return None
        try:
            return datetime.strptime(value, time_format).time()
        except ValueError:
            raise ValueError(
                f"Cannot convert environment variable '{var_name}' to a time."
            )

    def as_datetime(
        self, var_name: str, datetime_format: str = "%Y-%m-%d %H:%M:%S"
    ) -> datetime:
        """
        Retrieve the environment variable as a datetime.

        Args:
            var_name (str): The name of the environment variable.
            datetime_format (str): The format to interpret the datetime. Defaults to "%Y-%m-%d %H:%M:%S".

        Returns:
            datetime: The value of the environment variable as a datetime.
        """
        value = self.__getattr__(var_name)
        if value.lower() in ("null", ""):
            return None
        try:
            return datetime.strptime(value, datetime_format)
        except ValueError:
            raise ValueError(
                f"Cannot convert environment variable '{var_name}' to a datetime."
            )
