from __future__ import annotations

__codegen__ = True

from typing import TYPE_CHECKING

# Config/alias imports

if TYPE_CHECKING:
    from nshtrainer.callbacks.timer import CallbackConfigBase as CallbackConfigBase
    from nshtrainer.callbacks.timer import (
        EpochTimerCallbackConfig as EpochTimerCallbackConfig,
    )
else:

    def __getattr__(name):
        import importlib

        if name in globals():
            return globals()[name]
        if name == "CallbackConfigBase":
            return importlib.import_module(
                "nshtrainer.callbacks.timer"
            ).CallbackConfigBase
        if name == "EpochTimerCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks.timer"
            ).EpochTimerCallbackConfig
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Submodule exports
