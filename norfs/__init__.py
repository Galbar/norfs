class Version:
    MAJOR: str = "1"
    MINOR: str = "3"
    PATCH: str = "2"

    VERSION: str = ".".join((MAJOR, MINOR))
    RELEASE: str = ".".join((MAJOR, MINOR, PATCH))
