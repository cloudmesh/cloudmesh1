"""Prints tables in html, text, or with right alighned columns"""


class cm_table:

    """
    Class to print a table in various formats.

    ::

      format = HTML | ASCII | "%20s"

    type is not used and wil be in future removed

    ::

      columns = number of columns

    structure is an array of rows

    ::

      header = True the firts row is a headline
    """

    _content = ""

    def __init__(self):
        self._content = ""
        return

    def __str__(self):
        return self._content

    #
    # TODO: change format as it is predifined function
    # TODO: change type as it is predefined function
    #
    def create(self, structure, columns, format=None, type=None, header=True):
        """ creates a table from a list of rows, where the row is also
        a list. The format can be specified and may be HTML | ASCII |
        formatstring. A format string may for example be '%20s' which
        prints the string in a field 20 spaces wide.  """

        self._content = self._begin(format)

        # Create header
        line = ""
        for col in columns:
            line += str(self._cell(str(col), format))
        self._content += self._row(line, format)

        # Create Rows
        for element in structure.items():
            attributes = element[1]
            line = ""
            for col in columns:
                line += self._cell(str(attributes[col]), format)
            self._content += self._row(line, format)
        self._content += self._end(format)

    def _begin(self, format=None):
        if format == 'HTML':
            return '<table>\n'
        return ""

    def _end(self, format=None):
        if format == 'HTML':
            return str('</table>\n')
        return ""

    def _cell(self, value, format=None):
        if format is None or format == 'ASCII':
            return value + ' '
        if format.startswith('%'):
            field = format % value
            return field
        if format == 'HTML':
            return '<td>' + value + '</td>'
        return ""

    def _row(self, value, format=None):
        if format is None or format == 'ASCII' or format.startswith('%'):
            return value + '\n'
        if format == 'HTML':
            return '    <tr>' + value + '</tr>\n'
        return ""
