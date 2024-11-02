from __future__ import annotations

__codegen__ = True

from typing import TYPE_CHECKING

# Config/alias imports

if TYPE_CHECKING:
    from nshtrainer.trainer.trainer import EnvironmentConfig as EnvironmentConfig
    from nshtrainer.trainer.trainer import TrainerConfig as TrainerConfig
else:

    def __getattr__(name):
        import importlib

        if name in globals():
            return globals()[name]
        if name == "EnvironmentConfig":
            return importlib.import_module(
                "nshtrainer.trainer.trainer"
            ).EnvironmentConfig
        if name == "TrainerConfig":
            return importlib.import_module("nshtrainer.trainer.trainer").TrainerConfig
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Submodule exports
