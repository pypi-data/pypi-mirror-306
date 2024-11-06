"""Enable importing of binary extensions from ZIP files.

This module extends Python's zipimport mechanism to support loading binary
extension modules (.so/.pyd files) directly from ZIP archives without
extracting them to temporary files first.
"""

import sys
import os
import tempfile
from zipimport import zipimporter
from importlib.machinery import (
    EXTENSION_SUFFIXES,
    ModuleSpec,
    ExtensionFileLoader
)


class ExtensionFilelessLoader(ExtensionFileLoader):
    """In-memory extension module loader """

    def __init__(self, name, path, binary):
        super().__init__(name, path)
        self.binary = binary

    def create_module(self, spec):
        # Debugging hint. May appear in /proc/PID/smaps and similar places.
        namehint = os.path.basename(spec.origin)
        try:                                    # Linux-specific
            f = os.fdopen(os.memfd_create(namehint), 'w+b')
            loadpath = '/proc/self/fd/{}'.format(f.fileno())
        except (AttributeError, OSError):       # Portable fallback
            f = tempfile.NamedTemporaryFile(mode='w+b', suffix='-' + namehint)
            loadpath = f.name

        with f:
            f.write(self.binary)
            f.flush()
            spec2 = ModuleSpec(spec.name, self, origin=loadpath)
            mod = super().create_module(spec2)
            mod.__file__ = spec.origin          # the/inside.zip/pathname
            return mod


class zipextimporter(zipimporter):
    """Extended zipimporter supporting binary extension modules."""

    def _find_extension_loader(self, name):
        """Locate extension module and create its loader if found."""
        for suffix in EXTENSION_SUFFIXES:
            basename = name.rpartition('.')[2] + suffix
            relpath = os.path.join(self.prefix, basename)
            fullpath = os.path.join(self.archive, relpath)
            try:
                binary = self.get_data(relpath)
                return ExtensionFilelessLoader(name, fullpath, binary)
            except IOError:
                continue

    def find_spec(self, name, target=None):
        loader = self._find_extension_loader(name)
        if not loader:
            return super().find_spec(name)
        return ModuleSpec(name, loader, origin=loader.path)

    # For compatibility with older versions:

    def find_module(self, name):
        loader = self._find_extension_loader(name)
        if not loader:
            return super().find_module(name)
        return self

    def find_loader(self, name):
        loader = self._find_extension_loader(name)
        if not loader:
            return super().find_loader(name)
        return loader, []

    try:
        zipimporter.find_spec
    except AttributeError:
        del find_spec  # Cannot fall back to super() if not present


def install():
    """Install the extended ZIP importer system-wide."""

    while zipimporter in sys.path_hooks:
        sys.path_hooks[sys.path_hooks.index(zipimporter)] = zipextimporter
    for k, v in list(sys.path_importer_cache.items()):
        if isinstance(v, zipimporter) and not isinstance(v, zipextimporter):
            del sys.path_importer_cache[k]


install()
