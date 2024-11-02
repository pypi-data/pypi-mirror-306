# CHANGELOG

* **2024.11.01    tSQLike-1.1.8**
  * `Table.get_column()` method returns either a column name by index or index by name. None if not found
  * `Table.rename_column()` renames a column name
  * `Table.import_*()` methods no more make short column names

* **2024.10.31    tSQLike-1.1.7.2**
  * `Table.import_*()` to respect `use_shortnames` argument

* **2024.10.24    tSQLike-1.1.7.1**
  * `Table.join()` Speed up `FULL_JOIN` operations

* **2024.10.24    tSQLike-1.1.7**
  * `Table.join()` `extend` replaces `append` lists method
  * `Table.__repr__()` returns object representation to be unambiguous
  * `Table.__str__()` returns string representation of data to be readable
  * module import simplified: `from tsqlike import tsqlike` can be replaced by just `import tsqlike`

* **2024.10.15    tSQLike-1.1.6**
  * Make `Table` object `iterable`, `iterate_header` boolean controls whether header to be included or not

* **2024.09.26    tSQLike-1.1.5.2**
  * `force=False/True` argument of `make_shortnames()`/`set_shortnames()` to wipe Dot-prefix with force
  * `set_shortnames()` - Remove Dot-prefix of the columns from self/Table header (changes Table object)
  * `make_shortnames()` - Return Header with no Dot-prefix of the columns (does not change Table object)

* **2024.09.25    tSQLike-1.1.5.1**
  * Children `Table` objects inherit `convert_bool`, `convert_numbers` and `use_none` from parent
  * `new_tname` methods argument renamed to `name`

* **2024.09.24    tSQLike-1.1.5**
  * `column_map()` respects `use_shortnames`; handles a case with no `function` argument
  * `group_by()` respects `use_shortnames`; `group_by()` to handle case with no `ftarget` or `function` arguments
  * `order_by()` respects `use_shortnames`
  * `join_lt()` respects `use_shortnames` for both Tables
  * make `_make_shortnames()` method public
  * `join()` respects `use_shortnames` for self Table
  * `select_lt()` method respects `use_shortnames` variable
  * `use_shortnames` in `select()` method
  * `export_*()`/`write_*()` methods respect `self.|use_shortnames=True` to output Table header ommitting Table name
  * `select()` supports applying functions to columns, eg. `select(columns='int(first.h1), first.h3.upper()')`
  * import external `tssplit` module for advanced strings splitting
  * `select()`, `select_lt()` may contain repetitive column names, specified in a random order
  * cosmetic changes

* **2024.09.20    tSQLike-1.1.4.1**
  *`convert_bool=True`, `convert_numbers=True`, `use_none=False`, see `str_to_type()` moved to `**kwargs`

* **2024.09.20    tSQLike-1.1.4**
  * `detect_str_types` obsolete by `convert_bool=True`, `convert_numbers=True`, `use_none=False`, see `str_to_type()`
  * `Table()` object, may be passed to a new `Table()` object, i.e., now possible: `Table(Table())`

* **2024.09.19    tSQLike-1.1.3**
  * `detect_types=False` renamed to `detect_str_types=False`
  * `str_to_type()` `use_none=False` whether to convert empty strings to `None` or not; Boolean conversion fix

* **2024.07.07    tSQLike-1.1.2**
  * `join_lt()` Fast modification

* **2024.07.03    tSQLike-1.1.1**
  * `select_lt()` to accept `<` comparison operator

* **2024.07.02    tSQLike-1.1.0**
  * Import methods use `detect_types` to detect if auto-conversion from `str` to `int`, `float` and `bool` is needed

* **2024.06.28    tSQLike-1.0.4**
  * `select_lt()` respects empty arguments

* **2024.06.24    tSQLike-1.0.3**
  * `write_json()` defaults to `export_f='export_list_dicts()'`
  * `read_json()` implemented as a standalone function
  * `read_csv()` became standalone
  * `Table` auto-import on init of `dict(lists)` fixed
  * `README.md` updated
  * `write_json_lt()` added
  * `README.md` updated

* **2024.06.06    tSQLike-1.0.2**
  * `tSQLike` has been published to PyPI automatically

* **2024.06.06    tSQLike-1.0.1**
  * Package created and uploaded to PyPI manually

* **2024.06.06    tSQLike-1.0.0**
  * The first release
