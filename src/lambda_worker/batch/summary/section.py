from .parse import (
    parse_comment_line,
    parse_section_line,
    parse_generic_line
)

class SummarySection(object):
    
    def __init__(self, keys, is_comment=False, last_item_any_char=False):
        self.keys = keys
        self.is_comment = is_comment
        self.last_item_any_char = last_item_any_char
        self.entries = []
        self.keys_set = set(keys)

    def __repr__(self):
        return f'SummarySection(n={len(self.entries)})'

    def parse(self, line):
        if self.is_comment:
            return parse_comment_line(line, self.keys_set)
        if self.last_item_any_char:
            return parse_section_line(line, self.keys[-1], self.keys_set)
        return parse_generic_line(line, self.keys_set)

    def add(self, line, extra_entries=None):
        d = self.parse(line)
        if extra_entries:
            d.update(extra_entries)
        self.entries.append(d)
