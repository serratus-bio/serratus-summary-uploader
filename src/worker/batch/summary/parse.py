import io

INT_KEYS = {'score', 'pctid', 'aln', 'glb', 'len', 'topscore', 'toplen'}
INT_KEYS |= {'readlength', 'totalalns'} # protein summary comment
INT_KEYS |= {'alns', 'avgcols'} # protein summary lines
DBL_KEYS = {'depth'}

def parse_summary(summary):
    prefix = summary.line_prefix_ignore
    try:
        with io.StringIO(summary.text) as fs:
            line = get_next_line(fs, prefix)
            for name, section in summary.sections.items():
                # comment is first section, single line
                if section.is_comment:
                    section.add(line)
                    summary.run_id = section.entries[0]['run_id']
                    line = get_next_line(fs, prefix)
                    continue
                while line.startswith(section.parse_keys[0]):
                    extra_entries = {
                        'run_id': summary.run_id
                    }
                    section.add(line, extra_entries)
                    line = get_next_line(fs, prefix)
            try:
                next(fs)
                raise ValueError('Did not parse all lines! Check section keys.')
            except StopIteration:
                pass # expected
    except StopIteration:
        return

def parse_comment_line(line):
    d = dict([pair.split('=') for pair in
        line.replace('SUMZER_COMMENT=', '')
        .rstrip(';\n')
        .replace(';', ',')
        .split(',')])
    cast_types(d)
    return d

def parse_section_line(line, last_key):
    # there can be ';' and '=' in the last entry, type string
    last_key_index = line.index(last_key)
    d1 = parse_generic_line(line[:last_key_index])
    d2 = dict([line[last_key_index:].strip(';\n').split('=', maxsplit=1)])
    d1.update(d2)
    return d1

def parse_generic_line(line):
    d = dict([pair.split('=') for pair in line.rstrip(';\n').split(';')])
    cast_types(d)
    return d

def cast_types(d):
    for key in d:
        if key in INT_KEYS:
            d[key] = int(d[key])
        elif key in DBL_KEYS:
            d[key] = float(d[key])

# hack to remove prefix from each line in psummary
def get_next_line(fs, prefix):
    line = next(fs)
    if prefix:
        if not line.startswith(prefix):
            raise ValueError(f'Line does not start with "{prefix}": {line}')
        return line[len(prefix):]
    return line