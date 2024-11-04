from collections import OrderedDict
from datetime import datetime
from typing import cast
from unittest.mock import MagicMock

import oracledb
import pytest

from oraclemanager import (
    ConnectionConfig,
    ConnectParams,
    OracleManager,
    StringFormattingOptions,
)

mock_connection_config: ConnectionConfig = {
    "DB1": {"username": "user1", "password": "pass123"},
    "DB2": {"username": "user2", "password": "pass321"},
}

mock_query_description = (
    ("First Name",),
    ("Last Name",),
    ("Age",),
    ("Country",),
    ("Birthday",),
    ("Weight",),
)

mock_query_data = [
    ("John", "Smith", 24, "United States", datetime(1999, 9, 10), 156.32432),
    ("Jane", "Doe", 32, "United Kingdom", datetime(1991, 1, 15), 110.43876),
    ("Robert", "Johnson", 51, "Canada", datetime(1972, 4, 13), 201.64454),
]


@pytest.fixture
def oracle_manager(mocker):
    mocker.patch("oracledb.connect")
    cursor_mock = cast(MagicMock, oracledb.connect().cursor)
    cursor_mock().description = mock_query_description
    cursor_mock().fetchall.return_value = mock_query_data

    return OracleManager(mock_connection_config)


def test_connects_with_sid(oracle_manager):
    connect_mock = cast(MagicMock, oracledb.connect)

    oracle_manager.connect("DB1")

    connect_mock.assert_any_call("user1/pass123@DB1")


def test_connects_with_sid_username_and_password(oracle_manager):
    connect_mock = cast(MagicMock, oracledb.connect)

    oracle_manager.connect("SID", "custom_username", "custom_password")

    connect_mock.assert_any_call("custom_username/custom_password@SID")


def test_connects_with_connection_params(oracle_manager):
    connect_mock = cast(MagicMock, oracledb.connect)
    connection_params = ConnectParams(
        user="custom_username", password="custom_password", sid="SID"
    )

    oracle_manager.connect(connection_params=connection_params)

    connect_mock.assert_any_call(params=connection_params)


def test_connects_with_context_manager_syntax(oracle_manager):
    connect_mock = cast(MagicMock, oracledb.connect)

    with oracle_manager("DB2"):
        connect_mock.assert_any_call("user2/pass321@DB2")
        assert oracle_manager.cursor is not None

    assert oracle_manager.cursor is None


def test_loads_connection_config_file(oracle_manager):
    oracle_manager.load_connection_config_file("tests/data/config.json")

    assert oracle_manager.connection_config == {
        "ABC": {"username": "username1", "password": "password123"},
        "DEF": {"username": "username2", "password": "password321"},
    }


def test_disconnects(oracle_manager):
    oracle_manager.disconnect()

    assert oracle_manager.cursor is None


def test_executes_sql(oracle_manager):
    cursor_mock = cast(MagicMock, oracledb.connect().cursor)
    execute_mock = cursor_mock().execute

    oracle_manager.connect("DB1")
    oracle_manager.execute_sql("select * from some_table")

    execute_mock.assert_called_once_with("select * from some_table")


def test_executes_sql_with_params(oracle_manager):
    params = {"param1": "test"}
    cursor_mock = cast(MagicMock, oracledb.connect().cursor)
    execute_mock = cursor_mock().execute

    oracle_manager.connect("DB1")
    oracle_manager.execute_sql(
        "select * from some_table where some_column = :param1", params
    )

    execute_mock.assert_called_once_with(
        "select * from some_table where some_column = :param1", params
    )


def test_shows_column_headers(oracle_manager):
    oracle_manager = cast(OracleManager, oracle_manager)

    oracle_manager.connect("DB1")

    assert oracle_manager.query_result_column_names == (
        "First Name",
        "Last Name",
        "Age",
        "Country",
        "Birthday",
        "Weight",
    )


def test_shows_raw_results(oracle_manager):
    oracle_manager = cast(OracleManager, oracle_manager)

    oracle_manager.connect("DB1")
    oracle_manager.execute_sql("select * from some_table")

    assert oracle_manager.query_results == mock_query_data


def test_converts_results_to_strings_with_formatting(oracle_manager):
    oracle_manager = cast(OracleManager, oracle_manager)
    string_formatting_options: StringFormattingOptions = {
        "datetime_format_code": "%m-%d-%Y",
        "decimal_rounding_places": 1,
    }

    oracle_manager.connect("DB1")
    oracle_manager.string_formatting_options = string_formatting_options
    oracle_manager.execute_sql("select * from some_table")

    assert oracle_manager.query_result_as_strings == [
        ("John", "Smith", "24", "United States", "09-10-1999", "156.3"),
        ("Jane", "Doe", "32", "United Kingdom", "01-15-1991", "110.4"),
        ("Robert", "Johnson", "51", "Canada", "04-13-1972", "201.6"),
    ]


def test_converts_results_to_ordered_dict_rows(oracle_manager):
    oracle_manager = cast(OracleManager, oracle_manager)
    string_formatting_options: StringFormattingOptions = {
        "datetime_format_code": "%m-%d-%Y",
        "decimal_rounding_places": 1,
    }

    oracle_manager.connect("DB1")
    oracle_manager.string_formatting_options = string_formatting_options
    oracle_manager.execute_sql("select * from some_table")

    assert oracle_manager.query_result_as_dicts == [
        OrderedDict(
            [
                ("First Name", "John"),
                ("Last Name", "Smith"),
                ("Age", 24),
                ("Country", "United States"),
                ("Birthday", datetime(1999, 9, 10, 0, 0)),
                ("Weight", 156.32432),
            ]
        ),
        OrderedDict(
            [
                ("First Name", "Jane"),
                ("Last Name", "Doe"),
                ("Age", 32),
                ("Country", "United Kingdom"),
                ("Birthday", datetime(1991, 1, 15, 0, 0)),
                ("Weight", 110.43876),
            ]
        ),
        OrderedDict(
            [
                ("First Name", "Robert"),
                ("Last Name", "Johnson"),
                ("Age", 51),
                ("Country", "Canada"),
                ("Birthday", datetime(1972, 4, 13, 0, 0)),
                ("Weight", 201.64454),
            ]
        ),
    ]
