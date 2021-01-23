from .parse import parse_section_line

class SummarySection(object):
    
    def __init__(self, name, keys, add_sra=False, last_item_any_char=False):
        self.name = name
        self.keys = keys
        self.add_sra = add_sra
        self.last_item_any_char = last_item_any_char
        self.entries = []
        self.keys_set = set(keys)

    def __repr__(self):
        return f'SummarySection(name={self.name}, entries={len(self.entries)})'

    def parse(self, line):
        return parse_section_line(line, self.keys[-1], self.keys_set)

    def add(self, line, extra_entries=None):
        d = self.parse(line)
        if extra_entries:
            d.update(extra_entries)
        self.entries.append(d)
