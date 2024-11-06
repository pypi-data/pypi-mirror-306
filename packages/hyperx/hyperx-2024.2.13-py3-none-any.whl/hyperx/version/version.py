major = 2024
minor = 2
revision = 13
patch = 0

if patch != 0:
    __version__ = ".".join([str(major), str(minor), str(revision), str(patch)])
else:
    __version__ = ".".join([str(major), str(minor), str(revision)])
