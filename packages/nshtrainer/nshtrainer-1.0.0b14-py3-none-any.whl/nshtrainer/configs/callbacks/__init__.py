from __future__ import annotations

__codegen__ = True

from typing import TYPE_CHECKING

# Config/alias imports

if TYPE_CHECKING:
    from nshtrainer.callbacks import (
        BestCheckpointCallbackConfig as BestCheckpointCallbackConfig,
    )
    from nshtrainer.callbacks import CallbackConfig as CallbackConfig
    from nshtrainer.callbacks import CallbackConfigBase as CallbackConfigBase
    from nshtrainer.callbacks import DebugFlagCallbackConfig as DebugFlagCallbackConfig
    from nshtrainer.callbacks import (
        DirectorySetupCallbackConfig as DirectorySetupCallbackConfig,
    )
    from nshtrainer.callbacks import (
        EarlyStoppingCallbackConfig as EarlyStoppingCallbackConfig,
    )
    from nshtrainer.callbacks import EMACallbackConfig as EMACallbackConfig
    from nshtrainer.callbacks import (
        EpochTimerCallbackConfig as EpochTimerCallbackConfig,
    )
    from nshtrainer.callbacks import (
        FiniteChecksCallbackConfig as FiniteChecksCallbackConfig,
    )
    from nshtrainer.callbacks import (
        GradientSkippingCallbackConfig as GradientSkippingCallbackConfig,
    )
    from nshtrainer.callbacks import (
        LastCheckpointCallbackConfig as LastCheckpointCallbackConfig,
    )
    from nshtrainer.callbacks import LogEpochCallbackConfig as LogEpochCallbackConfig
    from nshtrainer.callbacks import (
        NormLoggingCallbackConfig as NormLoggingCallbackConfig,
    )
    from nshtrainer.callbacks import (
        OnExceptionCheckpointCallbackConfig as OnExceptionCheckpointCallbackConfig,
    )
    from nshtrainer.callbacks import (
        PrintTableMetricsCallbackConfig as PrintTableMetricsCallbackConfig,
    )
    from nshtrainer.callbacks import (
        RLPSanityChecksCallbackConfig as RLPSanityChecksCallbackConfig,
    )
    from nshtrainer.callbacks import (
        SharedParametersCallbackConfig as SharedParametersCallbackConfig,
    )
    from nshtrainer.callbacks import (
        WandbUploadCodeCallbackConfig as WandbUploadCodeCallbackConfig,
    )
    from nshtrainer.callbacks import (
        WandbWatchCallbackConfig as WandbWatchCallbackConfig,
    )
    from nshtrainer.callbacks.actsave import ActSaveConfig as ActSaveConfig
    from nshtrainer.callbacks.checkpoint._base import (
        BaseCheckpointCallbackConfig as BaseCheckpointCallbackConfig,
    )
    from nshtrainer.callbacks.checkpoint._base import (
        CheckpointMetadata as CheckpointMetadata,
    )
    from nshtrainer.callbacks.early_stopping import MetricConfig as MetricConfig
    from nshtrainer.callbacks.lr_monitor import (
        LearningRateMonitorConfig as LearningRateMonitorConfig,
    )
else:

    def __getattr__(name):
        import importlib

        if name in globals():
            return globals()[name]
        if name == "ActSaveConfig":
            return importlib.import_module("nshtrainer.callbacks.actsave").ActSaveConfig
        if name == "BaseCheckpointCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks.checkpoint._base"
            ).BaseCheckpointCallbackConfig
        if name == "BestCheckpointCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).BestCheckpointCallbackConfig
        if name == "CallbackConfigBase":
            return importlib.import_module("nshtrainer.callbacks").CallbackConfigBase
        if name == "CheckpointMetadata":
            return importlib.import_module(
                "nshtrainer.callbacks.checkpoint._base"
            ).CheckpointMetadata
        if name == "DebugFlagCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).DebugFlagCallbackConfig
        if name == "DirectorySetupCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).DirectorySetupCallbackConfig
        if name == "EMACallbackConfig":
            return importlib.import_module("nshtrainer.callbacks").EMACallbackConfig
        if name == "EarlyStoppingCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).EarlyStoppingCallbackConfig
        if name == "EpochTimerCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).EpochTimerCallbackConfig
        if name == "FiniteChecksCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).FiniteChecksCallbackConfig
        if name == "GradientSkippingCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).GradientSkippingCallbackConfig
        if name == "LastCheckpointCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).LastCheckpointCallbackConfig
        if name == "LearningRateMonitorConfig":
            return importlib.import_module(
                "nshtrainer.callbacks.lr_monitor"
            ).LearningRateMonitorConfig
        if name == "LogEpochCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).LogEpochCallbackConfig
        if name == "MetricConfig":
            return importlib.import_module(
                "nshtrainer.callbacks.early_stopping"
            ).MetricConfig
        if name == "NormLoggingCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).NormLoggingCallbackConfig
        if name == "OnExceptionCheckpointCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).OnExceptionCheckpointCallbackConfig
        if name == "PrintTableMetricsCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).PrintTableMetricsCallbackConfig
        if name == "RLPSanityChecksCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).RLPSanityChecksCallbackConfig
        if name == "SharedParametersCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).SharedParametersCallbackConfig
        if name == "WandbUploadCodeCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).WandbUploadCodeCallbackConfig
        if name == "WandbWatchCallbackConfig":
            return importlib.import_module(
                "nshtrainer.callbacks"
            ).WandbWatchCallbackConfig
        if name == "CallbackConfig":
            return importlib.import_module("nshtrainer.callbacks").CallbackConfig
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Submodule exports
from . import actsave as actsave
from . import base as base
from . import checkpoint as checkpoint
from . import debug_flag as debug_flag
from . import directory_setup as directory_setup
from . import early_stopping as early_stopping
from . import ema as ema
from . import finite_checks as finite_checks
from . import gradient_skipping as gradient_skipping
from . import log_epoch as log_epoch
from . import lr_monitor as lr_monitor
from . import norm_logging as norm_logging
from . import print_table as print_table
from . import rlp_sanity_checks as rlp_sanity_checks
from . import shared_parameters as shared_parameters
from . import timer as timer
from . import wandb_upload_code as wandb_upload_code
from . import wandb_watch as wandb_watch
