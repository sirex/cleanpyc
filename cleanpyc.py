import os
import logging

COMPILED_SUFFIXES = '.pyc', '.pyo'


def filter_dirnames(path, dirnames):
    for name in dirnames:
        if '__pycache__' == name:
            # Do not recurse in there: we would end up removing all pyc
            # files because the main loop checks for py files in the same
            # directory. Besides, stale pyc files in __pycache__ are
            # harmless, see PEP-3147 for details (sourceless imports
            # work only when pyc lives in the source dir directly).
            continue
        elif not os.path.join(path, name, '__init__.py'):
            continue
        else:
            yield name


def remove_stale_bytecode(path):
    log = logging.getLogger(__name__)
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = filter_dirnames(dirpath, dirnames)
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            pyfile = name + '.py'
            if ext in COMPILED_SUFFIXES and pyfile not in filenames:
                stalepath = os.path.join(dirpath, filename)
                log.info("Removing stale bytecode file %s" % stalepath)
                os.unlink(stalepath)
