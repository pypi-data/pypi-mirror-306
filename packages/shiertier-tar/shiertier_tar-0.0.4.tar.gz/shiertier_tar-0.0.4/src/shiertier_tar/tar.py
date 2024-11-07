import os.path
from os import getcwd
from typing import List
from hfutils.archive.base import archive_unpack
from hfutils.index.make import tar_create_index
from hfutils.index.local_fetch import (
    tar_get_index, tar_list_files, tar_file_exists, tar_file_size, tar_file_info, tar_file_download
)
from tarfile import TarFile

__all__ = [
    "pack_directory_to_tarfile", 
    "unpack_tarfile", 
    "create_index_from_tarfile", 
    "create_tarfile_index_for_directory",
    "get_tarfile_index", 
    "list_files_in_tarfile", 
    "is_file_in_tarfile", 
    "get_file_size_in_tarfile",
    "get_file_info_in_tarfile", 
    "export_file_from_tarfile"
]

def pack_directory_to_tarfile(src_directory: str, 
                              archive_file: str | None = None, 
                              pattern: str | None = None, 
                              silent: bool = False):
    if archive_file is None:
        archive_file = os.path.join(getcwd(), f"{os.path.basename(src_directory)}.tar")
    os.makedirs(os.path.dirname(archive_file), exist_ok=True)
    with TarFile.open(archive_file, "w") as tar:
        for root, dirs, files in os.walk(src_directory):
            for file in files:
                if pattern:
                    pattern_list = [p.strip() for p in pattern.split(";") if p.strip()]
                    if pattern_list:
                        if any(file.endswith(p) for p in pattern_list):
                            continue
                file_path = os.path.join(root, file)
                tar.add(file_path, arcname=os.path.relpath(file_path, src_directory))

def unpack_tarfile(archive_file: str, 
                   directory: str = None, 
                   silent: bool = False):
    if directory is None:
        directory = getcwd()
    directory = os.path.join(directory, os.path.basename(archive_file))
    return archive_unpack(archive_file, directory, silent)

def create_index_from_tarfile(archive_file: str, 
                              index_file_path: str = None, 
                              silent: bool = False):
    if index_file_path is None:
        index_file_path = archive_file.replace(".tar", ".json")
    return tar_create_index(archive_file, index_file_path, silent)

def create_tarfile_index_for_directory(src_directory: str, 
                                       archive_file: str | None = None, 
                                       index_file_path: str | None = None, 
                                       pattern: str | None = None, 
                                       silent: bool = False):
    pack_directory_to_tarfile(src_directory, archive_file, pattern, silent=silent)
    create_index_from_tarfile(archive_file, index_file_path, silent=silent)

def get_file_size_in_tarfile(archive_file: str, 
                            file_in_archive: str, 
                            idx_file_path: str | None = None) -> int:
    if idx_file_path is None:
        idx_file_path = archive_file.replace(".tar", ".json")
    return tar_file_size(archive_file, file_in_archive, idx_file_path)

def get_file_info_in_tarfile(archive_file: str, 
                            file_in_archive: str, 
                            idx_file_path: str | None = None) -> dict:
    if idx_file_path is None:
        idx_file_path = archive_file.replace(".tar", ".json")
    return tar_file_info(archive_file, file_in_archive, idx_file_path)

def get_tarfile_index(archive_file: str, 
                      idx_file_path: str | None = None) -> dict:
    if idx_file_path is None:
        idx_file_path = archive_file.replace(".tar", ".json")
    return tar_get_index(archive_file, idx_file_path)

def export_file_from_tarfile(archive_file: str, 
                            file_in_archive: str, 
                            local_file: str, 
                            idx_file_path: str | None = None, 
                            chunk_size: int = 1048576, 
                            force_download: bool = False):
    if idx_file_path is None:
        idx_file_path = archive_file.replace(".tar", ".json")
    return tar_file_download(archive_file, file_in_archive, local_file, idx_file_path, chunk_size, force_download)


def list_files_in_tarfile(archive_file: str, 
                         idx_file_path: str | None = None) -> List[str]:
    if idx_file_path is None:
        idx_file_path = archive_file.replace(".tar", ".json")
    return tar_list_files(archive_file, idx_file_path)

def is_file_in_tarfile(archive_file: str, 
                       file_in_archive: str, 
                       idx_file_path: str | None = None) -> bool:
    if idx_file_path is None:
        idx_file_path = archive_file.replace(".tar", ".json")
    return tar_file_exists(archive_file, file_in_archive, idx_file_path)
