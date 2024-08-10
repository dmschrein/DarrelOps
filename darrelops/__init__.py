"""
Top-level package for DarrelOps.
"""
# darrelops/__init__.py

__app_name__ = "darrelops"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    REG_ERROR,
    ART_READ_ERROR, 
    ART_WRITE_ERROR,
    JSON_ERROR,
) = range(6)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    REG_ERROR: "program registration error",
    ART_READ_ERROR: "artifactory read error",
    ART_WRITE_ERROR: "artifactory write error",
}


