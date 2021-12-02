from heartrate import trace, files
trace(files = files.path_contains('Chess'), host='0.0.0.0', port='7777', browser=True)

from Chess import Board

b = Board()
b.calculate()
