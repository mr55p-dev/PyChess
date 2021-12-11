from .constants import BLACK, WHITE, USE_CPP
if USE_CPP:
    import sys
    sys.path.append("vendor/pychessbinds/build-release")
