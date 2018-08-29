class Version:
    MAJOR: str = "2"
    MINOR: str = "0"
    PATCH: str = "1"

    VERSION: str = ".".join((MAJOR, MINOR))
    RELEASE: str = ".".join((MAJOR, MINOR, PATCH))
