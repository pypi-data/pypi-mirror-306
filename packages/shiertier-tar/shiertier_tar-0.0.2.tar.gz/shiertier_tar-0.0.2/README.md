# shiertier_tar

English | [中文](https://github.com/shiertier-utils/shiertier_tar/blob/main/README_zh.md)

## Introduction

`shiertier_tar` is a Python library designed to simplify the process of working with tar archives. It provides a set of utility functions to pack directories into tar files, unpack tar files, create and manage tar file indexes, and perform various operations on tar files. This library is particularly useful for managing large datasets or archives in a structured manner.
This project is a simplified version of [hfutils].

## Installation

You can install `shiertier_tar` via `pip`:

```bash
pip install shiertier_tar
```

Please note that this project is still under development.

## Usage

### Packing a Directory to a Tar File

You can pack a directory into a tar file using the `pack_directory_to_tarfile` function. This function allows you to specify a source directory, an optional archive file name, and a pattern to filter files.

```python
from shiertier_tar import pack_directory_to_tarfile

# Pack a directory into a tar file
pack_directory_to_tarfile(src_directory='path/to/source_directory', archive_file='path/to/archive.tar', pattern='*.txt;*.md')
```

### Unpacking a Tar File

You can unpack a tar file using the `unpack_tarfile` function. This function allows you to specify the tar file and an optional destination directory.

```python
from shiertier_tar import unpack_tarfile

# Unpack a tar file
unpack_tarfile(archive_file='path/to/archive.tar', directory='path/to/destination_directory')
```

### Creating an Index from a Tar File

You can create an index from a tar file using the `create_index_from_tarfile` function. This function allows you to specify the tar file and an optional index directory.

```python
from shiertier_tar import create_index_from_tarfile

# Create an index from a tar file
create_index_from_tarfile(archive_file='path/to/archive.tar', directory='path/to/index_directory')
```

### Creating a Tar File Index for a Directory

You can create a tar file index for a directory using the `create_tarfile_index_for_directory` function. This function allows you to specify the source directory, an optional archive file name, an optional index directory, and a pattern to filter files.

```python
from shiertier_tar import create_tarfile_index_for_directory

# Create a tar file index for a directory
create_tarfile_index_for_directory(src_directory='path/to/source_directory', archive_file='path/to/archive.tar', index_directory='path/to/index_directory', pattern='*.txt;*.md')
```

### Listing Files in a Tar File

You can list files in a tar file using the `list_files_in_tarfile` function. This function allows you to specify the tar file and an optional index file.

```python
from shiertier_tar import list_files_in_tarfile

# List files in a tar file
files = list_files_in_tarfile(archive_file='path/to/archive.tar')
print(files)
```

### Checking if a File Exists in a Tar File

You can check if a file exists in a tar file using the `is_file_in_tarfile` function. This function allows you to specify the tar file, the file in the archive, and an optional index file.

```python
from shiertier_tar import is_file_in_tarfile

# Check if a file exists in a tar file
exists = is_file_in_tarfile(archive_file='path/to/archive.tar', file_in_archive='file_in_archive.txt')
print(exists)
```

### Getting File Size in a Tar File

You can get the size of a file in a tar file using the `get_file_size_in_tarfile` function. This function allows you to specify the tar file, the file in the archive, and an optional index file.

```python
from shiertier_tar import get_file_size_in_tarfile

# Get the size of a file in a tar file
size = get_file_size_in_tarfile(archive_file='path/to/archive.tar', file_in_archive='file_in_archive.txt')
print(size)
```

### Getting File Info in a Tar File

You can get information about a file in a tar file using the `get_file_info_in_tarfile` function. This function allows you to specify the tar file, the file in the archive, and an optional index file.

```python
from shiertier_tar import get_file_info_in_tarfile

# Get information about a file in a tar file
info = get_file_info_in_tarfile(archive_file='path/to/archive.tar', file_in_archive='file_in_archive.txt')
print(info)
```

### Exporting a File from a Tar File

You can export a file from a tar file using the `export_file_from_tarfile` function. This function allows you to specify the tar file, the file in the archive, the local file path, an optional index file, and an optional chunk size.

```python
from shiertier_tar import export_file_from_tarfile

# Export a file from a tar file
export_file_from_tarfile(archive_file='path/to/archive.tar', file_in_archive='file_in_archive.txt', local_file='path/to/local_file.txt')
```

## Dependencies

- `hfutils`

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.