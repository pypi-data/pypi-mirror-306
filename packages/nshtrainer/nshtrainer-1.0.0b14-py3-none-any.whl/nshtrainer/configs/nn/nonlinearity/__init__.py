from __future__ import annotations

__codegen__ = True

from typing import TYPE_CHECKING

# Config/alias imports

if TYPE_CHECKING:
    from nshtrainer.nn.nonlinearity import (
        BaseNonlinearityConfig as BaseNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import (
        ELUNonlinearityConfig as ELUNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import (
        GELUNonlinearityConfig as GELUNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import (
        LeakyReLUNonlinearityConfig as LeakyReLUNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import (
        MishNonlinearityConfig as MishNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import NonlinearityConfig as NonlinearityConfig
    from nshtrainer.nn.nonlinearity import PReLUConfig as PReLUConfig
    from nshtrainer.nn.nonlinearity import (
        ReLUNonlinearityConfig as ReLUNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import (
        SigmoidNonlinearityConfig as SigmoidNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import (
        SiLUNonlinearityConfig as SiLUNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import (
        SoftmaxNonlinearityConfig as SoftmaxNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import (
        SoftplusNonlinearityConfig as SoftplusNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import (
        SoftsignNonlinearityConfig as SoftsignNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import (
        SwiGLUNonlinearityConfig as SwiGLUNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import (
        SwishNonlinearityConfig as SwishNonlinearityConfig,
    )
    from nshtrainer.nn.nonlinearity import (
        TanhNonlinearityConfig as TanhNonlinearityConfig,
    )
else:

    def __getattr__(name):
        import importlib

        if name in globals():
            return globals()[name]
        if name == "BaseNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).BaseNonlinearityConfig
        if name == "ELUNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).ELUNonlinearityConfig
        if name == "GELUNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).GELUNonlinearityConfig
        if name == "LeakyReLUNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).LeakyReLUNonlinearityConfig
        if name == "MishNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).MishNonlinearityConfig
        if name == "PReLUConfig":
            return importlib.import_module("nshtrainer.nn.nonlinearity").PReLUConfig
        if name == "ReLUNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).ReLUNonlinearityConfig
        if name == "SiLUNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).SiLUNonlinearityConfig
        if name == "SigmoidNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).SigmoidNonlinearityConfig
        if name == "SoftmaxNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).SoftmaxNonlinearityConfig
        if name == "SoftplusNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).SoftplusNonlinearityConfig
        if name == "SoftsignNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).SoftsignNonlinearityConfig
        if name == "SwiGLUNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).SwiGLUNonlinearityConfig
        if name == "SwishNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).SwishNonlinearityConfig
        if name == "TanhNonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).TanhNonlinearityConfig
        if name == "NonlinearityConfig":
            return importlib.import_module(
                "nshtrainer.nn.nonlinearity"
            ).NonlinearityConfig
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Submodule exports
