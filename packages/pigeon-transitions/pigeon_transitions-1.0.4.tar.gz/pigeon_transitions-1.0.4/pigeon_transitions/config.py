from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from typing import Optional, Mapping, Any
from importlib import import_module
import yaml


class MachineConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    config: Optional[Mapping[str, Any]] = {}

    @model_validator(mode="after")
    def validate_extra(self):
        for key, val in self.__pydantic_extra__.items():
            setattr(self, key, MachineConfig(**val))
        return self


class PigeonTransitionsConfig(BaseModel):
    root: str
    machines: Optional[MachineConfig] = MachineConfig()

    @field_validator("root")
    @classmethod
    def get_class(cls, root: str):
        from .base import RootMachine

        package_name = ".".join(root.split(".")[:-1])
        class_name = root.split(".")[-1]
        package = import_module(package_name)
        class_obj = getattr(package, class_name)
        assert issubclass(class_obj, RootMachine)
        return class_obj

    @classmethod
    def load(cls, data):
        return cls(**yaml.safe_load(data))

    @classmethod
    def load_file(cls, file):
        with open(file) as f:
            return cls.load(f.read())
