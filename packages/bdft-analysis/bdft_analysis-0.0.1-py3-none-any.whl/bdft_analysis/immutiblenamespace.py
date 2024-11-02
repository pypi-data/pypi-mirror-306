from dataclasses import dataclass, field, replace, Field, is_dataclass


def imns(cls):
    '''Immutible Namespace, one honking great idea'''
    for name, type in cls.__annotations__.items():
        val = cls.__dict__.get(name)
        if is_dataclass(type):
            if val is None:
                val = field(default_factory=type)
            elif isinstance(val, dict):
                val = field(default=type(**val))
            elif isinstance(val, Field):
                val = val
            elif callable(val):
                val = field(default_factory=val)
            else:
                assert False, ("unsupported default type", cls, name, type, val)
        else:
            if val is None: continue
            if callable(val):
                val = field(default_factory=val)
            else:
                val = field(default=val)

        setattr(cls, name, val)

    cls.__call__ = replace
    return dataclass(cls, frozen=True)
