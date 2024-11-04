"""
A module containting utilitiy functions
"""

import pathlib
from copy import copy, deepcopy
import os

import yaml


def clean_dict(data: dict) -> dict:
    """
    Clean the input dictionary (recursively). Removing any keys where the value is
    none, changing pathlib.Path to strings and converting tuples to strings.

    The input is a single dictionary, the output is a cleaned dictionary.
    """
    # iterate over entries
    keys_to_delete = []
    for key, value in data.items():
        # remove empty entries
        if value is None:
            keys_to_delete.append(key)
        else:
            data[key] = _clean_object(value)
    # delete empty entries
    for key in keys_to_delete:
        del data[key]
    return data


def _clean_object(obj: object) -> object:
    # clean up lists
    if isinstance(obj, list):
        return [_clean_object(x) for x in obj]
    # clean up dicts
    if isinstance(obj, dict):
        return clean_dict(obj)
    if isinstance(obj, tuple):
        # convert to string like "(1,2,3)"
        return str(obj)
    if isinstance(obj, pathlib.Path):
        # convert to string
        return str(obj)
    return obj


def get_nested_dict(dictionary, keylist, add_if_missing=False):
    """
    Return the object nested within a dictionary, given the list of
    key names. Optionally an empty dictionary can be added if the
    key is missing.
    """
    d = dictionary
    for key_name in keylist:
        if key_name not in d:
            if add_if_missing:
                d[key_name] = {}
            else:
                raise KeyError(f"Couldn't access {keylist} in dict {dictionary}. No key {key_name}")
        if not isinstance(d[key_name], dict):
            raise TypeError(f"Couldn't access {keylist} in dict {dictionary}. "
                            f"{key_name} has a non-dict value")
        d = d[key_name]
    return d

class Export:

    """
    This is a base class that should not be used directly.
    """

    def __init__(
        self,
        key: str,
        name: str,
        description: str,
        output_files: list,
        source_files: list,
        parameters: dict,
        application: str
    ) -> None:

        self._key = key
        self._name = name
        self._description = description
        self._output_files = output_files
        self._source_files = source_files
        self._parameters = parameters
        self._application = application
        self._parameter_file = None

    def __eq__(self, other):
        if isinstance(other, str):
            return self.key==str
        if isinstance(other, Export):
            return self.as_exsource_dict == other.as_exsource_dict
        return NotImplemented

    @property
    def key(self):
        """Return the unique key identifying the component"""
        return self._key

    @property
    def name(self):
        """Return the human readable name of the component"""
        return self._name

    @property
    def description(self):
        """Return the description of the component"""
        return self._description

    @property
    def output_files(self):
        """Return a copy of the list of output CAD files that represent the component"""
        return copy(self._output_files)

    @property
    def source_files(self):
        """Return a copy of the list of the input CAD files that represent the component"""
        return copy(self._source_files)

    @property
    def parameters(self):
        """Return the parameters associated with generating this mechancial component"""
        if self._parameter_file:
            return {self._parameter_file[0]: self._parameter_file[1]}
        return deepcopy(self._parameters)

    @property
    def application(self):
        """Return the name of the application used to process the input CAD files"""
        return self._application

    @property
    def dependencies(self):
        """Return the list of dependent files, or None if none are set.
        Note this currently is not implemented except for in the child classes.
        """
        return None

    @property
    def as_exsource_dict(self):
        """Return this object as a dictionary of the part information for exsource"""
        component_data = {
            "name": self.name,
            "description": self.description,
            "output-files": self.output_files,
            "source-files": self.source_files,
            "parameters": self.parameters,
            "application": self.application,
            "dependencies": self.dependencies
        }
        component_data = clean_dict(component_data)
        return {self.key: component_data}

    def set_parameter_file(self, file_id: str, filename: str):
        """
        As standard parameters are directly entered into the exsoruce-definition.

        Run this method to output the parameters to a yaml file (of specified filename)
        In the exsource dictionary the parameter entry will become:
        {file_id: filename}
        """
        self._parameter_file = (file_id, filename)

    def write_parameter_file(self, root_dir='.'):
        """
        Write parameter file to disk
        """
        if not self._parameter_file:
            return
        filename = os.path.join(root_dir, self._parameter_file[1])
        with open(filename, "w", encoding="utf-8") as f:
            yaml.dump(clean_dict(self._parameters), f, sort_keys=False)

    def add_parameter(self, key, value, add_missing_keys=False):
        """
        Add a parameter to the parameter dictionary.

        To access nested parameters without overwriting all separate keys by `.`.
        For example to add `key2` to `key1` if `key1` already
        exists and its value is a dictionary set key to `"key1.key2"`
        """
        keys = key.split('.')
        if len(keys) == 1:
            d = self._parameters
        else:
            d = get_nested_dict(self._parameters, keys[:-1], add_missing_keys)
        d[keys[-1]] = value

    def append_to_parameter(self, key, value):
        """
        Append to a list parameter in the parameter dictionary.

        To access nested parameters seperate keys by `.`.
        For example `key="key1.key2"` will append to the list at parameters["key1"]["key2"]
        """
        keys = key.split('.')
        if len(keys) == 1:
            d = self._parameters
        else:
            d = get_nested_dict(self._parameters, keys[:-1])


        if not isinstance(d[keys[-1]], list):
            raise TypeError(f"Could not append to {keys} in parameters. "
                            f"{keys[-1]} has a non-list value")
        d[keys[-1]].append(value)
