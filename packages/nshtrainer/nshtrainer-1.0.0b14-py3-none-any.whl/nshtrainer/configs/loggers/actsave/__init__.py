from __future__ import annotations

__codegen__ = True

from typing import TYPE_CHECKING

# Config/alias imports

if TYPE_CHECKING:
    from nshtrainer.loggers.actsave import ActSaveLoggerConfig as ActSaveLoggerConfig
    from nshtrainer.loggers.actsave import BaseLoggerConfig as BaseLoggerConfig
else:

    def __getattr__(name):
        import importlib

        if name in globals():
            return globals()[name]
        if name == "ActSaveLoggerConfig":
            return importlib.import_module(
                "nshtrainer.loggers.actsave"
            ).ActSaveLoggerConfig
        if name == "BaseLoggerConfig":
            return importlib.import_module(
                "nshtrainer.loggers.actsave"
            ).BaseLoggerConfig
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Submodule exports
