class Version:
    MAJOR: str = "3"
    MINOR: str = "1"
    PATCH: str = "0"

    VERSION: str = ".".join((MAJOR, MINOR))
    RELEASE: str = ".".join((MAJOR, MINOR, PATCH))
