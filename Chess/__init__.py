from .constants import USE_CPP
if USE_CPP:
    import sys
    sys.path.append("vendor/pychessbinds/build-release")
    sys.path.append("vendor/pychessbinds/build")
