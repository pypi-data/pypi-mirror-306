import inspect
from typing import Any, Self, Callable

from .errs_from_check import *
from .generictypes import *

__all__ = ["check"]


def _get_all_f(cls):
    return [
        name
        for name, method in inspect.getmembers(cls, predicate=inspect.ismethod)
        if not name.startswith("__")
    ]


class _ErrorFs:
    def __new__(cls) -> Self:
        return {"is_num": "%(obj_name)s must be a number: %(obj_value)s"}


class _Tables:
    def __init__(self) -> None:
        self.errorfs = _ErrorFs()

    def __call__(self, *args: Any, **kwds: Any) -> dict:
        return self.errorfs


_tables = _Tables()


class _R_FORMAT:
    def __init__(self, error_type: Exception, check: bool) -> None:
        self.err_t = error_type
        self.check = check


class _Rules:
    def __init__(self, obj) -> None:
        self.obj = obj

    def is_num(self) -> _R_FORMAT:
        return _R_FORMAT(
            InvalidTypeError, isinstance(self.obj, (Integer, Decimal, Complex))
        )


class _check_out:
    def __init__(self) -> None:
        self.passed_all: bool = Null
        self.rules_passed: int = 0
        self.expected_passed: int = len(_Rules)
        self.error: int = 0

        self.errors = {}

    def __iadd__(self, other: int) -> Self:
        if isinstance(other, int):
            self.error += other
        return self

    def __repr__(self) -> str:
        errs = True if self.error == 1 else False
        return "check(\n%(tab)scontains_errors={}({}),\n%(tab)spassed_all={},\n%(tab)srules_passed={}\n)".format(
            self.error, errs, self.passed_all, self.rules_passed
        ) % {
            "tab": "    "
        }

    def is_passed(self) -> bool:
        return (
            self.passed_all
            and self.rules_passed == self.expected_passed
            and not self.error
        )

    def inc(self, attr: str, int_val: int = 1) -> Self:
        if hasattr(self, attr):
            _a = getattr(self, attr)
            if isinstance(int_val, int):
                setattr(self, attr, _a + int_val)
        return self


class check:
    def __init__(self, obj: object) -> None:
        self._obj = obj
        self._objn = self._get_var_name(obj)
        self._r = _Rules(obj)
        self._allf = _get_all_f(self._r)

    @property
    def obj(self) -> object:
        """The obj property."""
        return self._obj

    @obj.setter
    def obj(self, value) -> None:
        self._obj = value

    def _get_var_name(self, obj: object) -> str | None:
        """Find the variable name of the object in the local scope."""
        frame = inspect.currentframe().f_back
        for name, value in frame.f_locals.items():
            if value is obj:
                return name
        return None  # Return None if no name found

    def __call__(self, extraRules: tuple[Callable] = None, **kwds: Any) -> _check_out:
        _options = {}
        _options["raise_err"] = kwds.get("raise_err", False)
        _options["ret_inst"] = (
            kwds.get("ret_inst", True) if _options["raise_err"] != True else False
        )

        if not isinstance(_options["ret_inst"], bool) and not isinstance(
            _options["raise_err"], bool
        ):
            raise RuntimeError("error retrieving call configs")

        outer = _check_out()

        for fname in self._allf:
            f: _R_FORMAT = getattr(self._r, fname)()

            if not f.check:
                if _options["raise_err"]:
                    raise f.err_t(
                        _tables.errorfs[fname]
                        % {
                            "obj_name": self._objn,
                            "obj_value": self._obj,
                        }
                    )
                if _options["ret_inst"]:
                    outer += 1
                    outer.passed_all = False
                    return outer
            else:
                outer.inc("rules_passed")
                continue

        if isinstance(extraRules, tuple):
            for rule in extraRules:
                if not callable(rule):
                    raise ValueError(
                        "rules in extraRules must be a callable function or class that returns a bool from a given value."
                    )

            outer.expected_passed += len(extraRules)

            for rule in extraRules:
                if not rule():
                    outer += 1
                    outer.passed_all = False
                    return outer
                else:
                    outer.inc("rules_passed")
                    continue

        outer.passed_all = True
        return outer
