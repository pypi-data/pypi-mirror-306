import json
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from typing import Any, NotRequired, TypedDict, TypeGuard

import oracledb


class DatabaseCredentials(TypedDict):
    username: str
    password: str


ConnectionConfig = dict[str, DatabaseCredentials]


class StringFormattingOptions(TypedDict):
    datetime_format_code: NotRequired[str]
    decimal_rounding_places: NotRequired[int]


ConnectParams = oracledb.ConnectParams


class OracleManager:
    def __init__(
        self,
        connection_config: ConnectionConfig | None = None,
        connection_config_file_path: str | None = None,
        string_formatting_options: StringFormattingOptions | None = None,
    ):
        """Initializes a new instance of the `OracleManager` class.

        Args:
            connection_config: A `ConnectionConfig` object that stores DB credentials. Defaults to None.
            connection_config_file_path: A file path to a file holding a `ConnectionConfig` object in JSON format.
                Can be loaded in place of providing a value for the `connection_config` argument. Defaults to None.
            string_formatting_options: A dict containing formatting options to be used if query results are
                converted to strings. Defaults to None.
        """

        if connection_config_file_path and not connection_config:
            connection_config = self.load_connection_config_file(
                connection_config_file_path
            )

        self.cursor = None

        self.string_formatting_options = string_formatting_options
        self.connection_config = connection_config
        self._connection = None
        self._query_result = _QueryResult(None, None, None)

    def __call__(
        self,
        tns_name: str | None = None,
        username: str | None = None,
        password: str | None = None,
        connection_params: ConnectParams | None = None,
    ):
        self.connect(tns_name, username, password, connection_params)

        return self

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        self.disconnect()

    @property
    def query_results(self):
        """Returns raw query results if available.

        Returns:
            Raw query results.
        """

        return self._query_result.raw

    @property
    def query_result_as_strings(self):
        """Returns raw query result elements in string format if results are available. Uses the formatting options set by the
        `string_formatting_options` property.

        Returns:
            Raw query results with data elements converted to strings.
        """

        if self._query_result.as_strings:
            return self._query_result.as_strings
        elif self._query_result.raw is not None:
            datetime_format_code = (
                self.string_formatting_options.get("datetime_format_code")
                if self.string_formatting_options
                else None
            )
            decimal_rounding_places = (
                self.string_formatting_options.get("decimal_rounding_places")
                if self.string_formatting_options
                else None
            )
            self._query_result.as_strings = [
                tuple(
                    self._convert_element_to_string(
                        element, datetime_format_code, decimal_rounding_places
                    )
                    for element in row
                )
                for row in self._query_result.raw
            ]

            return self._query_result.as_strings
        else:
            return None

    @property
    def query_result_as_dicts(self):
        """Returns raw query result rows in `OrderedDict` format if results are available.

        Returns:
            Raw query results with rows converted to `OrderedDict`s.
        """

        if self._query_result.as_dicts:
            return self._query_result.as_dicts
        elif self._query_result.raw is not None:
            columns = self.query_result_column_names

            if not columns:
                return None

            self._query_result.as_dicts = [
                OrderedDict(zip(columns, row)) for row in self._query_result.raw
            ]

            return self._query_result.as_dicts
        else:
            return None

    @property
    def query_result_column_names(self):
        """Returns the column names of the current query results if available.

        Returns:
            A tuple of column headers.
        """

        if self.cursor:
            return tuple(
                str(result_column[0]) for result_column in self.cursor.description
            )
        else:
            return None

    def load_connection_config_file(self, connection_config_file_path: str):
        """Loads validated content from a JSON file path as a `ConnnectionConfig` object.

        Args:
            connection_config_file_path: The file path to load.

        Raises:
            TypeError: If the loaded file content can not be validated as a `ConnectionConfig` object.
        """

        with open(connection_config_file_path, "r") as connection_config_file:
            connection_config = json.load(connection_config_file)

            if self._isconnection_config(connection_config):
                self.connection_config = connection_config
            else:
                raise TypeError(
                    f"The file content loaded from {connection_config_file_path} could not be parsed "
                    "into the correct `ConnectionConfig` data type."
                )

    def connect(
        self,
        sid: str | None = None,
        username: str | None = None,
        password: str | None = None,
        connection_params: ConnectParams | None = None,
    ):
        """Establishes a connection to a specified Oracle database.

        Args:
            sid: The SID of the database. If the SID is included in the `connection_config`, no other arguments
                are needed. Defaults to None.
            username: The username of the database profile to use to connect. This argument can be passed with a
                `sid` and `password` to manually connect to a database using the EZConnect string format. Defaults to None.
            password: The password of the database profile to usee to connect. This argument can be passed with a
                `sid` and `username` to manually connect to a database using the EZConnect string format. Defaults to None.
            connection_params: A connection params object. Can be used to manually connect to a database
                if the `connection_config` object or an EZConnect string cannot be used. Defaults to None.

        Raises:
            ValueError: If only a `sid` value is passed and cannot be found in the `connection_config`, or if an invalid combination of
                arguments were passed.
        """

        self.disconnect()
        connection_config_record = (
            self.connection_config.get(sid) if self.connection_config and sid else None
        )

        if connection_config_record and not username and not password:
            saved_username = connection_config_record["username"]
            saved_password = connection_config_record["password"]
            self._connection = oracledb.connect(
                f"{saved_username}/{saved_password}@{sid}"
            )
            self.cursor = self._connection.cursor()
        elif sid and username and password:
            self._connection = oracledb.connect(f"{username}/{password}@{sid}")
            self.cursor = self._connection.cursor()
        elif connection_params:
            self._connection = oracledb.connect(params=connection_params)
            self.cursor = self._connection.cursor()
        else:
            if sid and self.connection_config and sid not in self.connection_config:
                raise ValueError(
                    f"The `sid` {sid} did not match any entries in the config."
                )
            elif sid and not self.connection_config:
                raise ValueError(
                    "Unable to connect using `sid` since no `connection_config` was provided."
                )
            else:
                raise ValueError(
                    "Unable to connect. Either all of the arguments `sid`, "
                    "`username`, and `password` OR `connection_params` need to be specified."
                )

    def disconnect(self):
        """Disconnects from any connected databases and resets query results."""

        if self._connection:
            self._connection.close()

        self.cursor = None
        self._query_result = _QueryResult(None, None, None)

    def execute_sql(
        self,
        sql: str,
        params: list[Any] | tuple[Any, ...] | dict[str, Any] | None = None,
    ):
        """Executes a SQL statement with specified params.

        Args:
            sql: A SQL statement to execute.
            params: SQL statement param values. Defaults to None.

        Raises:
            RuntimeError: If no database connection has been established, or if there was an error executing SQL.
        """

        if not self._connection or not self.cursor:
            raise RuntimeError("No database connection has been established.")

        if params:
            try:
                self.cursor.execute(sql, params)
            except Exception as exception:
                raise RuntimeError(
                    "An exception occurred while executing SQL.\n"
                    f"SQL: {sql}\n"
                    f"Params:{params}\n"
                    f"Exception: {exception}"
                )
        else:
            try:
                self.cursor.execute(sql)
            except Exception as exception:
                raise RuntimeError(
                    "An exception occurred while executing SQL.\n"
                    f"SQL: {sql}\n"
                    f"Exception: {exception}"
                )

        try:
            self._query_result.raw = [row for row in self.cursor.fetchall()]
            self._query_result.as_strings = None
            self._query_result.as_dicts = None
        except oracledb.InterfaceError:
            # SQL statement was not a SELECT, clear query result
            self._query_result = _QueryResult(None, None, None)

    def commit(self):
        """Commits current database changes.

        Raises:
            RuntimeError: If a commit is attempted but no database connection has been established.
        """

        if not self._connection:
            raise RuntimeError("No database connection has been established.")

        self._connection.commit()

    def _convert_element_to_string(
        self,
        element: Any,
        datetime_format_code: str | None,
        decimal_rounding_places: int | None,
    ):
        if element is None:
            return ""
        elif isinstance(element, datetime):
            return (
                element.strftime(datetime_format_code)
                if datetime_format_code
                else str(element)
            )
        elif isinstance(element, float):
            return str(
                round(element, decimal_rounding_places)
                if decimal_rounding_places is not None
                else element
            )
        else:
            return str(element)

    @staticmethod
    def _isconnection_config(data: Any) -> TypeGuard[ConnectionConfig]:
        def _is_database_credentials(data: Any) -> TypeGuard[DatabaseCredentials]:
            if not isinstance(data, dict):
                return False

            for key in ("username", "password"):
                if not key in data:
                    return False

                if not isinstance(data[key], str):
                    return False

            return True

        if not isinstance(data, dict):
            return False

        if any(key for key in data.keys() if not isinstance(key, str)):
            return False

        for value in data.values():
            if not _is_database_credentials(value):
                return False

        return True


@dataclass
class _QueryResult:
    raw: list[tuple[Any, ...]] | None
    as_strings: list[tuple[str, ...]] | None
    as_dicts: list[OrderedDict[str, Any]] | None
