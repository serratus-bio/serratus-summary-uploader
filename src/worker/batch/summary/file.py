from io import StringIO
import urllib
import time
from typing import Dict
from .file_parse import get_next_line
from .file_section import SummaryFileSection


class SummaryFile(object):
    """Represents a summary file.

    The file format is described in:
    https://github.com/ababaian/serratus/wiki/.summary-Reports
    """

    def __init__(self, run_id):
        self.run_id = run_id

        # The following are set by specific implementations.
        self.text: str = None
        self.sections: Dict[str, SummaryFileSection] = {}
        self.line_prefix_ignore: str = None

        self.parsed = False

    def set_text(self, bucket, prefix, suffix, max_retries = 5):
        """Get the text of a summary file from S3."""
        url = f'https://s3.amazonaws.com/{bucket}/{prefix}{self.run_id}{suffix}'
        retry_count = 0
        while retry_count < max_retries:
            try:
                file_response = urllib.request.urlopen(url)
                self.text = file_response.read().decode('utf-8')
                return
            except (ConnectionResetError, urllib.error.URLError):
                retry_count += 1
                time.sleep(2 ** retry_count)

        raise Exception(f"Failed to retrieve contents of summary file at <{url}>.")

    def parse(self):
        """Parse the file with a top-level exception handler."""
        # The text should already be populated.
        assert self.text is not None

        try:
            self._parse_raising_errors()
            self.parsed = True
        except Exception as e:
            raise ValueError(f'Failed to parse {self.run_id}: {e!r}') from e
        
    def _parse_raising_errors(self):
        """Parse the file and raise any exceptions."""
        # Wrap all occurrences of get_next_line in a try/except to handle when
        # the end of file is reached.
        try:
            with StringIO(self.text) as fs:
                # Start with the first line.
                line = get_next_line(fs, self.line_prefix_ignore)

                for name, section in self.sections.items():
                    if section.is_comment:
                        # Comment is always the first section and only a single line.
                        assert section.entries == []
                        section.parse_and_add(line)

                        # Retrieve the run_id from the comment section.
                        self.run_id = section.entries[0]['run_id']

                        line = get_next_line(fs, self.line_prefix_ignore)
                        continue

                    while line.startswith(section.parse_keys[0]):
                        # Include the run_id as an extra entry.
                        extra_entries = {
                            'run_id': self.run_id
                        }
                        section.parse_and_add(line, extra_entries)
                        line = get_next_line(fs, self.line_prefix_ignore)

                # If all sections have been exhausted, make sure we have reached the end of the file.
                # FIXME: this should be handled only once, not twice
                try:
                    next(fs)
                    raise ValueError('Did not parse all lines! Check section keys.')
                except StopIteration:
                    pass

        except StopIteration:
            # Expected end of file
            return

    def __repr__(self):
        if self.parsed:
            section_info = ''.join(self.sections)
            return f'SummaryFile(run_id={self.run_id}, sections={"todo"})'
        return f'SummaryFile(run_id={self.run_id})'
