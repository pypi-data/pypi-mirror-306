from abc import ABC, abstractmethod
from typing import TypeVar
from argparse import Namespace

CommandType = TypeVar("CommandType", bound="Command")


class ArgsMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        # Merging 'args' dictionaries of parent classes and the new class
        new_args = {}
        for base in reversed(bases):
            if hasattr(base, "args"):
                new_args.update(base.args)
        if "args" in attrs:
            new_args.update(attrs["args"])
        attrs["args"] = new_args

        return super().__new__(mcs, name, bases, attrs)


class Command(metaclass=ArgsMetaclass):

    args = {}
    help = ""

    def __init__(self, cliargs: Namespace) -> None:
        self.cliargs = cliargs

    @classmethod
    def method(cls) -> str:
        return cls.__name__.lower()

    def __call__(self) -> int:
        raise NotImplementedError
