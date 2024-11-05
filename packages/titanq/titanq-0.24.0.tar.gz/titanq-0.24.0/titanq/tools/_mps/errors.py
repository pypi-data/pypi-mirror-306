# Copyright (c) 2024, InfinityQ Technology, Inc.

"""Some exceptions that can be raised while parsing MPS files"""

class MPSFileError(Exception):
    """Errors related to .mps files"""

class MPSMissingValueError(Exception):
    """A required value is missing"""

class MPSMissingSectionError(Exception):
    """A required section is missing"""

class MPSMalormedFileError(Exception):
    """The file is malformed"""

class MPSUnexpectedValueError(Exception):
    """Found an unexpected value"""

class MPSUnsupportedError(Exception):
    """Found an unsupported value"""
