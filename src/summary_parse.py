def parse(summary, fs):
    comment_line = next(fs)
    summary.properties = parse_comment_line(comment_line)
    summary.run_id = summary.properties['sra']
    line = next(fs)
    summary.families = []
    while line.startswith('famcvg'):
        d = parse_family_line(line)
        d['run'] = summary.run_id
        summary.families.append(d)
        line = next(fs)
    summary.sequences = []
    while line.startswith('seqcvg'):
        d = parse_sequence_line(line)
        d['run'] = summary.run_id
        summary.sequences.append(d)
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
    # there can be ';' and '=' in the last entry (name)
    name_index = line.index('name=')
    d1 = parse_generic_line(line[:name_index])
    d2 = dict([line[name_index:].strip(';\n').split('=', maxsplit=1)])
    d1.update(d2)
    return d1
