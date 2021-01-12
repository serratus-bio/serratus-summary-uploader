import io
from summary_download import get_summary_text

class Summary(object):

    properties = None
    families = None
    sequences = None
    run_id = None

    def __init__(self, run_id):
        self.run_id = run_id
        summary_text = get_summary_text(run_id)
        self._parse(io.StringIO(summary_text))

    def _parse(self, fs):
        comment_line = next(fs)
        self.properties = parse_comment_line(comment_line)
        self.run_id = self.properties['sra']
        line = next(fs)
        self.families = []
        while line.startswith('famcvg'):
            d = parse_family_line(line)
            d['run'] = self.run_id
            self.families.append(d)
            line = next(fs)
        self.sequences = []
        while line.startswith('seqcvg'):
            d = parse_sequence_line(line)
            d['run'] = self.run_id
            self.sequences.append(d)
            try:
                line = next(fs)
            except StopIteration:
                break

    def __str__(self):
        return self.run_id


def parse_comment_line(line):
    return dict([pair.split('=') for pair in
        line.replace('SUMZER_COMMENT=', '')
        .rstrip(';\n')
        .replace(';', ',')
        .split(',')])


def parse_generic_line(line):
    return dict([pair.split('=') for pair in line.rstrip(';\n').split(';')])


def parse_family_line(line):
    return parse_generic_line(line)


def parse_sequence_line(line):
    # there can be ';' and '=' in the last entry (name)
    name_index = line.index('name=')
    d1 = parse_generic_line(line[:name_index])
    d2 = dict([line[name_index:].strip(';\n').split('=', maxsplit=1)])
    d1.update(d2)
    return d1
