from .parse import (
    parse_comment_line,
    parse_section_line,
    parse_generic_line
)

class SummarySection(object):
    
    def __init__(self, parse_keys, optional_keys=[], name_map={}, is_comment=False, last_item_any_char=False):
        self.parse_keys = parse_keys
        self.optional_keys = optional_keys
        self.name_map = name_map
        self.is_comment = is_comment
        self.last_item_any_char = last_item_any_char
        self.entries = []

    def __repr__(self):
        return f'SummarySection(n={len(self.entries)})'

    def parse(self, line):
        if self.is_comment:
            d = parse_comment_line(line)
        elif self.last_item_any_char:
            d = parse_section_line(line, self.parse_keys[-1])
        else:
            d = parse_generic_line(line)
        for key in self.optional_keys:
            if key not in d:
                d[key] = None
        self.parse_check(d)
        return d

    def parse_check(self, d):
        if set(d) != set(self.parse_keys):
            raise ValueError(f'Expected {set(self.parse_keys)}, got {set(d)}')

    def add(self, line, extra_entries=None):
        d = self.parse(line)
        if self.name_map:
            d = {new: d[old] for old, new in self.name_map.items() if new}
        if extra_entries:
            d.update(extra_entries)
        if hasattr(self, 'expand_entry'):
            d = self.expand_entry(d)
        self.entries.append(d)
