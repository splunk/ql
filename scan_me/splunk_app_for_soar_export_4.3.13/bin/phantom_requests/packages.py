import sys

try:
    import chardet
except ImportError:
    import warnings

    import charset_normalizer as chardet

    warnings.filterwarnings("ignore", "Trying to detect", module="charset_normalizer")

# This code exists for backwards compatibility reasons.
# I don't like it either. Just look the other way. :)

for package in ("urllib3", "idna"):
    locals()[package] = __import__(package)
    # This traversal is apparently necessary such that the identities are
    # preserved (requests.packages.urllib3.* is urllib3.*)
    for mod in list(sys.modules):
        if mod == package or mod.startswith("{}.".format(package)):
            sys.modules["requests.packages.{}".format(mod)] = sys.modules[mod]

target = chardet.__name__
for mod in list(sys.modules):
    if mod == target or mod.startswith("{}.".format(target)):
        target = target.replace(target, "chardet")
        sys.modules["requests.packages.{}".format(target)] = sys.modules[mod]
# Kinda cool, though, right?
