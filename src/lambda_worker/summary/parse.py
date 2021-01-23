import io

COMMENT_KEYS = {'readlength', 'sra', 'genome', 'version', 'date'}
INT_KEYS = {'score', 'pctid', 'aln', 'glb', 'len', 'topscore', 'toplen'}
DBL_KEYS = {'depth'}

def parse_summary(summary):
    try:
        with io.StringIO(summary.text) as fs:
            line = next(fs)
            summary.props = parse_comment_line(line)
            summary.sra_id = summary.props['sra']
            line = next(fs)
            for name, section in summary.sections.items():
                while line.startswith(section.keys[0]):
                    extra_entries = {
                        'sra': summary.sra_id
                    }
                    section.add(line, extra_entries)
                    line = next(fs)
    except StopIteration:
        return

def parse_comment_line(line):
    d = dict([pair.split('=') for pair in
        line.replace('SUMZER_COMMENT=', '')
        .rstrip(';\n')
        .replace(';', ',')
        .split(',')])
    if (set(d) != COMMENT_KEYS):
        raise ValueError(f'Expected {COMMENT_KEYS}, got {set(d1)}')
    return d

def parse_section_line(line, last_key, expected_keys):
    # there can be ';' and '=' in the last entry
    last_key_index = line.index(last_key)
    d1 = parse_generic_line(line[:last_key_index])
    d2 = dict([line[last_key_index:].strip(';\n').split('=', maxsplit=1)])
    d1.update(d2)
    if (set(d1) != expected_keys):
        raise ValueError(f'Expected {expected_keys}, got {set(d1)}')
    return d1


def parse_generic_line(line):
    d = dict([pair.split('=') for pair in line.rstrip(';\n').split(';')])
    for key in d:
        if key in INT_KEYS:
            d[key] = int(d[key])
        elif key in DBL_KEYS:
            d[key] = float(d[key])
    return d
