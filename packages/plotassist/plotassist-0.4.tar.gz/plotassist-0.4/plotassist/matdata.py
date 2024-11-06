# matdata.py

# A class to help with loading and accessing data from MATLAB mat files.

# imports
from os import PathLike
from pathlib import Path
from typing import Sequence
import numpy.typing as npt
import scipy.io as sio


class MatData:
    """
    A class to help with loading and accessing data from MATLAB mat files.

    Attributes:
    ----------
    mat_file : Path
        The path to the MATLAB mat file.
    data : dict
        The data loaded from the MATLAB mat file.

    Methods:
    -------
    __init__(self, mat_file: PathLike, variable_names: Sequence = None)
        Initializes the MatData object and loads the data from the specified mat file.

    get_file(self) -> Path
        Returns the path to the MATLAB mat file.

    get(self, var: str) -> npt.ArrayLike
        Returns the data for the specified variable from the mat file.

    get_keys(self) -> Sequence[str]
        Returns the keys of the data dictionary.

    __repr__(self)
        Returns a string representation of the MatData object, including the file location and keys.
    """

    def __init__(self, mat_file: PathLike, variable_names: Sequence = None):
        """
        Initializes the MatData object and loads the data from the specified mat file.

        Parameters:
        ----------
        mat_file : PathLike
            The path to the MATLAB mat file.
        variable_names : Sequence, optional
            A sequence of variable names to load from the mat file. If None, all variables are loaded.

        Raises:
        ------
        FileNotFoundError
            If the specified mat file does not exist.
        """
        self.mat_file = Path(mat_file)
        if not mat_file.exists():
            raise FileNotFoundError(f"File {mat_file} not found")

        self.data = sio.loadmat(
            mat_file,
            squeeze_me=True,
            simplify_cells=True,
            variable_names=variable_names,
        )

    def get_file(self) -> Path:
        """
        Returns the path to the MATLAB mat file.

        Returns:
        -------
        Path
            The path to the MATLAB mat file.
        """
        return self.mat_file

    def get(self, var: str) -> npt.ArrayLike:
        """
        Returns the data for the specified variable from the mat file.

        Parameters:
        ----------
        var : str
            The name of the variable to retrieve from the mat file.

        Returns:
        -------
        npt.ArrayLike
            The data for the specified variable.

        Raises:
        ------
        KeyError
            If the specified variable is not found in the data.
        """
        if var not in self.data:
            raise KeyError(f"Variable '{var}' not found in data")

        return self.data[var]

    def get_keys(self) -> Sequence[str]:
        """
        Returns the keys of the data dictionary.

        Returns:
        -------
        Sequence[str]
            The keys of the data dictionary.
        """
        return self.data.keys()

    def __repr__(self):
        """
        Returns a string representation of the MatData object, including the file location and keys.

        Returns:
        -------
        str
            A string representation of the MatData object.
        """
        file_location = self.mat_file.resolve()
        keys = list(self.data.keys())
        repr_str = f"MatData:\n\tmat_file={file_location}\n\tkeys={keys}"
        return repr_str
