"""
SQL-like interface to tabular structured data
"""

# ------------------------------------------------------------------------------------------------ #
# Copyright (c) 2024, Mikhail Zakharov <zmey20000@yahoo.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# ------------------------------------------------------------------------------------------------ #
import csv
import json
import sys
import signal
import time

from tssplit import tssplit

# -- Constants ----------------------------------------------------------------------------------- #
# JOIN
JOIN_INNER = 0
JOIN_LEFT = 1
JOIN_RIGHT = 2
JOIN_FULL = 3

# ORDER BY
ORDER_BY_INC = 0  # Increasing
ORDER_BY_DEC = 1  # Decreasing

# Syntax
LINETERMINATOR = '\n'                   # '\n' is autoconverted to '\r\n' on Windows
TNAME_COLUMN_DELIMITER = '.'            # Delimiter between table name and a column: table.column
TNAME_TNAME_DELIMITER = '_'             # Delimiter between table names e.g, on join(): table_table

# ------------------------------------------------------------------------------------------------ #
try:
    # If tsqlike has been imported
    from tsqlike.__about__ import __version__
except ModuleNotFoundError:
    try:
        # If it is called directly as a Python file
        from __about__ import __version__
    except ModuleNotFoundError:
        __version__ = '?.?.?'


# -- Standalone functions ------------------------------------------------------------------------ #
def open_file(file_name=None, file_mode='r+', encoding=None, newline=None):

    """ Open a file """

    # Detect default file: STDIN or STDOUT
    default_file = sys.stdin if 'r' in file_mode else sys.stdout

    try:
        f = file_name and open(file_name, file_mode, encoding=encoding,
                               newline=newline) or default_file
    except (FileNotFoundError, PermissionError, OSError) as _err:
        print(f'FATAL@open_file(): {_err}')
        sys.exit(1)

    # Ignore BrokenPipeError on *NIX if piping output
    if f == sys.stdout and sys.platform != 'win32':
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    return f


# ------------------------------------------------------------------------------------------------ #
def close_file(file):

    """
    Close the file

    :param file:    File to close
    """

    if file and file is not sys.stdout and file is not sys.stdin:
        file.close()


# ------------------------------------------------------------------------------------------------ #
def str_to_type(s, convert_bool=True, convert_numbers=True, use_none=False):

    """ Convert string s to a proper type: int, float or boolean """

    # Convert '' - empty strings to None?
    if s == '' and use_none:
        return None

    if convert_bool:
        if s in ('True', 'true'):
            return True

        if s in ('False', 'false'):
            return False

    if convert_numbers:
        try:
            return float(s) if '.' in s or ',' in s else int(s) # to float and int
        except (ValueError, TypeError):
            return s                                            # no conversion possible -> string

    return s


# ------------------------------------------------------------------------------------------------ #
def read_csv(in_file=None, encoding=None, newline='', name='', dialect='excel', **kwargs):

    """
    Read CSV from a file and import into a Table object

    :param in_file:             Filename to read CSV from
    :param encoding:            Character encoding
    :param newline:             UNIX/Windows/Mac style line ending
    :param name:                Table name to assign
    :param dialect:             CSV dialect, e.g: excel, unix
    :param **kwargs:            Various optional string conversion and CSV parameters:
        :param delimiter:       CSV field delimiter
        :param quotechar:       CSV quote character
        :param quoting:         CSV quote style
        :param convert_bool:    Convert strings into Booleans
        :param convert_numbers: Convert strings to integers or float
        :param use_none:        Convert empty strings to None type
    :return: Table
    """

    f = open_file(in_file, file_mode='r', encoding=encoding, newline=newline)
    fmtparams={}|kwargs
    _data = csv.reader(f, dialect=dialect, **fmtparams)
    t = Table(data=list(_data), name=name, **kwargs)
    close_file(f)
    return t


