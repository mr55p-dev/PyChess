"""I, Ellis Lunnon, have read and understood the School's Academic Integrity Policy, as well as guidance relating to this
module, and confirm that this submission complies with the policy. The content of this file is my own original work,
with any significant material copied or adapted from other sources clearly indicated and attributed."""
from .constants import USE_CPP
if USE_CPP:
    import sys
    sys.path.append("vendor/pychessbinds/build-release")
    sys.path.append("vendor/pychessbinds/build")
