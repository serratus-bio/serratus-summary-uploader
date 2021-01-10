class Summary(object):

    properties = None
    families = None
    sequences = None
    id = None

    def __init__(self, fs):
        comment_line = next(fs)
        self.properties = parse_comment_line(comment_line)
        self.id = self.properties['sra']
        line = next(fs)
        self.families = []
        while line.startswith('famcvg'):
            d = parse_family_line(line)
            d['run'] = self.id
            self.families.append(d)
            line = next(fs)
        self.sequences = []
        while line.startswith('seqcvg'):
            d = parse_sequence_line(line)
            d['run'] = self.id
            self.sequences.append(d)
            try:
                line = next(fs)
            except StopIteration:
                break


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
    # there can be ';' in the last entry (name)
    d1 = parse_generic_line(line[:line.index('name=')])
    d2 = dict([line[line.index('name='):].strip(';\n').split('=')])
    d1.update(d2)
    return d1