# -------------------------------------------------------------------------------------------- #
def read_json(in_file=None, name='', **kwargs):

    """ Read JSON data from file

    :param in_file:             Filename to read JSON from
    :param name:                Table name to assign
    :param **kwargs:          	optional string conversion parameters:
        :param convert_bool:    Convert strings into Booleans
        :param convert_numbers: Convert strings to integers or float
        :param use_none:        Convert empty strings to None type
    :return                     Table
    """

    _data = {}
    f = open_file(file_name=in_file, file_mode='r')
    try:
        _data = json.load(f)
    except (IOError, OSError) as _err:
        print(f'FATAL@Table.read_json(): Unable to load JSON structure: {_err}')
    t = Table(data=_data, name=name, **kwargs)
    close_file(f)
    return t


# ------------------------------------------------------------------------------------------------ #
class EvalCtrl:

    """
    Control eval() function with white/black lists
    """

    blacklist = ['call(', 'popen(', 'Popen(', 'run(', 'system(']

    # -------------------------------------------------------------------------------------------- #
    def blacklisted(self, stanza):

        """
        Checks if there is any of the blacklised words in stanza

        :param stanza:      String to sanitize
        :return:            Boolean and the first blacklisted word
        """

        for word in self.blacklist:
            if word in stanza.replace(' ', '').replace('\t', ''):
                return True, word
        return False, None

    # -------------------------------------------------------------------------------------------- #
    def blacklist_add(self, word):

        """
        Add a new word into the black list

        :param word:    The word to add
        """

        if word not in self.blacklist:
            self.blacklist.append(word)

        return self

    # -------------------------------------------------------------------------------------------- #
    def blacklist_remove(self, word):

        """
        Remove the word from the blacklist

        :param word:    The word to remove from the blacklist
        """

        if word in self.blacklist:
            self.blacklist.remove(word)

        return self


