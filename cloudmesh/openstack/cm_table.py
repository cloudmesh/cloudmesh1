
class table:

    content = ""

    def __init__(self):
        self.content = ""
        return

    def __str__(self):
        return self.content

    def create(self, structure, columns, format=None, type=None, header=True):
        self.content = self._begin(format)

        # Create header
        line = ""
        for col in columns:
            line += str(self._cell(str(col), format))
        self.content += self._row(line, format)

        # Create Rows
        for element in structure.items():
            attributes = element[1]
            line = ""
            for col in columns:
                line += self._cell(str(attributes[col]), format)
            self.content += self._row(line, format)
        self.content += self._end(format)

    def _begin(self, format=None):
        if format == 'HTML':
            return '<table>\n'
        return ""

    def _end(self, format=None):
        if format == 'HTML':
            return str('</table>\n')
        return ""

    def _cell(self, value, format=None):
        if format == None or format == 'ASCII':
            return value + ' '
        if format.startswith('%'):
            field = format % value
            return field
        if format == 'HTML':
            return '<td>' + value + '</td>'
        return ""

    def _row(self, value, format=None):
        if format == None or format == 'ASCII' or format.startswith('%'):
            return value + '\n'
        if format == 'HTML':
            return '    <tr>' + value + '</tr>\n'
        return ""
