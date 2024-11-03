This module offers a class that combines pathlib.Path, os.walk,
cached os.struct_stat, debug/trace logging, and the ability to execute
a --dry-run through 'most' of the code without changing the filesystem.

File(object) represents a filesystem item, such as a file or folder, which
may or may not exist when the object is initialized.  This differs
from os.DirEntry(object), which is only instantiated for an existing item.