# ------------------------------------------------------------------------------------------------ #
class Table:

    """
    Represents an tSQLike Table object with the below structure:
        * name:         string()
        * table:        list(list_1() ... list_n())
            * header:   list()
            * row:      list()
        * timestamp:    integer()
        * rows:         integer()
        * cols:         integer()
    """

    # -------------------------------------------------------------------------------------------- #
    def __init__(self, data=None, name=None, **kwargs):

        """
        Initialize Table() object

        :param data:                Data to import formatted as list of dictionaries
        :param name:                If not None, set it as the Table name
        :param **kwargs:          	optional string conversion parameters:
            :param convert_bool:    Convert strings into Booleans
            :param convert_numbers: Convert strings to integers or float
            :param use_none:        Convert empty strings to None type
            :param globals:         Pass globals into the object
            :param use_shortnames   if True, Column names in Table header do not contain Table name
        """

        self.timestamp = int(time.time())
        self.name = name or str(self.timestamp)

        self.convert_bool = kwargs.get('convert_bool', True)
        self.convert_numbers = kwargs.get('convert_numbers', True)
        self.use_none = kwargs.get('use_none', False)
        # Pass globals=globals() when creating a Table object,
        # to allow select() using custom defined functions
        self.globals = kwargs.get('globals', {})
        self.use_shortnames = kwargs.get('use_shortnames', False)
        self.iterate_header = kwargs.get('iterate_header', False)

        if not data:
            self.table = []
            self.header = []
            self.rows = 0
            self.cols = 0
        elif isinstance(data, list) and len(data):
            if isinstance(data[0], dict):                   # list(dicts())
                self.import_list_dicts(data)
            if isinstance(data[0], list):                   # list(lists())
                self.import_list_lists(data)
        elif isinstance(data, dict) and len(data):
            if isinstance(data[next(iter(data))], list):    # dict(lists())
                self.import_dict_lists(data)
        elif isinstance(data, Table):                       # Table()
            # Import/export is done to allow type conversion to happen
            self.import_list_lists(data.export_list_lists())
        else:
            raise ValueError('FATAL@Table.__init__: Unexpected data format')

        # TODO: Invent nice aliases for the methods
        # Method aliases - Import
        self.import_table = self.import_list_lists
        self.import_thashes = self.import_list_dicts
        self.import_htables = self.import_dict_lists
        # Export data
        self.export_table = self.export_list_lists
        self.export_thashes = self.export_list_dicts
        self.export_htables = self.export_dict_lists

    # -------------------------------------------------------------------------------------------- #
    def __iter__(self):
        if self.iterate_header:
            yield self.header if not self.use_shortnames else self.make_shortnames()

        r = 0
        while  r < self.rows:
            yield self.table[r]
            r += 1

    # -------------------------------------------------------------------------------------------- #
    def __repr__(self):
        me = self.__class__.__module__ + '.' + self.__class__.__qualname__
        return str(f"{me}(data={self.export_list_lists()}, name='{self.name}', "
            f"timestamp={self.timestamp}, convert_bool={self.convert_bool}, "
            f"convert_numbers={self.convert_numbers}, use_none={self.use_none}, "
            f"globals={self.globals}, use_shortnames={self.use_shortnames}, "
            f"iterate_header={self.iterate_header})")

    # -------------------------------------------------------------------------------------------- #
    def __str__(self):
        return str(self.export_list_lists())

    # -------------------------------------------------------------------------------------------- #
    def _redimension(self):

        """ Recalculate dimensions of the Table.table """

        self.rows = len(self.table)
        self.cols = self.rows and len(self.table[0]) or 0

    # -- Header manipulation methods ------------------------------------------------------------- #
    def get_column(self, column=None, **kwargs):

        """Return a column name by index or return column ID by its name. None if not found"""

        header = self.header
        if kwargs.get('use_shortnames', self.use_shortnames):
            header = self.make_shortnames()

        if isinstance(column, str) and column in header:
            return header.index(column)

        if isinstance(column, int) and column >= 0 and column < len(header):
            return header[column]

        return None

    # -------------------------------------------------------------------------------------------- #
    def rename_column(self, oldname, newname, **kwargs):

        """Rename a column name in the header"""

        idx = self.get_column(oldname, **kwargs)
        if idx is not None:
            idx = idx if isinstance(idx, int) else oldname

            self.header[idx] = (self.header[idx].split(TNAME_COLUMN_DELIMITER)[0] +
                                TNAME_COLUMN_DELIMITER + newname)

        return idx

    # -------------------------------------------------------------------------------------------- #
    def make_shortnames(self, header='', force=False):

        """Return Header with no Dot-prefix of the columns"""

        if not header:
            header = self.header

        if force:
            return [h.split(TNAME_COLUMN_DELIMITER)[1] for h in header]

        return [h.split(TNAME_COLUMN_DELIMITER)[1]
                       if h.startswith(self.name + TNAME_COLUMN_DELIMITER) else h for h in header]

    # -------------------------------------------------------------------------------------------- #
    def set_shortnames(self, table=None, force=False):

        """Remove Dot-prefix of the columns from self/Table header"""

        table = table if isinstance(table, Table) else self
        table.header = self.make_shortnames(table.header, force)
        return table

    # -- Import methods -------------------------------------------------------------------------- #
    def import_list_dicts(self, data, name=None, **kwargs):

        """
        Import a list of dictionaries

        :alias:                     import_thashes()
        :param data:                Data to import formatted as list of dictionaries
        :param name:                If not None, set it as the Table name
        :param **kwargs:          	optional string conversion parameters:
            :param convert_bool:    Convert strings into Booleans
            :param convert_numbers: Convert strings to integers or float
            :param use_none:        Convert empty strings to None type
            :param use_shortnames   if True, Column names in Table header do not contain Table name
        :return:                    self
        """

        # Set a new Table name if requested
        if name:
            self.name = str(name)

        if isinstance(data, list) and len(data) and isinstance(data[0], dict):
            self.header = [self.name + TNAME_COLUMN_DELIMITER + str(f)
                           if TNAME_COLUMN_DELIMITER not in str(f) else f for f in (data[0].keys())]

            cb = kwargs.get('convert_bool', self.convert_bool)
            cn = kwargs.get('convert_numbers', self.convert_numbers)
            un = kwargs.get('use_none', self.use_none)
            self.table = [[str_to_type(v, cb, cn, un) for v in r.values()] for r in data]

        else:
            raise ValueError('FATAL@Table.import_list_dicts: Unexpected data format')

        self._redimension()
        self.timestamp = int(time.time())

        return self

    # -------------------------------------------------------------------------------------------- #
    def import_dict_lists(self, data, name=None, **kwargs):

        """
        Import a dictionary of lists
        """

        if name:
            self.name = name

        if isinstance(data, dict) and len(data) and isinstance(data[next(iter(data))], list):
            self.header = [self.name + TNAME_COLUMN_DELIMITER + str(h)
                           if TNAME_COLUMN_DELIMITER not in str(h) else str(h) for h in
                           list(data.keys())]

            self.table = [[None for _ in range(len(data.keys()))]
                          for _ in range(len(data[next(iter(data))]))]

            cb = kwargs.get('convert_bool', self.convert_bool)
            cn = kwargs.get('convert_numbers', self.convert_numbers)
            un = kwargs.get('use_none', self.use_none)
            for c, f in enumerate(data.keys()):
                for r, v in enumerate(data[f]):
                    self.table[r][c] = str_to_type(v, cb, cn, un)
            self._redimension()
        else:
            raise ValueError('FATAL@Table.import_dict_lists: Unexpected data format')

        self.timestamp = int(time.time())
        return self

    # -------------------------------------------------------------------------------------------- #
    def import_list_lists(self, data, header=True, name=None, **kwargs):

        """
        Import list(list_1(), list_n()) with optional first row as the header

        :param data:                Data to import formatted as list of lists
        :param header:              If True, data to import HAS a header
        :param name:                If not None, set it as the Table name
        :param **kwargs:          	optional string conversion parameters:
            :param convert_bool:    Convert strings into Booleans
            :param convert_numbers: Convert strings to integers or float
            :param use_none:        Convert empty strings to None type
            :param use_shortnames   if True, Column names in Table header do not contain Table name
        :return:                    self
        """

        # Set a new Table name if requested
        if name:
            self.name = str(name)

        if isinstance(data, list) and len(data) and isinstance(data[0], list):
            # TODO: Check all rows to be equal length

            cb = kwargs.get('convert_bool', self.convert_bool)
            cn = kwargs.get('convert_numbers', self.convert_numbers)
            un = kwargs.get('use_none', self.use_none)
            self.table = [[str_to_type(v, cb, cn, un) for v in r] for r in data[1:]]

            self._redimension()

            # If table header is not properly initiated, make each column: "name.column"
            if header and data[0]:
                self.header = [self.name + TNAME_COLUMN_DELIMITER + str(f)
                               if TNAME_COLUMN_DELIMITER not in str(f) else f for f in data[0]]
            else:
                # Let's create a header, if there is no one
                self.header = [str(h) for h in range(self.cols)]
        else:
            raise ValueError('FATAL@Table.import_list_lists: Unexpected data format')

        self.timestamp = int(time.time())
        return self

    # -- Export data ----------------------------------------------------------------------------- #
    def export_list_dicts(self, **kwargs):

        """ Export as list of dictionaries """

        sn = kwargs.get('use_shortnames', self.use_shortnames)
        return [{self.make_shortnames()[c] if sn else self.header[c]:
                 r[c] for c in range(self.cols)} for r in self.table]

    # -------------------------------------------------------------------------------------------- #
    def export_list_lists(self, header=True, **kwargs):

        """ Export Table """

        sn = kwargs.get('use_shortnames', self.use_shortnames)
        return ([self.make_shortnames() if sn else self.header] +
                self.table) if header else self.table

    # -------------------------------------------------------------------------------------------- #
    def export_dict_lists(self, **kwargs):

        """ Export a dictionary of lists """

        sn = kwargs.get('use_shortnames', self.use_shortnames)
        return {self.make_shortnames()[c] if sn else self.header[c]: [self.table[r][c]
                                 for r in range(self.rows)] for c in range(self.cols)}

    # -------------------------------------------------------------------------------------------- #
    def write_csv(self, out_file=None, encoding=None,
                  dialect='excel', lineterminator=LINETERMINATOR, **fmtparams):

        """
        Make CSV from the Table object and write it to a file or stdout

        :param out_file:            Filename to write CSV data or None for stdout
        :param encoding:            Character encoding
        :param lineterminator:      Line ends
        :**fmtparams:               Various optional CSV parameters:
            :param delimiter:           CSV field delimiter
            :param quotechar:           CSV quote character
            :param quoting:             CSV quote style
        :return:                    Nothing
        """

        f = open_file(out_file, 'w', encoding=encoding)
        wr = csv.writer(f, dialect=dialect, lineterminator=lineterminator, **fmtparams)

        try:
            # Write the header ...
            wr.writerow(self.make_shortnames() if self.use_shortnames else self.header)
            # and the body of the table
            for r in self.table:
                wr.writerow(r)
        except BrokenPipeError as _err:
            print(f'FATAL@Table.write_csv: {_err}', file=sys.stderr)

        close_file(f)

    # -------------------------------------------------------------------------------------------- #
    def write_json(self, out_file=None, export_f='export_list_dicts()',
                   indent=None, separators=None, sort_keys=False, evalctrl=EvalCtrl()):

        """
        Make JSON from the Table object and write it to a file or stdout

        :param out_file:    Filename to write CSV data or None for stdout
        :param export_f:    Function with arguments, an internal "export_*" or an external one
        :param indent:      JSON indentation
        :param separators:  JSON separators tuple
        :param sort_keys:   Whether to sort keys or not
        :param evalctrl:    eval() controlling class
        :return: Nothing
        """

        # Usage example: t.write_json(out_file='1.json', export_f='export_dict_lists()')

        if export_f:
            bl = evalctrl.blacklisted(export_f)
            if bl[0]:
                raise ValueError(f'FATAL@Table.write_json: Found blacklisted expression: [{bl[1]}]')

            methods = [method for method in dir(self) if
                       method.startswith('export_') and callable(getattr(self, method))]

            if export_f.split('(')[0].strip() in methods:
                # Our internal export_* method
                export_f = 'self.' + export_f

            efunc = eval(compile(export_f, '<string>', 'eval'))
            f = open_file(out_file, 'w')
            try:
                f.write(json.dumps(efunc, indent=indent,
                                   separators=separators, sort_keys=sort_keys))
            except (IOError, OSError) as _err:
                print(f'FATAL@Table.write_json(): {_err}')
                sys.exit(1)

            close_file(f)

    # -------------------------------------------------------------------------------------------- #
    def write_json_lt(self, out_file=None, indent=None, separators=None, sort_keys=False):

        """
        Lite, no eval() version of write_json() method

        :param out_file:    Filename to write CSV data or None for stdout
        :param indent:      JSON indentation
        :param separators:  JSON separators tuple
        :param sort_keys:   Whether to sort keys or not
        :return: Nothing
        """

        f = open_file(out_file, 'w')
        try:
            f.write(json.dumps(self.export_list_dicts(), indent=indent,
                               separators=separators, sort_keys=sort_keys))
        except (IOError, OSError) as _err:
            print(f'FATAL@Table.write_json_lt(): {_err}')
            sys.exit(1)

        close_file(f)
        return self

    # -------------------------------------------------------------------------------------------- #
    def write_xml(self):

        """ Not implemented """

        # TODO: Implement me

    # -- Data processing ------------------------------------------------------------------------- #
    def join(self, table, on='', mode=JOIN_INNER, name='', replace=False,
             evalctrl=EvalCtrl(), **kwargs):

        """Join two Tables (self and table) on an expression

        :param table:               Table to join self with
        :param on:                  Valid Python expression
        :param mode:                Join mode
        :param name:                Give a name of the returned Table
        :param replace:             Replace source with the new data or not
        :param evalctrl:            eval() controlling class
        :param **kwargs:
            :param use_shortnames   If True, Columns of Self Table header do not contain Table name
        :return:                    self
        """

        s_header = self.header
        if kwargs.get('use_shortnames', self.use_shortnames):
            s_header = self.make_shortnames()

        cb = kwargs.get('convert_bool', self.convert_bool)
        cn = kwargs.get('convert_numbers', self.convert_numbers)
        un = kwargs.get('use_none', self.use_none)

        # Replace 'on' to work with eval() on per row entry
        if on:
            bl = evalctrl.blacklisted(on)
            if bl[0]:
                raise ValueError(f'FATAL@Table.join: Found blacklisted expression: [{bl[1]}]')

            for column in table.header:
                if column in on:
                    on = on.replace(column, 'tr[' + str(table.header.index(column)) + ']')
            for column in s_header:
                if column in on:
                    on = on.replace(column, 'tl[' + str(s_header.index(column)) + ']')
        else:
            on = 'True'                             # Will perform FULL JOIN

        # Best performance of eval():
        # https://mezzantrop.wordpress.com/2024/05/08/beating-eval-slowness-in-python
        efunc = eval(compile('lambda tl, tr:' + on, '<string>', 'eval'))

        r_table = []
        tl_match = []
        tr_match = []

        # Concatenate table headers as row[0] of the results table
        r_table.append(self.header + table.header)

        for c_tl, tl in enumerate(self.table):
            for c_tr, tr in enumerate(table.table):
                if mode == JOIN_FULL:
                    r_table.extend([tl + tr])
                else:
                    # Inner JOIN
                    if efunc(tl, tr):
                        r_table.extend([tl + tr])
                        tl_match.append(c_tl)
                        tr_match.append(c_tr)

        if mode == JOIN_LEFT:
            for it in range(0, self.rows):
                if it not in tl_match:
                    r_table.extend([self.table[it] + [None] * table.cols])
        if mode == JOIN_RIGHT:
            for it in range(0, table.rows):
                if it not in tr_match:
                    r_table.extend([[None] * self.cols + table.table[it]])

        if replace:
            # Replace source - self - with the joined Table
            return Table.import_list_lists(self, name=name if name else
                                           self.name + TNAME_TNAME_DELIMITER + table.name,
                                           data=r_table)
        # Return a new Table
        return Table(name=name if name
                     else self.name + TNAME_TNAME_DELIMITER + table.name, data=r_table,
                     convert_bool=cb, convert_numbers=cn, use_none=un)

    # -------------------------------------------------------------------------------------------- #
    def join_lt(self, table, scol, tcol, mode=JOIN_INNER, name='', replace=False, **kwargs):

        """
        Light, limited and safe Join, that doesn't use eval()
        :param table:       Table to join self with
        :param scol:        Self column to join on
        :param tcol:        Table column to join on
        :param mode:        Join mode
        :param name:        Give a name of the returned Table
        :param replace:     Replace source with the new data or not
        :return:            self
        """

        l_header = self.header
        r_header = table.header
        if kwargs.get('use_shortnames', self.use_shortnames):
            l_header = self.make_shortnames()
            r_header = table.make_shortnames()

        cb = kwargs.get('convert_bool', self.convert_bool)
        cn = kwargs.get('convert_numbers', self.convert_numbers)
        un = kwargs.get('use_none', self.use_none)

        rci = r_header.index(tcol) if tcol in r_header else None
        lci = l_header.index(scol) if scol in l_header else None

        if None in (lci, rci):
            return Table()

        r_table = []
        l_dict = {}
        r_dict = {}

        # Concatenate table headers as row[0] of the results table
        r_table.append(self.header + table.header)

        for tl in range(self.rows):
            if not l_dict.get(self.table[tl][lci]):
                l_dict[self.table[tl][lci]] = [self.table[tl]]
            else:
                l_dict[self.table[tl][lci]].append(self.table[tl])

        for tr in range(table.rows):
            if not r_dict.get(table.table[tr][rci]):
                r_dict[table.table[tr][rci]] = [table.table[tr]]
            else:
                r_dict[table.table[tr][rci]].append(table.table[tr])

        ldk = l_dict.keys()
        rdk = r_dict.keys()
        for lk in ldk:
            for rk in rdk:
                if lk == rk:
                    # Inner JOIN
                    for lv in l_dict[lk]:
                        for rv in r_dict[rk]:
                            r_table.append(lv + rv)
                    continue
                if mode in (JOIN_RIGHT, JOIN_FULL):
                    if rk not in ldk:
                        for rv in r_dict[rk]:
                            r_table.append([None] * self.cols + rv)
                    continue
            if mode in (JOIN_LEFT, JOIN_FULL):
                if lk not in rdk:
                    for lv in l_dict[lk]:
                        r_table.append(lv + [None] * table.cols)

        if replace:
            # Replace source - self - with the joined Table
            return Table.import_list_lists(self, name=name if name else
                                           self.name + TNAME_TNAME_DELIMITER + table.name,
                                           data=r_table)
        # Return a new Table
        return Table(name=name if name
                     else self.name + TNAME_TNAME_DELIMITER + table.name, data=r_table,
                     convert_bool=cb, convert_numbers=cn, use_none=un)

    # -------------------------------------------------------------------------------------------- #
    def select(self, columns='*', where='', name='', evalctrl=EvalCtrl(), **kwargs):

        """Select one or more columns from the Table if condition "where" is met.
        Return a new Table object

        :param columns:             Columns of the Table or '*' to return
        :param where:               Valid Python expression
        :param name:                Give a name of the returned Table
        :param evalctrl:            eval() controlling class
        :param **kwargs:
            :param use_shortnames   if True, Column names in Table header do not contain Table name
        :return:                    A new Table object
        """

        r_table = [[]]
        r_columns = []
        columns = self.header if columns == '*' else tssplit(columns, delimiter=', \t',
                                                             quote='', escape='', trim='',
                                                             remark='')

        header = self.header
        if kwargs.get('use_shortnames', self.use_shortnames):
            columns = self.make_shortnames(header=columns)
            header = self.make_shortnames()

        cb = kwargs.get('convert_bool', self.convert_bool)
        cn = kwargs.get('convert_numbers', self.convert_numbers)
        un = kwargs.get('use_none', self.use_none)

        if where:
            bl = evalctrl.blacklisted(where)
            if bl[0]:
                raise ValueError(f'FATAL@select: Found blacklisted expression: [{bl[1]}]')

        for column in columns:
            for _column in header:
                if _column in column:
                    c_idx = header.index(_column)
                    if where:
                        where = where.replace(_column, 'r[' + str(c_idx) + ']')
                    ev_column = column.replace(_column, 'r[' + str(c_idx) + ']')
                    r_columns.append(eval(compile('lambda r:' + ev_column, '<string>', 'eval'),
                                          self.globals))
                    r_table[0].append(column)

        if not where:
            where = 'True'

        efunc = eval(compile('lambda r:' + where, '<string>', 'eval'))

        return Table(name=name if name else
                     self.name + TNAME_TNAME_DELIMITER + str(self.timestamp),
                     data=r_table + [[sf(r) for sf in r_columns] for r in self.table if efunc(r)],
                     convert_bool=cb, convert_numbers=cn, use_none=un)

    # -------------------------------------------------------------------------------------------- #
    def select_lt(self, columns='*', where='', comp='==', val='', name='', **kwargs):

        """ eval()-free version of select()

        :param columns:             Columns of the Table or '*' to return
        :param where:               Column name
        :param comp:                Comparison or membership operator
        :param val:                 Value to compare with
        :param name:                Give a name of the returned Table
        :param **kwargs:
            :param use_shortnames   if True, Column names in Table header do not contain Table name
        :return:                    A new Table object
        """

        r_table = [[]]
        r_columns = []
        columns = self.header if columns in ('*', '') else tssplit(columns, delimiter=', \t',
                                                                   quote='', escape='', trim='',
                                                                   remark='')

        header = self.header
        if kwargs.get('use_shortnames', self.use_shortnames):
            columns = self.make_shortnames(header=columns)
            header = self.make_shortnames()

        cb = kwargs.get('convert_bool', self.convert_bool)
        cn = kwargs.get('convert_numbers', self.convert_numbers)
        un = kwargs.get('use_none', self.use_none)

        for column in header:
            if column in columns:
                r_table[0].append(column)
                r_columns.append(header.index(column))

        if not where or not comp or not val:
            return Table(name=name if name else
                         self.name + TNAME_TNAME_DELIMITER + str(self.timestamp),
                         data=r_table + [[r[c] for c in r_columns] for r in self.table],
                         convert_bool=cb, convert_numbers=cn, use_none=un)

        scol_idx = header.index(where)
        _type = type(val)
        return Table(name=name if name else
                     self.name + TNAME_TNAME_DELIMITER + str(self.timestamp),
                     data=r_table + [[r[c] for c in r_columns]
                                     for r in self.table
                                     if comp == '==' and _type(r[scol_idx]) == val or
                                     comp == '!=' and _type(r[scol_idx]) != val or
                                     comp == '>' and _type(r[scol_idx]) > val or
                                     comp == '<' and _type(r[scol_idx]) < val or
                                     comp == '>=' and _type(r[scol_idx]) >= val or
                                     comp == '<=' and _type(r[scol_idx]) <= val or
                                     comp == 'in' and _type(r[scol_idx]) in val or
                                     comp == 'not in' and _type(r[scol_idx]) not in val],
                     convert_bool=cb, convert_numbers=cn, use_none=un)

    # -------------------------------------------------------------------------------------------- #
    def order_by(self, column='', direction=ORDER_BY_INC, name='', **kwargs):

        """
        ORDER BY primitive of SQL SELECT

        :param column:          Order by this column
        :param direction:       Sort direction ORDER_BY_INC/ORDER_BY_DEC to specify sorting order
        :param name:            Give a new name for the returned Table
        :param **kwargs:
            :param use_shortnames   if True, Column names in Table header do not contain Table name
        :return:            A new Table object
        """

        header = self.header
        if kwargs.get('use_shortnames', self.use_shortnames):
            header = self.make_shortnames()

        cb = kwargs.get('convert_bool', self.convert_bool)
        cn = kwargs.get('convert_numbers', self.convert_numbers)
        un = kwargs.get('use_none', self.use_none)

        # Extract a column referenced by order_by and sort it
        sl = [(self.table[r][header.index(column)], r) for r in range(self.rows)]
        sl.sort()
        if direction != ORDER_BY_INC:               # Assuming the decreasing order is desired
            sl = sl[::-1]

        return Table(name=name if name else
                     self.name + TNAME_TNAME_DELIMITER + str(self.timestamp),
                     data=[self.header] + [[self.table[r[1]][c]
                                            for c in range(self.cols)] for r in sl],
                     convert_bool=cb, convert_numbers=cn, use_none=un)

    # -------------------------------------------------------------------------------------------- #
    def group_by(self, column='', function=None, ftarget=None, name='', **kwargs):

        """
        GROUP BY primitive of SQL SELECT

        :param column:              Group by this column
        :param function:            Aggregate function to apply
        :param ftarget:             Column to apply aggregate function
        :param name:                Give a new name for the returned Table
        :param **kwargs:
            :param use_shortnames   if True, Column names in Table header do not contain Table name
        :return:                    A new Table object
        """

        if not ftarget or not function:
            return Table(name=name if name else
                     self.name + TNAME_TNAME_DELIMITER + str(self.timestamp), data=self.table)

        header = self.header
        if kwargs.get('use_shortnames', self.use_shortnames):
            header = self.make_shortnames()

        cb = kwargs.get('convert_bool', self.convert_bool)
        cn = kwargs.get('convert_numbers', self.convert_numbers)
        un = kwargs.get('use_none', self.use_none)

        gd = {r[header.index(column)]: function(r[header.index(ftarget)])
              for r in self.table}

        return Table(name=name if name else
                     self.name + TNAME_TNAME_DELIMITER + str(self.timestamp),
                     data=[[column, ftarget]] + [[k, v] for k, v in gd.items()],
                     convert_bool=cb, convert_numbers=cn, use_none=un)

    # -------------------------------------------------------------------------------------------- #
    def column_map(self, column='', function=None, name='', **kwargs):

        """
        Apply a function to a column
        """

        if not function:
            return Table(name=name if name else
                     self.name + TNAME_TNAME_DELIMITER + str(self.timestamp), data=self.table)

        header = self.header
        if kwargs.get('use_shortnames', self.use_shortnames):
            header = self.make_shortnames()

        cb = kwargs.get('convert_bool', self.convert_bool)
        cn = kwargs.get('convert_numbers', self.convert_numbers)
        un = kwargs.get('use_none', self.use_none)

        try:
            col = -1
            if column != '*':
                col = header.index(column)
        except ValueError:
            return Table()

        return Table(name=name if name else
                     self.name + TNAME_TNAME_DELIMITER + str(self.timestamp),
                     data=[self.header] +
                        [[function(r[c]) if c == col or column == '*' else
                            r[c] for c in range(self.cols)] for r in self.table],
                     convert_bool=cb, convert_numbers=cn, use_none=un)

# -- MAIN starts here ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    print(f'tSQLike (https://github.com/mezantrop/tSQLike) version: {__version__}\n\n')
    print('This is a Python3 library module.')
    print('To use tSQLike in the code, import it:\n\nfrom tsqlike import tsqlike')
