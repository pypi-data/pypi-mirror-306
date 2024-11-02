from __future__ import annotations

__codegen__ = True

from typing import TYPE_CHECKING

# Config/alias imports

if TYPE_CHECKING:
    from nshtrainer.callbacks.finite_checks import (
        CallbackConfigBase as CallbackConfigBase,
    )
    from nshtrainer.callbacks.finite_checks import (
        FiniteChecksCallbackConfig as FiniteChecksCallbackConfig,
    )
else:

    def __getattr__(name):
        import importlib

        if name in globals():
            return globals()[name]
        if name == "CallbackConfigBase":
            return importlib.import_module(
                "nshtrainer.callbacks.finite_checks"
            ).CallbackConfigBase
        if name == "FiniteChecksCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks.finite_checks"
            ).FiniteChecksCallbackConfig
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Submodule exports
