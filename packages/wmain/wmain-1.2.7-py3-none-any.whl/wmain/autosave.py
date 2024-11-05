import json
import os
from typing import Iterator
from wmain.base import create_path

__autosave_allow_types__ = (int, float, str)
__autosave_attr_whitelist__ = [
    "__autosave_filepath__",
    "__autosave_callback__",
    "__dict__",
]

class WAutoSave:

    def bind_autosave(self, filepath) -> None:
        self.__autosave_filepath__ = filepath
        for instance in self.__autosave_iter_instances__():
            instance.__dict__["__autosave_callback__"] = self.__autosave__

        if not os.path.exists(filepath):
            self.__autosave__()
        else:
            with open(filepath, "r") as f:
                attr_dict = dict(json.load(f))
                self.__autosave_load_attr_dict__(attr_dict)

    def __autosave__(self) -> None:
        if "__autosave_filepath__" in self.__dict__:
            create_path(self.__autosave_filepath__)
            attr_dict = self.__autosave_get_attr_dict__()
            with open(self.__autosave_filepath__, "w") as f:
                json.dump(attr_dict, f)
        elif "__autosave_callback__" in self.__dict__:
            self.__autosave_callback__()

    def __autosave_iter_instances__(self) -> Iterator["WAutoSave"]:
        for v in self.__dict__.values():
            if isinstance(v, WAutoSave):
                yield v
                yield from v.__autosave_iter_instances__()

    def __autosave_get_attr_dict__(self) -> dict:
        attr_dict = {}
        for k, v in self.__dict__.items():
            if k in __autosave_attr_whitelist__:
                continue
            if isinstance(v, __autosave_allow_types__):
                attr_dict[k] = v
            elif isinstance(v, WAutoSave):
                attr_dict[k] = v.__autosave_get_attr_dict__()
            else:
                raise TypeError(
                    f"Type {type(v)} of Attribute {k} in {type(self)} is not allowed to be autosaved."
                )
        return attr_dict

    def __autosave_load_attr_dict__(self, attr_dict: dict):
        for k, v in attr_dict.items():
            target_type = type(self.__dict__.get(k))
            if target_type in __autosave_allow_types__:
                self.__dict__[k] = target_type(v)
            elif issubclass(target_type, WAutoSave):
                self.__dict__[k].__autosave_load_attr_dict__(v)
            else:
                raise TypeError(
                    f"Type {target_type} of Attribute {k} in {type(self)} is not allowed to be autosaved."
                )

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if (
            not callable(getattr(self, name, None))
            and name not in __autosave_attr_whitelist__
        ):
            self.__autosave__()
