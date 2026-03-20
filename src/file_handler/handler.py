import os
import json
import pickle
import yaml
import h5py
import numpy as np
from typing import Any

from .type import FileType

class FileHandler:
    """
    A utility class for handling file operations with automatic format detection.
    
    This class provides static methods to save and load objects in various formats
    (pickle, JSON, YAML, HDF5) based on file extensions. It automatically creates
    directories as needed and handles format-specific serialization.
    """
    
    @staticmethod
    def save(
        obj: Any, 
        path: str
        ) -> None:
        """
        Save an object to a file in the appropriate format.
        
        The format is automatically determined from the file extension:
        - .json: JSON format  
        - .pkl: Pickle format
        - .yml/.yaml: YAML format
        - .h5/.hdf5: HDF5 format
        
        Parameters:
        ----------
        obj: Any
            The object to save. Can be any Python object for pickle,
            dict/list for JSON/YAML, or dict/array for HDF5.
        path: str
            The file path where the object should be saved.

        Raises:
        --------
        ValueError: If the file extension is not supported.
        Exception: If there's an error creating directories or writing the file.
        """
        # Create directory if it doesn't exist
        dir_name = os.path.dirname(path)
        if dir_name != '':
            os.makedirs(dir_name, exist_ok=True)
        type_ = FileType.from_path(path)

        try:
            FileHandler._run_save(obj, path, type_)
        except OSError as e:
            raise Exception(f"Error creating directory or writing file: {e}")

    @staticmethod
    def _run_save(
        obj: Any, 
        path: str, 
        type_: FileType
        ) -> None:
        """ Process the save operation.

        Parameters:
        ----------
        obj: Any
            The object to save. Can be any Python object for pickle,
            dict/list for JSON/YAML, or dict/array for HDF5.
        path: str
            The file path where the object should be saved.
        type_: FileType
            The type of the file.
        """
        match type_:
            case FileType.PICKLE:
                with open(path, mode='wb') as f:
                    pickle.dump(obj, f)
            case FileType.JSON:
                with open(path, mode='w') as f:
                    json.dump(obj, f)
            case FileType.YAML:
                with open(path, mode='w') as f:
                    yaml.safe_dump(obj, f, allow_unicode=True)
            case FileType.H5:
                with h5py.File(path, 'w') as f:
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            f.create_dataset(key, data=np.array(value))
                    else:
                        f.create_dataset('data', data=np.array(obj))

    @staticmethod
    def load(path: str) -> Any:
        """
        Load an object from a file in the appropriate format.
        
        The format is automatically determined from the file extension:
        - .pkl: Pickle format
        - .json: JSON format
        - .yml/.yaml: YAML format  
        - .h5/.hdf5: HDF5 format (returns h5py.File object)
        
        Parameters:
        ----------
        path: str
            The file path to load the object from.
            
        Returns:
        ---------
        Any: The loaded object. For HDF5 files, returns an h5py.File object.
            
        Raises:
        --------
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the file extension is not supported.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        type_ = FileType.from_path(path)

        match type_:
            case FileType.PICKLE:
                with open(path, mode='rb') as f:
                    return pickle.load(f)
            case FileType.JSON:
                with open(path, mode='r') as f:
                    return json.load(f)
            case FileType.YAML:
                with open(path, mode='r') as f:
                    return yaml.safe_load(f)
            case FileType.H5:
                return h5py.File(path, 'a')

