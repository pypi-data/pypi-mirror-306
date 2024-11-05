import importlib.metadata
import os

import psutil

from ._readxml import from_structure_dictionary as _read_xml_from_dictionary
from ._readxml import from_structure_file as _read_xml_from_structure_file
from .storage import default_data_dir

__all__ = ["read_xml"]
package_name = "pubmedparser2"
__version__ = importlib.metadata.version(package_name)


def _unprocessed_files(files: list[str], processed_files: str) -> list[str]:
    """Filter that returns a list of files that have not been processed yet."""
    if not os.path.exists(processed_files):
        return files

    file_set = set(files)
    with open(processed_files, "r") as read_files:
        for f in read_files.readlines():
            try:
                file_set.remove(f.strip("\n"))
            except KeyError:
                continue

    return list(file_set)


def read_xml(
    files: str | list[str],
    path_structure: dict | str,
    data_dir: str,
    relative_to_default_data: bool = True,
    progress_file: str = "processed.txt",
    n_threads: int = -1,
    mode: str = "append",
    reprocess_all: bool = False,
    exts: tuple[str, ...] = (".xml", ".xml.gz"),
) -> str:
    """Collect values matching xpaths in XML files.

    Parameters
    ----------
    files : str, list
        A path to the directory containing the paths to read or a list of
        absolute paths to the files to read.
    path_structure : dict, str
        A set of xpaths to collect. Either as a dictionary with keys
        representing names and values representing the paths or a path to a
        yaml file describing the same information.
    data_dir : str
        Where to save the results.
    relative_to_default_data : bool
        If true, `data_dir` is a subdirectory under pubmedparser's default
        data directory. If false, `data_dir` is relative to the cwd.
    progress_file : str, default "processed.txt"
        If not none, save successfully parsed files to the progress file. If
        the file already exists, only files not listed in it will be read.
    n_threads : int, default -1
        Number of files to process in parallel. If -1, use 1 thread per
        available CPU (if hyper-threading is available this is the number of
        logical CPUs not physical CPUs). If the number of files to be processed
        is less than the requested number of threads, n_threads is reduced to
        number of files.
    mode : str {"append", "write"}
        If "write", write over the old collected results, otherwise append to
        the end. In either case, only xml files that haven't been processed yet
        will be read unless reprocess_all is set to true.
    reprocess_all : bool
        If True process all xml files passed to the files argument, even if
        they were previously parsed. This overrides mode, also delete the old
        results to prevent duplication.
    exts : tuple, default (".xml", ".xml.gz")
        A tuple of file extensions to include. Any file ending with an
        extension not included will be ignored.

    Returns
    -------
    data_dir : the location the collected data was written to.

    """
    if isinstance(files, str):
        if os.path.isdir(files):
            files = [os.path.join(files, f) for f in os.listdir(files)]
        elif os.path.exists(files):
            files = [files]
        else:
            raise FileNotFoundError("Files path not found")

    if relative_to_default_data:
        data_dir = default_data_dir(data_dir)

    if mode == "write" or reprocess_all:
        overwrite_cache = True
    elif mode == "append":
        overwrite_cache = False
    else:
        raise KeyError(f'Mode should be "append" or "write" got {mode}')

    if n_threads == -1:
        n_threads = len(psutil.Process().cpu_affinity())

    files = [f for f in files if f.endswith(exts)]
    if reprocess_all and os.path.exists(os.path.join(data_dir, progress_file)):
        os.unlink(os.path.join(data_dir, progress_file))
    else:
        files = _unprocessed_files(
            files, processed_files=os.path.join(data_dir, progress_file)
        )

    if isinstance(path_structure, str):
        assert os.path.exists(
            path_structure
        ), "File for path structure not found."
        _read_xml_from_structure_file(
            files,
            path_structure,
            data_dir,
            progress_file,
            n_threads,
            overwrite_cache,
        )
    else:
        _read_xml_from_dictionary(
            files,
            path_structure,
            data_dir,
            progress_file,
            n_threads,
            overwrite_cache,
        )

    return data_dir
