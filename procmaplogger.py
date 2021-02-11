import sys
from pathlib import Path
import datetime


class MapLine:

    def __init__(self):
        self.start = 0
        self.end = 0
        self.size = 0
        self.permissions = 0
        self.inode = 0
        self.path = ''

    def set_address(self, address):
        address = address.split('-')
        self.start = int(address[0], 16)
        self.end = int(address[1], 16)
        self.size = self.end - self.start

    @staticmethod
    def from_line(line):
        tokens = line.strip().split(' ')
        mapline = MapLine()
        mapline.set_address(tokens[0])
        mapline.permissions = tokens[1]
        mapline.inode = int(tokens[4])
        if len(tokens) > 4:
            mapline.path = ''.join(tokens[5:]).strip()
        return mapline


def write_summary(summary, outfile):
    for path, summary in summary_by_path.items():
        summary_line = '{:>5}\t{:>12}\t{}'.format(summary[1], summary[0], path)
        print(summary_line, file=outfile)


if __name__ == '__main__':
    summary_by_path = dict()

    for line in sys.stdin:
        mapline = MapLine.from_line(line)

        try:
            (currentsize, pagecount) = summary_by_path[mapline.path]
        except KeyError:
            currentsize = 0
            pagecount = 0

        currentsize += mapline.size
        pagecount += 1
        summary_by_path[mapline.path] = (currentsize, pagecount)

    write_summary(summary_by_path, sys.stdout)

    try:
        write_to_file = (sys.argv[1] == '-f')
    except IndexError:
        write_to_file = False

    if write_to_file:
        folder = Path(sys.argv[2])
        folder.mkdir(exist_ok=True, parents=True)
        timetoken = datetime.datetime.now()
        outfile = folder / 'summary_{}.txt'.format(timetoken.isoformat())
        with outfile.open('w') as f:
            write_summary(summary_by_path, f)
