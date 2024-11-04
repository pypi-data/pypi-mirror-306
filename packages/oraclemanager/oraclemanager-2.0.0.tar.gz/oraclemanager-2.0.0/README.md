# Introduction

`oraclemanager` is a wrapper around [python-oracledb](https://oracle.github.io/python-oracledb/) designed to simplify repetitive database actions. It deliberately omits much of the advanced functionality of the core library in favor of a stripped down API focused on connecting, querying, commiting changes, and performing basic result transformations.

`oraclemanager` is ideal for applications that involve a high volume of repetitive and basic database actions. If your applications require multiple concurrent database connections, advanced scripting/querying, or high efficiency, consider using the `python-oracledb` library and API directly.

# Installation

```
pip install oraclemanager
```

# Usage

Most of the package's main functionality is exposed through the `OracleManager` class:

```py
from oraclemanager import OracleManager

oracle = OracleManager()
```

## Connecting to Databases

The `connect` method allows for several methods of connecting to a database. A username, password, and SID can be passed which will cause the `OracleManager` to attempt to connect using the EZConnect string format:

```py
oracle.connect(username="username", password="password", sid="SID")
```

Alternatively, a `ConnectionConfig` object can be passed to the `OracleManager` to store credentials by SID.

```py
config: ConnectionConfig = {
    "DB1": {"username": "user1", "password": "pass123"},
    "DB2": {"username": "user2", "password": "pass321"},
}
oracle = OracleManager(connection_config=config)
oracle.connect("DB1")
```

For connections that might not support EZConnect, a `ConnectParams` object can be passed.

```py
connect_params = ConnectParams(
    user="hr", password="pwd", host="dbhost", port=1521, service_name="orclpdb"
)
oracle = OracleManager()
oracle.connect(connection_params=connect_params)
```

## Executing SQL and Accessing Query Results

The `execute_sql` method can be used to gather query results from `SELECT` statements or to execute changes to the database through `INSERT` or `UPDATE` statements.

```py
oracle.execute_sql("select * from some_table where some_column = 'some_value'")

# Raw query results
raw_results = oracle.query_results

# Query results with data converted to strings.
results_as_strings = oracle.query_result_as_strings

# Query results with rows as ordered dictionaries.
results_as_dicts = oracle.query_result_as_dicts

# Query result column headers.
result_column_headers = oracle.query_result_column_names
```

Query results data formatting can be customized before conversion to strings by setting the `string_formatting_options` property.

```py
formatting: StringFormattingOptions = {
    "datetime_format_code": "%Y-%m-%d",
    "decimal_rounding_places": 2,
}
oracle.string_formatting_options = formatting
```

## Commiting Database Changes

```py
oracle.execute_sql(
    "update some_table t set t.some_column = 'value'
)
oracle.commit()
```
