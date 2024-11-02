from __future__ import annotations

__codegen__ = True

from typing import TYPE_CHECKING

# Config/alias imports

if TYPE_CHECKING:
    from nshtrainer.callbacks.log_epoch import CallbackConfigBase as CallbackConfigBase
    from nshtrainer.callbacks.log_epoch import (
        LogEpochCallbackConfig as LogEpochCallbackConfig,
    )
else:

    def __getattr__(name):
        import importlib

        if name in globals():
            return globals()[name]
        if name == "CallbackConfigBase":
            return importlib.import_module(
                "nshtrainer.callbacks.log_epoch"
            ).CallbackConfigBase
        if name == "LogEpochCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks.log_epoch"
            ).LogEpochCallbackConfig
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Submodule exports
