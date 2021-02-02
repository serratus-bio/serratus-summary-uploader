from .parse import (
    parse_comment_line,
    parse_section_line,
    parse_generic_line
)

class SummarySection(object):
    
    def __init__(self, parse_keys, name_map={}, is_comment=False, last_item_any_char=False):
        self.parse_keys = parse_keys
        self.name_map = name_map
        self.is_comment = is_comment
        self.last_item_any_char = last_item_any_char
        self.entries = []
        self.parse_keys_set = set(parse_keys)

    def __repr__(self):
        return f'SummarySection(n={len(self.entries)})'

    def parse(self, line):
        if self.is_comment:
            return parse_comment_line(line, self.parse_keys_set)
        if self.last_item_any_char:
            return parse_section_line(line, self.parse_keys[-1], self.parse_keys_set)
        return parse_generic_line(line, self.parse_keys_set)

    def add(self, line, extra_entries=None):
        d = self.parse(line)
        if self.name_map:
            d = {new: d[old] for old, new in self.name_map.items() if new}
        if extra_entries:
            d.update(extra_entries)
        if hasattr(self, 'expand_entry'):
            d = self.expand_entry(d)
        self.entries.append(d)
