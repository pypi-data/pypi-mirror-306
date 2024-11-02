# tSQLike

[![Python package](https://github.com/mezantrop/tSQLike/actions/workflows/python-package.yml/badge.svg)](https://github.com/mezantrop/tSQLike/actions/workflows/python-package.yml)
[![CodeQL](https://github.com/mezantrop/tSQLike/actions/workflows/codeql.yml/badge.svg)](https://github.com/mezantrop/tSQLike/actions/workflows/codeql.yml)

## SQL-like interface to tabular structured data

<a href="https://www.buymeacoffee.com/mezantrop" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Description

**tSQLike** is a `Python3` module that is written with a hope to make tabular data process easier using SQL-like primitives.

## Notes

**Not that early stage, but still in development: may contain bugs**

## Usage

```Python3
import tsqlike

t1 = tsqlike.Table(data=[['h1', 'h2', 'h3', 'h4'],
                        ['a', 'b', 'c', 'd'],
                        ['b', 'c', 'd', 'd'],
                        ['f', 'g', 'h', 'i']],
                   name='first')
t2 = tsqlike.Table().import_list_dicts(data=[{'h1': 1, 'h2': 2, 'h3': 3},
                                            {'h1': 'd', 'h2': 'e', 'h3': 'f'}],
                                       name='second')
t3 = t1.join(t2, on='first.h4 == second.h1').select('*').order_by('second.h2', direction=tsqlike.ORDER_BY_DEC)
t3.write_csv(dialect='unix')

"first.h1", "first.h2", "first.h3", "first.h4", "second.h1", "second.h2", "second.h3"
"b", "c", "d", "d", "d", "e", "f"
"a", "b", "c", "d", "d", "e", "f"
```

## Installation

```sh
pip install tsqlike
```

## Functionality

### Table class

The main class of the module

#### Data processing methods

| Name        | Status  | Description                                                                                |
|-------------|---------|--------------------------------------------------------------------------------------------|
| `column_map`| &#9745; | Apply a function to a column                                                               |
| `join`      | &#9745; | Join two Tables (`self` and `table`) on an expression [*](#Warning). Complex, but **slow** |
| `join_lt`   | &#9745; | Light, limited, **fast** and safe `Join`, that doesn't use `eval()`                        |
| `select`    | &#9745; | Select column(s) from the `Table` [*](#Warning)                                            |
| `select_lt` | &#9745; | `eval()`-free version of select                                                            |
| `order_by`  | &#9745; | ORDER BY primitive of SQL SELECT to sort the Table by a column                             |
| `group_by`  | &#9745; | GROUP BY primitive of SQL SELECT to apply aggregate function on a column                   |

#### Import methods

| Name                | Status  | Description                                                             |
|---------------------|---------|-------------------------------------------------------------------------|
| `import_dict_lists` | &#9745; | Import a dictionary of lists into Table object                          |
| `import_list_dicts` | &#9745; | Import a list of horizontal arranged dictionaries into the `Table`      |
| `import_list_lists` | &#9745; | Import `list(list_1(), list_n())` with optional first row as the header |

#### Export methods

| Name                | Status  | Description                                                             |
|---------------------|---------|-------------------------------------------------------------------------|
| `export_dict_lists` | &#9745; | Export a dictionary of lists                                            |
| `export_list_dicts` | &#9745; | Export list of dictionaries                                             |
| `export_list_lists` | &#9745; | Export `list(list_1(), list_n())` with optional first row as the header |

#### Write methods

| Name            | Status  | Description                                                         |
|-----------------|---------|---------------------------------------------------------------------|
| `write_csv`     | &#9745; | Make `CSV` from the `Table` object and write it to a file or stdout |
| `write_json`    | &#9745; | Write `JSON` into file or `STDOUT` [*](#Warning)                    |
| `write_json_lt` | &#9745; | `eval()`-free version of `Table.write_json`                         |
| `write_xml`     | &#9744; | Write `XML`. NB: Do we need this?                                   |

#### Header manipulation methods

| Name              | Status  | Description                                                                |
|-------------------|---------|----------------------------------------------------------------------------|
| `get_column`      | &#9745; | Return either a column name by index or index by name. None if not found   |
| `rename_column`   | &#9745; | Rename a column name in the header                                         |
| `make_shortnames` | &#9745; | Return Header with no Dot-prefix of the columns                            |
| `set_shortnames`  | &#9745; | Remove Dot-prefix of the columns from self/Table header                    |

#### Private methods

| Name           | Status  | Description                               |
|----------------|---------|-------------------------------------------|
| `_redimension` | &#9745; | Recalculate dimensions of the Table.table |

### EvalCtrl class

Controls what arguments are available to `eval()` function

| Name               | Status  | Description                                              |
|--------------------|---------|----------------------------------------------------------|
| `blacklisted`      | &#9745; | Checks if there is any of the blacklised words in stanza |
| `blacklist_add`    | &#9745; | Add a new word into the black list                       |
| `blacklist_remove` | &#9745; | Remove the word from the blacklist                       |

### Standalone functions

| Name          | Status  | Description                                                |
|---------------|---------|------------------------------------------------------------|
| `open_file`   | &#9745; | Open a file                                                |
| `close_file`  | &#9745; | Close a file                                               |
| `read_json`   | &#9745; | Read `JSON` file                                           |
| `read_csv`    | &#9745; | Read `CSV` file                                            |
| `read_xml`    | &#9744; | Read `XML`. NB: Do we need XML support?                    |
| `str_to_type` | &#9745; | Convert a `str` to a proper type: `int`, `float` or `bool` |

#### WARNING

Methods `Table.join(on=)`, `Table.select(where=)` and `Table.write_json(export_f=)`, use `eval()` function
to run specified expressions within the program. **ANY** expression, including one that is potentially **DANGEROUS**
from security point of view, can be passed as the values of the above arguments. It is your duty to ensure correctness
and safety of these arguments and `EvalCtrl` helps to block potentially dangerous function/method names.

Alternatively you can use `Table.join_lt()`, `Table.select_lt()` and `Table.write_json()`. They are significantly less
powerful, but do not use `eval()`.

## TODO

* Rework: Table Names, Header Column Names, Dot-Prefixes
* Documentation!

## Contacts

If you have an idea, a question, or have found a problem, do not hesitate to open an issue or mail me directly:
Mikhail Zakharov <zmey20000@yahoo.com>
