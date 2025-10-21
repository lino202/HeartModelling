# Code from https://github.com/openep/openep-py/tree/dev

import scipy.io


def _load_mat_v73(filename):
    """
    Load a v7.3 MATLAB file.

    h5py is used to read the file.

    Currently, all references in the HDF5 file are resolved except for 'data/rfindex/grid'
    """
    pass
    # import h5py

    # with h5py.File(filename, "r") as f:
    #     data = _visit_mat_v73_(f)


    # # Some arrays need to be flattened or transposed
    # data = _mat_v73_transform_arrays(data)

    # return data


def _load_mat_below_v73(filename):
    """
    Load a MATLAB file of version less than v7.3

    scipy.io.loadmat is used to read the file.
    """

    data = scipy.io.loadmat(
        filename,
        appendmat=False,
        mat_dtype=False,
        chars_as_strings=True,
        struct_as_record=False,
        squeeze_me=True,
        simplify_cells=True,
    )

    return data

def _check_mat_version_73(filename):
    """Check if a MATLAB file is of version 7.3"""

    byte_stream, _ = scipy.io.matlab._mio._open_file(filename, appendmat=False)
    major_version, _ = scipy.io.matlab._miobase.get_matfile_version(byte_stream)

    return major_version == 2


def load_mat(filename):
    """Load a MATLAB file."""

    if _check_mat_version_73(filename):
        data = _load_mat_v73(filename)
    else:
        data = _load_mat_below_v73(filename)

    return data

