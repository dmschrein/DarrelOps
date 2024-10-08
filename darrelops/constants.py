"""Constants file"""


(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    REG_ERROR,
    ART_READ_ERROR, 
    ART_WRITE_ERROR,
    JSON_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    REG_ERROR: "program registration error",
    ART_READ_ERROR: "artifactory read error",
    ART_WRITE_ERROR: "artifactory write error",
}
