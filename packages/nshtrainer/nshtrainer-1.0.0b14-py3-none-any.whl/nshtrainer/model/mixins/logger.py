from __future__ import annotations

import copy
import dataclasses
from collections import deque
from collections.abc import Callable, Generator
from contextlib import contextmanager
from typing import Any, ClassVar

from lightning.pytorch import LightningModule
from lightning.pytorch.utilities.types import _METRIC
from lightning_utilities.core.rank_zero import rank_zero_warn
from typing_extensions import Self, override

from ...util.typing_utils import mixin_base_type


@dataclasses.dataclass(frozen=True, kw_only=True)
class _LogContextKwargs:
    __ignore_fields__: ClassVar[set[str]] = {"prefix", "disabled"}

    prefix: str | None = None
    disabled: bool | None = None
    prog_bar: bool | None = None
    logger: bool | None = None
    on_step: bool | None = None
    on_epoch: bool | None = None
    reduce_fx: str | Callable | None = None
    enable_graph: bool | None = None
    sync_dist: bool | None = None
    sync_dist_group: Any | None = None
    add_dataloader_idx: bool | None = None
    batch_size: int | None = None
    rank_zero_only: bool | None = None

    def copy_from(self, other: Self):
        kwargs = copy.deepcopy(self)

        # Copy over all the not-None values from the other object
        updates = {}
        for field in dataclasses.fields(self):
            # Ignore disabled fields
            if field.name in self.__ignore_fields__:
                continue

            if (value := getattr(other, field.name, None)) is None:
                continue
            # setattr(kwargs, field.name, value)
            updates[field.name] = value

        return dataclasses.replace(kwargs, **updates)

    def to_dict(self):
        d = dataclasses.asdict(self)
        for field in self.__ignore_fields__:
            d.pop(field, None)
        return d


class LoggerLightningModuleMixin(mixin_base_type(LightningModule)):
    @override
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._logger_prefix_stack = deque[_LogContextKwargs]()

    @contextmanager
    def log_context(
        self,
        prefix: str | None = None,
        disabled: bool | None = None,
        prog_bar: bool | None = None,
        logger: bool | None = None,
        on_step: bool | None = None,
        on_epoch: bool | None = None,
        reduce_fx: str | Callable | None = None,
        enable_graph: bool | None = None,
        sync_dist: bool | None = None,
        sync_dist_group: Any | None = None,
        add_dataloader_idx: bool | None = None,
        batch_size: int | None = None,
        rank_zero_only: bool | None = None,
    ) -> Generator[None, None, None]:
        self._logger_prefix_stack.append(
            _LogContextKwargs(
                prefix=prefix,
                disabled=disabled,
                prog_bar=prog_bar,
                logger=logger,
                on_step=on_step,
                on_epoch=on_epoch,
                reduce_fx=reduce_fx,
                enable_graph=enable_graph,
                sync_dist=sync_dist,
                sync_dist_group=sync_dist_group,
                add_dataloader_idx=add_dataloader_idx,
                batch_size=batch_size,
                rank_zero_only=rank_zero_only,
            )
        )
        try:
            yield
        finally:
            _ = self._logger_prefix_stack.pop()

    @override
    def log(
        self,
        name: str,
        value: _METRIC,
        prog_bar: bool = False,
        logger: bool | None = None,
        on_step: bool | None = None,
        on_epoch: bool | None = None,
        reduce_fx: str | Callable = "mean",
        enable_graph: bool = False,
        sync_dist: bool = False,
        sync_dist_group: Any | None = None,
        add_dataloader_idx: bool = True,
        batch_size: int | None = None,
        metric_attribute: str | None = None,
        rank_zero_only: bool = False,
    ) -> None:
        # join all prefixes
        prefix = "".join(c.prefix for c in self._logger_prefix_stack if c.prefix)
        name = f"{prefix}{name}"

        # check for disabled context:
        # if the topmost non-null context is disabled, then we don't log
        for c in reversed(self._logger_prefix_stack):
            if c.disabled is not None:
                if c.disabled:
                    rank_zero_warn(
                        f"Skipping logging of {name} due to disabled context"
                    )
                    return
                else:
                    break

        fn_kwargs = _LogContextKwargs()
        for c in self._logger_prefix_stack:
            fn_kwargs = fn_kwargs.copy_from(c)
        fn_kwargs = fn_kwargs.copy_from(
            _LogContextKwargs(
                prog_bar=prog_bar,
                logger=logger,
                on_step=on_step,
                on_epoch=on_epoch,
                reduce_fx=reduce_fx,
                enable_graph=enable_graph,
                sync_dist=sync_dist,
                sync_dist_group=sync_dist_group,
                add_dataloader_idx=add_dataloader_idx,
                batch_size=batch_size,
                rank_zero_only=rank_zero_only,
            )
        )
        return super().log(
            name,
            value,
            metric_attribute=metric_attribute,
            **fn_kwargs.to_dict(),
        )
