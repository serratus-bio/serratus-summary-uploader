import io

COMMENT_KEYS = {'readlength', 'sra', 'genome', 'version', 'date'}
FAM_KEYS = {'famcvg', 'fam', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'top', 'topscore', 'toplen', 'topname'}
SEQ_KEYS = {'seqcvg', 'seq', 'score', 'pctid', 'depth', 'aln', 'glb', 'len', 'family', 'name'}
INT_KEYS = {'score', 'pctid', 'aln', 'glb', 'len', 'topscore', 'toplen'}
DBL_KEYS = {'depth'}

def parse_summary(summary):
    try:
        with io.StringIO(summary.text) as fs:
            comment_line = next(fs)
            summary.props = parse_comment_line(comment_line)
            summary.run_id = summary.props['sra']
            line = next(fs)
            while line.startswith('famcvg'):
                d = parse_family_line(line)
                d['run'] = summary.run_id
                summary.fams.append(d)
                line = next(fs)
            while line.startswith('seqcvg'):
                d = parse_sequence_line(line)
                d['run'] = summary.run_id
                summary.seqs.append(d)
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
        raise ValueError(f'Expected {SEQ_KEYS}, got {set(d1)}')
    return d

def parse_generic_line(line):
    d = dict([pair.split('=') for pair in line.rstrip(';\n').split(';')])
    for key in d:
        if key in INT_KEYS:
            d[key] = int(d[key])
        elif key in DBL_KEYS:
            d[key] = float(d[key])
    return d

def parse_family_line(line):
    # there can be ';' and '=' in the last entry (topname)
    name_index = line.index('topname=')
    d1 = parse_generic_line(line[:name_index])
    d2 = dict([line[name_index:].strip(';\n').split('=', maxsplit=1)])
    d1.update(d2)
    if (set(d1) != FAM_KEYS):
        raise ValueError(f'Expected {SEQ_KEYS}, got {set(d1)}')
    return d1

def parse_sequence_line(line):
    # there can be ';' and '=' in the last entry (name)
    name_index = line.index('name=')
    d1 = parse_generic_line(line[:name_index])
    d2 = dict([line[name_index:].strip(';\n').split('=', maxsplit=1)])
    d1.update(d2)
    if (set(d1) != SEQ_KEYS):
        raise ValueError(f'Expected {SEQ_KEYS}, got {set(d1)}')
    return d1
