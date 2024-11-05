# Copyright (c) 2024, InfinityQ Technology, Inc.
from typing import Any, Generator, Optional

from .options import MPSParseOptions
from .section_parser import (
    BoundParser,
    ColumnParser,
    EndataParser,
    NameParser,
    QuadobjParser,
    RangesParser,
    RhsParser,
    RowsParser,
    SectionParser
)
from .utils import SectionType


class SectionReader:
    """
    Reads an MPS file and generate section by section with
    the method sections()
    """
    def __init__(self, path: str, options: MPSParseOptions) -> None:
        self._path = path
        self._options = options


    def _new_section(self, line: str) -> Optional[SectionType]:
        """returns a section if encountered a new one, returns None otherwise"""
        # an exception for NAME, where the value is on the same line
        if line.startswith(SectionType.NAME):
            return SectionType.NAME

        for section in [section.value for section in SectionType]:
            if line == section:
                return section
        return None


    def sections(self) -> Generator[SectionParser, Any, Any]:
        """generate sections by yielding one at a time"""
        current_section = None
        lines = []

        # open context manager is already lazy loading, since
        # the file is line-based. This way it loads into memory by chunks
        with open(self._path, 'r') as file:
            line_numer = 1
            for line in file:
                line = line.strip() # always strip the line

                if self._options.empty_line_check(line_numer, line):
                    continue

                new_section = self._new_section(line)
                if new_section is not None:
                    if current_section == SectionType.ROWS:
                        yield RowsParser(lines)
                    elif current_section == SectionType.COLUMNS:
                        yield ColumnParser(lines)
                    elif current_section == SectionType.RHS:
                        yield RhsParser(lines)
                    elif current_section == SectionType.RANGES:
                        yield RangesParser(lines)
                    elif current_section == SectionType.BOUNDS:
                        yield BoundParser(lines)
                    elif current_section == SectionType.QUADOBJ:
                        yield QuadobjParser(lines, SectionType.QUADOBJ)
                    # same as QUADOBJ, but QMATRIX specifies each entry of the matrix
                    elif current_section == SectionType.QMATRIX:
                        yield QuadobjParser(lines, SectionType.QMATRIX)

                    # NAME and ENDATA yield immediatly
                    if new_section == SectionType.NAME:
                        yield NameParser([line])
                    elif new_section == SectionType.ENDATA:
                        yield EndataParser([line])
                        break # end of file, stop here

                    lines = []
                    current_section = new_section
                else:
                    lines.append(line) # just add the line

                line_numer += 1

