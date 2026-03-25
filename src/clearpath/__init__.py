# ====================================================================
# WHAT IS THIS FILE?
# This file is called "__init__.py" (that's two underscores on each side).
#
# In Python, a regular folder is just a folder. But if you put a file
# called __init__.py inside a folder, Python treats that folder as a
# "package" — meaning other Python code can IMPORT things from it.
#
# ANALOGY: Think of __init__.py as a "OPEN" sign on a store. Without
# the sign (this file), Python walks right past the folder and doesn't
# know there's code inside it can use.
#
# This particular __init__.py is for the "clearpath" package — the
# main package that contains ALL of the ClearPath Health source code.
#
# WHY IS IT (MOSTLY) EMPTY?
# It doesn't need much code. Just existing is enough to tell Python
# "hey, this folder is a package you can import from." We just put
# the project version here so it's easy to find.
# ====================================================================

# This is the version number for the entire ClearPath Health project.
# We follow "semantic versioning": MAJOR.MINOR.PATCH
# - MAJOR = big breaking changes (we're at 0 because it's not released yet)
# - MINOR = new features added
# - PATCH = small bug fixes
__version__ = "0.1.0"
